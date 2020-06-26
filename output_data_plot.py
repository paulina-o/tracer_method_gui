# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'base/output_data_plot.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_OutputPlot(object):
    def setupUi(self, OutputPlot):
        OutputPlot.setObjectName("OutputPlot")
        OutputPlot.resize(600, 500)
        OutputPlot.setMinimumSize(QtCore.QSize(600, 500))
        self.horizontalLayout = QtWidgets.QHBoxLayout(OutputPlot)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plotWidget = QtWidgets.QWidget(OutputPlot)
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

        self.retranslateUi(OutputPlot)
        QtCore.QMetaObject.connectSlotsByName(OutputPlot)

    def retranslateUi(self, OutputPlot):
        _translate = QtCore.QCoreApplication.translate
        OutputPlot.setWindowTitle(_translate("OutputPlot", "Observations Data"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OutputPlot = QtWidgets.QWidget()
    ui = Ui_OutputPlot()
    ui.setupUi(OutputPlot)
    OutputPlot.show()
    sys.exit(app.exec_())

