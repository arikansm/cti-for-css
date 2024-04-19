import pickle
import tensorflow as tf
from abc import ABC, abstractmethod
from tensorflow.keras.layers import TextVectorization


class Vectorizer(ABC):
    # to eliminate "mangled names are not yet supported" tensorflow warning, it should be protected
    # if this variable was private, tf would not be able to use it (and throw the warning)
    _function_data_vectorizer = None
    _function_data_vectorizer_parameters = None

    @abstractmethod
    def perform_text_vectorization(self, maximum_size_of_vocabulary: int, sequence_length: int,
                                   serialized_vectorizer: bytes = b'') -> list[tf.data.Dataset]:
        pass

    def _initialize_vectorizer(self, adaptation_array, serialized_vectorizer,
                               maximum_size_of_vocabulary, sequence_length):
        self._function_data_vectorizer = TextVectorization(max_tokens=maximum_size_of_vocabulary,
                                                           output_mode="int",
                                                           output_sequence_length=sequence_length)

        self._function_data_vectorizer.adapt(adaptation_array)

        if serialized_vectorizer == b'':
            self._function_data_vectorizer_parameters = pickle.dumps(
                {'config': self._function_data_vectorizer.get_config(),
                 'weights': self._function_data_vectorizer.get_weights()})
        else:
            deserialized_vectorizer_parameters = pickle.loads(serialized_vectorizer)
            deserialized_vectorizer = TextVectorization.from_config(deserialized_vectorizer_parameters['config'])
            # adapt have to be called (bug)
            deserialized_vectorizer.adapt(adaptation_array)
            deserialized_vectorizer.set_weights(deserialized_vectorizer_parameters['weights'])
            self._function_data_vectorizer = deserialized_vectorizer
            self._function_data_vectorizer_parameters = serialized_vectorizer

    def vectorize_text(self, text, label):
        return self._function_data_vectorizer(tf.expand_dims(text, -1)), label

    def vectorize_text_for_prediction(self, text):
        return self._function_data_vectorizer(tf.expand_dims(text ,-1))

    def get_vectorizer_parameters_information(self) -> bytes:
        return self._function_data_vectorizer_parameters

