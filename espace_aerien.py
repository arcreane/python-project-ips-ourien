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