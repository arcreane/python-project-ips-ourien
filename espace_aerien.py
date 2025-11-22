import math
from app import Avion

class EspaceAerien:
    def __init__(self):
        self.avions = []

    def ajouter_avion(self, avion: Avion):
        self.avions.append(avion)

    def maj(self, dt):
        """Met à jour les positions de tous les avions"""
        for avion in self.avions:
            avion.move(dt)

    def distance_horizontale(self, a1, a2):
        return math.sqrt((a1.xa - a2.xa) ** 2 + (a1.ya - a2.ya) ** 2)

    def distance_verticale(self, a1, a2):
        return abs(a1.altitude - a2.altitude)

    def detect_collisions(self, distance_min=5.0, altitude_min=300):
        collisions = []

        for i, a1 in enumerate(self.avions):
            for a2 in self.avions[i+1:]:

                d_h = self.distance_horizontale(a1, a2)
                d_v = self.distance_verticale(a1, a2)

                if d_h < distance_min and d_v < altitude_min:
                    collisions.append((a1, a2, d_h, d_v))

        return collisions