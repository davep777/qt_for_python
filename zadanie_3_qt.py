import sys
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QWidget
from PySide6.QtGui import QDoubleValidator

app = QApplication()

window = QWidget()
window.setWindowTitle("Kalkulator")
window.setGeometry(100,100,300,300)


pole1 = QLineEdit(window)
pole1.setGeometry(50,30,200,30)
pole1.setValidator(QDoubleValidator())

pole2 = QLineEdit(window)
pole2.setGeometry(50,70,200,30)
pole2.setValidator(QDoubleValidator())

wynik = QLabel("Wynik:", window)
wynik.setGeometry(50,200,200,30)


def dodawanie():
    liczba1 = float(pole1.text() or 0)
    liczba2 = float(pole2.text() or 0)
    wynik.setText(f"Wynik: {liczba1 + liczba2}")

def odejmowanie():
    liczba1 = float(pole1.text() or 0)
    liczba2 = float(pole2.text() or 0)
    wynik.setText(f"Wynik: {liczba1-liczba2}")

def mnozenie():
    liczba1 = float(pole1.text() or 0)
    liczba2 = float(pole2.text() or 0)
    wynik.setText(f"Wynik: {liczba1 * liczba2}")

def dzielenie():
    liczba1 = float(pole1.text() or 0)
    liczba2 = float(pole2.text() or 0)
    if liczba1 or liczba2 == 0:
        wynik.setText("Nie dzielimy przez zero")
    else:
        wynik.setText(f"Wynik: {liczba1 / liczba2}")

def wyczysc():
    pole1.clear()
    pole2.clear()
    wynik.setText("Wynik: ")

button_dodawanie = QPushButton("Dodaj", window)
button_dodawanie.setGeometry(50,120,90,30)
button_dodawanie.clicked.connect(dodawanie)

button_odejmowanie = QPushButton("Odejmij", window)
button_odejmowanie.setGeometry(160,120,90,30)
button_odejmowanie.clicked.connect(odejmowanie)

button_mnozenie = QPushButton("Pomnóż", window)
button_mnozenie.setGeometry(50,160,90,30)
button_mnozenie.clicked.connect(mnozenie)

button_dzielenie = QPushButton("Podziel", window)
button_dzielenie.setGeometry(160,160,90,30)
button_dzielenie.clicked.connect(dzielenie)

button_wyczyszczenie = QPushButton("Wyczyść", window)
button_wyczyszczenie.setGeometry(105,240,90,30)
button_wyczyszczenie.clicked.connect(wyczysc)

window.show()
app.exec()

