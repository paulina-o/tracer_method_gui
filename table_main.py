import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from tracer_method.core.fitting_result import FittingResult

from base.table_base import Ui_Table
from gui_utils import round_sig


class TableUi(Ui_Table):
    def __init__(self):
        super(Ui_Table, self).__init__()
        self.params: Dict[str, List[str]] = {
            'PFM': {'display': ['\u03C4'], 'csv': ['T']},
            'EM': {'display': ['\u03C4'], 'csv': ['T']},
            'EPM': {'display': ['\u03C4', '\u03B7'], 'csv': ['T', 'n']},
            'DM': {'display': ['\u03C4', 'PD'], 'csv': ['T', 'PD']}
        }

    def setup_table(self):
        self.tableWidget.setColumnWidth(0, 160)
        self.tableWidget.setColumnWidth(1, 80)
        self.tableWidget.setColumnWidth(2, 250)
        self.tableWidget.setColumnWidth(3, 170)
        self.tableWidget.setColumnWidth(4, 57)
        self.tableWidget.setColumnWidth(5, 57)

    def update_table(self, name: str, data: FittingResult):
        """ Update table with new row. """
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        if data.confidence_interval:
            params = ', '.join([f'{i} {round_sig(j)}' for i, j in zip(data.params, data.confidence_interval)])
            confidence_level = ', '.join(f'{i * 100}% ({j})' for i, j in zip(data.confidence_level,
                                                                             self.params[data.model_type]['display']))
        else:
            params = ', '.join([f'{i} (-)' for i in data.params])
            confidence_level = '-'

        beta = str(data.beta) if data.beta else '-'

        data_list = [name, data.model_type, params, confidence_level, beta, str(data.mse), str(data.model_efficiency)]

        for index, data in enumerate(data_list):
            item = QtWidgets.QTableWidgetItem(data)
            item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            self.tableWidget.setItem(row_position, index, item)

    def save_button_clicked(self):
        """ Select name of the file. """
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory")

        results_name = f'parameters_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv'

        if directory:
            with open(Path(directory, results_name), 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(['Name', 'Model Type', 'Params', 'Beta', 'MSE', 'ME'])

                for row in range(self.tableWidget.rowCount()):
                    text = [self.tableWidget.item(row, col).text() for col in range(self.tableWidget.columnCount())]

                    writer.writerow(text)

    def setup_callbacks(self):
        """ Setup callbacks. """
        self.saveButton.clicked.connect(self.save_button_clicked)
