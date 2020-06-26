from PyQt5 import QtCore
from tracer_method.core.tritium.tritium_method import tritium_method


class ThreadClass(QtCore.QThread):
    notifyProgress = QtCore.pyqtSignal(int)
    notifyProgressLabel = QtCore.pyqtSignal(str)
    notifyCalculationsLabel = QtCore.pyqtSignal(str)
    finalData = QtCore.pyqtSignal(list)

    def __init__(self, models, input, obs, alpha, calculate_uncertainty, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.models_picked = models
        self.input = input
        self.obs = obs
        self.alpha = alpha
        self.calculate_uncertainty = calculate_uncertainty

    def run(self):
        self.notifyCalculationsLabel.emit('Calculations in progress')

        for index, model_picked in enumerate(self.models_picked):
            data = tritium_method(self.input, self.obs, self.alpha, [model_picked], self.calculate_uncertainty)
            value = round((index + 1) / len(self.models_picked), 2) * 100
            self.notifyProgress.emit(value)
            self.notifyProgressLabel.emit(f'{value}%')
            self.finalData.emit(data)

        self.notifyCalculationsLabel.emit('')
