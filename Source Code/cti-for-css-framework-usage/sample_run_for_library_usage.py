# to suppress the tensorflow logs
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

tf.get_logger().setLevel('ERROR')

# to use cti-for-css as a library (from source code)
import sys

sys.path.append("C:/cti-for-css/Source Code/cti-for-css")

# to configure parameters (from source code)
from src.commons.configuration_manager import ConfigurationManager
from src.commons.enums import NeuralNetwork
from src.commons.enums import DeepLearningOperation

# to start the cti-for-css
from src.orchestrator import Orchestrator


def train_sample_usage():
    ConfigurationManager.DeepLearning.Dataset.functions_path_for_x64 = r"C:\datafiles\binaries-64-windows.data"
    ConfigurationManager.DeepLearning.Dataset.labels_path_for_x64 = r"C:\datafiles\labels-64-windows.data"

    ConfigurationManager.DeepLearning.Dataset.inclusion_of_x32 = False
    ConfigurationManager.DeepLearning.model_preparation = DeepLearningOperation.TRAIN
    ConfigurationManager.DeepLearning.Method.selected_algorithm = NeuralNetwork.BI_LSTM

    Orchestrator().orchestrate()


def import_sample_usage_analyzing_on_premise_code():
    ConfigurationManager.DeepLearning.model_preparation = DeepLearningOperation.IMPORT
    ConfigurationManager.DeepLearning.Method.model_import_path = "C:/results/bilstm-results-forall-02-05-20/bidirectional_lstm_rnn.h5"
    ConfigurationManager.Reconstruction.retdec_installation_directory = "C:/retdec2"
    ConfigurationManager.CyberThreatIntelligence.build_cti = True
    ConfigurationManager.CyberThreatIntelligence.target_files = ["C:/cti-for-css/Sample Applications/hello_world.exe", "C:/cti-for-css/Sample Applications/vulnerable_binary.exe"]
    ConfigurationManager.CyberThreatIntelligence.vulnerability_threshold = 0.7
    ConfigurationManager.CyberThreatIntelligence.analyze_only_functions = ["sayHello", "bad"]

    Orchestrator().orchestrate()

def import_sample_usage_analyzing_third_party_code():
    ConfigurationManager.DeepLearning.model_preparation = DeepLearningOperation.IMPORT
    ConfigurationManager.DeepLearning.Method.model_import_path = "C:/results/bilstm-results-forall-02-05-20/bidirectional_lstm_rnn.h5"
    ConfigurationManager.Reconstruction.retdec_installation_directory = "C:/retdec2"
    ConfigurationManager.CyberThreatIntelligence.build_cti = True
    ConfigurationManager.CyberThreatIntelligence.target_files = ["C:/Users/smArikan/Desktop/test/dosyalar/cmd.exe"]
    ConfigurationManager.CyberThreatIntelligence.vulnerability_threshold = 0.99
    ConfigurationManager.CyberThreatIntelligence.analyze_only_functions = []

    Orchestrator().orchestrate()


if __name__ == "__main__":
    import_sample_usage_analyzing_on_premise_code()
