import tensorflow as tf
from tensorflow.keras import layers

from src.commons.configuration_manager import ConfigurationManager
from src.model_manager.algorithms.algorithm import Algorithm
from src.commons.log_manager import LogManager


class BidirectionalLongShortTermMemory(Algorithm):
    """
    Bidirectional Long Short-Term Memory (BiLSTM) is a recurrent neural network used primarily on natural language processing

    BiLSTM adds one more LSTM layer, which reverses the direction of information flow.
    Briefly, it means that the input sequence flows backward in the additional LSTM layer.
    """

    def __init__(self):
        self.__logger = LogManager.get_logger()
        self.__maximum_epoch = 20
        self.maximum_size_of_vocabulary: int = 20000
        self.embedding_dimension: int = 128
        self.sequence_length: int = 500

    def train(self, train_functions: list[str], train_labels: list[str],
              validation_functions: list[str], validation_labels: list[str]) -> [tf.keras.Model, bytes]:
        train_dataset, validation_dataset, vectorizer_parameters = \
            Algorithm._prepare_training_dataset(train_functions, train_labels, validation_functions, validation_labels,
                                                self.maximum_size_of_vocabulary, self.sequence_length)

        model = tf.keras.Sequential()
        model.add(layers.Embedding(self.maximum_size_of_vocabulary, self.embedding_dimension))
        model.add(layers.Bidirectional(layers.LSTM(128, return_sequences=True)))
        model.add(layers.Bidirectional(layers.LSTM(128)))

        model.add(layers.Dense(1, activation="sigmoid", name="predictions"))

        model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy",
                                                                             tf.keras.metrics.Precision(),
                                                                             tf.keras.metrics.Recall(),
                                                                             tf.keras.metrics.AUC(),
                                                                             tf.keras.metrics.TruePositives(),
                                                                             tf.keras.metrics.TrueNegatives(),
                                                                             tf.keras.metrics.FalsePositives(),
                                                                             tf.keras.metrics.FalseNegatives()])

        self.__logger.debug("bidirectional long short-term memory has been started to learn")
        history = None
        if validation_dataset is not None:
            history = model.fit(train_dataset, validation_data=validation_dataset, epochs=self.__maximum_epoch)
        else:
            history = model.fit(train_dataset, epochs=self.__maximum_epoch)

        Algorithm._plot_history(history, validation_dataset is not None)
        self.__logger.debug("bidirectional long short-term memory model is acquired")

        model.save(f"{ConfigurationManager.DeepLearning.Method.model_save_path}/bidirectional_lstm_rnn.h5", save_format="h5")

        return model, vectorizer_parameters

    def evaluate(self, test_functions: list[str], test_labels: list[str],
                 model: tf.keras.Model, serialized_vectorizer: bytes = b''):
        self.__logger.debug("bidirectional long short-term memory model has been started to evaluation")
        test_dataset = Algorithm._prepare_test_dataset(serialized_vectorizer, test_functions, test_labels,
                                                       self.maximum_size_of_vocabulary, self.sequence_length)
        model.evaluate(test_dataset)
        self.__logger.debug("bidirectional long short-term memory model is evaluated")
