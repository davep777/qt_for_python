import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class PrzegladarkaObrazow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Przeglądarka obrazów")

        self.etykieta = QLabel("Wybierz plik graficzny...", self)
        self.etykieta.setAlignment(Qt.AlignCenter)

        self.przycisk_otworz = QPushButton("Otwórz plik graficzny")
        self.przycisk_otworz.clicked.connect(self.otworz_plik)

        self.przycisk_zapisz = QPushButton("Zapisz pod inną nazwą")
        self.przycisk_zapisz.clicked.connect(self.zapisz_plik)

        uklad = QVBoxLayout()
        uklad.addWidget(self.etykieta)
        uklad.addWidget(self.przycisk_otworz)
        uklad.addWidget(self.przycisk_zapisz)

        kontener = QWidget()
        kontener.setLayout(uklad)
        self.setCentralWidget(kontener)

        self.obecny_obraz = None

    def otworz_plik(self):
        sciezka_pliku, _ = QFileDialog.getOpenFileName(
            self, "Wybierz plik graficzny", "", "Pliki graficzne (*.jpg *.jpeg *.png)"
        )
        if sciezka_pliku:
            self.obecny_obraz = QPixmap(sciezka_pliku)
            self.etykieta.setPixmap(self.obecny_obraz)
            self.etykieta.setScaledContents(True)

    def zapisz_plik(self):
        if self.obecny_obraz:
            sciezka_zapisu, _ = QFileDialog.getSaveFileName(
                self, "Zapisz plik graficzny jako", "", "Pliki graficzne (*.jpg *.jpeg *.png)"
            )
            if sciezka_zapisu:
                self.obecny_obraz.save(sciezka_zapisu)


if __name__ == "__main__":
    aplikacja = QApplication(sys.argv)
    przegladarka = PrzegladarkaObrazow()
    przegladarka.show()
    sys.exit(aplikacja.exec())
