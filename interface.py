import sys

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
    def the_button_was_clicked(self):
            print("L'altitude de l'avion.identifiant a augmentée de 500ft")
            if avion.altitude() >= 11000:
                print("l'avion ne peut pas monter plus haut")
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()