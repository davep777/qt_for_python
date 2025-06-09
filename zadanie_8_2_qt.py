import sys
import random
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsRectItem, QPushButton
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, QPointF, QEvent

class Labirynt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Labirynt - przechodzenie kursorem")
        self.setGeometry(100, 100, 600, 600)

        self.scena = QGraphicsScene(0, 0, 500, 500)
        self.widok = QGraphicsView(self.scena, self)
        self.widok.setGeometry(50, 50, 500, 500)
        self.widok.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.przycisk_start = QPushButton("Start", self)
        self.przycisk_start.setGeometry(250, 10, 100, 30)
        self.przycisk_start.clicked.connect(self.start_gry)

        self.start_pozycja = QPointF(60, 460)
        self.meta_pozycja = QPointF(440, 40)

        self.sciezka = []
        self.gra_trwa = False
        self.start_czas = None

        self.generuj_labirynt()
        self.widok.viewport().setMouseTracking(True)
        self.widok.viewport().installEventFilter(self)

    def generuj_labirynt(self):
        """Losowy wybór jednego z trzech bardziej realistycznych labiryntów."""
        self.scena.clear()
        labirynty = [self.labirynt_1, self.labirynt_2, self.labirynt_3]
        random.choice(labirynty)()

        # Punkt startu - zielony okrąg
        start = QGraphicsEllipseItem(60, 460, 30, 30)
        start.setPen(QPen(Qt.GlobalColor.green, 3))
        self.scena.addItem(start)

        # Punkt mety - czerwony okrąg
        meta = QGraphicsEllipseItem(440, 40, 30, 30)
        meta.setPen(QPen(Qt.GlobalColor.red, 3))
        self.scena.addItem(meta)

    def labirynt_1(self):
        """Labirynt z zakrętami i węższymi ścieżkami."""
        self.scena.addRect(100, 50, 300, 20, QPen(Qt.GlobalColor.black))
        self.scena.addRect(380, 50, 20, 300, QPen(Qt.GlobalColor.black))
        self.scena.addRect(100, 330, 300, 20, QPen(Qt.GlobalColor.black))
        self.scena.addRect(100, 150, 20, 200, QPen(Qt.GlobalColor.black))
        self.scena.addRect(200, 150, 100, 20, QPen(Qt.GlobalColor.black))

    def labirynt_2(self):
        """Labirynt ze zwężeniami i długimi przejściami."""
        self.scena.addRect(50, 100, 400, 20, QPen(Qt.GlobalColor.black))
        self.scena.addRect(450, 100, 20, 300, QPen(Qt.GlobalColor.black))
        self.scena.addRect(50, 400, 420, 20, QPen(Qt.GlobalColor.black))
        self.scena.addRect(150, 200, 200, 20, QPen(Qt.GlobalColor.black))
        self.scena.addRect(350, 220, 20, 100, QPen(Qt.GlobalColor.black))

    def labirynt_3(self):
        """Labirynt z zakrętami i wąskimi przejściami."""
        self.scena.addRect(50, 50, 400, 20, QPen(Qt.GlobalColor.black))
        self.scena.addRect(450, 50, 20, 400, QPen(Qt.GlobalColor.black))
        self.scena.addRect(50, 450, 400, 20, QPen(Qt.GlobalColor.black))
        self.scena.addRect(250, 100, 20, 300, QPen(Qt.GlobalColor.black))
        self.scena.addRect(100, 200, 150, 20, QPen(Qt.GlobalColor.black))

    def start_gry(self):
        """Rozpoczyna grę, resetuje ścieżkę i czas."""
        self.sciezka.clear()
        self.gra_trwa = True
        self.start_czas = time.time()
        self.generuj_labirynt()

    def eventFilter(self, source, event):
        """Śledzenie ruchu myszki i rysowanie ścieżki."""
        if event.type() == QEvent.Type.MouseMove and self.gra_trwa:
            pozycja = event.position().toPoint()

            if len(self.sciezka) == 0 and not self.start_pozycja_contains(pozycja):
                return True  # Gracz nie zaczyna od startu

            self.sciezka.append(pozycja)
            self.rysuj_sciezke()

            if self.meta_pozycja_contains(pozycja):
                self.koniec_gry()

            if self.sprawdzenie_kolizji(pozycja):
                self.koniec_gry(fail=True)

        return super().eventFilter(source, event)

    def rysuj_sciezke(self):
        """Rysowanie ścieżki gracza."""
        if len(self.sciezka) < 2:
            return
        linia = self.sciezka[-2], self.sciezka[-1]
        pen = QPen(QColor("blue"), 3)
        self.scena.addLine(linia[0].x(), linia[0].y(), linia[1].x(), linia[1].y(), pen)

    def meta_pozycja_contains(self, pozycja):
        """Sprawdza, czy gracz osiągnął metę."""
        return self.meta_pozycja.x() - 10 < pozycja.x() < self.meta_pozycja.x() + 30 and \
               self.meta_pozycja.y() - 10 < pozycja.y() < self.meta_pozycja.y() + 30

    def start_pozycja_contains(self, pozycja):
        """Sprawdza, czy gracz zaczyna od startu."""
        return self.start_pozycja.x() - 10 < pozycja.x() < self.start_pozycja.x() + 30 and \
               self.start_pozycja.y() - 10 < pozycja.y() < self.start_pozycja.y() + 30

    def sprawdzenie_kolizji(self, pozycja):
        """Sprawdza, czy gracz najechał na ścianę."""
        for item in self.scena.items():
            if isinstance(item, QGraphicsRectItem) and item.pen().color() == Qt.GlobalColor.black:
                if item.rect().contains(pozycja):
                    return True
        return False

    def koniec_gry(self, fail=False):
        """Zakończenie gry, wyświetlenie czasu."""
        self.gra_trwa = False

        if fail:
            print("Przegrałeś! Dotknąłeś ściany.")
        else:
            czas_gry = round(time.time() - self.start_czas, 2)
            print(f"Gratulacje! Przeszedłeś labirynt w {czas_gry} sekund.")

if __name__ == "__main__":
    aplikacja = QApplication(sys.argv)
    okno = Labirynt()
    okno.show()
    sys.exit(aplikacja.exec())

