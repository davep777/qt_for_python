from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu,
QMessageBox)
from PySide6.QtGui import QAction, QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Aplikacja z QAction")
        self.setGeometry(100,100,600,400)

        #akcje

        nowa_akcja = QAction(QIcon("C:/Users/Davev/Desktop/Python/qt/zadania/notebook.png"),"Nowy", self)
        nowa_akcja.setShortcut("Ctrl+N")
        nowa_akcja.setStatusTip("Utwórz nowy plik")
        nowa_akcja.triggered.connect(self.new_file)

        otworz_akcja = QAction(QIcon("C:/Users/Davev/Desktop/Python/qt/zadania/notebook--pencil.png"),"Otwórz", self)
        otworz_akcja.setShortcut("Ctrl+O")
        otworz_akcja.setStatusTip("Otwórz istniejący plik")
        otworz_akcja.triggered.connect(self.open_file)

        zapisz_akcja = QAction("Zapisz",  self)
        zapisz_akcja.setShortcut("Ctrl+S")
        zapisz_akcja.setStatusTip("Zapisz plik")
        zapisz_akcja.triggered.connect(self.save_file)

        zamknij_akcja = QAction("Zamknij", self)
        zamknij_akcja.setShortcut("Ctrl+Q")
        zamknij_akcja.triggered.connect(self.close)

        #menu
        menu_bar = self.menuBar()

        #pierwsze
        plik_menu = menu_bar.addMenu("&Plik")
        plik_menu.addAction(nowa_akcja)
        plik_menu.addAction(otworz_akcja)
        plik_menu.addSeparator()
        plik_menu.addAction(zapisz_akcja)
        plik_menu.addAction(zamknij_akcja)

        #drugie
        edycja_menu = menu_bar.addMenu("&Edycja")

        kopiuj_akcja = QAction("Kopiuj", self)
        kopiuj_akcja.setShortcut("Ctrl+C")
        kopiuj_akcja.setStatusTip("Skopiuj")

        wklej_akcja = QAction("Wklej", self)
        wklej_akcja.setShortcut("Ctrl+V")
        wklej_akcja.setStatusTip("Wklej")

        #podmenu
        sub_menu = QMenu("Więcej opcji", self)
        sub_menu.addAction(kopiuj_akcja)
        sub_menu.addAction(wklej_akcja)

        edycja_menu.addMenu(sub_menu)

        self.statusBar()

    def new_file(self):
        QMessageBox.information(self, "Nowy Plik", "Tworzenie nowego pliku")

    def open_file(self):
        QMessageBox.information(self, "Otwórz Plik", "Otwieranie nowego pliku")

    def save_file(self):
        QMessageBox.information(self, "Zapisz Plik", "Zapisywanie nowego pliku")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()





        





