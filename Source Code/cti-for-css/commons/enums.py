from enum import Enum, unique


@unique
class NeuralNetwork(Enum):
    UNKNOWN = "undefined algorithm"
    BI_LSTM = "Bidirectional Long Short Term Memory"
    LSTM = "Long Short Term Memory"
    ONE_D_CNN = "1D Convolutional Neural Network"
    MLP = "Multi Layer Perceptron"

@unique
class DeepLearningOperation(Enum):
    TRAIN = "train from dataset"
    IMPORT = "import saved model"
