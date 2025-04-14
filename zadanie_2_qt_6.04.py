import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt


class PersistentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Okno Persistent")
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)

        self.etykieta_obrazka = QLabel("Brak obrazka", self)
        self.etykieta_obrazka.setAlignment(Qt.AlignCenter)

        uklad = QVBoxLayout()
        uklad.addWidget(self.etykieta_obrazka)

        kontener = QWidget()
        kontener.setLayout(uklad)
        self.setCentralWidget(kontener)

    def pokaz_obrazek(self, obrazek):
        self.etykieta_obrazka.setPixmap(obrazek)
        self.etykieta_obrazka.setScaledContents(True)
        self.show()

    def ukryj_okno(self):
        self.hide()


class OnDemandWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Okno On Demand")
        self.resize(300, 150)

        self.przycisk_szary = QPushButton("Skala szarości")
        self.przycisk_szary.clicked.connect(self.skala_szarosci)

        self.przycisk_lustrzany = QPushButton("Odbicie lustrzane")
        self.przycisk_lustrzany.clicked.connect(self.odbicie_lustrzane)

        self.przycisk_reset = QPushButton("Reset obrazka")
        self.przycisk_reset.clicked.connect(self.reset_obrazka)

        uklad = QVBoxLayout()
        uklad.addWidget(self.przycisk_szary)
        uklad.addWidget(self.przycisk_lustrzany)
        uklad.addWidget(self.przycisk_reset)

        kontener = QWidget()
        kontener.setLayout(uklad)
        self.setCentralWidget(kontener)

        self.obrazek_original = None
        self.obrazek_w_formacie_pixmap = None
        self.okno_persistent = None  

    def ustaw_obrazek(self, obrazek, okno_persistent):
        self.obrazek_original = obrazek.toImage()
        self.obrazek_w_formacie_pixmap = obrazek
        self.okno_persistent = okno_persistent  

    def skala_szarosci(self):
        if self.obrazek_original:
            obraz_szary = self.obrazek_original.convertToFormat(QImage.Format_Grayscale8)
            self.zaktualizuj_obrazek(obraz_szary)

    def odbicie_lustrzane(self):
        if self.obrazek_original:
            obraz_lustrzany = self.obrazek_original.mirrored(True, False)
            self.zaktualizuj_obrazek(obraz_lustrzany)

    def reset_obrazka(self):
        if self.obrazek_original:
            self.zaktualizuj_obrazek(self.obrazek_original)

    def zaktualizuj_obrazek(self, obrazek):
        pixmap = QPixmap.fromImage(obrazek)
        self.obrazek_w_formacie_pixmap = pixmap
        if self.okno_persistent:
            self.okno_persistent.pokaz_obrazek(pixmap)  


class GlowneOkno(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Główna Aplikacja")

        self.okno_persistent = PersistentWindow()
        self.okno_on_demand = OnDemandWindow()

        self.etykieta = QLabel("Wybierz plik graficzny...", self)
        self.etykieta.setAlignment(Qt.AlignCenter)

        self.przycisk_otworz = QPushButton("Otwórz plik graficzny")
        self.przycisk_otworz.clicked.connect(self.otworz_plik)

        self.przycisk_ustawienia = QPushButton("Ustawienia obrazka")
        self.przycisk_ustawienia.clicked.connect(self.pokaz_okno_ustawienia)

        uklad = QVBoxLayout()
        uklad.addWidget(self.etykieta)
        uklad.addWidget(self.przycisk_otworz)
        uklad.addWidget(self.przycisk_ustawienia)

        kontener = QWidget()
        kontener.setLayout(uklad)
        self.setCentralWidget(kontener)

    def otworz_plik(self):
        sciezka_pliku, _ = QFileDialog.getOpenFileName(
            self, "Wybierz plik graficzny", "", "Pliki graficzne (*.jpg *.jpeg *.png)"
        )
        if sciezka_pliku:
            obrazek = QPixmap(sciezka_pliku)
            self.etykieta.setPixmap(obrazek)
            self.etykieta.setScaledContents(True)

            pozycja_glownego_okna = self.geometry()
            self.okno_persistent.move(pozycja_glownego_okna.right() + 10, pozycja_glownego_okna.top())
            self.okno_persistent.pokaz_obrazek(obrazek)

            self.okno_on_demand.ustaw_obrazek(obrazek, self.okno_persistent)

    def pokaz_okno_ustawienia(self):
        pozycja_glownego_okna = self.geometry()
        szerokosc_okna = self.okno_on_demand.width()
        self.okno_on_demand.move(pozycja_glownego_okna.left() - szerokosc_okna - 10, pozycja_glownego_okna.top())
        self.okno_on_demand.show()
        self.okno_on_demand.raise_()
        self.okno_on_demand.activateWindow()


if __name__ == "__main__":
    aplikacja = QApplication(sys.argv)
    glowne_okno = GlowneOkno()
    glowne_okno.show()
    sys.exit(aplikacja.exec())
