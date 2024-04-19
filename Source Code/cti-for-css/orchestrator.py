import tensorflow as tf

from src.commons.configuration_manager import ConfigurationManager
from src.commons.log_manager import LogManager
from src.commons.io_helper import IOHelper
from src.commons.dependency_checker import DependencyChecker
from src.model_manager.analyzer import Analyzer
from src.model_manager.learner import Learner
from src.model_manager.importer import Importer
from src.cti_manager.exporter import Exporter
from src.cti_manager.builder import Builder
from src.cti_manager.crud_provider import CrudProvider
from src.commons.enums import DeepLearningOperation


class Orchestrator:
    def __init__(self):
        self.__orchestrated = False

        # To avoid circular import, checking log file directory is handled in orchestrator class
        if ConfigurationManager.Log.File.enabled:
            IOHelper.DirectoryOperator.create_if_not_exist(ConfigurationManager.Log.File.directory)
        IOHelper.DirectoryOperator.create_if_not_exist(ConfigurationManager.All.temporary_files_directory)

        self.__logger = LogManager.get_logger()
        self.__learner = Learner()
        self.__importer = Importer()
        self.__crud_provider = CrudProvider()
        self.__exporter = Exporter()

    def orchestrate(self) -> None:
        self.__logger.debug(f"orchestration has been started (via gpu: {DependencyChecker.is_gpu_usage_available()})")

        model = self.__prepare_model()

        if ConfigurationManager.CyberThreatIntelligence.build_cti:
            vulnerable_functions = Analyzer().analyze(model, ConfigurationManager.CyberThreatIntelligence.target_files)
            self.__create_cti_for_file(vulnerable_functions)

        self.__logger.debug("orchestration has been done")
        self.__orchestrated = True

    # noinspection PyMethodMayBeStatic
    def __prepare_model(self):
        match ConfigurationManager.DeepLearning.model_preparation:
            case DeepLearningOperation.TRAIN:
                model, vectorizer_parameters = self.__learner.train()
                return model
            case DeepLearningOperation.IMPORT:
                return self.__importer.import_model()
            case _:
                raise Exception("unknown operation")

    def __create_cti_for_file(self, vulnerable_functions: list[dict]) -> None:
        for function_info in vulnerable_functions:
            stix_dictionary = Builder(function_info).build()
            self.__crud_provider.add(stix_dictionary)
        self.__exporter.export(self.__crud_provider.list())

