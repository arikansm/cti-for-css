import os  # to suppress tensorflow warnings

from src.commons.enums import NeuralNetwork

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
import numpy
from sklearn.model_selection import train_test_split
from src.model_manager.algorithms.algorithm import Algorithm
from src.model_manager.algorithms.multi_layer_perceptron import MultiLayerPerceptronWithSingleHiddenLayerAndPooling
from src.model_manager.algorithms.one_dimensional_cnn import OneDimensionalCNN
from src.model_manager.algorithms.lstm_rnn import LongShortTermMemory
from src.model_manager.algorithms.bidirectional_lstm_rnn import BidirectionalLongShortTermMemory
from src.commons.io_helper import IOHelper
from src.commons.configuration_manager import ConfigurationManager
from src.commons.log_manager import LogManager
from src.commons.plotter import Plotter
from src.form_manager.function_transformer import FunctionTransformer

class Learner:
    def __init__(self):
        self.__logger = LogManager.get_logger()
        self.__function_transformer = FunctionTransformer()

    def train(self) -> tf.keras.Model:
        self.__logger.debug("training has been started")

        functions, labels = self.__get_functions_and_labels()
        self.__check_dataset_coherency(functions, labels)

        model = self.__learn(functions, labels)

        return model

    def __check_dataset_coherency(self, functions, labels):
        if len(functions) != len(labels):
            self.__logger.critical(f"functions (len: {len(functions)}) and labels (len: {len(labels)}) have "
                                   f"not got the same length")
            raise Exception("the dataset is not coherent")
        else:
            self.__logger.debug(f"functions and labels have got the same length (len: {len(functions)})")

    def __get_functions_and_labels(self) -> [list[str], list[str]]:
        self.__logger.debug("acquiring functions and labels has been started")

        functions_dataset_raw_64 = IOHelper.FileOperator.read_content(ConfigurationManager.DeepLearning.Dataset
                                                                      .functions_path_for_x64)
        functions = self.__function_transformer.prepare_functions_from_string(functions_dataset_raw_64)

        self.__logger.debug(f"64-bit functions (len: {len(functions)}) have been acquired")

        labels_dataset_raw_64 = IOHelper.FileOperator.read_content(ConfigurationManager.DeepLearning.Dataset
                                                                   .labels_path_for_x64)
        labels = self.__function_transformer.prepare_labels_from_string(labels_dataset_raw_64)
        self.__logger.debug(f"64-bit labels (len: {len(labels)}) have been acquired")

        if ConfigurationManager.DeepLearning.Dataset.inclusion_of_x32:
            functions_dataset_raw_32 = IOHelper.FileOperator.read_content(ConfigurationManager.DeepLearning.Dataset
                                                                          .functions_path_for_x32)
            functions_32 = functions = self.__function_transformer.prepare_functions_from_string(functions_dataset_raw_32)

            functions = [*functions, *functions_32]
            self.__logger.debug(f"32-bit functions (len: {len(functions_32)}) have been acquired")

            labels_dataset_raw_32 = IOHelper.FileOperator.read_content(ConfigurationManager.DeepLearning.Dataset
                                                                       .labels_path_for_x32)
            labels_32 = self.__function_transformer.prepare_labels_from_string(labels_dataset_raw_32)
            labels = [*labels, *labels_32]
            self.__logger.debug(f"32-bit labels (len: {len(labels_32)}) have been acquired")

        return functions, labels

    def __split_dataset(self, functions: list[str], labels: list[str]) -> [list[str], list[str],
                                                                           list[str], list[str],
                                                                           list[str], list[str]]:
        self.__logger.debug(f"splitting dataset has been started (linear,"
                            f" shuffle: {ConfigurationManager.DeepLearning.Validation.shuffle},"
                            f" ratio: {ConfigurationManager.DeepLearning.Validation.holdout_split_ratio})")
        train_functions, holdout_functions, \
            train_labels, holdout_labels = train_test_split(functions, labels,
                                                            test_size=ConfigurationManager.DeepLearning
                                                            .Validation.holdout_split_ratio,
                                                            shuffle=ConfigurationManager.DeepLearning
                                                            .Validation.shuffle)
        self.__logger.debug(f"train (len: {len(train_labels)}) and holdout (len: {len(holdout_labels)}) "
                            f"sets have been created")

        Plotter.plot_distribution_of_dataset(train_labels)
        Plotter.plot_distribution_of_dataset(holdout_labels, training_dataset=False)

        if ConfigurationManager.DeepLearning.Validation.validation_split_ratio == 0:
            self.__logger.debug(f"test (len: 0) and validation (len: {len(holdout_functions)}) "
                                f"sets have been created")
            return train_functions, None, holdout_functions, train_labels, None, holdout_labels
        elif ConfigurationManager.DeepLearning.Validation.validation_split_ratio == 1:
            self.__logger.debug(f"test (len: {len(holdout_functions)}) and validation (len: 0) "
                                f"sets have been created")
            return train_functions, holdout_functions, None, train_labels, holdout_labels, None
        else:
            test_functions, validation_functions, \
                test_labels, validation_labels = train_test_split(holdout_functions, holdout_labels,
                                                                  test_size=ConfigurationManager.DeepLearning
                                                                  .Validation.validation_split_ratio,
                                                                  shuffle=ConfigurationManager.DeepLearning
                                                                  .Validation.shuffle)

            self.__logger.debug(f"test (len: {len(test_functions)}) and validation (len: {len(validation_functions)}) "
                                f"sets have been created")

            return train_functions, test_functions, validation_functions, train_labels, test_labels, validation_labels

    def __learn(self, functions: list[str], labels: list[str]) -> tf.keras.Model:
        train_functions, test_functions, validation_functions, train_labels, test_labels, validation_labels \
            = self.__split_dataset(functions, labels)

        algorithm = self.__get_algorithm()

        model, serialized_vectorizer = algorithm.train(train_functions, train_labels,
                                                       validation_functions, validation_labels)

        if ConfigurationManager.DeepLearning.Validation.validation_split_ratio != 1:
            algorithm.evaluate(test_functions, test_labels, model, serialized_vectorizer)
        return model

    def __get_algorithm(self) -> Algorithm:
        match ConfigurationManager.DeepLearning.Method.selected_algorithm:
            case NeuralNetwork.BI_LSTM:
                algorithm = BidirectionalLongShortTermMemory()
            case NeuralNetwork.LSTM:
                algorithm = LongShortTermMemory()
            case NeuralNetwork.ONE_D_CNN:
                algorithm = OneDimensionalCNN()
            case NeuralNetwork.MLP:
                algorithm = MultiLayerPerceptronWithSingleHiddenLayerAndPooling()
            case _:
                self.__logger.error(f"No algorithm has been specified! Use ConfigurationManager to select one")
                raise Exception("algorithm is undefined")
        return algorithm
