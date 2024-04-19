import sys
import logging
from src.commons.configuration_manager import ConfigurationManager


class LogManager:
    __logger = None

    @staticmethod
    def get_logger() -> logging.Logger:
        if LogManager.__logger is None:
            LogManager.__initialize_logger()
        return LogManager.__logger

    @staticmethod
    def __initialize_logger() -> None:
        LogManager.__logger = logging.getLogger(__name__)

        # The level of our root logger have to be the lowest in order to support handlers to log any level
        LogManager.__logger.setLevel(logging.DEBUG)

        LogManager.__logger.handlers = []

        if ConfigurationManager.Log.File.enabled:
            file_handler = logging.FileHandler(ConfigurationManager.Log.File.directory
                                               + "/" + ConfigurationManager.Log.File.name)
            file_handler.setFormatter(logging.Formatter(ConfigurationManager.Log.File.format))
            file_handler.setLevel(ConfigurationManager.Log.File.level)
            LogManager.__logger.addHandler(file_handler)

        if ConfigurationManager.Log.Console.enabled:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(logging.Formatter(ConfigurationManager.Log.Console.format))
            console_handler.setLevel(ConfigurationManager.Log.Console.level)
            LogManager.__logger.addHandler(console_handler)
