import tensorflow as tf

from src.commons.configuration_manager import ConfigurationManager
from src.commons.io_helper import IOHelper
from src.commons.log_manager import LogManager


class Importer:
    def __init__(self):
        self.__logger = LogManager.get_logger()

    def import_model(self) -> tf.keras.Model:
        self.__logger.debug("importing model has been started")
        if IOHelper.FileOperator.exists(ConfigurationManager.DeepLearning.Method.model_import_path):
            model = tf.keras.models.load_model(f'{ConfigurationManager.DeepLearning.Method.model_import_path}')
            self.__logger.debug("importing model has been done")
            return model
        else:
            self.__logger.error(f"Model file could not be found: "
                                f"'{ConfigurationManager.DeepLearning.Method.model_import_path}'")
            raise Exception("model file could not be found")
