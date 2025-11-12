import math
class Avion:
    ALTITUDE_MAX = 36000
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
        if self.altitude > self.ALTITUDE_MAX:
            self.altitude = self.ALTITUDE_MAX
            print(f"{self.identifiant} ne peut pas dépasser {self.ALTITUDE_MAX} ft.")
        elif self.altitude < 0:
            self.altitude = 0
            print(f"{self.identifiant} est au sol (0 ft).")
        else:
            self.altitude += delta_altitude
            print(f"{self.identifiant} → altitude : {self.altitude} ft")

    def affiche(self):
        print(self.identifiant,self.vitesse,self.cap,self.altitude)

