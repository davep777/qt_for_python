import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QComboBox, QColorDialog, QWidget, QVBoxLayout
from PyQt6.QtGui import QPainter, QPixmap, QColor

class WidzetWzor(QWidget):
    def __init__(self):
        super().__init__()
        self.typ_wzoru = "Kropki"
        self.kolory = [QColor("black")]

    def ustaw_wzor(self, typ_wzoru):
        self.typ_wzoru = typ_wzoru
        self.update()

    def ustaw_kolory(self, kolory):
        self.kolory = kolory
        self.update()

    def paintEvent(self, event):
        malarz = QPainter(self)
        obraz = QPixmap(self.size())
        obraz.fill(QColor("white"))
        malarz.drawPixmap(0, 0, obraz)

        szerokosc, wysokosc = self.width(), self.height()
        liczba_kolorow = len(self.kolory)

        if self.typ_wzoru == "Kropki":
            for x in range(0, szerokosc, 20):
                for y in range(0, wysokosc, 20):
                    malarz.setBrush(self.kolory[(x // 20 + y // 20) % liczba_kolorow])
                    malarz.drawEllipse(x, y, 10, 10)

        elif self.typ_wzoru == "Pionowe linie":
            for x in range(0, szerokosc, 20):
                malarz.setPen(self.kolory[x // 20 % liczba_kolorow])
                malarz.drawLine(x, 0, x, wysokosc)

        elif self.typ_wzoru == "Małe kółka":
            for x in range(0, szerokosc, 30):
                for y in range(0, wysokosc, 30):
                    malarz.setBrush(self.kolory[(x // 30 + y // 30) % liczba_kolorow])
                    malarz.drawEllipse(x, y, 15, 15)

class GeneratorWzorow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generator Wzorów")
        self.setGeometry(100, 100, 400, 400)

        self.widzet = WidzetWzor()
        uklad = QVBoxLayout()

        self.lista_wzorow = QComboBox()
        self.lista_wzorow.addItems(["Kropki", "Pionowe linie", "Małe kółka"])
        self.lista_wzorow.currentTextChanged.connect(self.widzet.ustaw_wzor)

        self.przyciski_kolorow = []
        for i in range(3):
            przycisk = QPushButton(f"Wybierz kolor {i+1}")
            przycisk.clicked.connect(lambda _, i=i: self.wybierz_kolor(i))
            uklad.addWidget(przycisk)
            self.przyciski_kolorow.append(przycisk)

        uklad.addWidget(self.lista_wzorow)
        uklad.addWidget(self.widzet)

        widzet_glowny = QWidget()
        widzet_glowny.setLayout(uklad)
        self.setCentralWidget(widzet_glowny)

    def wybierz_kolor(self, indeks):
        kolor = QColorDialog.getColor()
        if kolor.isValid():
            kolory = self.widzet.kolory[:indeks] + [kolor] + self.widzet.kolory[indeks+1:]
            self.widzet.ustaw_kolory(kolory)

if __name__ == "__main__":
    aplikacja = QApplication(sys.argv)
    okno = GeneratorWzorow()
    okno.show()
    sys.exit(aplikacja.exec())

