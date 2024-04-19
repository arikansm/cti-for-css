import numpy as np
import tensorflow as tf
from src.commons.log_manager import LogManager
from src.form_manager.vectorizer import Vectorizer


class TrainingSetVectorizer(Vectorizer):
    def __init__(self, train_functions: list[str], train_labels: list[str],
                 validation_functions: list[str], validation_labels: list[str]):
        self.__logger = LogManager.get_logger()

        self.__train_functions = train_functions
        self.__train_labels = train_labels
        self.__validation_functions = validation_functions
        self.__validation_labels = validation_labels

    def perform_text_vectorization(self, maximum_size_of_vocabulary: int, sequence_length: int,
                                   serialized_vectorizer: bytes = b'') -> [tf.data.Dataset,
                                                                           tf.data.Dataset]:
        self.__logger.debug("text form_manager has been started for training sets")

        self._initialize_vectorizer(self.__train_functions, serialized_vectorizer,
                                    maximum_size_of_vocabulary, sequence_length)

        self.__logger.debug("form_manager is ready for training sets")

        self.__logger.debug("dataset standardization has been started for training sets")
        self.__train_labels = np.asarray(self.__train_labels).astype('int32').reshape((-1, 1))
        self.__train_functions = tf.data.Dataset.from_tensor_slices((self.__train_functions, self.__train_labels))

        if self.__validation_labels is not None:
            self.__validation_labels = np.asarray(self.__validation_labels).astype('int32').reshape((-1, 1))
            self.__validation_functions = tf.data.Dataset.from_tensor_slices((self.__validation_functions,
                                                                              self.__validation_labels))
        self.__logger.debug("dataset standardization has been finished for training sets")

        self.__logger.debug("form_manager for datasets has been started for training sets")
        train_dataset = self.__train_functions.map(self.vectorize_text)

        validation_dataset = None
        if self.__validation_labels is not None:
            validation_dataset = self.__validation_functions.map(self.vectorize_text)
        self.__logger.debug("form_manager for datasets has been finished for training sets")

        # Do async prefetching / buffering of the data for best performance on GPU.
        train_dataset = train_dataset.cache().prefetch(buffer_size=10)

        if validation_dataset is not None:
            validation_dataset = validation_dataset.cache().prefetch(buffer_size=10)

        self.__logger.debug("text form_manager has been finished for training sets")

        return [train_dataset, validation_dataset]
