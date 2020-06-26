# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'table_base.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Table(object):
    def setupUi(self, Table):
        Table.setObjectName("Data Table")
        Table.resize(650, 300)
        Table.setMinimumSize(QtCore.QSize(650, 300))
        self.gridLayout = QtWidgets.QGridLayout(Table)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(Table)
        self.tableWidget.setMinimumSize(QtCore.QSize(110, 80))
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.saveButton = QtWidgets.QToolButton(Table)
        self.saveButton.setMinimumSize(QtCore.QSize(80, 0))
        self.saveButton.setMaximumSize(QtCore.QSize(80, 60))
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 1, 0, 1, 1)

        self.retranslateUi(Table)
        QtCore.QMetaObject.connectSlotsByName(Table)

    def retranslateUi(self, Table):
        _translate = QtCore.QCoreApplication.translate
        Table.setWindowTitle(_translate("Table", "Data Table"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Table", "Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Table", "Model Type"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Table", "Parameters"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Table", "Beta"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Table", "MSE"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Table", "ME"))
        self.saveButton.setText(_translate("Table", "Save to csv"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Table = QtWidgets.QWidget()
    ui = Ui_Table()
    ui.setupUi(Table)
    Table.show()
    sys.exit(app.exec_())

