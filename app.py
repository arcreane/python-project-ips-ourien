# app.py
import math
import time

class Avion:
    ALTITUDE_MAX = 36000  # ft

    def __init__(self, identifiant, vitesse, cap, altitude, xa, ya, urgence=False):
        self.identifiant = identifiant
        self.vitesse = vitesse  # en km/h
        self.cap = cap  # en degrés
        self.altitude = altitude  # en ft
        self.xa = xa  # position x (km)
        self.ya = ya  # position y (km)
        self.urgence = urgence

        self.spawn_time = time.time()

        # --- nouveaux attributs pour l’atterrissage ---
        self.en_approche = False
        self.termine_atterrissage = False
        self.cible_x = None
        self.cible_y = None

    def demarrer_atterrissage(self, cible_x, cible_y):
        self.en_approche = True
        self.termine_atterrissage = False
        self.cible_x = cible_x
        self.cible_y = cible_y

    def move(self, dt):
        v = self.vitesse / 3600.0  # km/s
        rad = math.radians(self.cap)
        self.xa += v * dt * math.cos(rad)
        self.ya += v * dt * math.sin(rad)

    def changement_vitesse(self, delta_v):
        self.vitesse += delta_v

    def changement_cap(self, delta_cap):
        self.cap = (self.cap + delta_cap) % 360

    def changement_altitude(self, delta_altitude):
        self.altitude += delta_altitude
        if self.altitude > self.ALTITUDE_MAX:
            self.altitude = self.ALTITUDE_MAX
        elif self.altitude < 0:
            self.altitude = 0

    def atterrir(self, center_x=0, center_y=0, distance_max=10, altitude_max=2000):
        distance = math.hypot(self.xa - center_x, self.ya - center_y)
        return distance <= distance_max and self.altitude <= altitude_max

    def sort_du_radar(self, rayon_max):
        distance = math.hypot(self.xa, self.ya)
        return distance > rayon_max

    def temps_urgence_ecoule(self, duree_sec=10):
        if not self.urgence:
            return False
        return (time.time() - self.spawn_time) > duree_sec

    def affiche(self):
        print(self.identifiant, self.vitesse, self.cap, self.altitude, f"({self.xa:.2f}, {self.ya:.2f})", "Urgence" if self.urgence else "")
