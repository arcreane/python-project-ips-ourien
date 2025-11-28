"""import sys
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from app import *

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.avion=Avion
        button = QPushButton("Altitude +500 ft ")
        self.setWindowTitle("My App")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)
        self.avions =[
        Avion("AF123", 900, 0, 10000, xa=0, ya=0),
        Avion("BA456", 900, 180, 10000, xa=0.5, ya=0),  # proche de AF123
        Avion("LH789", 800, 90, 12000, xa=10, ya=10),
        Avion("KL101", 850, 270, 11000, xa=10.5, ya=10),  # proche de LH789
        Avion("UA202", 950, 45, 9000, xa=50, ya=50)  # loin des autres
    ]

        self.setFixedSize(QSize(400, 300))

        # Set the central widget of the Window.
        self.setCentralWidget(button)
    def the_button_was_clicked(self):
        for avion in self.Avions:
            avion.changement_altitude(500)
        print(f"L'altitude de l'{Avion.identifiant} a augmentée de 500ft pour atteindre {Avion.altitude} ft")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()"""

"""import sys
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from app import Avion


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        # Liste d'avions
        self.Avions = [
            Avion("AF123", 900, 0, 10000, xa=0,   ya=0),
            Avion("BA456", 900, 180, 10000, xa=0.5, ya=0),
            Avion("LH789", 800, 90, 12000, xa=10,  ya=10),
            Avion("KL101", 850, 270, 11000, xa=10.5, ya=10),
            Avion("UA202", 950, 45, 9000,  xa=50,  ya=50),
        ]

        # Bouton
        button = QPushButton("Altitude +500 ft")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)

        # ENLEVER le setFixedSize → ça bloque toute la future interface 3 zones
        # self.setFixedSize(QSize(400, 300))

        self.setCentralWidget(button)

    def the_button_was_clicked(self):
        for avion in self.Avions:
            avion.changement_altitude(500)
            print(
                f"L'altitude de l'avion {avion.identifiant} "
                f"a augmenté à {avion.altitude} ft"
            )


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()"""
"""
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel,
    QHBoxLayout, QVBoxLayout, QWidget, QListWidget
)
from PySide6.QtCore import Qt, QTimer

from utils import Simulation


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Espace Aérien - Simulation Radar")
        self.setStyleSheet("background-color: black; color: white;")

        self.sim = Simulation()
        self.sim.charger_avions_test()

        # --- Layout global en 3 parties ---
        layout = QHBoxLayout()

        # gauche
        self.left_panel = QListWidget()
        self.left_panel.setStyleSheet("background: #222; color: white;")
        layout.addWidget(self.left_panel, 1)

        # centre (map)
        self.map_label = QLabel("MAP ICI")
        self.map_label.setAlignment(Qt.AlignCenter)
        self.map_label.setStyleSheet("background: #333; color: white;")
        layout.addWidget(self.map_label, 3)

        # droite
        self.right_panel = QListWidget()
        self.right_panel.setStyleSheet("background: #222; color: white;")
        layout.addWidget(self.right_panel, 1)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Timer de simulation
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(1000)  # 1 seconde

    def update_ui(self):
        collisions = self.sim.tick()

        # Mise à jour de la liste des avions
        self.left_panel.clear()
        for a in self.sim.espace.avions:
            self.left_panel.addItem(
                f"{a.identifiant} → pos=({a.xa:.2f}, {a.ya:.2f}) alt={a.altitude}"
            )

        # Mise à jour des collisions
        self.right_panel.clear()
        if collisions:
            for a1, a2, d_h, d_v in collisions:
                self.right_panel.addItem(
                    f"⚠ {a1.identifiant} / {a2.identifiant} → {d_h:.2f} km, {d_v} ft"
                )
        else:
            self.right_panel.addItem("Aucune collision !")

    if __name__ == "__main__":
        from utils import lancer_application
        lancer_application()
"""
"""
import sys
import random
import math
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton,
    QHBoxLayout, QVBoxLayout, QWidget, QListWidget, QGroupBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QColor, QPainter, QPen

from utils import Simulation
from app import Avion  # classe Avion

RADAR_IMAGE_PATH = "/mnt/data/56928953-4e27-41b3-ae49-f5e120ec2089.png"

class RadarWidget(QWidget):
    def __init__(self, parent_window=None):
        super().__init__()
        self.setMinimumSize(500, 500)
        self.avions = []
        self.selected_identifiant = None
        self.parent_window = parent_window  # référence à MainWindow pour la sélection
        self.bg = QPixmap()
        if not self.bg.load(RADAR_IMAGE_PATH):
            print(f"Erreur : impossible de charger l'image radar depuis {RADAR_IMAGE_PATH}")

    def update_positions(self, avions, selected_identifiant=None):
        self.avions = avions
        self.selected_identifiant = selected_identifiant
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        rect = self.rect()
        center = rect.center()

        # Fond
        if not self.bg.isNull():
            painter.drawPixmap(rect, self.bg)

        # Cercle radar
        pen = QPen(QColor("#1EC8FF"))
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        radius = min(rect.width(), rect.height()) // 2 - 20
        painter.drawEllipse(center, radius, radius)

        # Avions
        for a in self.avions:
            px = center.x() + int(a.xa * 12)
            py = center.y() + int(a.ya * 12)
            color = QColor("#FF0000") if self.selected_identifiant == a.identifiant else (QColor("#FFB43B") if a.altitude >= 2000 else QColor("#FF4F5A"))
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(px - 6, py - 6, 12, 12)

    def mousePressEvent(self, event):
        if not self.avions:
            return
        center = self.rect().center()
        pos = event.position()  # QPointF
        ex, ey = pos.x(), pos.y()
        for a in self.avions:
            px = center.x() + int(a.xa * 12)
            py = center.y() + int(a.ya * 12)
            r = 6
            if (px - r <= ex <= px + r) and (py - r <= ey <= py + r):
                if self.parent_window:
                    self.parent_window.select_plane_by_id(a.identifiant)
                break


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ATC Simulator")
        self.setStyleSheet("
            QWidget { background-color: #0A0F1A; color: white; font-family: Arial; }
            QListWidget { background: #1C2233; border: 2px solid #22C5FF; }
            QGroupBox { border: 2px solid #22C5FF; border-radius: 8px; padding: 10px; margin: 8px; }
            QPushButton {
                background-color: #0ABAF4; padding: 10px;
                border-radius: 6px; font-weight: bold;
            }
            QPushButton:hover { background-color: #08A3D8; }
        ")

        # Simulation
        self.sim = Simulation()
        self.sim.charger_avions_test()

        # Layout principal
        layout = QHBoxLayout()

        # Colonne gauche
        left = QVBoxLayout()
        stats_box = QGroupBox("STATS")
        stats_layout = QVBoxLayout()
        self.label_avions = QLabel("Avions: 0")
        self.label_niveau = QLabel("Niveau: 1")
        stats_layout.addWidget(self.label_avions)
        stats_layout.addWidget(self.label_niveau)
        stats_box.setLayout(stats_layout)

        self.liste_avions = QListWidget()
        self.liste_avions.itemClicked.connect(self.select_plane)

        left.addWidget(stats_box)
        left.addWidget(QLabel("AVIONS"))
        left.addWidget(self.liste_avions)

        # Centre : radar
        self.radar = RadarWidget(parent_window=self)

        # Colonne droite
        right = QVBoxLayout()
        controls = QGroupBox("CONTROLES")
        c_layout = QVBoxLayout()
        self.label_selected = QLabel("Sélectionné : Aucun")
        btn_up = QPushButton("⬆ Monter")
        btn_dn = QPushButton("⬇ Descendre")
        btn_up.clicked.connect(self.monter_avion)
        btn_dn.clicked.connect(self.descendre_avion)
        c_layout.addWidget(self.label_selected)
        c_layout.addWidget(btn_up)
        c_layout.addWidget(btn_dn)
        controls.setLayout(c_layout)

        actions = QGroupBox("ACTIONS")
        a_layout = QVBoxLayout()
        btn_land = QPushButton("✔ Atterrir")
        btn_hold = QPushButton("⟳ Attente")
        btn_emergency = QPushButton("🛑 Urgence")
        btn_emergency.setStyleSheet("background-color:#FF4F5A;")
        a_layout.addWidget(btn_land)
        a_layout.addWidget(btn_hold)
        a_layout.addWidget(btn_emergency)
        actions.setLayout(a_layout)

        right.addWidget(controls)
        right.addWidget(actions)

        # Ajout colonnes
        layout.addLayout(left, 1)
        layout.addWidget(self.radar, 3)
        layout.addLayout(right, 1)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Timer UI
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(800)

        # Spawn automatique toutes les 10 secondes
        self.spawn_timer = QTimer()
        self.spawn_timer.timeout.connect(self.spawn_plane)
        self.spawn_timer.start(10_000)

        # Déplacement avions
        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.move_planes)
        self.move_timer.start(800)

    # Mise à jour UI
    def update_ui(self):
        self.sim.tick()

        # Stats
        self.label_avions.setText(f"Avions: {len(self.sim.espace.avions)}")
        self.label_niveau.setText(f"Niveau: {getattr(self.sim, 'niveau', 1)}")

        # Liste
        self.liste_avions.clear()
        for a in self.sim.espace.avions:
            self.liste_avions.addItem(
                f"{a.identifiant} — Alt: {a.altitude} ft — V: {a.vitesse} km/h — Cap: {a.cap}°"
            )

        # Radar
        selected_id = self.get_selected_identifiant()
        self.radar.update_positions(self.sim.espace.avions, selected_identifiant=selected_id)

        # Infos avion sélectionné
        if selected_id:
            for a in self.sim.espace.avions:
                if a.identifiant == selected_id:
                    self.label_selected.setText(
                        f"Avion: {a.identifiant}\n"
                        f"Altitude: {a.altitude} ft\n"
                        f"Vitesse: {a.vitesse} km/h\n"
                        f"Cap: {a.cap}°\n"
                        f"Position: ({a.xa:.2f}, {a.ya:.2f})"
                    )
                    break
        else:
            self.label_selected.setText("Sélectionné : Aucun")

    # Spawn automatique
    def spawn_plane(self):
        ident = "AV" + str(len(self.sim.espace.avions) + 1)
        angle = random.uniform(0, 360)
        distance = 8
        xa = distance * math.cos(math.radians(angle))
        ya = distance * math.sin(math.radians(angle))
        vitesse = random.randint(300, 750)
        cap = random.randint(0, 360)
        altitude = random.randint(2000, 9000)
        a = Avion(ident, vitesse, cap, altitude, xa, ya)
        self.sim.espace.avions.append(a)
        self.update_ui()

    # Déplacement avions
    def move_planes(self):
        dt = 0.8
        for a in self.sim.espace.avions:
            a.move(dt)
        self.update_ui()

    # Sélection avion
    def select_plane(self, item):
        identifiant = item.text().split(" — ")[0]
        self.select_plane_by_id(identifiant)

    def select_plane_by_id(self, identifiant):
        for idx, a in enumerate(self.sim.espace.avions):
            if a.identifiant == identifiant:
                self.liste_avions.setCurrentRow(idx)
                break
        self.update_ui()

    def get_selected_identifiant(self):
        item = self.liste_avions.currentItem()
        if not item:
            return None
        return item.text().split(" — ")[0]

    # Monter / Descendre
    def monter_avion(self):
        identifiant = self.get_selected_identifiant()
        if not identifiant:
            return
        for a in self.sim.espace.avions:
            if a.identifiant == identifiant:
                a.changement_altitude(1000)
                break
        self.update_ui()

    def descendre_avion(self):
        identifiant = self.get_selected_identifiant()
        if not identifiant:
            return
        for a in self.sim.espace.avions:
            if a.identifiant == identifiant:
                a.changement_altitude(-1000)
                break
        self.update_ui()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.showMaximized()
    sys.exit(app.exec())

"""
import sys
import random
import math
import string
import requests
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton,
    QHBoxLayout, QVBoxLayout, QWidget, QListWidget, QGroupBox, QSlider
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QPainter, QPen, QTransform, QColor

from utils import Simulation
from app import Avion

# Images depuis Internet
RADAR_IMAGE_URL = "https://i.imgur.com/7z4JZxR.png"
PLANE_IMAGE_URL = "https://i.imgur.com/9zQ5rSL.png"
PLANE_RED_IMAGE_URL = "https://i.imgur.com/Rt3R0Dw.png"
TOWER_IMAGE_URL = "https://i.imgur.com/kbYhXxW.png"  # Tour de contrôle

class RadarWidget(QWidget):
    def __init__(self, parent_window=None):
        super().__init__()
        self.setMinimumSize(500, 500)
        self.avions = []
        self.selected_identifiant = None
        self.parent_window = parent_window

        self.bg = self.load_pixmap_from_url(RADAR_IMAGE_URL)
        self.plane_icon = self.load_pixmap_from_url(PLANE_IMAGE_URL)
        self.plane_icon_red = self.load_pixmap_from_url(PLANE_RED_IMAGE_URL)
        self.tower_icon = self.load_pixmap_from_url(TOWER_IMAGE_URL)

    def load_pixmap_from_url(self, url):
        try:
            img_data = requests.get(url).content
            pixmap = QPixmap()
            pixmap.loadFromData(img_data)
            return pixmap
        except Exception as e:
            print(f"Erreur chargement image {url}: {e}")
            return QPixmap()

    def update_positions(self, avions, selected_identifiant=None):
        self.avions = avions
        self.selected_identifiant = selected_identifiant
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        rect = self.rect()
        center = rect.center()

        # Fond radar
        if not self.bg.isNull():
            painter.drawPixmap(rect, self.bg)
        else:
            painter.fillRect(rect, Qt.black)

        # Cercle radar
        pen = QPen(QColor("#1EC8FF"))
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        radius = min(rect.width(), rect.height()) // 2 - 20
        painter.drawEllipse(center, radius, radius)

        # Tour de contrôle au centre
        if not self.tower_icon.isNull():
            tw, th = self.tower_icon.width(), self.tower_icon.height()
            painter.drawPixmap(center.x() - tw//2, center.y() - th//2, self.tower_icon)

        # Avions
        for a in self.avions:
            px = center.x() + int(a.xa * 12)
            py = center.y() + int(a.ya * 12)
            icon = self.plane_icon_red if self.selected_identifiant == a.identifiant else self.plane_icon
            if not icon.isNull():
                w, h = icon.width(), icon.height()
                transform = QTransform().rotate(-a.cap)
                rotated = icon.transformed(transform, Qt.SmoothTransformation)
                painter.drawPixmap(px - w//2, py - h//2, rotated)
            else:
                color = QColor("#FF0000") if self.selected_identifiant == a.identifiant else QColor("#FFB43B")
                painter.setBrush(color)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(px - 6, py - 6, 12, 12)

            # Affiche l'identifiant au-dessus de l'avion
            painter.setPen(QColor("#FFFFFF"))
            painter.drawText(px - 10, py - 10, a.identifiant)

    def mousePressEvent(self, event):
        if not self.avions:
            return
        center = self.rect().center()
        ex, ey = event.position().x(), event.position().y()
        for a in self.avions:
            px = center.x() + int(a.xa * 12)
            py = center.y() + int(a.ya * 12)
            r = max(self.plane_icon.width(), self.plane_icon.height())//2 if not self.plane_icon.isNull() else 6
            if (px - ex)**2 + (py - ey)**2 <= r**2:
                if self.parent_window:
                    self.parent_window.select_plane_by_id(a.identifiant)
                break

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ATC Simulator")
        self.sim = Simulation()
        self.sim.charger_avions_test()
        self.init_ui()
        self.start_timers()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget { background-color: #0A0F1A; color: white; font-family: Arial; }
            QListWidget { background: #1C2233; border: 2px solid #22C5FF; }
            QGroupBox { border: 2px solid #22C5FF; border-radius: 8px; padding: 10px; margin: 8px; }
            QPushButton {
                background-color: #0ABAF4; padding: 10px;
                border-radius: 6px; font-weight: bold;
            }
            QPushButton:hover { background-color: #08A3D8; }
        """)

        layout = QHBoxLayout()
        # Colonne gauche
        left = QVBoxLayout()
        stats_box = QGroupBox("STATS")
        stats_layout = QVBoxLayout()
        self.label_avions = QLabel("Avions: 0")
        self.label_niveau = QLabel("Niveau: 1")
        stats_layout.addWidget(self.label_avions)
        stats_layout.addWidget(self.label_niveau)
        stats_box.setLayout(stats_layout)
        self.liste_avions = QListWidget()
        self.liste_avions.itemClicked.connect(self.select_plane)
        left.addWidget(stats_box)
        left.addWidget(QLabel("AVIONS"))
        left.addWidget(self.liste_avions)

        # Centre radar
        self.radar = RadarWidget(parent_window=self)

        # Colonne droite
        right = QVBoxLayout()
        controls = QGroupBox("CONTROLES")
        c_layout = QVBoxLayout()
        self.label_selected = QLabel("Sélectionné : Aucun")

        # Boutons altitude
        btn_up = QPushButton("⬆ Monter")
        btn_dn = QPushButton("⬇ Descendre")
        # Boutons vitesse
        btn_speed_up = QPushButton("⬆ Accélérer")
        btn_speed_down = QPushButton("⬇ Ralentir")

        btn_up.clicked.connect(self.monter_avion)
        btn_dn.clicked.connect(self.descendre_avion)
        btn_speed_up.clicked.connect(self.accelerer_avion)
        btn_speed_down.clicked.connect(self.ralentir_avion)

        c_layout.addWidget(self.label_selected)
        c_layout.addWidget(btn_up)
        c_layout.addWidget(btn_dn)
        c_layout.addWidget(btn_speed_up)
        c_layout.addWidget(btn_speed_down)

        # Slider cap
        self.label_slider_cap = QLabel("Cap: 0°")
        c_layout.addWidget(self.label_slider_cap)

        self.slider_cap = QSlider(Qt.Horizontal)
        self.slider_cap.setMinimum(0)
        self.slider_cap.setMaximum(360)
        self.slider_cap.setValue(0)
        self.slider_cap.setTickInterval(10)
        self.slider_cap.setTickPosition(QSlider.TicksBelow)
        self.slider_cap.valueChanged.connect(self.slider_cap_changed)
        c_layout.addWidget(self.slider_cap)

        controls.setLayout(c_layout)

        actions = QGroupBox("ACTIONS")
        a_layout = QVBoxLayout()
        btn_land = QPushButton("✔ Atterrir")
        btn_hold = QPushButton("⟳ Attente")
        btn_emergency = QPushButton("🛑 Urgence")
        btn_emergency.setStyleSheet("background-color:#FF4F5A;")
        a_layout.addWidget(btn_land)
        a_layout.addWidget(btn_hold)
        a_layout.addWidget(btn_emergency)
        actions.setLayout(a_layout)

        right.addWidget(controls)
        right.addWidget(actions)

        layout.addLayout(left, 1)
        layout.addWidget(self.radar, 3)
        layout.addLayout(right, 1)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_timers(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(800)
        self.spawn_timer = QTimer()
        self.spawn_timer.timeout.connect(self.spawn_plane)
        self.spawn_timer.start(10000)
        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.move_planes)
        self.move_timer.start(800)

    def update_ui(self):
        self.sim.tick()
        self.label_avions.setText(f"Avions: {len(self.sim.espace.avions)}")
        self.label_niveau.setText(f"Niveau: {getattr(self.sim, 'niveau',1)}")
        current_id = self.get_selected_identifiant()
        self.liste_avions.clear()
        for a in self.sim.espace.avions:
            self.liste_avions.addItem(
                f"{a.identifiant} — Alt: {a.altitude} ft — V: {a.vitesse} km/h — Cap: {a.cap}°"
            )
        if current_id:
            self.select_plane_by_id(current_id)
        else:
            self.radar.update_positions(self.sim.espace.avions)

    def spawn_plane(self):
        letters = ''.join(random.choices(string.ascii_uppercase, k=2))
        digits = ''.join(random.choices(string.digits, k=3))
        ident = letters + digits

        angle = random.uniform(0,360)
        distance = 8
        xa = distance * math.cos(math.radians(angle))
        ya = distance * math.sin(math.radians(angle))
        vitesse = random.randint(300,750)
        cap = random.randint(0,360)
        altitude = random.randint(2000,9000)
        a = Avion(ident,vitesse,cap,altitude,xa,ya)
        self.sim.espace.avions.append(a)
        self.update_ui()

    def move_planes(self):
        dt = 0.8
        for a in self.sim.espace.avions:
            a.move(dt)
        self.update_ui()

    def select_plane(self, item):
        identifiant = item.text().split(" — ")[0]
        self.select_plane_by_id(identifiant)

    def select_plane_by_id(self, identifiant):
        for idx, a in enumerate(self.sim.espace.avions):
            if a.identifiant == identifiant:
                self.liste_avions.setCurrentRow(idx)
                self.slider_cap.setValue(a.cap)
                self.label_slider_cap.setText(f"Cap: {a.cap}°")
                break
        self.radar.update_positions(self.sim.espace.avions, selected_identifiant=identifiant)
        for a in self.sim.espace.avions:
            if a.identifiant == identifiant:
                self.label_selected.setText(
                    f"Avion: {a.identifiant}\nAltitude: {a.altitude} ft\nVitesse: {a.vitesse} km/h\nCap: {a.cap}°\nPosition: ({a.xa:.2f}, {a.ya:.2f})"
                )
                break

    def get_selected_identifiant(self):
        item = self.liste_avions.currentItem()
        if not item:
            return None
        return item.text().split(" — ")[0]

    # Monter / Descendre
    def monter_avion(self):
        identifiant = self.get_selected_identifiant()
        if identifiant:
            for a in self.sim.espace.avions:
                if a.identifiant == identifiant:
                    a.changement_altitude(1000)
                    break
        self.update_ui()

    def descendre_avion(self):
        identifiant = self.get_selected_identifiant()
        if identifiant:
            for a in self.sim.espace.avions:
                if a.identifiant == identifiant:
                    a.changement_altitude(-1000)
                    break
        self.update_ui()

    # Accélérer / Ralentir
    def accelerer_avion(self):
        identifiant = self.get_selected_identifiant()
        if identifiant:
            for a in self.sim.espace.avions:
                if a.identifiant == identifiant:
                    a.changement_vitesse(50)
                    break
        self.update_ui()

    def ralentir_avion(self):
        identifiant = self.get_selected_identifiant()
        if identifiant:
            for a in self.sim.espace.avions:
                if a.identifiant == identifiant:
                    a.changement_vitesse(-50)
                    break
        self.update_ui()

    # Slider cap
    def slider_cap_changed(self, value):
        self.label_slider_cap.setText(f"Cap: {value}°")
        identifiant = self.get_selected_identifiant()
        if identifiant:
            for a in self.sim.espace.avions:
                if a.identifiant == identifiant:
                    a.cap = value
                    break
        self.update_ui()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.showMaximized()
    sys.exit(app.exec())















