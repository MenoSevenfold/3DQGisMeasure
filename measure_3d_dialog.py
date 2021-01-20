

import os

from PyQt5 import *
from PyQt5 import QtCore, QtGui, QtWidgets

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'measure_3d_dialog_base.ui'))


class Measure3dDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(Measure3dDialog, self).__init__(parent)
        self.setupUi(self)
