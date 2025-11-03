from avion import Avion
import math
class EspaceAerien:
    def __init__(avions):
        self.avions = []
    def ajouter_avion(self, avion: Avion):
        self.avions.append(avion)
    def maj(self,dt):
        for avion in self.avions:
            avion.deplacer(dt)
    def detect_collisions(self,distance_min=1000):
        collisions = []