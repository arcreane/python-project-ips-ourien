import sys
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from app import *

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.avion=Avion
        button = QPushButton("Altitude +500 ft ")
        self.setWindowTitle("My App")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)
        self.avions =[
        Avion("AF123", 900, 0, 10000, xa=0, ya=0),
        Avion("BA456", 900, 180, 10000, xa=0.5, ya=0),  # proche de AF123
        Avion("LH789", 800, 90, 12000, xa=10, ya=10),
        Avion("KL101", 850, 270, 11000, xa=10.5, ya=10),  # proche de LH789
        Avion("UA202", 950, 45, 9000, xa=50, ya=50)  # loin des autres
    ]

        self.setFixedSize(QSize(400, 300))

        # Set the central widget of the Window.
        self.setCentralWidget(button)
    def the_button_was_clicked(self):
        for avion in self.avions:
            avion.changement_altitude(500)
        print(f"L'altitude de l'{avion.identifiant} a augmentée de 500ft pour atteindre {avion.altitude} ft")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()