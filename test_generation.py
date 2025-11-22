from jeu import Jeu
import time

jeu = Jeu()

print("👉 Test de génération d'avions…")

# On simule 20 secondes de jeu pour voir si des avions apparaissent
for i in range(20):
    jeu.mise_a_jour(1)  # dt = 1 seconde
    time.sleep(0.2)     # juste pour éviter un spam trop rapide

print("✅ Test terminé.")