import sys
from PySide6.QtWidgets import (
QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
QGridLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QGroupBox,
QComboBox )
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kreator postaci")
        centralny_widget = QWidget()
        self.setCentralWidget(centralny_widget)
        glowny_layout = QVBoxLayout(centralny_widget)

        #naglowek
        naglowek = QLabel("Kreator postaci")
        naglowek.setAlignment(Qt.AlignCenter)
        naglowek.setStyleSheet("background-color: grey; color white; padding: 10px; font-size: 24px; font-weight: bold")
        glowny_layout.addWidget(naglowek)
        
        #centralny podzial na dwa panele
        centralny_layout = QHBoxLayout()
        glowny_layout.addLayout(centralny_layout)

        #lewy panel / szczegoly postaci
        detale_layout = QFormLayout()
        detale_layout.setContentsMargins(20,30,20,20)

        self.nazwa = QLineEdit()
        self.klasa = QComboBox()
        self.klasa.addItems(["Wojownik", "Mag", "Łowca"])
        self.rasa = QComboBox()
        self.rasa.addItems(["Człowiek", "Elf", "Krasnolud"])
        self.plec = QComboBox()
        self.plec.addItems(["Mężczyzna", "Kobieta", "Inna"])
        self.level = QLineEdit()
        self.level.setPlaceholderText("1")

        detale_layout.addRow("Nazwa postaci: ", self.nazwa)
        detale_layout.addRow("Klasa:", self.klasa)
        detale_layout.addRow("Rasa:", self.rasa)
        detale_layout.addRow("Płeć: ", self.plec)
        detale_layout.addRow("Poziom: ", self.level)

        detale_widget = QWidget()
        detale_widget.setLayout(detale_layout)
        centralny_layout.addWidget(detale_widget)

        # prawy panel / wyposazenie
        wyposazenie = QGroupBox("Wyposażenie")
        wyposazenie.setStyleSheet("font-size: 16px; margin-top: 10px; padding: 15px;")
        wyposazenie_layout = QGridLayout(wyposazenie)

        przedmioty = ["Miecz", "Tarcza", "Łuk", "Kostur", "Hełm", "Zbroja", "Buty", "Pierścień", "Amulet"]
        pozycje = [(i,j) for i in range(3) for j in range(3)]
        for pos, item in zip(pozycje, przedmioty):
            button = QPushButton(item)
            button.setStyleSheet("background-color: white; color: black, padding: 8px")
            button.clicked.connect(lambda checked, it=item: self.wybierz_ekwipunek(it))
            wyposazenie_layout.addWidget(button, pos[0], pos[1])
        
        centralny_layout.addWidget(wyposazenie)

        #dolny panel
        operacje_layout = QHBoxLayout()

        self.utworz_postac_button = QPushButton("Utwórz postać")
        self.wyczysc_button = QPushButton("Wyczyść formularz")
        self.utworz_postac_button.clicked.connect(self.utworz_postac)
        self.wyczysc_button.clicked.connect(self.czyszczenie)

        self.tryb = QLabel("Tryb gry (Poziom trudności do wyboru):")
        self.tryb_combo = QComboBox()
        self.tryb_combo.addItems(["Łatwy", "Średni", "Trudny"])

        operacje_layout.addWidget(self.utworz_postac_button)
        operacje_layout.addWidget(self.wyczysc_button)
        operacje_layout.addWidget(self.tryb)
        operacje_layout.addWidget(self.tryb_combo)

        operacje_widget = QWidget()
        operacje_widget.setLayout(operacje_layout)
        glowny_layout.addWidget(operacje_widget)



    def wybierz_ekwipunek(self, wyposazenie):
        print("Wybrane wyposażenie: ", wyposazenie)

    def utworz_postac(self):
        nazwa = self.nazwa.text()
        klasa = self.klasa.currentText()
        rasa = self.rasa.currentText()
        plec = self.plec.currentText()
        level = self.level.text() or "1"
        print(f"Tworzenie postaci: {nazwa}, Klasa: {klasa}, Rasa: {rasa}, Płeć: {plec}, Poziom: {level}")

    def czyszczenie(self):
        self.nazwa.clear()
        self.level.clear()
        print("Formularz wyczyszczony")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.resize(800,600)
    window.show()
    sys.exit(app.exec())


