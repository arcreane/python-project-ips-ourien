import math
from app import *
class EspaceAerien:
    def __init__(self):
        self.avions = []
    def ajouter_avion(self, avion: Avion):
        self.avions.append(avion)
    def maj(self,dt):
        for avion in self.avions:
            avion.move(dt)
    def detect_collisions(self,distance_min=1000,altitude_min = 100):
        collisions = []
        for i,a1 in enumerate(self.avions):
            for a2 in self.avions[i+1:]:
                dist=math.sqrt((a1.xa-a2.xa)**2 + (a1.ya-a2.ya)**2)
                if dist < distance_min:
                    if a1.altitude -a2.altitude < altitude_min:
                        collisions.append((a1,a2))
        return collisions



if __name__ == "__main__":
    espace = EspaceAerien()

    # Création de 5 avions à des positions différentes
    avions = [
        Avion("AF123", 900, 0, 15000, xa=0, ya=0),
        Avion("BA456", 900, 180, 10000, xa=0.5, ya=0),  # proche de AF123
        Avion("LH789", 800, 90, 12000, xa=10, ya=10),
        Avion("KL101", 850, 270, 11000, xa=10.5, ya=10),  # proche de LH789
        Avion("UA202", 950, 45, 9000, xa=50, ya=50)  # loin des autres
    ]

    for a in avions:
        espace.ajouter_avion(a)
    espace.maj(dt=1)
    collisions = espace.detect_collisions(distance_min=1.0,altitude_min = 100)

    print("Positions actuelles :")
    for a in espace.avions:
        print(f" - {a.identifiant}: ({a.xa:.2f}, {a.ya:.2f})")

    print("\nRésultat de la détection de collisions :")
    if collisions:
        for a1, a2 in collisions:
            print(f"⚠️ Collision détectée entre {a1.identifiant} et {a2.identifiant}")
    else:
        print("✅ Aucune collision détectée.")