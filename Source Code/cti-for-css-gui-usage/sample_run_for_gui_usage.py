# to suppress the tensorflow logs
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
tf.get_logger().setLevel('ERROR')

import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import tkinter.scrolledtext as st
import zlib, base64
from PIL import ImageTk
import time
from base64 import b64decode
from threading import *
import threading
import ctypes
import tensorflow as tf
from contextlib import redirect_stdout
import webbrowser

import logging
import sys

from media.splash_screen_photo_provider import SplashScreenPhotoProvider

# to use cti-for-css as a library (from source code)
sys.path.append("C:/cti-for-css/Source Code/cti-for-css")

# to configure parameters (from source code)
from src.commons.enums import DeepLearningOperation
from src.commons.enums import NeuralNetwork
from src.commons.configuration_manager import ConfigurationManager

# to start the cti-for-css
from src.orchestrator import Orchestrator


# noinspection PyAttributeOutsideInit
class GraphicalInterface:
    INITIAL_MAIN_WINDOW_HEIGHT = 780
    INITIAL_MAIN_WINDOW_WIDTH = 1505
    GENERAL_AND_LOGGING_WINDOW_HEIGHT = 665
    GENERAL_AND_LOGGING_WINDOW_WIDTH = 760

    """
        ↓ callback functions ↓
    """

    def __model_preparation_changed(self):
        if self.model_preparation_value.get() == 1:
            self.neural_network_list.config(state="normal")
            self.model_save_path_entry.config(state="normal")
            self.model_save_path_browse.config(state="normal")
            self.model_import_path_entry.config(state="disabled")
            self.model_import_path_browse.config(state="disabled")

            if len(self.deep_learning_dataset_group.grid_info()) == 0:
                self.__add_deep_learning_dataset_group()
            if len(self.deep_learning_validation_group.grid_info()) == 0:
                self.__add_deep_learning_validation_group()
            if len(self.deep_learning_plot_group.grid_info()) == 0:
                self.__add_deep_learning_plot_group()
        else:
            self.neural_network_list.config(state="disabled")
            self.model_save_path_entry.config(state="disabled")
            self.model_save_path_browse.config(state="disabled")
            self.model_import_path_entry.config(state="normal")
            self.model_import_path_browse.config(state="normal")

            self.deep_learning_dataset_group.grid_remove()
            self.deep_learning_validation_group.grid_remove()
            self.deep_learning_plot_group.grid_remove()

        self.neural_network_list.update()
        self.model_save_path_entry.update()
        self.model_import_path_entry.update()
        self.model_import_path_entry.update()
        self.model_import_path_browse.update()

    def __inclusion_of_x32_changed(self):
        new_state = "normal" if self.inclusion_of_x32_value.get() == 1 else "disabled"

        self.functions_path_for_x32_entry.config(state=new_state)
        self.functions_path_for_x32_entry.update()

        self.functions_path_for_x32_browse.config(state=new_state)
        self.functions_path_for_x32_browse.update()

        self.labels_path_for_x32_entry.config(state=new_state)
        self.labels_path_for_x32_entry.update()

        self.labels_path_for_x32_browse.config(state=new_state)
        self.labels_path_for_x32_browse.update()

    def __save_related_state_changed(self):
        new_state = "disabled"
        if self.save_model_history_value.get() == 1 or self.save_dataset_label_distribution_value.get() == 1:
            new_state = "normal"

        self.figure_save_path_directory_entry.config(state=new_state)
        self.figure_save_path_directory_entry.update()

        self.figure_save_path_directory_browse.config(state=new_state)
        self.figure_save_path_directory_browse.update()

    def __console_logging_state_changed(self):
        if self.console_logging_value.get() == 1:
            self.console_log_level_combobox.config(state="readonly")
            self.console_log_format_text.config(state="normal")
        else:
            self.console_log_level_combobox.config(state="disabled")
            self.console_log_format_text.config(state="disabled")

        self.console_log_level_combobox.update()
        self.console_log_format_text.update()

    def __file_logging_state_changed(self):
        if self.file_logging_value.get() == 1:
            self.file_log_level_combobox.config(state="readonly")
            self.file_log_format_text.config(state="normal")
            self.file_log_directory_entry.config(state="normal")
            self.file_log_name_entry.config(state="normal")
        else:
            self.file_log_level_combobox.config(state="disabled")
            self.file_log_format_text.config(state="disabled")
            self.file_log_directory_entry.config(state="disabled")
            self.file_log_name_entry.config(state="disabled")

        self.file_log_level_combobox.update()
        self.file_log_format_text.update()
        self.file_log_directory_entry.update()
        self.file_log_name_entry.update()

    def __build_cti_state_changed(self):
        new_state = "normal" if self.build_cti_value.get() == 1 else "disabled"

        self.cti_targets_list.config(state=new_state)
        self.cti_targets_list.update()

        self.cti_targets_browse.config(state=new_state)
        self.cti_targets_browse.update()

        self.cti_targets_remove.config(state=new_state)
        self.cti_targets_remove.update()

        self.cti_targets_clear.config(state=new_state)
        self.cti_targets_clear.update()

        self.cti_threshold_entry.config(state=new_state)
        self.cti_threshold_entry.update()

        self.cti_save_directory_entry.config(state=new_state)
        self.cti_save_directory_entry.update()

        self.cti_save_directory_browse.config(state=new_state)
        self.cti_save_directory_browse.update()

        self.cti_analyze_only_functions_entry.config(state=new_state)
        self.cti_analyze_only_functions_entry.update()

    """
        ↓ button commands ↓
    """

    def __browse_for_x32_functions(self):
        file_name = filedialog.askopenfilename()
        if len(file_name) != 0:
            self.functions_path_for_x32_value.set(file_name)
            self.functions_path_for_x32_entry.update()

    def __browse_for_x32_labels(self):
        file_name = filedialog.askopenfilename()
        if len(file_name) != 0:
            self.labels_path_for_x32_value.set(file_name)
            self.labels_path_for_x32_entry.update()

    def __browse_for_x64_functions(self):
        file_name = filedialog.askopenfilename()
        if len(file_name) != 0:
            self.functions_path_for_x64_value.set(file_name)
            self.functions_path_for_x64_entry.update()

    def __browse_for_x64_labels(self):
        file_name = filedialog.askopenfilename()
        if len(file_name) != 0:
            self.labels_path_for_x64_value.set(file_name)
            self.labels_path_for_x64_entry.update()

    def __browse_for_temporary_file_directory(self):
        directory_path = filedialog.askdirectory()
        if len(directory_path) != 0:
            self.temporary_files_directory_value.set(directory_path)
            self.temporary_files_directory_entry.update()

    def __browse_for_model_save_path(self):
        directory_path = filedialog.askdirectory()
        if len(directory_path) != 0:
            self.model_save_path_value.set(directory_path)
            self.model_save_path_entry.update()

    def __browse_for_model_import_path(self):
        file_name = filedialog.askopenfilename()
        if len(file_name) != 0:
            self.model_import_path_value.set(file_name)
            self.model_import_path_entry.update()

    def __browse_for_figure_save_path(self):
        directory_path = filedialog.askdirectory()
        if len(directory_path) != 0:
            self.figure_save_path_directory_value.set(directory_path)
            self.figure_save_path_directory_entry.update()

    def __browse_for_retdec_directory(self):
        directory_path = filedialog.askdirectory()
        if len(directory_path) != 0:
            self.retdec_installation_directory_value.set(directory_path)
            self.retdec_installation_directory_entry.update()

    def __browse_for_cti_save_directory(self):
        directory_path = filedialog.askdirectory()
        if len(directory_path) != 0:
            self.cti_save_directory_value.set(directory_path)
            self.cti_save_directory_entry.update()

    def __browse_for_file_log_directory(self):
        directory_path = filedialog.askdirectory()
        if len(directory_path) != 0:
            self.file_log_directory_value.set(directory_path)
            self.file_log_directory_entry.update()

    def __browse_for_cti_targets(self):
        file_name = filedialog.askopenfilename()
        if len(file_name) != 0:
            if file_name in self.cti_targets_list.get(0, END):
                tkinter.messagebox.showerror(title="Unique Item Violation",
                                             message="The selected binary is already in the list!")
            else:
                self.cti_targets_list.insert(END, file_name)

    def __delete_from_cti_targets(self):
        selected_item = self.cti_targets_list.curselection()
        if len(selected_item) < 1:
            tkinter.messagebox.showwarning(title="No Selected Item",
                                           message="You need to choose a binary from the list!")
        else:
            self.cti_targets_list.delete(selected_item[0])

    def __clear_cti_targets(self):
        item_number = len(self.cti_targets_list.get(0, END))
        if item_number == 0:
            tkinter.messagebox.showwarning(title="Already Empty List",
                                           message="The list cannot be cleared because it is already empty!")
        else:
            decision = tkinter.messagebox.askyesno(title="Cleaning Confirmation",
                                                   message="The list will be cleared! "
                                                           "Are you sure you want to continue?")
            if decision:
                self.cti_targets_list.delete(0, END)

    def __show_general_and_logging_configurations(self):
        if hasattr(self, 'navigation_group') and hasattr(self, 'general_group') and hasattr(self, 'log_group'):
            if not (len(self.navigation_group.grid_info()) == 0 and len(self.general_group.grid_info()) == 0 and len(
                    self.log_group.grid_info()) == 0):
                return

        self.menu_operations.entryconfig("Run With Current Configuration", state="disabled")
        self.menu_operations.entryconfig("Reset General & Logging Configurations", state="disabled")
        self.__add_navigation_group()
        self.__add_general_group()
        self.__add_log_group()
        self.main_window.maxsize(self.navigation_group.winfo_width() + 15, self.GENERAL_AND_LOGGING_WINDOW_HEIGHT)

    def __hide_general_and_logging_configurations(self):
        try:
            self.menu_operations.entryconfig("Run With Current Configuration", state="active")
            self.menu_operations.entryconfig("Reset General & Logging Configurations", state="active")
            self.navigation_group.grid_remove()
            self.general_group.grid_remove()
            self.log_group.grid_remove()
            self.main_window.maxsize(self.INITIAL_MAIN_WINDOW_WIDTH, self.INITIAL_MAIN_WINDOW_HEIGHT)
        except AttributeError:
            pass

    # noinspection PyMethodMayBeStatic
    def __run_with_current_configuration(self):
        decision = tkinter.messagebox.askyesno(title="Run",
                                               message="Orchestration is about to start! "
                                                       "Are you sure you want to continue?")
        if decision:
            self.__show_active_process()
            self.compute_thread = CtiForCssRunner(self)
            self.compute_thread.start()

    def __stop_active_process(self):
        if not self.compute_thread.is_alive():
            tkinter.messagebox.showerror(title="Terminated Process",
                                         message="There is no running process!")
        else:
            decision = tkinter.messagebox.askyesno(title="Stop",
                                                   message="Current activity will be terminated! "
                                                           "Are you sure you want to continue?")
            if decision:
                self.compute_thread.terminate()

    def __close_active_process_window(self):
        if self.compute_thread.is_alive():
            title = "Stop & Close"
            message = "Current activity will be terminated and the window will be closed! "
        else:
            title = "Close"
            message = "You are about to close the window! "

        message += "Are you sure you want to continue?"

        decision = tkinter.messagebox.askyesno(title=title,
                                               message=message)
        if decision:
            self.compute_thread.terminate()
            while self.compute_thread.is_alive():
                time.sleep(1)
            self.active_process_window.destroy()

    def __check_gpu_usage(self):
        physical_devices = tf.config.list_physical_devices('GPU')
        status = "GPU Usage: " + ("Enabled" if len(physical_devices) > 0 else "Not Activated")

        devices = "-------\n"
        if len(physical_devices) > 0:
            devices += '\n'.join(map(str, physical_devices))
        else:
            devices += "There is no GPU device!"

        tkinter.messagebox.showinfo(title="Check GPU Usage", message=f"{status}\n{devices}")

    def __open_cti_viewer(self):
        webbrowser.open_new_tab(f'file://{os.path.realpath("cti-for-css-stix-viewer/index.html")}')

    """
        ↓ builders for window entities ↓
    """

    def __add_navigation_group(self):
        self.navigation_group = LabelFrame(self.main_window, text='')
        self.navigation_group.grid(sticky='ew', row=2, padx=10, pady=10)
        self.save_and_continue_button = Button(self.navigation_group, text='Save and Continue >',
                                               command=self.__hide_general_and_logging_configurations)
        self.informative_label = Label(self.navigation_group,
                                       text='You can then reset these configurations from the menu\nOperations | Reset General & Logging Configurations')

        self.save_and_continue_button.pack(side='top', padx=10)
        self.informative_label.pack(side='top', padx=10)

    def __add_general_group(self):
        self.general_group = LabelFrame(self.main_window, text='General')
        self.general_group.grid(sticky='ew', row=0, padx=10, pady=10)

        self.temporary_files_directory_label = Label(self.general_group, text='Temporary Files Directory:')
        self.temporary_files_directory_value = StringVar(self.main_window, "cti_for_css_temporary_files")
        self.temporary_files_directory_entry = Entry(self.general_group,
                                                     textvariable=self.temporary_files_directory_value, width=47)
        self.temporary_files_directory_label.grid(sticky="W", row=0, column=0, padx=10, pady=5)
        self.temporary_files_directory_entry.grid(sticky="W", row=0, column=1, padx=(0, 10))

        self.temporary_files_directory_browse = Button(self.general_group, text='Browse',
                                                       command=self.__browse_for_temporary_file_directory)

        self.temporary_files_directory_browse.grid(sticky="w", row=0, column=2, padx=10, pady=5)

    def __add_deep_learning_group(self):
        self.deep_learning_group = LabelFrame(self.main_window, text='Deep Learning')
        self.deep_learning_group.grid(sticky='ewn', row=0, column=4, rowspan=500, padx=10, pady=10)

        self.model_preparation_label = Label(self.deep_learning_group, text='Model Preparation:')
        self.model_preparation_value = IntVar(self.main_window, 1)
        self.model_preparation_radiobutton_learn = Radiobutton(self.deep_learning_group,
                                                               text="Learn Model Through Dataset",
                                                               command=self.__model_preparation_changed,
                                                               variable=self.model_preparation_value, value=1)
        self.model_preparation_radiobutton_import = Radiobutton(self.deep_learning_group, text="Import Model From File",
                                                                command=self.__model_preparation_changed,
                                                                variable=self.model_preparation_value, value=2)
        self.model_preparation_label.grid(sticky="w", row=0, column=0, padx=10, pady=5)
        self.model_preparation_radiobutton_learn.grid(sticky="W", row=0, column=1, pady=5)
        self.model_preparation_radiobutton_import.grid(sticky="W", row=0, column=2, pady=5)

        self.__add_deep_learning_method_group()
        self.__add_deep_learning_dataset_group()
        self.__add_deep_learning_validation_group()
        self.__add_deep_learning_plot_group()

        self.__model_preparation_changed()

    def __add_deep_learning_plot_group(self):
        self.deep_learning_plot_group = LabelFrame(self.deep_learning_group, text='Plot')
        self.deep_learning_plot_group.grid(sticky='ew', row=4, columnspan=3, padx=10, pady=10)
        self.save_model_history_value = IntVar(self.main_window, 1)
        self.save_model_history_checkbox = Checkbutton(self.deep_learning_plot_group,
                                                       text='Save Model History',
                                                       variable=self.save_model_history_value,
                                                       command=self.__save_related_state_changed,
                                                       onvalue=1, offvalue=0)
        self.save_model_history_checkbox.grid(sticky="w", row=0, column=0, padx=10, pady=5)
        self.save_dataset_label_distribution_value = IntVar(self.main_window, 1)
        self.save_dataset_label_distribution_checkbox = Checkbutton(self.deep_learning_plot_group,
                                                                    text='Save Dataset Label Distribution',
                                                                    variable=self.save_dataset_label_distribution_value,
                                                                    command=self.__save_related_state_changed,
                                                                    onvalue=1, offvalue=0)
        self.save_dataset_label_distribution_checkbox.grid(sticky="w", row=0, column=1, padx=10, pady=5)
        self.figure_save_path_directory_label = Label(self.deep_learning_plot_group, text='Save Path:')
        self.figure_save_path_directory_value = StringVar(self.main_window, "cti_for_css_temporary_files")
        self.figure_save_path_directory_browse = Button(self.deep_learning_plot_group, text='Browse',
                                                        command=self.__browse_for_figure_save_path)
        self.figure_save_path_directory_entry = Entry(self.deep_learning_plot_group,
                                                      textvariable=self.figure_save_path_directory_value, width=44)
        self.figure_save_path_directory_label.grid(sticky="W", row=2, column=0, padx=10, pady=5)
        self.figure_save_path_directory_entry.grid(sticky="W", row=2, column=1, padx=10, pady=5)
        self.figure_save_path_directory_browse.grid(sticky="w", row=2, column=2, padx=10, pady=5)

    def __add_deep_learning_validation_group(self):
        self.deep_learning_validation_group = LabelFrame(self.deep_learning_group, text='Validation')
        self.deep_learning_validation_group.grid(sticky='ew', row=3, columnspan=3, padx=10, pady=10)
        self.shuffle_value = IntVar()
        self.shuffle_checkbox = Checkbutton(self.deep_learning_validation_group, text='Shuffle',
                                            variable=self.shuffle_value, onvalue=1, offvalue=0)
        self.shuffle_checkbox.grid(sticky="w", row=0, column=0, padx=10, pady=5)
        self.holdout_label = Label(self.deep_learning_validation_group, text='Holdout Split Ratio [0..1]:')
        self.holdout_value = DoubleVar(self.main_window, 0.5)
        self.holdout_entry = Entry(self.deep_learning_validation_group, textvariable=self.holdout_value, width=5)
        self.holdout_label.grid(sticky="w", row=1, column=0, padx=10, pady=5)
        self.holdout_entry.grid(sticky="w", row=1, column=1, padx=20, pady=5)
        self.validation_label = Label(self.deep_learning_validation_group, text='Validation Split Ratio [0..1]:')
        self.validation_value = DoubleVar(self.main_window, 0.5)
        self.validation_entry = Entry(self.deep_learning_validation_group, textvariable=self.validation_value, width=5)
        self.validation_label.grid(sticky="w", row=2, column=0, padx=10, pady=5)
        self.validation_entry.grid(sticky="w", row=2, column=1, padx=20, pady=5)

    def __add_deep_learning_dataset_group(self):
        self.deep_learning_dataset_group = LabelFrame(self.deep_learning_group, text='Dataset')
        self.deep_learning_dataset_group.grid(sticky='ew', row=2, columnspan=3, padx=10, pady=10)
        self.inclusion_of_x32_value = IntVar()
        self.inclusion_of_x32_checkbox = Checkbutton(self.deep_learning_dataset_group, text='Inclusion of x32 Records',
                                                     variable=self.inclusion_of_x32_value, onvalue=1, offvalue=0,
                                                     command=self.__inclusion_of_x32_changed)
        self.inclusion_of_x32_checkbox.grid(sticky="w", row=0, column=0, padx=10, pady=5)
        self.functions_path_for_x32_label = Label(self.deep_learning_dataset_group, text='x32 Functions File Path:')
        self.functions_path_for_x32_value = StringVar(self.main_window, "not selected")
        self.functions_path_for_x32_entry = Entry(self.deep_learning_dataset_group,
                                                  textvariable=self.functions_path_for_x32_value,
                                                  width=40)
        self.functions_path_for_x32_browse = Button(self.deep_learning_dataset_group, text='Browse',
                                                    command=self.__browse_for_x32_functions)
        self.functions_path_for_x32_label.grid(sticky="w", row=1, column=0, padx=10, pady=5)
        self.functions_path_for_x32_entry.grid(sticky="w", row=1, column=1, padx=10, pady=5)
        self.functions_path_for_x32_browse.grid(sticky="w", row=1, column=2, padx=10, pady=5)
        self.labels_path_for_x32_label = Label(self.deep_learning_dataset_group, text='x32 Labels File Path:')
        self.labels_path_for_x32_value = StringVar(self.main_window, "not selected")
        self.labels_path_for_x32_entry = Entry(self.deep_learning_dataset_group,
                                               textvariable=self.labels_path_for_x32_value, width=40)
        self.labels_path_for_x32_browse = Button(self.deep_learning_dataset_group, text='Browse',
                                                 command=self.__browse_for_x32_labels)
        self.labels_path_for_x32_label.grid(sticky="w", row=2, column=0, padx=10, pady=5)
        self.labels_path_for_x32_entry.grid(sticky="w", row=2, column=1, padx=10, pady=5)
        self.labels_path_for_x32_browse.grid(sticky="w", row=2, column=2, padx=10, pady=5)
        self.functions_path_for_x64_label = Label(self.deep_learning_dataset_group, text='x64 Functions File Path:')
        self.functions_path_for_x64_value = StringVar(self.main_window, "not selected")
        self.functions_path_for_x64_entry = Entry(self.deep_learning_dataset_group,
                                                  textvariable=self.functions_path_for_x64_value,
                                                  width=40)
        self.functions_path_for_x64_browse = Button(self.deep_learning_dataset_group, text='Browse',
                                                    command=self.__browse_for_x64_functions)
        self.functions_path_for_x64_label.grid(sticky="w", row=3, column=0, padx=10, pady=5)
        self.functions_path_for_x64_entry.grid(sticky="w", row=3, column=1, padx=10, pady=5)
        self.functions_path_for_x64_browse.grid(sticky="w", row=3, column=2, padx=10, pady=5)
        self.labels_path_for_x64_label = Label(self.deep_learning_dataset_group, text='x64 Labels File Path:')
        self.labels_path_for_x64_value = StringVar(self.main_window, "not selected")
        self.labels_path_for_x64_entry = Entry(self.deep_learning_dataset_group,
                                               textvariable=self.labels_path_for_x64_value, width=40)
        self.labels_path_for_x64_browse = Button(self.deep_learning_dataset_group, text='Browse',
                                                 command=self.__browse_for_x64_labels)
        self.labels_path_for_x64_label.grid(sticky="w", row=4, column=0, padx=10, pady=5)
        self.labels_path_for_x64_entry.grid(sticky="w", row=4, column=1, padx=10, pady=5)
        self.labels_path_for_x64_browse.grid(sticky="w", row=4, column=2, padx=10, pady=5)

        self.__inclusion_of_x32_changed()

    def __add_deep_learning_method_group(self):
        self.deep_learning_method_group = LabelFrame(self.deep_learning_group, text='Method')
        self.deep_learning_method_group.grid(sticky='ew', row=1, columnspan=3, padx=10, pady=10)
        self.neural_network_list_label = Label(self.deep_learning_method_group, text='Neural Network:')
        self.neural_network_list = Listbox(self.deep_learning_method_group, height=5, width=35)
        self.neural_network_list_scrollbar = Scrollbar(self.deep_learning_method_group, orient=VERTICAL)
        self.neural_network_list.config(yscrollcommand=self.neural_network_list_scrollbar.set)
        self.neural_network_list_scrollbar.config(command=self.neural_network_list.yview)
        self.neural_network_list.insert(1, str(NeuralNetwork.BI_LSTM.value))
        self.neural_network_list.insert(2, str(NeuralNetwork.LSTM.value))
        self.neural_network_list.insert(3, str(NeuralNetwork.ONE_D_CNN.value))
        self.neural_network_list.insert(4, str(NeuralNetwork.MLP.value))
        self.neural_network_list_label.grid(sticky="wn", row=0, column=0, padx=10, pady=5)
        self.neural_network_list.grid(sticky='ew', row=0, column=1, padx=10, pady=5)
        self.neural_network_list_scrollbar.grid(row=0, column=1, padx=11, pady=7, sticky='sne')
        self.model_save_path_label = Label(self.deep_learning_method_group, text='Model Save Path:')
        self.model_save_path_value = StringVar(self.main_window, "cti_for_css_temporary_files")
        self.model_save_path_entry = Entry(self.deep_learning_method_group, textvariable=self.model_save_path_value,
                                           width=48)
        self.model_save_path_browse = Button(self.deep_learning_method_group, text='Browse',
                                             command=self.__browse_for_model_save_path)
        self.model_save_path_label.grid(sticky="w", row=1, column=0, padx=10, pady=5)
        self.model_save_path_entry.grid(sticky="w", row=1, column=1, padx=10, pady=5)
        self.model_save_path_browse.grid(sticky="w", row=1, column=2, padx=10, pady=5)
        self.model_import_path_label = Label(self.deep_learning_method_group, text='Model Import Path:')
        self.model_import_path_value = StringVar(self.main_window, "cti_for_css_temporary_files")
        self.model_import_path_entry = Entry(self.deep_learning_method_group, textvariable=self.model_import_path_value,
                                             width=48)
        self.model_import_path_browse = Button(self.deep_learning_method_group, text='Browse',
                                               command=self.__browse_for_model_import_path)
        self.model_import_path_label.grid(sticky="w", row=2, column=0, padx=10, pady=5)
        self.model_import_path_entry.grid(sticky="w", row=2, column=1, padx=10, pady=5)
        self.model_import_path_browse.grid(sticky="w", row=2, column=2, padx=10, pady=5)

    def __add_log_group(self):
        self.log_group = LabelFrame(self.main_window, text='Logging')
        self.log_group.grid(sticky='ewn', row=1, column=0, padx=10, pady=10)

        self.__add_log_console_group()
        self.__add_log_file_group()

    def __add_log_file_group(self):
        self.log_file_group = LabelFrame(self.log_group, text='File')
        self.log_file_group.grid(sticky='ew', row=1, column=0, columnspan=3, padx=10, pady=10)
        self.file_logging_value = IntVar(self.main_window, 1)
        self.file_logging_checkbox = Checkbutton(self.log_file_group,
                                                 text='Enable',
                                                 variable=self.file_logging_value,
                                                 command=self.__file_logging_state_changed,
                                                 onvalue=1, offvalue=0)
        self.file_logging_checkbox.grid(sticky="w", row=0, column=0, padx=10, pady=5)
        self.file_log_level_label = Label(self.log_file_group, text='Minimum Log Level:')
        self.file_log_level_value = StringVar(self.main_window, "Debug")
        self.file_log_level_combobox = ttk.Combobox(self.log_file_group,
                                                    textvariable=self.file_log_level_value,
                                                    state="readonly")
        self.file_log_level_combobox['values'] = (' Debug', ' Warning', ' Info', ' Error',)
        self.file_log_level_label.grid(sticky="W", row=1, column=0, padx=10, pady=5)
        self.file_log_level_combobox.grid(sticky="W", row=1, column=1, padx=(0, 10), pady=5)
        self.file_log_format_label = Label(self.log_file_group, text='Log Format:')
        self.file_log_format_text = Text(self.log_file_group, width=62, height=5)
        self.file_log_format_text.insert(INSERT, "%(asctime)s - %(levelname)s - %(thread)d (%(threadName)s) - "
                                                 "%(module)s:%(funcName)s:%(lineno)d - %(message)s ")
        self.file_log_format_label.grid(sticky="WN", row=2, column=0, padx=10, pady=5)
        self.file_log_format_text.grid(sticky="W", row=2, column=1, columnspan=3, padx=(0, 10), pady=5)
        self.file_log_directory_label = Label(self.log_file_group, text='File Directory:')
        self.file_log_directory_value = StringVar(self.main_window, "cti_for_css_temporary_files")
        self.file_log_directory_entry = Entry(self.log_file_group, textvariable=self.file_log_directory_value,
                                              width=48)
        self.file_log_directory_browse = Button(self.log_file_group, text='Browse',
                                                command=self.__browse_for_file_log_directory)
        self.file_log_directory_label.grid(sticky="w", row=3, column=0, padx=10, pady=5)
        self.file_log_directory_entry.grid(sticky="w", row=3, column=1, padx=0, pady=5)
        self.file_log_directory_browse.grid(sticky="w", row=3, column=2, padx=10, pady=5)
        self.file_log_name_label = Label(self.log_file_group, text='Log File Name:')
        self.file_log_name_value = StringVar(self.main_window, "cti_for_css.log")
        self.file_log_name_entry = Entry(self.log_file_group, textvariable=self.file_log_name_value,
                                         width=48)
        self.file_log_name_label.grid(sticky="w", row=4, column=0, padx=10, pady=5)
        self.file_log_name_entry.grid(sticky="w", row=4, column=1, padx=0, pady=5)

        self.__file_logging_state_changed()

    def __add_log_console_group(self):
        self.log_console_group = LabelFrame(self.log_group, text='Console')
        self.log_console_group.grid(sticky='ew', row=0, column=0, columnspan=3, padx=10, pady=10)
        self.console_logging_value = IntVar(self.main_window, 1)
        self.console_logging_checkbox = Checkbutton(self.log_console_group,
                                                    text='Enable',
                                                    variable=self.console_logging_value,
                                                    command=self.__console_logging_state_changed,
                                                    onvalue=1, offvalue=0)
        self.console_logging_checkbox.grid(sticky="w", row=0, column=0, padx=10, pady=5)
        self.console_log_level_label = Label(self.log_console_group, text='Minimum Log Level:')
        self.console_log_level_value = StringVar(self.main_window, "Debug")
        self.console_log_level_combobox = ttk.Combobox(self.log_console_group,
                                                       textvariable=self.console_log_level_value,
                                                       state="readonly")
        self.console_log_level_combobox['values'] = (' Debug', ' Warning', ' Info', ' Error',)
        self.console_log_level_label.grid(sticky="W", row=1, column=0, padx=10, pady=5)
        self.console_log_level_combobox.grid(sticky="W", row=1, column=1, padx=(0, 10), pady=5)
        self.console_log_format_label = Label(self.log_console_group, text='Log Format:')
        self.console_log_format_text = Text(self.log_console_group, width=62, height=5)
        self.console_log_format_text.insert(INSERT, "%(asctime)s - %(levelname)s - %(thread)d (%(threadName)s) - "
                                                    "%(module)s:%(funcName)s:%(lineno)d - %(message)s ")
        self.console_log_format_label.grid(sticky="WN", row=2, column=0, padx=10, pady=5)
        self.console_log_format_text.grid(sticky="W", row=2, column=1, columnspan=3, padx=(0, 10), pady=5)

        self.__console_logging_state_changed()

    def __add_reconstruction_group(self):
        self.reconstruction_group = LabelFrame(self.main_window, text='Reconstruction')
        self.reconstruction_group.grid(sticky='ewn', row=0, column=7, padx=10, pady=10)

        self.retdec_installation_directory_label = Label(self.reconstruction_group, text='Retdec Root Directory:')
        self.retdec_installation_directory_value = StringVar(self.main_window, "retdec")
        self.retdec_installation_directory_entry = Entry(self.reconstruction_group,
                                                         textvariable=self.retdec_installation_directory_value,
                                                         width=47)
        self.retdec_installation_directory_label.grid(sticky="W", row=0, column=0, padx=10, pady=5)
        self.retdec_installation_directory_entry.grid(sticky="W", row=0, column=1, padx=(0, 10))
        self.retdec_installation_directory_browse = Button(self.reconstruction_group, text='Browse',
                                                           command=self.__browse_for_retdec_directory)
        self.retdec_installation_directory_browse.grid(sticky="w", row=0, column=2, padx=10, pady=5)

    def __add_cti_group(self):
        self.cti_group = LabelFrame(self.main_window, text='Cyber Threat Intelligence')
        self.cti_group.grid(sticky='new', row=1, column=7, padx=10, pady=10)

        self.build_cti_value = IntVar(self.main_window, 0)
        self.build_cti_checkbox = Checkbutton(self.cti_group,
                                              text='Build CTI',
                                              variable=self.build_cti_value,
                                              command=self.__build_cti_state_changed,
                                              onvalue=1, offvalue=0)
        self.build_cti_checkbox.grid(sticky="w", row=0, column=0, padx=10, pady=5)

        self.cti_targets_label = Label(self.cti_group, text='Binaries To Analyze:')
        self.cti_targets_list = Listbox(self.cti_group, height=8, width=59)
        self.cti_targets_list_scrollbar_x = Scrollbar(self.cti_group, orient=HORIZONTAL)
        self.cti_targets_list.config(xscrollcommand=self.cti_targets_list_scrollbar_x.set)
        self.cti_targets_list_scrollbar_x.config(command=self.cti_targets_list.xview)
        self.cti_targets_list_scrollbar_y = Scrollbar(self.cti_group, orient=VERTICAL)
        self.cti_targets_list.config(yscrollcommand=self.cti_targets_list_scrollbar_y.set)
        self.cti_targets_list_scrollbar_y.config(command=self.cti_targets_list.yview)
        self.cti_targets_browse = Button(self.cti_group, text='Add A New Binary',
                                         command=self.__browse_for_cti_targets)
        self.cti_targets_remove = Button(self.cti_group, text='Remove The Binary',
                                         command=self.__delete_from_cti_targets)
        self.cti_targets_clear = Button(self.cti_group, text='Clear The List',
                                        command=self.__clear_cti_targets)
        self.cti_save_directory_label = Label(self.cti_group, text='CTI Save Directory (all the cti data will be bundled within the file):')
        self.cti_save_directory_value = StringVar(self.cti_group, "cti_for_css_temporary_files")
        self.cti_save_directory_entry = Entry(self.cti_group, textvariable=self.cti_save_directory_value, width=56)
        self.cti_save_directory_browse = Button(self.cti_group, text='Browse', command=self.__browse_for_cti_save_directory)
        self.cti_threshold_label = Label(self.cti_group, text='Prediction Threshold for Positivity (for the vulnerable class) [0..1]:')
        self.cti_threshold_value = DoubleVar(self.cti_group, 0.7)
        self.cti_threshold_entry = Entry(self.cti_group, textvariable=self.cti_threshold_value, width=5)
        self.cti_analyze_only_functions_label = Label(self.cti_group, text='Analyze Only These Functions (separate with comma or leave blank for all):')
        self.cti_analyze_only_functions_value = StringVar(self.cti_group, "")
        self.cti_analyze_only_functions_entry = Entry(self.cti_group, textvariable=self.cti_analyze_only_functions_value, width=56)
        self.cti_targets_label.grid(sticky="w", row=1, column=0, padx=10)
        self.cti_targets_list.grid(sticky="w", row=2, column=0, rowspan=3, padx=10, pady=5)
        self.cti_targets_list_scrollbar_x.grid(row=2, column=0, padx=11, rowspan=3, pady=7, sticky='ews')
        self.cti_targets_list_scrollbar_y.grid(row=2, column=0, padx=11, rowspan=3, pady=7, sticky='sne')
        self.cti_targets_browse.grid(sticky="ew", row=2, column=1, padx=10, pady=5)
        self.cti_targets_remove.grid(sticky="ew", row=3, column=1, padx=10, pady=5)
        self.cti_targets_clear.grid(sticky="ew", row=4, column=1, padx=10, pady=5)
        self.cti_save_directory_label.grid(sticky="W", row=6, column=0, padx=10, pady=5)
        self.cti_save_directory_entry.grid(sticky="W", row=7, column=0, padx=10, pady=5)
        self.cti_save_directory_browse.grid(sticky="w", row=7, column=1, padx=10, pady=5)
        self.cti_threshold_label.grid(sticky="W", row=5, column=0, padx=10, pady=5)
        self.cti_threshold_entry.grid(sticky="W", row=5, column=1, padx=10, pady=5)
        self.cti_analyze_only_functions_label.grid(sticky="W", row=8, column=0, padx=10, pady=5)
        self.cti_analyze_only_functions_entry.grid(sticky="W", row=9, column=0, padx=10, pady=5)

        self.__build_cti_state_changed()

    def __add_menu(self):
        self.menu = Menu(self.main_window)

        self.menu_operations = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Operations", menu=self.menu_operations)
        self.menu_operations.add_command(label="Run With Current Configuration",
                                         command=self.__run_with_current_configuration)
        self.menu_operations.add_separator()
        self.menu_operations.add_command(label="Reset General & Logging Configurations",
                                         command=self.__show_general_and_logging_configurations)
        self.menu_operations.add_separator()
        self.menu_operations.add_command(label="Exit", command=self.main_window.destroy)

        menu_info = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Info", menu=menu_info)
        menu_info.add_command(label="GPU Status", command=self.__check_gpu_usage)
        menu_info.add_separator()
        menu_info.add_command(label="Open cti-for-css-stix-viewer", command=self.__open_cti_viewer)

        self.main_window.config(menu=self.menu)

    def __delete_default_icon(self):
        self.main_window.tk.call('wm', 'iconphoto', self.main_window._w,
                                 ImageTk.PhotoImage(data=zlib.decompress(base64.b64decode('eJxjYGAEQgEBBiDJwZDBysAgxs'
                                                                                          'DAoAHEQCEGBQaIOAg4sDIgACMU'
                                                                                          'j4JRMApGwQgF/ykEAFXxQRc='))))

    def __show_splash_screen(self):
        splash_screen = Toplevel(background="white")
        splash_screen.overrideredirect(True)
        splash_screen.title("css-vud-cti")
        splash_width = 710
        splash_height = 473

        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()

        x = int((screen_width / 2) - (splash_width / 2))
        y = int((screen_height / 2) - (splash_height / 2))
        splash_screen.geometry(f"{splash_width}x{splash_height}+{x}+{y}")

        background_image = PhotoImage(data=SplashScreenPhotoProvider.get_png_photo_as_base64())
        background_label = Label(splash_screen, image=background_image)
        background_label.place(x=0, y=0)
        photo_label = Label(splash_screen, text="Photo by Roberto Sorin on Unsplash",
                            width=30, font=("Arial", 7))
        photo_label.place(x=0, y=458)

        title_label = Label(splash_screen,
                            text="Cyber Threat Intelligence \nwith Deep Learning Based Vulnerability Detection System "
                                 "\nfor Closed Source Software",
                            width=48, font=("Arial Rounded MT Bold", 14), bg="#fa5502", anchor="e", justify=LEFT)
        title_label.place(x=0, y=110)

        abbreviation_label = Label(splash_screen,
                                   text="cti-for-css",
                                   width=14, font=("Rockwell Extra Bold", 16), bg="#fa5502")
        abbreviation_label.place(x=0, y=271)

        splash_screen.update()

        time.sleep(5)  # The wait here is for the main window to be prepared

        self.main_window.deiconify()
        splash_screen.destroy()

    def __show_active_process(self):
        self.active_process_window = Toplevel(self.main_window)
        self.active_process_window.title("Active Process")
        self.active_process_window.geometry("500x500")
        self.active_process_window.protocol("WM_DELETE_WINDOW", self.__close_active_process_window)

        self.active_process_text = st.ScrolledText(self.active_process_window)
        self.active_process_text.pack(expand=True, fill='both')

        self.active_process_stop_button = Button(self.active_process_window, text='Stop The Process',
                                                 command=self.__stop_active_process)
        self.active_process_stop_button.pack(pady=5)

        self.active_process_window.grab_set()

    def inform_for_active_process(self, information: str, replace_last_information: bool) -> None:
        information = information.rstrip().replace("\x08", "")
        if len(information) == 0:
            return

        if not replace_last_information:
            self.active_process_text.insert(END, "\n")
            self.active_process_text.insert(END, information)
        else:
            candicate = self.active_process_text.get("end - 1 lines", END)
            if "Epoch" not in candicate:
                self.active_process_text.delete("end - 1 lines", END)
            self.active_process_text.insert(END, "\n")
            self.active_process_text.insert(END, information)
        self.active_process_text.yview(END)

    def show_window(self):
        self.main_window = tkinter.Tk()
        self.main_window.resizable(False, False)
        self.main_window.withdraw()

        self.main_window.title('cti-for-css')
        self.__delete_default_icon()
        self.__add_menu()

        self.__show_general_and_logging_configurations()
        self.__add_deep_learning_group()
        self.__add_reconstruction_group()
        self.__add_cti_group()

        self.__show_splash_screen()

        mainloop()


class CtiForCssRunner(Thread):
    def __init__(self, gui_data: GraphicalInterface):
        super().__init__()
        self.gui_data = gui_data
        self.error_occurred_while_configuring = False

    def __set_configurations(self):
        ConfigurationManager.All.temporary_files_directory = self.gui_data.temporary_files_directory_value.get()

        ConfigurationManager.Log.Console.enable = True if self.gui_data.console_logging_value.get() == 1 else False
        if ConfigurationManager.Log.Console.enable:
            match self.gui_data.console_log_level_value.get():
                case "Debug":
                    ConfigurationManager.Log.Console.level = logging.DEBUG
                case "Info":
                    ConfigurationManager.Log.Console.level = logging.INFO
                case "Warning":
                    ConfigurationManager.Log.Console.level = logging.WARNING
                case "Error":
                    ConfigurationManager.Log.Console.level = logging.ERROR
            ConfigurationManager.Log.Console.format = self.gui_data.console_log_format_text.get(0.0, END)

        ConfigurationManager.Log.File.enable = True if self.gui_data.file_logging_value.get() == 1 else False
        if ConfigurationManager.Log.File.enable:
            match self.gui_data.file_log_level_value.get():
                case "Debug":
                    ConfigurationManager.Log.File.level = logging.DEBUG
                case "Info":
                    ConfigurationManager.Log.File.level = logging.INFO
                case "Warning":
                    ConfigurationManager.Log.File.level = logging.WARNING
                case "Error":
                    ConfigurationManager.Log.File.level = logging.ERROR
            ConfigurationManager.Log.File.format = self.gui_data.file_log_format_text.get(0.0, END)
            ConfigurationManager.Log.File.directory = self.gui_data.file_log_directory_value.get()
            ConfigurationManager.Log.File.name = self.gui_data.file_log_name_value.get()

        match self.gui_data.model_preparation_value.get():
            case 1:
                ConfigurationManager.DeepLearning.model_preparation = DeepLearningOperation.TRAIN
                selected_neural_network = self.gui_data.neural_network_list.curselection()
                if len(selected_neural_network) < 1:
                    tkinter.messagebox.showerror(title="No Neural Network Selected",
                                                 message="You have to select a neural network!")
                    self.gui_data.active_process_window.destroy()
                    self.error_occurred_while_configuring = True
                    return

                match selected_neural_network[0]:
                    case 0:
                        ConfigurationManager.DeepLearning.Method.selected_algorithm = NeuralNetwork.BI_LSTM
                    case 1:
                        ConfigurationManager.DeepLearning.Method.selected_algorithm = NeuralNetwork.LSTM
                    case 2:
                        ConfigurationManager.DeepLearning.Method.selected_algorithm = NeuralNetwork.ONE_D_CNN
                    case 3:
                        ConfigurationManager.DeepLearning.Method.selected_algorithm = NeuralNetwork.MLP
                    case 4:
                        ConfigurationManager.DeepLearning.Method.selected_algorithm = NeuralNetwork.GRU
                    case 5:
                        ConfigurationManager.DeepLearning.Method.selected_algorithm = NeuralNetwork.ESN
                    case 6:
                        ConfigurationManager.DeepLearning.Method.selected_algorithm = NeuralNetwork.DISTIL_BERT
                    case 7:
                        ConfigurationManager.DeepLearning.Method.selected_algorithm = NeuralNetwork.BERT

                ConfigurationManager.DeepLearning.Method.model_save_path: str = self.gui_data.model_save_path_value.get()

                ConfigurationManager.DeepLearning.Dataset.inclusion_of_x32 = True if self.gui_data.inclusion_of_x32_value.get() == 1 else False
                if ConfigurationManager.DeepLearning.Dataset.inclusion_of_x32:
                    ConfigurationManager.DeepLearning.Dataset.labels_path_for_x32 = self.gui_data.labels_path_for_x32_value.get()
                    ConfigurationManager.DeepLearning.Dataset.functions_path_for_x32 = self.gui_data.functions_path_for_x32_value.get()
                ConfigurationManager.DeepLearning.Dataset.labels_path_for_x64 = self.gui_data.labels_path_for_x64_value.get()
                ConfigurationManager.DeepLearning.Dataset.functions_path_for_x64 = self.gui_data.functions_path_for_x64_value.get()

                ConfigurationManager.DeepLearning.Validation.shuffle = True if self.gui_data.shuffle_value.get() == 1 else False
                ConfigurationManager.DeepLearning.Validation.holdout_split_ratio = self.gui_data.holdout_value.get()
                ConfigurationManager.DeepLearning.Validation.validation_split_ratio = self.gui_data.validation_value.get()

                ConfigurationManager.DeepLearning.Plot.save_model_history = True if self.gui_data.save_model_history_value == 1 else False
                ConfigurationManager.DeepLearning.Plot.save_dataset_label_distribution = True if self.gui_data.save_dataset_label_distribution_value == 1 else False
                if (ConfigurationManager.DeepLearning.Plot.save_model_history or
                        ConfigurationManager.DeepLearning.Plot.save_dataset_label_distribution):
                    ConfigurationManager.DeepLearning.Plot.save_path = self.gui_data.figure_save_path_directory_value.get()
            case 2:
                ConfigurationManager.DeepLearning.model_preparation = DeepLearningOperation.IMPORT
                ConfigurationManager.DeepLearning.Method.selected_algorithm = NeuralNetwork.UNKNOWN
                ConfigurationManager.DeepLearning.Method.model_import_path: str = self.gui_data.model_import_path_value.get()

        ConfigurationManager.CyberThreatIntelligence.build_cti = True if self.gui_data.build_cti_value.get() == 1 else False
        if ConfigurationManager.CyberThreatIntelligence.build_cti:
            ConfigurationManager.Reconstruction.retdec_installation_directory = self.gui_data.retdec_installation_directory_value.get()

            if self.gui_data.cti_targets_list.index("end") == 0:
                tkinter.messagebox.showerror(title="No Binary Inserted",
                                             message="You have to insert a binary to the list!")
                self.gui_data.active_process_window.destroy()
                self.error_occurred_while_configuring = True
                return
            ConfigurationManager.CyberThreatIntelligence.target_files = self.gui_data.cti_targets_list.get("0", END)
            ConfigurationManager.CyberThreatIntelligence.save_path = self.gui_data.cti_save_directory_value.get()
            ConfigurationManager.CyberThreatIntelligence.vulnerability_threshold = self.gui_data.cti_threshold_value.get()
            analyze_only_functions_input = self.gui_data.cti_analyze_only_functions_value.get()
            analyze_only_functions = [function_name.strip() for function_name in analyze_only_functions_input.split(',') if len(function_name.strip()) > 0]
            ConfigurationManager.CyberThreatIntelligence.analyze_only_functions = analyze_only_functions

    def run(self):
        try:
            self.__set_configurations()

            if not self.error_occurred_while_configuring:
                with redirect_stdout(CtiForCssRunner.WriteProcessor(self.gui_data)):
                    Orchestrator().orchestrate()
        except Exception as exception:
            try:
                tkinter.messagebox.showerror(title="Error", message="An exception has occurred: " + str(exception))
            except Exception:
                pass

    def __get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id

        for id, thread in threading._active.items():
            if thread is self:
                return id

    def terminate(self):
        thread_id = self.__get_id()
        result = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if result > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

    class WriteProcessor:

        def __init__(self, gui_data: GraphicalInterface):
            self.real_stdout_for_test = sys.stdout
            self.main_buffer = ""
            self.gui_data = gui_data

        # noinspection PyMethodMayBeStatic
        def flush(self):
            self.real_stdout_for_test.flush()

        def write(self, temporary_buffer):
            while temporary_buffer:
                try:
                    newline_index = temporary_buffer.index("\n")
                    data = self.main_buffer + temporary_buffer[:newline_index + 1]
                    self.gui_data.inform_for_active_process(data, False)
                    self.main_buffer = ""
                    temporary_buffer = temporary_buffer[newline_index + 1:]
                except ValueError:
                    print("")
                    self.main_buffer += temporary_buffer
                    data = self.main_buffer
                    self.gui_data.inform_for_active_process(data, True)
                    self.main_buffer = ""
                    break


if __name__ == "__main__":
    GraphicalInterface().show_window()
