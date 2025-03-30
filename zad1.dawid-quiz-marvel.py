import sys
from PySide6.QtWidgets import (QApplication, 
QMainWindow, QLineEdit, QWidget,QLabel,QVBoxLayout, 
QRadioButton, QCheckBox, QPushButton, QScrollArea, QButtonGroup, QMessageBox)
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator

def stylizuj_tekst(tekst):
    return f"<div style='background-color:white; color:black; padding:5px;'><b>{tekst}</b></div>"

class Quiz(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Marvel Quiz")

        scroll_area = QScrollArea()
        centralny_widget = QWidget()
        scroll_area.setWidget(centralny_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) #ukrywa poziomy pasek przewijania
        self.setCentralWidget(scroll_area)
        self.resize(700,550) #zmiana rozmiaru okna

        layout = QVBoxLayout()

        self.tytul = QLabel("MARVEL QUIZ - PYTANIA Z MCU")
        self.tytul.setAlignment(Qt.AlignCenter)
        self.tytul.setStyleSheet("font-weight: bold")
        layout.addWidget(self.tytul)

        #walidacja 
        regex = QRegularExpression(r"^[a-zA-Z\s,]+$")
        validator = QRegularExpressionValidator(regex)

        # Pytanie nr 1:
        self.pytanie1 = QLabel(stylizuj_tekst("1. Kto jest Iron Manem:"))
        self.radio_group1 = QButtonGroup(self)
        self.radio_button1_1 = QRadioButton("Tony Stark")
        self.radio_button1_2 = QRadioButton("Steve Rogers")
        self.radio_button1_3 = QRadioButton("Bruce Banner")
        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("Wpisz odpowiedź...")
        self.input1.setValidator(validator)

        self.radio_group1.addButton(self.radio_button1_1)
        self.radio_group1.addButton(self.radio_button1_2)
        self.radio_group1.addButton(self.radio_button1_3)

        layout.addWidget(self.pytanie1)
        layout.addWidget(self.radio_button1_1)
        layout.addWidget(self.radio_button1_2)
        layout.addWidget(self.radio_button1_3)
        layout.addWidget(self.input1)

        # Pytanie nr 2:
        self.pytanie2 = QLabel(stylizuj_tekst("2. Kto z poniższych jest członkiem Avengers:"))
        self.checkbox2_1 = QCheckBox("Thor")
        self.checkbox2_2 = QCheckBox("Loki")
        self.checkbox2_3 = QCheckBox("Hawkeye")
        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("Wpisz odpowiedź...")
        self.input2.setValidator(validator)

        layout.addWidget(self.pytanie2)
        layout.addWidget(self.checkbox2_1)
        layout.addWidget(self.checkbox2_2)
        layout.addWidget(self.checkbox2_3)
        layout.addWidget(self.input2)

        # Pytanie nr 3:
        self.pytanie3 = QLabel(stylizuj_tekst("3. Kto gra rolę Thora w filmach Marvela?"))
        self.radio_group3 = QButtonGroup(self)
        self.radio_button3_1 = QRadioButton("Chris Hemsworth")
        self.radio_button3_2 = QRadioButton("Chris Evans")
        self.radio_button3_3 = QRadioButton("Chris Pratt")
        self.input3 = QLineEdit()
        self.input3.setPlaceholderText("Wpisz odpowiedź...")
        self.input3.setValidator(validator)

        self.radio_group3.addButton(self.radio_button3_1)
        self.radio_group3.addButton(self.radio_button3_2)
        self.radio_group3.addButton(self.radio_button3_3)

        layout.addWidget(self.pytanie3)
        layout.addWidget(self.radio_button3_1)
        layout.addWidget(self.radio_button3_2)
        layout.addWidget(self.radio_button3_3)
        layout.addWidget(self.input3)

        # Pytanie nr 4:
        self.pytanie4 = QLabel(stylizuj_tekst("4. Kto jest siostrą Gamory:"))
        self.radio_group4 = QButtonGroup(self)
        self.radio_button4_1 = QRadioButton("Nebula")
        self.radio_button4_2 = QRadioButton("Valkyrie")
        self.radio_button4_3 = QRadioButton("Shuri")
        self.input4 = QLineEdit()
        self.input4.setPlaceholderText("Wpisz odpowiedź...")
        self.input4.setValidator(validator)

        self.radio_group4.addButton(self.radio_button4_1)
        self.radio_group4.addButton(self.radio_button4_2)
        self.radio_group4.addButton(self.radio_button4_3)

        layout.addWidget(self.pytanie4)
        layout.addWidget(self.radio_button4_1)
        layout.addWidget(self.radio_button4_2)
        layout.addWidget(self.radio_button4_3)
        layout.addWidget(self.input4)

        # Pytanie nr 5:
        self.pytanie5 = QLabel(stylizuj_tekst("Które z poniższych postaci występuje w filmie 'Guardians of the Galaxy':"))
        self.checkbox5_1 = QCheckBox("Rocket Racoon")
        self.checkbox5_2 = QCheckBox("Black Widow")
        self.checkbox5_3 = QCheckBox("Drax the Destroyer")
        self.input5 = QLineEdit()
        self.input5.setPlaceholderText("Wpisz odpowiedź...")
        self.input5.setValidator(validator)

        layout.addWidget(self.pytanie5)
        layout.addWidget(self.checkbox5_1)
        layout.addWidget(self.checkbox5_2)
        layout.addWidget(self.checkbox5_3)
        layout.addWidget(self.input5)

        centralny_widget.setLayout(layout)

        # Przycisk sprawdzający:

        self.check_button = QPushButton("Sprawdź")
        self.check_button.clicked.connect(self.sprawdzenie_odp)
        layout.addWidget(self.check_button)

        

    def sprawdzenie_odp(self):
        punkty = 0

        if self.radio_button1_1.isChecked():
            self.radio_button1_1.setStyleSheet("color:green")
            punkty += 1
        elif self.input1.text().strip().lower() == "tony stark":
            self.input1.setStyleSheet("color:green")
            punkty += 1
        else:
            self.radio_button1_1.setStyleSheet("color:green")
            self.radio_button1_2.setStyleSheet("color: red")
            self.radio_button1_3.setStyleSheet("color: red")
            self.input1.setStyleSheet("color: red")
        
        if self.checkbox2_1.isChecked() and not self.checkbox2_2.isChecked() and self.checkbox2_3.isChecked():
            self.checkbox2_1.setStyleSheet("color: green;")
            self.checkbox2_3.setStyleSheet("color: green;")
            self.checkbox2_2.setStyleSheet("color: red;")
            punkty += 1
        elif self.input2.text().strip().lower() in ["thor, hawkeye"]:
            self.input2.setStyleSheet("color: green;")
            punkty += 1
        else:
            self.checkbox2_1.setStyleSheet("color: green;")
            self.checkbox2_2.setStyleSheet("color: red;")
            self.checkbox2_3.setStyleSheet("color: green;")
            self.input2.setStyleSheet("color: red;")
        
            
        if self.radio_button3_1.isChecked():
            self.radio_button3_1.setStyleSheet("color:green")
            punkty += 1
        elif self.input3.text().strip().lower() == "chris hemsworth":
            self.input3.setStyleSheet("color:green")
            punkty += 1
        else:
            self.radio_button3_1.setStyleSheet("color: green")
            self.radio_button3_2.setStyleSheet("color: red")
            self.radio_button3_3.setStyleSheet("color: red")
            self.input3.setStyleSheet("color: red")
        
        if self.radio_button4_1.isChecked():
           self.radio_button4_1.setStyleSheet("color:green")
           punkty += 1
        elif self.input4.text().strip().lower() == "nebula":
                self.input4.setStyleSheet("color:green")
                punkty += 1
        else:
                self.radio_button4_1.setStyleSheet("color:green")
                self.radio_button4_2.setStyleSheet("color: red")
                self.radio_button4_3.setStyleSheet("color: red")
                self.input4.setStyleSheet("color: red")
        
        if self.checkbox5_1.isChecked() and not self.checkbox5_2.isChecked() and self.checkbox5_3.isChecked():
            self.checkbox5_1.setStyleSheet("color: green;")
            self.checkbox5_3.setStyleSheet("color: green;")
            self.checkbox5_2.setStyleSheet("color: red;")
            punkty += 1
        elif self.input5.text().strip().lower() in ["rocket racoon", "drax the destroyer"]:
            self.input5.setStyleSheet("color:green")
            punkty += 1
        else:
            self.checkbox5_1.setStyleSheet("color: green;")
            self.checkbox5_2.setStyleSheet("color: red;")
            self.checkbox5_3.setStyleSheet("color: green;")
            self.input5.setStyleSheet("color: red")
        
        QMessageBox.information(self, "Wynik", f"Zdobyłeś {punkty} na 5 punktów!")


app = QApplication([])
quiz = Quiz()
quiz.show()
app.exec()





    

