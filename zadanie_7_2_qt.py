import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel
from PySide6.QtGui import QPixmap, QTransform
from PySide6.QtCore import Qt, QRect

class PuzzlePiece(QLabel):
    def __init__(self, obrazek, okno):
        super().__init__(okno)
        self.setPixmap(obrazek)
        self.setStyleSheet("border: 2px solid black;")
        self.locked = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.locked:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if not self.locked and event.buttons() == Qt.LeftButton:
            self.move(self.x() + event.x() - self.offset.x(), self.y() + event.y() - self.offset.y())

    def mouseReleaseEvent(self, event):
        if not self.locked and event.button() == Qt.LeftButton:
            index = self.parentWidget().puzzle_kawałki.index(self)
            poprawne_x = 50 + (index % 3) * self.width()
            poprawne_y = 50 + (index // 3) * self.height()
            if abs(self.x() - poprawne_x) < 30 and abs(self.y() - poprawne_y) < 30:
                self.move(poprawne_x, poprawne_y)
                self.setStyleSheet("border: 2px solid green;")
                self.locked = True

        elif not self.locked and event.button() == Qt.RightButton:
            self.setPixmap(self.pixmap().transformed(QTransform().rotate(90)))

class PuzzleOkno(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)

        self.przycisk_wczytaj = QPushButton("Wczytaj obrazek", self)
        self.przycisk_wczytaj.setGeometry(150, 560, 120, 30)
        self.przycisk_wczytaj.clicked.connect(self.wczytaj_obrazek)

        self.przycisk_start = QPushButton("Ułóż puzzle!", self)
        self.przycisk_start.setGeometry(350, 560, 120, 30)
        self.przycisk_start.setVisible(False)
        self.przycisk_start.clicked.connect(self.podziel_obrazek)

        self.przycisk_reset = QPushButton("Reset", self)
        self.przycisk_reset.setGeometry(550, 560, 120, 30)
        self.przycisk_reset.setVisible(False)
        self.przycisk_reset.clicked.connect(self.resetuj_grę)

        self.obrazek = None
        self.etykieta_obrazka = None
        self.puzzle_kawałki = []

    def wczytaj_obrazek(self):
        plik, _ = QFileDialog.getOpenFileName(self, "Wybierz obraz", "", "Obrazy (*.png *.jpg *.jpeg)")
        if plik:
            self.obrazek = QPixmap(plik).scaled(700, 500, Qt.KeepAspectRatio)
            self.etykieta_obrazka = QLabel(self)
            self.etykieta_obrazka.setPixmap(self.obrazek)
            self.etykieta_obrazka.setGeometry(50, 50, 700, 500)
            self.etykieta_obrazka.show()
            self.przycisk_start.setVisible(True)
            self.przycisk_reset.setVisible(True)

    def podziel_obrazek(self):
        if self.obrazek:
            self.etykieta_obrazka.hide()
            self.puzzle_kawałki.clear()
            for i in range(9):
                szer, wys = self.obrazek.width() // 3, self.obrazek.height() // 3
                kawałek_obrazka = self.obrazek.copy(QRect((i % 3) * szer, (i // 3) * wys, szer, wys))
                x, y = random.randint(50, 750 - szer), random.randint(50, 550 - wys)
                kawałek = PuzzlePiece(kawałek_obrazka, self)
                kawałek.setGeometry(x, y, szer, wys)
                self.puzzle_kawałki.append(kawałek)
                kawałek.show()

    def resetuj_grę(self):
        for kawałek in self.puzzle_kawałki:
            kawałek.deleteLater()
        self.puzzle_kawałki.clear()
        self.etykieta_obrazka.show()
        self.przycisk_start.setVisible(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    okno = PuzzleOkno()
    okno.show()
    sys.exit(app.exec())
