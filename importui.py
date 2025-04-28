import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("C:/Users/Davev/Documents/zadanie_1_qt_1304/form.ui", self)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()