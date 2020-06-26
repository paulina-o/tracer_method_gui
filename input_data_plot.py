# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'input_plot.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_InputPlot(object):
    def setupUi(self, InputPlot):
        InputPlot.setObjectName("InputPlot")
        InputPlot.resize(600, 500)
        InputPlot.setMinimumSize(QtCore.QSize(600, 500))
        self.horizontalLayout = QtWidgets.QHBoxLayout(InputPlot)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plotWidget = QtWidgets.QWidget(InputPlot)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotWidget.sizePolicy().hasHeightForWidth())
        self.plotWidget.setSizePolicy(sizePolicy)
        self.plotWidget.setMinimumSize(QtCore.QSize(400, 300))
        self.plotWidget.setMaximumSize(QtCore.QSize(100000, 100000))
        self.plotWidget.setObjectName("plotWidget")
        self.plotWidgetLayout = QtWidgets.QVBoxLayout(self.plotWidget)
        self.plotWidgetLayout.setObjectName("plotWidgetLayout")
        self.horizontalLayout.addWidget(self.plotWidget)

        self.retranslateUi(InputPlot)
        QtCore.QMetaObject.connectSlotsByName(InputPlot)

    def retranslateUi(self, InputPlot):
        _translate = QtCore.QCoreApplication.translate
        InputPlot.setWindowTitle(_translate("InputPlot", "Input data"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    InputPlot = QtWidgets.QWidget()
    ui = Ui_InputPlot()
    ui.setupUi(InputPlot)
    InputPlot.show()
    sys.exit(app.exec_())

