import matplotlib.pyplot as plotter
import matplotlib
matplotlib.use('agg')
import numpy

from src.commons.configuration_manager import ConfigurationManager


class Plotter:
    figure_number = 1991

    @staticmethod
    def plot_distribution_of_dataset(labels, training_dataset=True):
        dataset_name = "training" if training_dataset else "test"

        plotter.figure(Plotter.__create_figure_number())
        plotter.title(f'label distribution of the {dataset_name} dataset\n'
                      f'0: {labels.count("0")}, 1: {labels.count("1")}')
        label_names = numpy.array(["0", "1"])
        label_counts = numpy.array([labels.count("0"), labels.count("1")])
        plotter.bar(label_names, label_counts)
        plotter.ylabel('count')
        plotter.xlabel('label')
        plotter.savefig(f'{ConfigurationManager.DeepLearning.Plot.save_path}/'
                        f'figure_distribution_{dataset_name}_label.png')

    @staticmethod
    def plot_history_for_two_custom_variable(history, variable1, variable2):
        plotter.figure(Plotter.__create_figure_number())
        plotter.plot(history.history[variable1])
        plotter.plot(history.history[variable2])
        plotter.title(f'{variable1} and {variable2} history')
        plotter.ylabel('value')
        plotter.xlabel('epoch')
        plotter.legend([variable1, variable2], loc='upper left')
        plotter.grid(visible=True)
        plotter.xticks(numpy.arange(history.params["epochs"]), numpy.arange(1, history.params["epochs"] + 1))
        plotter.savefig(f'{ConfigurationManager.DeepLearning.Plot.save_path}/'
                        f'figure_history_{variable1}_{variable2}.png')

    @staticmethod
    def __create_figure_number() -> int:
        Plotter.figure_number = Plotter.figure_number + 1
        return Plotter.figure_number
