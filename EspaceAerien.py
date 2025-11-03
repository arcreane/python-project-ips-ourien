from avion import Avion
import math
class EspaceAerien:
    def __init__(avions):
        self.avions = []
    def ajouter_avion(self, avion: Avion):
        self.avions.append(avion)
    def maj(self,dt):
        for avion in self.avions:
            avion.move(dt)
    def detect_collisions(self,distance_min=1000):
        collisions = []
        for i,a1 in enumerate(self.avions):
            for a2 in self.avions[i+1:]:
                dist=math.sqrt((a1.xa-a2.xa)**2 + (a1.ya-a2.ya)**2)
                if dist < distance_min:
                    collisions.append((a1,a2))
        return collisions