from espace_aerien import EspaceAerien
from app import Avion
import random

class Jeu:
    def __init__(self):
        self.espace = EspaceAerien()
        self.score = 0
        self.temps_ecoule = 0
        self.taux_generation=5

        self.avions = self.espace.avions


    def generer_avion(self):
        # Coordonnées initiales aléatoires
        self.xa = random.randint(0, 11000)
        self.ya = random.randint(0, 11000)
        self.altitude = random.randint(1500, 36000)
        self.vitesse = random.randint(350, 900)
        self.cap = random.randint(0, 359)
        self.carburant = random.randint(10,100)


        self.identifiant = f"FL{self.altitude//100}"

        avion = Avion(self.identifiant,self.vitesse,self.cap,self.altitude,self.xa,self.ya)

        self.espace.ajouter_avion(avion)

        print(f"✈️ Avion généré : {self.identifiant}")

    def mise_a_jour(self, dt):
        self.espace.maj(dt)

        collisions = self.espace.detect_collisions()
        if collisions:
            print("Collision détectée")

        self.temps_ecoule += dt
        # Générer de nouveaux avions régulièrement
        if self.temps_ecoule >= self.taux_generation:
            self.generer_avion()
            self.temps_ecoule = 0

        # Mise à jour du mouvement des avions
        self.espace.maj(dt)