
class Avion:

    def __init__(self,identifiant,vitesse,cap,altitude):
        self.identifiant = identifiant
        self.vitesse = vitesse
        self.cap = cap
        self.altitude = altitude
    def changement_vitesse(self,delta_v):
        self.vitesse += delta_v
    def changement_cap(self,delta_cap):
        self.cap += delta_cap
    def changement_altitude(self,delta_altitude):
        self.altitude += delta_altitude
    def affiche(self):
        print(self.identifiant,self.vitesse,self.cap,self.altitude)

A1 = Avion("AF012",800,249,10000)
A1.affiche()
