from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QStatusBar, QVBoxLayout, QWidget, QPushButton, QDialog, QLabel, QCheckBox, QRadioButton, QLineEdit, QMessageBox
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QSize, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Aplikacja z QAction")
        self.setGeometry(100, 100, 600, 400)

        # Menu Bar
        menu_bar = self.menuBar()

        plik_menu = menu_bar.addMenu("&Plik")
        nowa_akcja = QAction(QIcon("C:/Users/Davev/Desktop/Python/qt/zadania/notebook.png"), "Nowy", self)
        nowa_akcja.setShortcut("Ctrl+N")
        nowa_akcja.setStatusTip("Utwórz nowy plik")
        nowa_akcja.triggered.connect(self.new_file)
        plik_menu.addAction(nowa_akcja)

        otworz_akcja = QAction(QIcon("C:/Users/Davev/Desktop/Python/qt/zadania/notebook--pencil.png"), "Otwórz", self)
        otworz_akcja.setShortcut("Ctrl+O")
        otworz_akcja.setStatusTip("Otwórz istniejący plik")
        otworz_akcja.triggered.connect(self.open_file)
        plik_menu.addAction(otworz_akcja)

        zapisz_akcja = QAction("Zapisz", self)
        zapisz_akcja.setShortcut("Ctrl+S")
        zapisz_akcja.setStatusTip("Zapisz plik")
        zapisz_akcja.triggered.connect(self.save_file)
        plik_menu.addAction(zapisz_akcja)

        zamknij_akcja = QAction("Zamknij", self)
        zamknij_akcja.setShortcut("Ctrl+Q")
        zamknij_akcja.setStatusTip("Zamknij aplikację")
        zamknij_akcja.triggered.connect(self.close)
        plik_menu.addAction(zamknij_akcja)

        edycja_menu = menu_bar.addMenu("&Edycja")

        kopiuj_akcja = QAction("Kopiuj", self)
        kopiuj_akcja.setShortcut("Ctrl+C")
        kopiuj_akcja.setStatusTip("Skopiuj")
        edycja_menu.addAction(kopiuj_akcja)

        wklej_akcja = QAction("Wklej", self)
        wklej_akcja.setShortcut("Ctrl+V")
        wklej_akcja.setStatusTip("Wklej")
        edycja_menu.addAction(wklej_akcja)

        # Toolbar
        toolbar = QToolBar("Nowy Toolbar")
        toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        toolbar.setIconSize(QSize(30, 30))  
        toolbar.setOrientation(Qt.Vertical)  
        self.addToolBar(Qt.LeftToolBarArea, toolbar)

        action1 = QAction(QIcon("C:/Users/Davev/Desktop/Python/qt/zadania/notebook--pencil.png"), "", self)
        action2 = QAction(QIcon("C:/Users/Davev/Desktop/Python/qt/zadania/notebook--pencil.png"), "", self)
        action3 = QAction(QIcon("C:/Users/Davev/Desktop/Python/qt/zadania/notebook--pencil.png"), "", self)

        toolbar.addAction(action1)
        toolbar.addAction(action2)
        toolbar.addSeparator()  
        toolbar.addAction(action3)

        self.setStatusBar(QStatusBar(self))

        # Centralny widget z przyciskami
        central_widget = QWidget()
        layout = QVBoxLayout()

        modal_button = QPushButton("Otwórz Modal")
        modal_button.clicked.connect(self.show_modal)
        layout.addWidget(modal_button)

        alert_button = QPushButton("Otwórz Alert")
        alert_button.clicked.connect(self.show_alert)
        layout.addWidget(alert_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def new_file(self):
        print("Tworzenie nowego pliku!")

    def open_file(self):
        print("Otwieranie istniejącego pliku!")

    def save_file(self):
        print("Zapisywanie pliku!")

    
    #modal
    def show_modal(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Modalna Decyzja")
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Czy kontynuować operację?"))
        layout.addWidget(QCheckBox("Zgadzam się z warunkami"))
        layout.addWidget(QRadioButton("Opcja 1"))
        layout.addWidget(QRadioButton("Opcja 2"))
        layout.addWidget(QLineEdit("Wpisz coś tutaj"))

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(lambda: print("Modal - OK clicked!"))
        layout.addWidget(ok_button)

        cancel_button = QPushButton("Anuluj")
        cancel_button.clicked.connect(dialog.close)
        layout.addWidget(cancel_button)

        dialog.setLayout(layout)
        dialog.exec()
  
  #alert
    def show_alert(self):
        alert = QMessageBox(self)
        alert.setIcon(QMessageBox.Information)
        alert.setWindowTitle("Alert")
        alert.setText("To jest alert informacyjny.")
        alert.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        button_clicked = alert.exec()
        if button_clicked == QMessageBox.Ok:
            print("OK clicked!")
        elif button_clicked == QMessageBox.Cancel:
            print("Cancel clicked!")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
