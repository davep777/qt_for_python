import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget
from PySide6.QtGui import QFont, QColor, QPixmap
from PySide6.QtCore import Qt

app = QApplication(sys.argv)

window = QWidget()
window.resize(400,300)

label1 = QLabel("Tekst po lewej stronie", window)
label1.move(10,10)
label1.setFont(QFont("Arial", 10,))
label1.setStyleSheet("background-color: purple; padding: 5px")

label2 = QLabel(window)
#fizyczny obrazek
#pixmap = QPixmap("C:/Users/Davev/Desktop/Python/qt/obrazek.jpg")
#scale_pixamp = pixmap.scaled(50,50)
#label2.setPixmap(scale_pixamp)
pixmap = QPixmap(50,50)
pixmap.fill(Qt.blue)
label2.setPixmap(pixmap)
label2.move(10,50)

label3 = QLabel("<b>Pogrubiony tekst, <i>kursywa</i>",window)
label3.setAlignment(Qt.AlignCenter)
label3.move(80,120)

label4 = QLabel("<a href = 'https://google.pl'>Kliknij link do wyszukiwarki</a>", window)
label4.setOpenExternalLinks(True)
label4.move(10,180)

label5 = QLabel("Kliknij mnie", window)
label5.setStyleSheet("color: red; background-color: lightgray; cursor: pointer")
label5.resize(400,30)
label5.setAlignment(Qt.AlignCenter)
label5.move(10,220)
label5.mousePressEvent = lambda event: label5.setText("Tekst zmieniony")
window.show()
app.exec()
