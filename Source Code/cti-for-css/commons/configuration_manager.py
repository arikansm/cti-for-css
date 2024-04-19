import datetime
import logging
from src.commons.enums import NeuralNetwork
from src.commons.enums import DeepLearningOperation


class ConfigurationManager:
    class All:
        temporary_files_directory: str = "cti_for_css_temporary_files"

    class DeepLearning:
        model_preparation: DeepLearningOperation = DeepLearningOperation.TRAIN

        class Method:
            selected_algorithm: NeuralNetwork = NeuralNetwork.UNKNOWN
            model_save_path: str = "cti_for_css_temporary_files"
            model_import_path: str = "sample"

        class Dataset:
            inclusion_of_x32: bool = False
            functions_path_for_x64: str = "sample"
            labels_path_for_x64: str = "sample"
            functions_path_for_x32: str = "sample"
            labels_path_for_x32: str = "sample"

        class Validation:
            shuffle: bool = True
            holdout_split_ratio: float = 0.2
            validation_split_ratio: float = 0.5

        class Plot:
            save_path: str = "cti_for_css_temporary_files"
            save_dataset_label_distribution: bool = True
            save_model_history: bool = True

    class Log:
        class Console:
            enabled: bool = True
            level: int = logging.DEBUG
            format: str = "%(asctime)s - %(levelname)s - %(thread)d (%(threadName)s) - %(module)s:%(funcName)s:%(" \
                          "lineno)d - %(message)s "

        class File:
            enabled: bool = True
            level: int = logging.DEBUG
            format: str = "%(asctime)s - %(levelname)s - :%(thread)d (%(threadName)s) - %(module)s:%(funcName)s:%(" \
                          "lineno)d - %(message)s "
            directory: str = "cti_for_css_temporary_files"
            name: str = "cti_manager-for-css.log"

    class Reconstruction:
        retdec_installation_directory: str = r"/retdec"

    class CyberThreatIntelligence:
        build_cti: bool = False
        target_files: list[str] = None
        vulnerability_threshold: float = 0.7
        analyze_only_functions: list[str] = []
        save_path: str = "cti_for_css_temporary_files"
