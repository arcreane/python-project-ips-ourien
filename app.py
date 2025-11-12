
import math
class Avion:

    def __init__(self,identifiant,vitesse,cap,altitude,xa,ya):
        self.identifiant = identifiant
        self.vitesse = vitesse
        self.cap = cap
        self.altitude = altitude
        self.xa = xa
        self.ya = ya

    def move(self, dt):
        """Met à jour la position selon le cap et la vitesse"""
        v = self.vitesse / 3600.0  # km/s
        rad = math.radians(self.cap)
        self.xa += v * dt * math.cos(rad)
        self.ya += v * dt * math.sin(rad)
    def changement_vitesse(self,delta_v):
        self.vitesse += delta_v
    def changement_cap(self,delta_cap):
        self.cap += delta_cap
    def changement_altitude(self,delta_altitude):
        self.altitude += delta_altitude
    def affiche(self):
        print(self.identifiant,self.vitesse,self.cap,self.altitude)

