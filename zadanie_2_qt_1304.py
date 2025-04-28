from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QSortFilterProxyModel
from PySide6.QtGui import QIcon, QPixmap, QBrush
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QComboBox, QMessageBox, QHeaderView
import sys
from dataclasses import dataclass
from datetime import date, timedelta

# Reprezentacja książki
@dataclass
class Book:
    title: str
    author: str
    genre: str
    status: str  # "dostępna" lub "wypożyczona"
    borrower_first: str = ""
    borrower_last: str = ""
    borrow_date: date = None

# Model tabelaryczny prezentujący dane o książkach
class LibraryModel(QAbstractTableModel):
    def __init__(self, books=None):
        super().__init__()
        self._books = books or []
        self.headers = ["Tytuł", "Autor", "Gatunek", "Status", "Czytelnik", "Data wypożyczenia"]

    def rowCount(self, parent=QModelIndex()):
        return len(self._books)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        book = self._books[index.row()]
        column = index.column()

        # Wyświetlanie danych tekstowych
        if role == Qt.DisplayRole:
            if column == 0:
                return book.title
            elif column == 1:
                return book.author
            elif column == 2:
                return book.genre
            elif column == 3:
                return book.status
            elif column == 4:
                # Jeśli książka jest wypożyczona, pokaż imię i nazwisko osoby, która ją wypożyczyła
                return f"{book.borrower_first} {book.borrower_last}" if book.status == "wypożyczona" else ""
            elif column == 5:
                if book.status == "wypożyczona" and book.borrow_date:
                    return book.borrow_date.strftime("%Y-%m-%d")
                else:
                    return ""
        
        # Dodanie ikony w kolumnie Status
        if role == Qt.DecorationRole:
            if column == 3:
                pixmap = QPixmap(16, 16)
                if book.status == "dostępna":
                    pixmap.fill(Qt.green)
                else:
                    pixmap.fill(Qt.red)
                return QIcon(pixmap)
        
        # Jeśli książka jest wypożyczona, a czas wypożyczenia przekracza 14 dni, oznacz tło na czerwono
        if role == Qt.BackgroundRole:
            if book.status == "wypożyczona" and book.borrow_date:
                if (date.today() - book.borrow_date).days > 14:
                    return QBrush(Qt.red)
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section < len(self.headers):
                return self.headers[section]
        return super().headerData(section, orientation, role)

    def sort(self, column, order):
        # Sortowanie według wybranej kolumny
        if column == 0:
            self._books.sort(key=lambda book: book.title)
        elif column == 1:
            self._books.sort(key=lambda book: book.author)
        elif column == 5:
            # Jeśli data wypożyczenia nie istnieje, traktujemy ją jak minimalną datę
            self._books.sort(key=lambda book: book.borrow_date if book.borrow_date else date.min)
        # Inne kolumny można dodać w razie potrzeby
        if order == Qt.DescendingOrder:
            self._books.reverse()
        self.layoutChanged.emit()

# Model proxy do filtrowania książek według statusu
class LibraryFilterProxyModel(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self.statusFilter = None  # "wypożyczona", "dostępna" lub None dla wszystkich

    def setStatusFilter(self, status):
        self.statusFilter = status
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        if self.statusFilter is None or self.statusFilter == "Wszystkie":
            return True
        index = self.sourceModel().index(source_row, 3, source_parent)  # kolumna status ma index 3
        data = self.sourceModel().data(index, Qt.DisplayRole)
        return data == self.statusFilter

# Główne okno aplikacji
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Biblioteka")
        self.resize(800, 600)

        # Dane przykładowe –  książki
        self.books = [
            Book("Drużyna Pierścieni", "J.R.R.Tolkien", "Fantasy", "dostępna"),
            Book("Lalka", "Bolesław Prus", "Powieść", "wypożyczona", "Jan", "Kowalski", date.today() - timedelta(days=10)),
            Book("Quo Vadis", "Henryk Sienkiewicz", "Historyczna", "wypożyczona", "Anna", "Nowak", date.today() - timedelta(days=20)),
            Book("Krew Elfów", "Andrzej Sapkowski", "Fantasy", "dostępna"),
        ]

        self.model = LibraryModel(self.books)
        self.proxyModel = LibraryFilterProxyModel()
        self.proxyModel.setSourceModel(self.model)

        # Widok tabelaryczny
        self.tableView = QTableView()
        self.tableView.setModel(self.proxyModel)
        self.tableView.setSortingEnabled(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # ComboBox do filtrowania po statusie
        self.filterCombo = QComboBox()
        self.filterCombo.addItems(["Wszystkie", "wypożyczona", "dostępna"])
        self.filterCombo.currentTextChanged.connect(self.proxyModel.setStatusFilter)

        # Układ – filtr na górze, a pod nim tabela
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout(centralWidget)
        layout.addWidget(self.filterCombo)
        layout.addWidget(self.tableView)

        # Po uruchomieniu aplikacji sprawdzamy, czy są wypożyczone książki po terminie
        self.checkOverdueBooks()

    def checkOverdueBooks(self):
        overdue_books = [book for book in self.books if book.status == "wypożyczona" and book.borrow_date and (date.today() - book.borrow_date).days > 14]
        if overdue_books:
            msg = "Następujące książki są przedawnione:\n"
            for book in overdue_books:
                days_overdue = (date.today() - book.borrow_date).days - 14
                msg += f"{book.title} – {days_overdue} dni po terminie\n"
            QMessageBox.warning(self, "Książki przedawnione", msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
