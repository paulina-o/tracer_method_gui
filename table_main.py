import csv
from datetime import datetime
from pathlib import Path

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from tracer_method.core.fitting_result import FittingResult

from gui_utils import round_sig
from table_base import Ui_Table


class TableUi(Ui_Table):
    def __init__(self):
        super(Ui_Table, self).__init__()

    def setup_table(self):
        self.tableWidget.setColumnWidth(0, 160)
        self.tableWidget.setColumnWidth(1, 80)
        self.tableWidget.setColumnWidth(2, 180)
        self.tableWidget.setColumnWidth(3, 57)
        self.tableWidget.setColumnWidth(4, 57)
        self.tableWidget.setColumnWidth(5, 57)

    def update_table(self, name: str, data: FittingResult):
        """ Update table with new row. """
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)

        params = ', '.join([f'{i}({round_sig(j)})' for i, j in zip(data.params, data.params_accuracy)])
        beta = str(data.beta) if data.beta else '-'

        data_list = [name, data.model_type, params, beta, str(data.mse), str(data.model_efficiency)]

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
