import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QSpinBox, QLabel, QColorDialog, QFileDialog,
    QGraphicsScene, QGraphicsView, QGraphicsItem
)
from PySide6.QtGui import QPainter, QPen, QColor, QPolygonF, QImage
from PySide6.QtCore import QRectF, QPointF, Qt

# Pojedynczy element rysowany – który w zależności od parametru "ksztalt"
# narysuje prostokąt, elipsę lub trójkąt.
class KsztaltItem(QGraphicsItem):
    def __init__(self, ksztalt, rect, kolor):
        super().__init__()
        self.ksztalt = ksztalt  # "prostokat", "elipsa" lub "trojkat"
        self.rect = rect
        self.kolor = kolor
        self.domyslny_pioro = QPen(Qt.black, 2)
        self.wybrany_pioro = QPen(Qt.red, 2, Qt.DashLine)
        # Tylko wybieralne – myszką nie można przesuwać
        self.setFlags(QGraphicsItem.ItemIsSelectable)

    def boundingRect(self):
        return self.rect

    def paint(self, malarz, opcje, widget=None):
        # Jeśli zaznaczony, używamy przerywanego obrysu
        if self.isSelected():
            malarz.setPen(self.wybrany_pioro)
        else:
            malarz.setPen(self.domyslny_pioro)
        malarz.setBrush(self.kolor)

        if self.ksztalt == "prostokat":
            malarz.drawRect(self.rect)
        elif self.ksztalt == "elipsa":
            malarz.drawEllipse(self.rect)
        elif self.ksztalt == "trojkat":
            # Trójkąt: wierzchołek górny, prawy dolny, lewy dolny
            szer = self.rect.width()
            wys = self.rect.height()
            punkty = [QPointF(szer / 2, 0), QPointF(szer, wys), QPointF(0, wys)]
            polygon = QPolygonF(punkty)
            malarz.drawPolygon(polygon)
        else:
            # W razie nieznanego typu – rysujemy prostokąt
            malarz.drawRect(self.rect)

class GlowneOkno(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prosty Edytor Grafiki")
        kontener = QWidget()
        self.setCentralWidget(kontener)
        uklad_glowny = QHBoxLayout(kontener)

        # Panel boczny (menu)
        self.panel = QWidget()
        uklad_panel = QVBoxLayout(self.panel)

        # Pozycja (X, Y)
        etykieta_pozycja = QLabel("Pozycja (X, Y):")
        uklad_panel.addWidget(etykieta_pozycja)
        self.spin_x = QSpinBox()
        self.spin_x.setRange(0, 1000)
        self.spin_x.setValue(50)
        self.spin_y = QSpinBox()
        self.spin_y.setRange(0, 1000)
        self.spin_y.setValue(50)
        uklad_pozycji = QHBoxLayout()
        uklad_pozycji.addWidget(self.spin_x)
        uklad_pozycji.addWidget(self.spin_y)
        uklad_panel.addLayout(uklad_pozycji)

        # Rozmiar (szerokość, wysokość)
        etykieta_rozmiar = QLabel("Rozmiar (szer., wys.):")
        uklad_panel.addWidget(etykieta_rozmiar)
        self.spin_szer = QSpinBox()
        self.spin_szer.setRange(10, 500)
        self.spin_szer.setValue(100)
        self.spin_wys = QSpinBox()
        self.spin_wys.setRange(10, 500)
        self.spin_wys.setValue(100)
        uklad_rozmiaru = QHBoxLayout()
        uklad_rozmiaru.addWidget(self.spin_szer)
        uklad_rozmiaru.addWidget(self.spin_wys)
        uklad_panel.addLayout(uklad_rozmiaru)

        # Wybór koloru
        self.przycisk_kolor = QPushButton("Wybierz kolor")
        self.przycisk_kolor.clicked.connect(self.wybierz_kolor)
        uklad_panel.addWidget(self.przycisk_kolor)
        self.aktualny_kolor = QColor(Qt.green)

        # Przyciski do dodawania kształtów
        self.przycisk_prostokat = QPushButton("Dodaj prostokąt")
        self.przycisk_prostokat.clicked.connect(lambda: self.dodaj_ksztalt("prostokat"))
        uklad_panel.addWidget(self.przycisk_prostokat)

        self.przycisk_elipsa = QPushButton("Dodaj elipsę")
        self.przycisk_elipsa.clicked.connect(lambda: self.dodaj_ksztalt("elipsa"))
        uklad_panel.addWidget(self.przycisk_elipsa)

        self.przycisk_trojkat = QPushButton("Dodaj trójkąt")
        self.przycisk_trojkat.clicked.connect(lambda: self.dodaj_ksztalt("trojkat"))
        uklad_panel.addWidget(self.przycisk_trojkat)

        # Przesuwanie zaznaczonych obiektów w pionie
        self.przycisk_gora = QPushButton("Przesuń w górę")
        self.przycisk_gora.clicked.connect(self.przesun_gora)
        uklad_panel.addWidget(self.przycisk_gora)
        self.przycisk_dol = QPushButton("Przesuń w dół")
        self.przycisk_dol.clicked.connect(self.przesun_dol)
        uklad_panel.addWidget(self.przycisk_dol)

        # Usuwanie zaznaczonych kształtów
        self.przycisk_usun = QPushButton("Usuń zaznaczone")
        self.przycisk_usun.clicked.connect(self.usun_zaznaczone)
        uklad_panel.addWidget(self.przycisk_usun)

        # Zapis do PNG
        self.przycisk_zapisz = QPushButton("Zapisz jako PNG")
        self.przycisk_zapisz.clicked.connect(self.zapisz_scene)
        uklad_panel.addWidget(self.przycisk_zapisz)

        uklad_panel.addStretch()
        uklad_glowny.addWidget(self.panel)

        # Obszar roboczy: scena i widok
        self.scene = QGraphicsScene(0, 0, 800, 600)
        self.view = QGraphicsView(self.scene)
        uklad_glowny.addWidget(self.view)

    def wybierz_kolor(self):
        kolor = QColorDialog.getColor(self.aktualny_kolor, self, "Wybierz kolor")
        if kolor.isValid():
            self.aktualny_kolor = kolor
            self.przycisk_kolor.setStyleSheet("background-color: %s" % kolor.name())

    def dodaj_ksztalt(self, typ):
        x = self.spin_x.value()
        y = self.spin_y.value()
        szer = self.spin_szer.value()
        wys = self.spin_wys.value()
        rect = QRectF(0, 0, szer, wys)
        ksztalt = KsztaltItem(typ, rect, self.aktualny_kolor)
        ksztalt.setPos(x, y)
        self.scene.addItem(ksztalt)

    def przesun_gora(self):
        delta = 10
        for obiekt in self.scene.selectedItems():
            pozycja = obiekt.pos()
            obiekt.setPos(pozycja.x(), pozycja.y() - delta)

    def przesun_dol(self):
        delta = 10
        for obiekt in self.scene.selectedItems():
            pozycja = obiekt.pos()
            obiekt.setPos(pozycja.x(), pozycja.y() + delta)

    def usun_zaznaczone(self):
        for obiekt in self.scene.selectedItems():
            self.scene.removeItem(obiekt)

    def zapisz_scene(self):
        nazwa_pliku, _ = QFileDialog.getSaveFileName(
            self, "Zapisz obraz jako PNG", "", "PNG Files (*.png)"
        )
        if nazwa_pliku:
            rect = self.scene.sceneRect()
            obraz = QImage(int(rect.width()), int(rect.height()), QImage.Format_ARGB32)
            obraz.fill(Qt.white)
            malarz = QPainter(obraz)
            self.scene.render(malarz)
            malarz.end()
            obraz.save(nazwa_pliku, "PNG")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    okno = GlowneOkno()
    okno.resize(1000, 600)
    okno.show()
    sys.exit(app.exec())
