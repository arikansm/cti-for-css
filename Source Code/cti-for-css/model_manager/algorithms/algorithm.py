from abc import ABC, abstractmethod
import tensorflow as tf

from src.commons.plotter import Plotter
from src.form_manager.training_set_vectorizer import TrainingSetVectorizer
from src.form_manager.test_set_vectorizer import TestSetVectorizer


class Algorithm(ABC):

    @abstractmethod
    def train(self, train_functions: list[str], train_labels: list[str],
              validation_functions: list[str], validation_labels: list[str]) -> [tf.keras.Model, bytes]:
        pass

    @abstractmethod
    def evaluate(self, model: tf.keras.Model, test_functions: list[str], test_labels: list[str],
                 serialized_vectorizer: bytes):
        pass

    @staticmethod
    def _prepare_training_dataset(train_functions: list[str], train_labels: list[str],
                                  validation_functions: list[str], validation_labels: list[str],
                                  maximum_size_of_vocabulary: int, sequence_length: int) -> [tf.data.Dataset,
                                                                                             tf.data.Dataset]:
        training_vectorizer = TrainingSetVectorizer(train_functions, train_labels,
                                                    validation_functions, validation_labels)
        train_dataset, validation_dataset = training_vectorizer.perform_text_vectorization(maximum_size_of_vocabulary,
                                                                                           sequence_length)
        return train_dataset, validation_dataset, training_vectorizer.get_vectorizer_parameters_information()

    @staticmethod
    def _prepare_test_dataset(serialized_vectorizer, test_functions: list[str], test_labels: list[str],
                              maximum_size_of_vocabulary: int, sequence_length: int) -> [tf.data.Dataset]:
        test_vectorizer = TestSetVectorizer(test_functions, test_labels)
        return test_vectorizer.perform_text_vectorization(maximum_size_of_vocabulary, sequence_length,
                                                          serialized_vectorizer)

    @staticmethod
    def _plot_history(history, with_validation: bool) -> None:
        if with_validation:
            Algorithm.__plot_history_variable_with_validation(history, 'accuracy')
            Algorithm.__plot_history_variable_with_validation(history, 'precision')
            Algorithm.__plot_history_variable_with_validation(history, 'recall')
            Algorithm.__plot_history_variable_with_validation(history, 'auc')
            Algorithm.__plot_history_variable_with_validation(history, 'loss')
        else:
            Plotter.plot_history_for_two_custom_variable(history, 'accuracy', 'loss')
            Plotter.plot_history_for_two_custom_variable(history, 'accuracy', 'auc')
            Plotter.plot_history_for_two_custom_variable(history, 'precision', 'recall')
            Plotter.plot_history_for_two_custom_variable(history, 'true_positives', 'true_negatives')
            Plotter.plot_history_for_two_custom_variable(history, 'false_positives', 'false_negatives')

    @staticmethod
    def __plot_history_variable_with_validation(history, variable):
        Plotter.plot_history_for_two_custom_variable(history, variable, f'val_{variable}')


