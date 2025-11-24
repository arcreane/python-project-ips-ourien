# utils.py
import sys
import time
from PySide6.QtWidgets import QApplication
from app import Avion
from espace_aerien import EspaceAerien
from jeu import Jeu

# -------------------------------------------------------------
#  PARTIE 1 : Simulation (remplace l'ancien fichier simulation.py)
# -------------------------------------------------------------
class Simulation:
    def __init__(self):
        # Crée un seul EspaceAerien partagé entre la Simulation et le Jeu
        self.espace = EspaceAerien()
        self.jeu = Jeu()
        # Faire pointer le jeu vers le même espace pour que les avions générés
        # dans Jeu se retrouvent bien dans self.espace.avions
        self.jeu.espace = self.espace
        self.jeu.avions = self.espace.avions

    def charger_avions_test(self):
        """Charge 5 avions de test comme dans tes anciens scripts"""
        # Générer quelques avions aléatoires via l'instance Jeu
        for _ in range(5):
                self.jeu.generer_avion()

    def tick(self, dt=1.0):
        """Met à jour l'espace aérien (positions + collisions)"""
        # Utiliser la logique de mise à jour du Jeu (qui met à jour l'espace)
        self.jeu.mise_a_jour(dt)
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