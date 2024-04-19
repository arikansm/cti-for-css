import numpy as np
import tensorflow as tf
from src.commons.log_manager import LogManager
from src.form_manager.vectorizer import Vectorizer


class PredictionSetVectorizer(Vectorizer):
    def __init__(self, functions: list[str]):
        self.__logger = LogManager.get_logger()

        self.__functions = functions

    def perform_text_vectorization(self, maximum_size_of_vocabulary: int, sequence_length: int,
                                   serialized_vectorizer: bytes = b'') -> [tf.data.Dataset,
                                                                           tf.data.Dataset]:
        self._initialize_vectorizer(self.__functions, serialized_vectorizer,
                                    maximum_size_of_vocabulary, sequence_length)

        self.__functions = tf.data.Dataset.from_tensor_slices(self.__functions)
        self.__functions = self.__functions.map(self.vectorize_text_for_prediction)
        self.__functions = self.__functions.cache().prefetch(buffer_size=10)

        return self.__functions
