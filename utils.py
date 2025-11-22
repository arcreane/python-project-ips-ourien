# utils.py
import sys
import time
from PySide6.QtWidgets import QApplication
from app import Avion
from espace_aerien import EspaceAerien


# -------------------------------------------------------------
#  PARTIE 1 : Simulation (remplace l'ancien fichier simulation.py)
# -------------------------------------------------------------
class Simulation:
    def __init__(self):
        self.espace = EspaceAerien()

    def charger_avions_test(self):
        """Charge 5 avions de test comme dans tes anciens scripts"""
        self.espace.avions = [
            Avion("AF123", 900, 0, 10000, 0, 0),
            Avion("BA456", 900, 180, 10000, 0.5, 0),
            Avion("LH789", 800, 90, 12000, 10, 10),
            Avion("KL101", 850, 270, 11000, 10.5, 10),
            Avion("UA202", 950, 45, 9000, 50, 50)
        ]

    def tick(self, dt=1.0):
        """Met à jour l'espace aérien (positions + collisions)"""
        self.espace.maj(dt)
        return self.espace.detect_collisions()



# --------------------------------------------------------------------
#  PARTIE 2 : Lancement global de l'application (ex-main.py)
#  👉 ATTENTION : on NE lance rien ici, car interface.py exécutera ceci
# --------------------------------------------------------------------
def lancer_application():
    """
    Fonction appelée par interface.py pour démarrer l’app.
    Permet de centraliser plus proprement le lancement.
    """
    from interface import MainWindow  # import ici pour éviter les import circulaires

    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    return app.exec()

    def tick(self, dt=1.0):
        """Met à jour l'espace aérien (positions + collisions)"""
        self.espace.maj(dt)
        return self.espace.detect_collisions()



# --------------------------------------------------------------------
#  PARTIE 2 : Lancement global de l'application (ex-main.py)
#  👉 ATTENTION : on NE lance rien ici, car interface.py exécutera ceci
# --------------------------------------------------------------------
def lancer_application():
    """
    Fonction appelée par interface.py pour démarrer l’app.
    Permet de centraliser plus proprement le lancement.
    """
    from interface import MainWindow  # import ici pour éviter les import circulaires

    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    return app.exec()