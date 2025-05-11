import sys
import numpy as np
import pandas as pd
from PySide6.QtCore import Qt, QAbstractTableModel
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView, QWidget, QVBoxLayout, QTabWidget
import pyqtgraph as pg
from pyqtgraph import DateAxisItem

# Ścieżka do pliku CSV
CSV_PATH = r"C:\Users\Davev\Desktop\Python\qt\zadania\weather_2024.csv"

# Model do wyświetlania pandas DataFrame w QTableView
class PandasModel(QAbstractTableModel):
    def __init__(self, df: pd.DataFrame, parent=None):
        super().__init__(parent)
        self._df = df.copy()

    def rowCount(self, parent=None):
        return self._df.shape[0]

    def columnCount(self, parent=None):
        return self._df.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        value = self._df.iloc[index.row(), index.column()]
        if role == Qt.DisplayRole:
            return str(value)
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._df.columns[section]
            else:
                return section
        return None

# Funkcja wykonująca analizę danych pogodowych
def analyze_weather_data(df):
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df["humidity"] = pd.to_numeric(df["humidity"], errors="coerce")
    df["precipitation"] = pd.to_numeric(df["precipitation"], errors="coerce")
    df = df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)

    # Obliczenie średniej kroczącej dla temperatury (okno 7-dniowe)
    df["temp_rolling"] = df["temperature"].rolling(window=7, center=True, min_periods=1).mean()

    # Wykrywanie anomalii na podstawie statystyk miesięcznych
    df["month"] = df["date"].dt.month
    monthly_stats = df.groupby("month")["temperature"].agg(["mean", "std"]).reset_index()
    df = df.merge(monthly_stats, on="month")
    df["temp_anomaly"] = np.abs(df["temperature"] - df["mean"]) > 2 * df["std"]
    df.drop(columns=["mean", "std"], inplace=True)

    # Grupowanie - sumaryczne opady dla każdego miesiąca
    monthly_precip = df.groupby("month")["precipitation"].sum().reset_index()

    # Obliczanie korelacji
    corr = df[["temperature", "humidity", "precipitation"]].corr()

    # Interpolacja braków - symulacja polegająca na usunięciu co trzeciego pomiaru
    df_interp = df.copy()
    df_interp.loc[df_interp.index % 3 == 0, ["temperature", "humidity", "precipitation"]] = np.nan
    df_interp[["temperature", "humidity", "precipitation"]] = df_interp[["temperature", "humidity", "precipitation"]].interpolate(method="linear")

    return df, monthly_precip, corr, df_interp

# Główne okno aplikacji
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikacja analizy danych pogodowych")
        self.resize(1200, 800)

        try:
            df = pd.read_csv(CSV_PATH, parse_dates=["date"])
        except FileNotFoundError:
            print(f"Nie znaleziono pliku '{CSV_PATH}', generuję przykładowe dane...")
            dates = pd.date_range(start="2024-01-01", periods=365, freq="D")
            temp = 10 + 10 * np.sin(np.linspace(0, 2 * np.pi, 365)) + np.random.normal(0, 2, 365)
            humidity = 50 + 10 * np.cos(np.linspace(0, 2 * np.pi, 365)) + np.random.normal(0, 5, 365)
            precipitation = np.abs(np.random.normal(5, 2, 365))
            df = pd.DataFrame({"date": dates, "temperature": temp, "humidity": humidity, "precipitation": precipitation})

        # Przeprowadzenie analiz na danych
        self.df, self.monthly_precip, self.corr, self.df_interp = analyze_weather_data(df)

        # Ustawienie widżetu z zakładkami
        tab_widget = QTabWidget()
        self.setCentralWidget(tab_widget)

        # Zakładka z widokiem tabelarycznym
        table_tab = QWidget()
        table_layout = QVBoxLayout()
        table_tab.setLayout(table_layout)
        self.table_view = QTableView()
        self.model = PandasModel(self.df)
        self.table_view.setModel(self.model)
        table_layout.addWidget(self.table_view)
        tab_widget.addTab(table_tab, "Dane i analiza (tabela)")

        # Zakładka z wykresami
        plot_tab = QWidget()
        plot_layout = QVBoxLayout()
        plot_tab.setLayout(plot_layout)
        tab_widget.addTab(plot_tab, "Wykresy")

        # Użycie DateAxisItem do wyświetlania dat na osi x
        date_axis_item = DateAxisItem(orientation='bottom')
        self.plot_widget = pg.PlotWidget(title="Temperatura: surowe dane vs średnia krocząca", axisItems={"bottom": date_axis_item})
        self.plot_widget.setLabel('left', "Temperatura [°C]")
        self.plot_widget.setLabel('bottom', "Data")

        # Konwersja dat do wartości numerycznych: unix timestamp (float)
        x_dates = np.array([d.timestamp() for d in self.df["date"]])
        
        # Rysowanie wykresu surowych danych i średniej kroczącej
        self.plot_widget.plot(x=x_dates, y=self.df["temperature"].values, pen=pg.mkPen('b', width=1.5), name="Temperatura")
        self.plot_widget.plot(x=x_dates, y=self.df["temp_rolling"].values, pen=pg.mkPen('r', width=2), name="Średnia krocząca")

        # Oznaczenie anomalii jako punkty
        anomaly_df = self.df[self.df["temp_anomaly"] == True]
        if not anomaly_df.empty:
            x_anom = np.array([d.timestamp() for d in anomaly_df["date"]])
            self.plot_widget.plot(x=x_anom, y=anomaly_df["temperature"].values,
                                  pen=None, symbol='o', symbolBrush='g', symbolSize=8, name="Anomalie")
        plot_layout.addWidget(self.plot_widget)

        # Wykres słupkowy - miesięczne opady
        self.bar_plot = pg.PlotWidget(title="Miesięczne opady")
        self.bar_plot.setLabel('left', "Suma opadów [mm]")
        self.bar_plot.setLabel('bottom', "Miesiąc")
        x_month = self.monthly_precip["month"].astype(float)
        bar_width = 0.6
        bg = pg.BarGraphItem(x=x_month, height=self.monthly_precip["precipitation"].values, width=bar_width, brush=pg.mkBrush('c'))
        self.bar_plot.addItem(bg)
        ticks = [list(zip(range(1, 13), [str(i) for i in range(1, 13)]))]
        self.bar_plot.getAxis('bottom').setTicks(ticks)
        plot_layout.addWidget(self.bar_plot)

        print("Macierz korelacji między temperaturą, wilgotnością i opadami:")
        print(self.corr)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
