import numpy as np
import tensorflow as tf
from src.commons.log_manager import LogManager
from src.form_manager.vectorizer import Vectorizer


class TestSetVectorizer(Vectorizer):
    def __init__(self, test_set_functions: list[str], test_set_labels: list[str]):
        self.__logger = LogManager.get_logger()

        self.__test_set_functions = test_set_functions
        self.__test_set_labels = test_set_labels

    def perform_text_vectorization(self, maximum_size_of_vocabulary: int, sequence_length: int,
                                   serialized_vectorizer: bytes = b'') -> [tf.data.Dataset]:
        self.__logger.debug("text form_manager has been started for test set")

        self._initialize_vectorizer(self.__test_set_functions, serialized_vectorizer,
                                    maximum_size_of_vocabulary, sequence_length)

        self.__logger.debug("form_manager is ready for test set")

        self.__logger.debug("dataset standardization has been started for test set")
        self.__test_set_labels = np.asarray(self.__test_set_labels).astype('int32').reshape((-1, 1))
        self.__test_set_functions = tf.data.Dataset.from_tensor_slices((self.__test_set_functions,
                                                                        self.__test_set_labels))
        self.__logger.debug("dataset standardization has been finished for test set")

        self.__logger.debug("form_manager for datasets has been started for test set")
        test_dataset = self.__test_set_functions.map(self.vectorize_text)
        self.__logger.debug("form_manager for datasets has been finished for test set")

        # Do async prefetching / buffering of the data for best performance on GPU.
        test_dataset = test_dataset.cache().prefetch(buffer_size=10)

        self.__logger.debug("text form_manager has been finished for test set")

        return test_dataset
