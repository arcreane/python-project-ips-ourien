
# app.py
# --- Dans app.py ---
import math
import time

class Avion:
    ALTITUDE_MAX = 36000  # ft

    def __init__(self, identifiant, vitesse, cap, altitude, xa, ya, urgence=False):
        self.identifiant = identifiant
        self.vitesse = vitesse      # km/h
        self.cap = cap              # degrés
        self.altitude = altitude    # ft
        self.xa = xa                # km (position relative au centre)
        self.ya = ya                # km
        self.urgence = urgence      # booléen
        self.spawn_time = time.time()

    def move(self, dt):
        """Met à jour la position selon le cap et la vitesse (dt en secondes)."""
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
        """Retourne True si l'avion est à portée pour atterrir et sous altitude max."""
        distance = math.hypot(self.xa - center_x, self.ya - center_y)
        if distance <= distance_max and self.altitude <= altitude_max:
            return True
        return False

    def sort_du_radar(self, rayon_max):
        """Retourne True si l'avion est hors du rayon du radar."""
        distance = math.hypot(self.xa, self.ya)
        return distance > rayon_max

    def temps_urgence_ecoule(self, duree_sec=10):
        """Retourne True si l'avion urgent dépasse le temps imparti."""
        if not self.urgence:
            return False
        return (time.time() - self.spawn_time) > duree_sec

    def affiche(self):
        print(self.identifiant, self.vitesse, self.cap, self.altitude, f"({self.xa:.2f}, {self.ya:.2f})", "Urgence" if self.urgence else "")
