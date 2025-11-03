from espace_aerien import EspaceAerien

class Jeu:
    def __init__(self):
        self.espace = EspaceAerien()
        self.score = 0

    def mise_a_jour(self, dt):
        self.espace.mettre_a_jour(dt)
        collisions = self.espace.detecter_collisions()
        if collisions:
            print("Collision détectée !")