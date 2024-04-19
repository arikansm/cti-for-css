import tensorflow as tf
import datetime
import numpy as np

from src.commons.configuration_manager import ConfigurationManager
from src.commons.io_helper import IOHelper
from src.commons.log_manager import LogManager
from src.reconstructor.machine_code_decompiler import MachineCodeDecompiler
from src.form_manager.function_transformer import FunctionTransformer
from src.form_manager.prediction_set_vectorizer import PredictionSetVectorizer


class Analyzer:

    def __init__(self):
        self.__logger = LogManager.get_logger()
        self.__reconstructor = MachineCodeDecompiler()
        self.__transformer = FunctionTransformer()
        self.__maximum_size_of_vocabulary = 20000
        self.__sequence_length = 500

    def analyze(self, model: tf.keras.Model, file_path: list[str]) -> list[dict]:
        vulnerable_functions = []

        for binary_path in file_path:
            vulnerable_functions_for_binary = []
            prepared_binary_path = self.__prepare_file(binary_path)
            if prepared_binary_path == "":
                continue

            self.__logger.debug(f"Functions are being prepared for the file '{binary_path}'")
            functions = self.__get_functions_from_prepared_file_path(prepared_binary_path)

            self.__logger.debug(f"Functions are being predicted for the file '{binary_path}'")
            index = 0
            total = len(functions)
            analyze_only = len(ConfigurationManager.CyberThreatIntelligence.analyze_only_functions) > 0
            for function_info, function_code in functions.items():
                index += 1
                if analyze_only:
                    if self.__check_function_included(function_info):
                        self.__analyze_function(function_code, function_info, index, model, total, vulnerable_functions_for_binary)
                    else:
                        self.__logger.debug(
                            f"The function \"{function_info}\" has been skipped [{index}/{total}]")
                else:
                    self.__analyze_function(function_code, function_info, index, model, total, vulnerable_functions_for_binary)

            vulnerable_function_number = len(vulnerable_functions_for_binary)
            if vulnerable_function_number > 0:
                vulnerable_functions.append({"binary_path": binary_path,
                                             "prepared_binary_path": prepared_binary_path,
                                             "vulnerable_functions": vulnerable_functions_for_binary})
            self.__logger.debug(f"The prediction process has been finished for the file '{binary_path}' (the number of vulnerable function: {vulnerable_function_number})")

        return vulnerable_functions

    def __check_function_included(self, function_info: str) -> bool:
        for analyze_only_function in ConfigurationManager.CyberThreatIntelligence.analyze_only_functions:
            if analyze_only_function in function_info:
                return True
        return False

    def __analyze_function(self, function_code, function_info, index, model, total, vulnerable_functions_for_binary):
        prediction_vectorizer = PredictionSetVectorizer([" ".join(function_code)])
        train_dataset = prediction_vectorizer.perform_text_vectorization(self.__maximum_size_of_vocabulary,
                                                                         self.__sequence_length)

        predicted_type = "suitable"
        prediction_result = np.max(model.predict(train_dataset))
        if prediction_result >= ConfigurationManager.CyberThreatIntelligence.vulnerability_threshold:
            predicted_type = "vulnerable"
        if predicted_type == "vulnerable":
            vulnerable_functions_for_binary.append(function_info)
        self.__logger.debug(
            f"The function \"{function_info}\" has been predicted: {predicted_type} (calculation: {prediction_result}) [{index}/{total}]")

    def __get_functions_from_prepared_file_path(self, prepared_file_path: str) -> dict:
        dsm_file_path = prepared_file_path + ".dsm"
        dsm_file_content = IOHelper.FileOperator.read_content(dsm_file_path)
        return self.__transformer.prepare_functions_from_dsm_file(dsm_file_content)

    def __prepare_file(self, file_path: str) -> str:
        decompiled_path = self.__reconstructor.decompile_binary_to_file(file_path, self.__temp_file_name_generator)

        if decompiled_path != "":
            self.__logger.debug(f"File has been extracted, constructed, and ready to deep learning activities: '{file_path}'")
            return decompiled_path
        else:
            self.__logger.error(f"File could not be extracted/constructed: '{file_path}'")
            return ""

    # noinspection PyMethodMayBeStatic
    def __temp_file_name_generator(self, file_path: str) -> str:
        return r"{0}\{1}\{2}".format(ConfigurationManager.All.temporary_files_directory,
                                     str(datetime.datetime.now().timestamp()).replace(".", ""),
                                     IOHelper.FileOperator.get_file_name_from_path(file_path))
