"""import sys
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
        for avion in self.Avions:
            avion.changement_altitude(500)
        print(f"L'altitude de l'{Avion.identifiant} a augmentée de 500ft pour atteindre {Avion.altitude} ft")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()"""

"""import sys
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from app import Avion


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        # Liste d'avions
        self.Avions = [
            Avion("AF123", 900, 0, 10000, xa=0,   ya=0),
            Avion("BA456", 900, 180, 10000, xa=0.5, ya=0),
            Avion("LH789", 800, 90, 12000, xa=10,  ya=10),
            Avion("KL101", 850, 270, 11000, xa=10.5, ya=10),
            Avion("UA202", 950, 45, 9000,  xa=50,  ya=50),
        ]

        # Bouton
        button = QPushButton("Altitude +500 ft")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)

        # ENLEVER le setFixedSize → ça bloque toute la future interface 3 zones
        # self.setFixedSize(QSize(400, 300))

        self.setCentralWidget(button)

    def the_button_was_clicked(self):
        for avion in self.Avions:
            avion.changement_altitude(500)
            print(
                f"L'altitude de l'avion {avion.identifiant} "
                f"a augmenté à {avion.altitude} ft"
            )


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel,
    QHBoxLayout, QVBoxLayout, QWidget, QListWidget
)
from PySide6.QtCore import Qt, QTimer

from utils import Simulation


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Espace Aérien - Simulation Radar")
        self.setStyleSheet("background-color: black; color: white;")

        self.sim = Simulation()
        self.sim.charger_avions_test()

        # --- Layout global en 3 parties ---
        layout = QHBoxLayout()

        # gauche
        self.left_panel = QListWidget()
        self.left_panel.setStyleSheet("background: #222; color: white;")
        layout.addWidget(self.left_panel, 1)

        # centre (map)
        self.map_label = QLabel("MAP ICI")
        self.map_label.setAlignment(Qt.AlignCenter)
        self.map_label.setStyleSheet("background: #333; color: white;")
        layout.addWidget(self.map_label, 3)

        # droite
        self.right_panel = QListWidget()
        self.right_panel.setStyleSheet("background: #222; color: white;")
        layout.addWidget(self.right_panel, 1)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Timer de simulation
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(1000)  # 1 seconde

    def update_ui(self):
        collisions = self.sim.tick()

        # Mise à jour de la liste des avions
        self.left_panel.clear()
        for a in self.sim.espace.avions:
            self.left_panel.addItem(
                f"{a.identifiant} → pos=({a.xa:.2f}, {a.ya:.2f}) alt={a.altitude}"
            )

        # Mise à jour des collisions
        self.right_panel.clear()
        if collisions:
            for a1, a2, d_h, d_v in collisions:
                self.right_panel.addItem(
                    f"⚠ {a1.identifiant} / {a2.identifiant} → {d_h:.2f} km, {d_v} ft"
                )
        else:
            self.right_panel.addItem("Aucune collision !")

    if __name__ == "__main__":
        from utils import lancer_application
        lancer_application()


