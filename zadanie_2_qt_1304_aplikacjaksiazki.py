from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QComboBox, QMessageBox
from PyQt6.QtGui import QBrush, QColor, QIcon, QPixmap
import sys
from datetime import date, timedelta

class OknoBiblioteki(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Biblioteka")
        self.resize(800, 600)

        # Lista książek
        self.ksiazki = [
            ["Drużyna Pierścieni", "J.R.R. Tolkien", "Fantasy", "dostępna", "", "", ""],
            ["Lalka", "Bolesław Prus", "Powieść", "wypożyczona", "Jan", "Kowalski", (date.today() - timedelta(days=10)).strftime("%Y-%m-%d")],
            ["Quo Vadis", "Henryk Sienkiewicz", "Historyczna", "wypożyczona", "Anna", "Nowak", (date.today() - timedelta(days=20)).strftime("%Y-%m-%d")],
            ["Krew Elfów", "Andrzej Sapkowski", "Fantasy", "dostępna", "", "", ""]
        ]

        # Tworzenie tabeli
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(7)
        self.tabela.setHorizontalHeaderLabels(["Tytuł", "Autor", "Gatunek", "Status", "Czytelnik", "Nazwisko", "Data wypożyczenia"])
        self.tabela.setSortingEnabled(True)

        # Wypełnianie tabeli danymi
        self.wypelnij_tabele()

        # Filtr statusu książek
        self.lista_filtr = QComboBox()
        self.lista_filtr.addItems(["Wszystkie", "wypożyczona", "dostępna"])
        self.lista_filtr.currentTextChanged.connect(self.filtruj_ksiazki)

        # Układ interfejsu
        centralny_widget = QWidget()
        self.setCentralWidget(centralny_widget)
        uklad = QVBoxLayout(centralny_widget)
        uklad.addWidget(self.lista_filtr)
        uklad.addWidget(self.tabela)

        # Sprawdzanie przeterminowanych książek
        self.sprawdz_przeterminowane()

    def wypelnij_tabele(self):
        self.tabela.setRowCount(len(self.ksiazki))
        for i, ksiazka in enumerate(self.ksiazki):
            for j, wartosc in enumerate(ksiazka):
                item = QTableWidgetItem(wartosc)

                # Dodanie ikonki dla statusu 
                if j == 3:  # Kolumna statusu
                    ikona = QPixmap(16, 16)
                    ikona.fill(QColor("green") if ksiazka[3] == "dostępna" else QColor("red"))
                    item.setIcon(QIcon(ikona))

                # Podświetlenie przeterminowanych książek
                if j == 6 and ksiazka[3] == "wypożyczona" and ksiazka[6]:
                    data_wypozyczenia = date.fromisoformat(ksiazka[6])
                    if (date.today() - data_wypozyczenia).days > 14:
                        item.setBackground(QBrush(QColor("red")))

                self.tabela.setItem(i, j, item)

    def filtruj_ksiazki(self, status):
        for i in range(self.tabela.rowCount()):
            pokaz = (status == "Wszystkie" or self.tabela.item(i, 3).text() == status)
            self.tabela.setRowHidden(i, not pokaz)

    def sprawdz_przeterminowane(self):
        przeterminowane = [ksiazka for ksiazka in self.ksiazki if ksiazka[3] == "wypożyczona" and ksiazka[6] and (date.today() - date.fromisoformat(ksiazka[6])).days > 14]
        if przeterminowane:
            msg = "Następujące książki są przedawnione:\n" + "\n".join([f"{ksiazka[0]} – {(date.today() - date.fromisoformat(ksiazka[6])).days - 14} dni po terminie" for ksiazka in przeterminowane])
            QMessageBox.warning(self, "Książki przedawnione", msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    okno = OknoBiblioteki()
    okno.show()
    sys.exit(app.exec())
