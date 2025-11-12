import sys
from app import *
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        button = QPushButton("Altitude +500 ft ")
        self.setWindowTitle("My App")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)



        self.setFixedSize(QSize(400, 300))

        # Set the central widget of the Window.
        self.setCentralWidget(button)
        self.avion = Avion("A320", 800, 90, 10000, 0, 0)

    def the_button_was_clicked(self):
            print(f"L'altitude de l'{self.avion.identifiant} a augmentée à {self.avion.altitude} ft.")
            if self.avion.altitude >= 11000:
                print("l'avion ne peut pas monter plus haut")
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()