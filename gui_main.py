import functools
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from tracer_method.core.exceptions import FileException
from tracer_method.core.read_data.read_input_file import read_tritium_file
from tracer_method.core.read_data.read_observations_file import read_observations
from tracer_method.core.tritium.tritium_method import tritium_method

from gui_base import Ui_Gui
from gui_utils import round_sig
from gui_utils import save_to_csv
from table_main import TableUi


class MainGui(Ui_Gui):
    def __init__(self):
        super(MainGui, self).__init__()
        self.input_file: str = ''
        self.observations_file: str = ''

        self.index = 0
        self.models_list = ['PFM', 'EM', 'EPM', 'DM']

        self.model_checked: Dict[str, dict] = {name: False for name in self.models_list}
        self.beta_checked: Dict[str, dict] = {name: False for name in self.models_list}

        self.params: Dict[str, List[str]] = {
            'PFM': {'display': ['\u03C4'], 'csv': ['T']},
            'EM': {'display': ['\u03C4'], 'csv': ['T']},
            'EPM': {'display': ['\u03C4', '\u03B7'], 'csv': ['T', 'n']},
            'DM': {'display': ['\u03C4', 'PD'], 'csv': ['T', 'PD']}
        }

        self.fig_dict = {}
        self.canvas_created = False

        self.table_form = QtWidgets.QWidget()
        self.table = TableUi()
        self.table.setupUi(self.table_form)
        self.table.setup_table()
        self.table.setup_callbacks()

    def input_file_button_clicked(self):
        """ Get input file name. """
        self.input_file = QtWidgets.QFileDialog.getOpenFileName(None, "Open ", '.', "(*.xlsx *.xls *.csv)")[0]
        if self.input_file:
            self.inputFileEdit.setText(self.input_file)

    def output_file_button_clicked(self):
        """ Get observations file name. """
        self.observations_file = QtWidgets.QFileDialog.getOpenFileName(None, "Open ", '.', "(*.xlsx *.xls *.csv)")[0]
        if self.observations_file:
            self.outputFileEdit.setText(self.observations_file)

    def start_button_clicked(self):
        """ Start program. """
        warnings = self.check_configuration()

        if warnings:
            QtWidgets.QMessageBox.warning(None, 'Error', warnings)
            return

        self.__setup_models()
        alpha = float(self.alphaDoubleSpinBox.text())
        models_picked = self.get_models_configs()

        input_data = read_tritium_file(Path(self.input_file))
        obs_data = read_observations(Path(self.observations_file))

        final_data = tritium_method(input_data, obs_data, alpha, models_picked)

        self.stackedWidget.setCurrentIndex(1)

        if not self.canvas_created:
            self.figure = Figure(figsize=(3, 2), dpi=100)
            self.canvas = FigureCanvas(self.figure)
            self.canvas.setMinimumSize(self.canvas.size())
            self.plotWidgetLayout.addWidget(self.canvas)
            self.canvas.draw()
            self.canvas_created = True

        name = Path(self.observations_file).stem
        for index, data in enumerate(final_data):
            self.add_figure(f'{name}', self.figure, data, self.index)

        self.checkButton.setEnabled(True)
        self.ModelsPushButton.setEnabled(True)

    def close_button_clicked(self):
        ret = QtWidgets.QMessageBox.question(None, 'Close request', 'Are you sure you want to quit?',
                                             QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                             QtWidgets.QMessageBox.Yes)
        if ret == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def save_button_clicked(self):
        """ Save output and response function of all checked results in directory with timestamp. """
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory")

        results_name = f'results_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'
        Path(Path(directory, results_name)).mkdir(parents=True, exist_ok=True)

        for i in range(self.plotListWidget.count()):
            if self.plotListWidget.item(i).checkState() == QtCore.Qt.Checked:
                name = self.plotListWidget.item(i).text()
                elem = self.fig_dict[name]

                data = elem[1]
                model_type = data.model_type
                params = [f'{i}={j}({round_sig(j)})'
                          for i, j, k in zip(self.params[model_type]['csv'], data.params, data.params_accuracy)]
                beta = data.beta
                x_o, y_o = data.output

                model_data = [model_type] + params
                if beta:
                    model_data.append(f'beta={beta}')

                path = Path(directory, results_name, name.split(' ')[-1])
                Path(path).mkdir(parents=True, exist_ok=True)

                save_to_csv(Path(path, 'output.csv'), model_data, x_o, y_o)

                if not model_type == 'PFM':
                    x_rf, y_rf = data.response_function
                    save_to_csv(Path(path, 'response_function.csv'), model_data, x_rf, y_rf)

    def check_button_clicked(self):
        """ Check/Uncheck all results."""
        if self.checkButton.text() == 'Check all':
            self.checkButton.setText('Uncheck')

            for index in range(self.plotListWidget.count()):
                self.plotListWidget.item(index).setCheckState(QtCore.Qt.Checked)

        else:
            self.checkButton.setText('Check all')

            for index in range(self.plotListWidget.count()):
                self.plotListWidget.item(index).setCheckState(QtCore.Qt.Unchecked)

    def delete_button_clicked(self):
        """ Delete selected results from list. """
        ret = QtWidgets.QMessageBox.question(None, 'Delete request', 'Are you sure you want to delete selected items?',
                                             QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                             QtWidgets.QMessageBox.Yes)
        if ret == QtWidgets.QMessageBox.Yes:
            checked_items = sorted([i for i in range(self.plotListWidget.count()) if
                                    self.plotListWidget.item(i).checkState() == QtCore.Qt.Checked], reverse=True)
            for i in checked_items:
                text = self.plotListWidget.item(i).text()
                del self.fig_dict[text]
                self.index -= 1
                self.plotListWidget.takeItem(i)
                self.table.tableWidget.removeRow(i)
                for j in range(i, self.plotListWidget.count()):
                    text = self.plotListWidget.item(j).text()
                    num = int(text.split('.')[0])
                    rest = text.split('.')[1]
                    self.plotListWidget.item(j).setText(f'{num - 1}.{rest}')
                    self.fig_dict[f'{num - 1}.{rest}'] = self.fig_dict.pop(text)
                    self.plotListWidget.item(i)

            if not self.plotListWidget.count():
                self.checkButton.setText('Check all')
                self.checkButton.setEnabled(False)
                self.savePushButton.setEnabled(False)
                self.deleteButton.setEnabled(False)
                self.ModelsPushButton.setEnabled(False)
                self.betaTextBrowser.setText(' ')
                self.paramsTextBrowser.setText(' ')
                self.modelTextBrowser.setText(' ')
                self.mseTextBrowser.setText(' ')
                self.figure.clf()
                self.canvas.draw()

            checked_items = [i for i in range(self.plotListWidget.count()) if
                             self.plotListWidget.item(i).checkState() == QtCore.Qt.Checked]

            if not checked_items:
                self.checkButton.setText('Check all')
                self.savePushButton.setEnabled(False)
                self.deleteButton.setEnabled(False)
        else:
            pass


    def model_check_box_clicked(self, type: str, check_box, group_boxes):
        """ Check model box. """
        state = check_box.isChecked()

        self.model_checked[type] = state

        for group_box in group_boxes:
            group_box.setEnabled(state)

    def model_beta_check_box_clicked(self, type: str, check_box, group_box):
        """ Check beta box. """
        state = check_box.isChecked()

        self.beta_checked[type] = state
        group_box.setEnabled(state)

    def go_back_button_clicked(self):
        """ Change page to configuration. """
        self.stackedWidget.setCurrentIndex(0)

    def plots_button_clicked(self):
        """ Change page to plots. """
        self.stackedWidget.setCurrentIndex(1)

    def table_button_clicked(self):
        """ Show table with models data. """
        self.table_form.show()

    def item_selected(self):
        """ Set and enable appropriate buttons related to selecting models. """
        if self.checkButton.text() == 'Check all':
            self.savePushButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        elif self.checkButton.text() == 'Uncheck':
            self.savePushButton.setEnabled(True)
            self.deleteButton.setEnabled(True)
        if any(self.plotListWidget.item(i).checkState() == QtCore.Qt.Checked for i in range(self.plotListWidget.count())):
            self.checkButton.setText('Uncheck')
            self.savePushButton.setEnabled(True)
            self.deleteButton.setEnabled(True)
        else:
            self.checkButton.setText('Check all')
            self.savePushButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def check_configuration(self):
        """ Check and validate configuration. """
        files = []
        models = []
        input_file = ''
        obs_file = ''
        bounds = ''

        if not self.input_file:
            files.append('input file')
        else:
            try:
                read_tritium_file(Path(self.input_file))
            except FileException as e:
                input_file = e.message

        if not self.input_file:
            files.append('observations file')
        else:
            try:
                read_observations(Path(self.observations_file))
            except FileException as e:
                obs_file = e.message

        if self.EMwrnLabel.text() or self.PFMwrnLabel.text() or self.DMwrnLabel.text() or self.EMwrnLabel.text():
            bounds = 'Set correct bounds'

        if not any(i for i in self.model_checked.values() if i):
            models = 'Select at least one model'

        if files or bounds or models or input_file or obs_file:
            files = f'Define {" and ".join(files)}\n' if files else ''
            models = f'{models}\n' if models else ''
            input_file = f'Input file: {input_file}\n' if input_file else ''
            obs_file = f'Observations file: {obs_file}\n' if obs_file else ''

            return f'{files}{bounds}{models}{input_file}{obs_file}'

        return ''

    def show_plot(self, fig_data):
        """ Show plot. """
        fig, data, index = fig_data
        fig.clf()
        self.axes = fig.add_subplot(111)

        self.axes.plot(data.observations[0], data.observations[1], 'x', color='red')
        self.axes.plot(data.output[0], data.output[1], color='blue')
        self.axes.set_xlim([min(data.observations[0]) - 2, max(data.observations[0]) + 2])
        self.axes.set_ylim([min(data.output[1]) - 2, max(data.output[1]) + 2])
        self.axes.set_ylabel('Tritium content [T.U.]')
        self.axes.set_xlabel('Year')
        fig.tight_layout()
        self.xlimDoubleSpinBox_1.setValue(min(data.observations[0]) - 2)
        self.xlimDoubleSpinBox_2.setValue(max(data.observations[0]) + 2)

        # y_lim_bottom, y_lim_top = self.axes.get_ylim()

        self.ylimDoubleSpinBox_1.setValue(min(data.observations[1]) - 2)
        self.ylimDoubleSpinBox_2.setValue(max(data.observations[1]) + 2)

        self.canvas.draw()

        self.betaTextBrowser.setText(f'{data.beta}' if data.beta else '-')

        params = self.params[data.model_type]['display']
        self.paramsTextBrowser.setText(', '.join(f'{i} = {j} ({round_sig(k)})'
                                                 for i, j, k in zip(params, data.params, data.params_accuracy)))
        self.modelTextBrowser.setText(data.model_type)
        self.mseTextBrowser.setText(f'{data.mse}')
        self.meTextBrowser.setText(f'{data.model_efficiency}')

        self.mseTextBrowser.setAlignment(QtCore.Qt.AlignCenter)
        self.meTextBrowser.setAlignment(QtCore.Qt.AlignCenter)
        self.betaTextBrowser.setAlignment(QtCore.Qt.AlignCenter)
        self.paramsTextBrowser.setAlignment(QtCore.Qt.AlignCenter)
        self.modelTextBrowser.setAlignment(QtCore.Qt.AlignCenter)

    def change_figure(self, item):
        """ Change figure."""
        text = item.text()
        self.show_plot(self.fig_dict[text])

    def add_figure(self, name, fig, data, index):
        """ Add figure to dictionary and update table with params information. """
        u = 0
        if any(name in i for i in self.fig_dict.keys()):
            u = len([i for i in self.fig_dict.keys() if name in i])
        name = f'{name}_{u}'

        self.fig_dict[f'{len(self.fig_dict.keys()) + 1}. {name}'] = (fig, data, index)

        item = QtWidgets.QListWidgetItem(f'{len(self.fig_dict.keys())}. {name}')
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Unchecked)

        self.plotListWidget.addItem(item)

        self.table.update_table(name, data)

    def upper_bound_changed(self, y, label, value: float):
        """ Set warnings if lower bound is greater than upper. """
        lower_bnd = float(y.text())
        if lower_bnd > value:
            label.setText("<font color='red'>Set correct bounds</font>")
        else:
            label.setText('')

    def lower_bound_changed(self, y, label, value: float):
        """ Set warnings if upper bound is lower than greater. """
        upper_bnd = float(y.text())
        if upper_bnd < value:
            label.setText("<font color='red'>Set correct bounds</font>")
        else:
            label.setText('')

    def axes_lower_bound_changed(self, x, x1, axis):
        """ Set minimum and maximum of axes if lower bound of axis is changed. """
        if axis == 'Y':
            current_limits = self.axes.get_ylim()
        else:
            current_limits = self.axes.get_xlim()

        value = float(x.text())

        if value < current_limits[1]:
            if axis == 'Y':
                self.axes.set_ylim(bottom=value)
            else:
                self.axes.set_xlim(left=value)
            self.canvas.draw()

        x1.setMinimum(value)
        x.setMaximum(current_limits[1])

    def axes_upper_bound_changed(self, x, x1, axis):
        """ Set minimum and maximum of axes if upper bound of axis is changed. """
        if axis == 'Y':
            current_limits = self.axes.get_ylim()
        else:
            current_limits = self.axes.get_xlim()
        value = float(x1.text())

        if value > current_limits[0]:
            if axis == 'Y':
                self.axes.set_ylim(top=value)
            else:
                self.axes.set_xlim(right=value)
            self.canvas.draw()

        x1.setMinimum(current_limits[0])
        x.setMaximum(value)

    def setup_callbacks(self):
        """ Setup callbacks. """
        self.savePushButton.setEnabled(False)
        self.deleteButton.setEnabled(False)

        # files buttons
        self.inputFileButton.clicked.connect(self.input_file_button_clicked)
        self.outputFileButton.clicked.connect(self.output_file_button_clicked)

        # buttons
        self.startButton.clicked.connect(self.start_button_clicked)
        self.closeButton.clicked.connect(self.close_button_clicked)
        self.closeButton_2.clicked.connect(self.close_button_clicked)
        self.goBackButton.clicked.connect(self.go_back_button_clicked)
        self.plotsButton.clicked.connect(self.plots_button_clicked)
        self.ModelsPushButton.clicked.connect(self.table_button_clicked)
        self.checkButton.clicked.connect(self.check_button_clicked)
        self.plotListWidget.itemChanged.connect(self.item_selected)

        # DM
        self.__setup_model_callbacks('DM', self.DMcheckBox, [self.DM_GroupBox, self.DM_timeGroupBox,
                                                             self.DM_pdGroupBox])
        self.__setup_beta_callbacks('DM', self.DM_betaCheckBox, self.DM_betaGroupBox)
        self.__setup_bounds_callbacks(self.DM_timeDoubleSpinBox_1, self.DM_timeDoubleSpinBox_2, self.DMwrnLabel)
        self.__setup_bounds_callbacks(self.DM_pdDoubleSpinBox_1, self.DM_pdDoubleSpinBox_2, self.DMwrnLabel)

        # EM
        self.__setup_model_callbacks('EM', self.EMcheckBox, [self.EM_GroupBox, self.EM_timeGroupBox])
        self.__setup_beta_callbacks('EM', self.EM_betaCheckBox, self.EM_betaGroupBox)
        self.__setup_bounds_callbacks(self.EM_timeDoubleSpinBox_1, self.EM_timeDoubleSpinBox_2, self.EMwrnLabel)

        # EPM
        self.__setup_model_callbacks('EPM', self.EPMcheckBox, [self.EPM_GroupBox, self.EPM_timeGroupBox,
                                                               self.EPM_etaGroupBox])
        self.__setup_beta_callbacks('EPM', self.EPM_betaCheckBox, self.EPM_betaGroupBox)
        self.__setup_bounds_callbacks(self.EPM_timeDoubleSpinBox_1, self.EPM_timeDoubleSpinBox_2, self.EPMwrnLabel)
        self.__setup_bounds_callbacks(self.EPM_etaDoubleSpinBox_1, self.EPM_etaDoubleSpinBox_2, self.EPMwrnLabel)

        # PFM
        self.__setup_model_callbacks('PFM', self.PFMcheckBox, [self.PFM_GroupBox, self.PFM_timeGroupBox])
        self.__setup_beta_callbacks('PFM', self.PFM_betaCheckBox, self.PFM_betaGroupBox)
        self.__setup_bounds_callbacks(self.PFM_timeDoubleSpinBox_1, self.PFM_timeDoubleSpinBox_2, self.PFMwrnLabel)

        # plot widget
        self.plotListWidget.itemClicked.connect(self.change_figure)

        self.savePushButton.clicked.connect(self.save_button_clicked)
        self.deleteButton.clicked.connect(self.delete_button_clicked)

        self.__setup_axes_bounds_callbacks(self.xlimDoubleSpinBox_1, self.xlimDoubleSpinBox_2, 'X')

        self.__setup_axes_bounds_callbacks(self.ylimDoubleSpinBox_1, self.ylimDoubleSpinBox_2, 'Y')

    def __setup_axes_bounds_callbacks(self, spin_box_1, spin_box_2, xy):
        """ Setup axes bounds callbacks. """
        spin_box_1.valueChanged.connect(functools.partial(self.axes_lower_bound_changed, spin_box_1, spin_box_2, xy))
        spin_box_2.valueChanged.connect(functools.partial(self.axes_upper_bound_changed, spin_box_1, spin_box_2, xy))

    def __setup_beta_callbacks(self, type, check_box, group_box):
        """ Setup beta callbacks. """
        check_box.clicked.connect(functools.partial(self.model_beta_check_box_clicked, type, check_box, group_box))

    def __setup_model_callbacks(self, type, check_box, group_boxes):
        """ Setup model callbacks. """
        check_box.clicked.connect(functools.partial(self.model_check_box_clicked, type, check_box, group_boxes))

    def __setup_bounds_callbacks(self, lower_spin_box, upper_spin_box, label):
        """ Setup params bounds callbacks. """
        lower_spin_box.valueChanged.connect(functools.partial(self.lower_bound_changed, upper_spin_box, label))
        upper_spin_box.valueChanged.connect(functools.partial(self.upper_bound_changed, lower_spin_box, label))

    def get_models_configs(self):
        """ Select models configurations which were chosen. """
        models = []
        for type, checked in self.model_checked.items():
            if checked:
                model = [type, self.models_setup[type]['params']]
                if self.beta_checked[type]:
                    model.append(self.models_setup[type]['beta'])

                models.append(model)

        return models

    def __setup_models(self):
        """ Get all defined models information. """
        self.models_setup = {
            'PFM': {'beta': float(self.PFM_betaDoubleSpinBox.text()),
                    'params': ((float(self.PFM_timeDoubleSpinBox_1.text()),
                                float(self.PFM_timeDoubleSpinBox_2.text())),)
                    },

            'DM': {'beta': float(self.DM_betaDoubleSpinBox.text()),
                   'params': ((float(self.DM_timeDoubleSpinBox_1.text()), float(self.DM_timeDoubleSpinBox_2.text())),
                              (float(self.DM_pdDoubleSpinBox_1.text()), float(self.DM_pdDoubleSpinBox_2.text())))
                   },

            'EM': {'beta': float(self.EM_betaDoubleSpinBox.text()),
                   'params': ((float(self.EM_timeDoubleSpinBox_1.text()), float(self.EM_timeDoubleSpinBox_2.text())), )
                   },

            'EPM': {'beta': float(self.EPM_betaDoubleSpinBox.text()),
                    'params': ((float(self.EPM_timeDoubleSpinBox_1.text()), float(self.EPM_timeDoubleSpinBox_2.text())),
                               (float(self.EPM_etaDoubleSpinBox_1.text()), float(self.EPM_etaDoubleSpinBox_2.text())))
                    }

        }


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Gui = QtWidgets.QWidget()
    ui = MainGui()
    ui.setupUi(Gui)
    ui.setup_callbacks()

    Gui.show()
    sys.exit(app.exec_())
