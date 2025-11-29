# Interface
import sys
import random
import math
import string
import time
import requests
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton,
    QHBoxLayout, QVBoxLayout, QWidget, QListWidget, QGroupBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QPainter, QPen, QTransform, QColor

from app import Avion  # Assurez-vous que Avion est bien défini

# Images depuis Internet
RADAR_IMAGE_URL = "https://i.imgur.com/7z4JZxR.png"
PLANE_IMAGE_URL = "https://i.imgur.com/9zQ5rSL.png"
PLANE_RED_IMAGE_URL = "https://i.imgur.com/Rt3R0Dw.png"
TOWER_IMAGE_URL = "https://i.imgur.com/kbYhXxW.png"

# --- Modèles ---
class Espace:
    def __init__(self):
        self.avions = []

class Simulation:
    def __init__(self):
        self.espace = Espace()
    def charger_avions_test(self):
        pass  # à compléter si besoin

# --- Radar Widget ---
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

        if not self.bg.isNull():
            painter.drawPixmap(rect, self.bg)
        else:
            painter.fillRect(rect, Qt.black)

        pen = QPen(QColor("#1EC8FF"))
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        radius = min(rect.width(), rect.height()) // 2 - 20
        painter.drawEllipse(center, radius, radius)

        if not self.tower_icon.isNull():
            tw, th = self.tower_icon.width(), self.tower_icon.height()
            painter.drawPixmap(center.x() - tw // 2, center.y() - th // 2, self.tower_icon)

        for a in self.avions:
            px = center.x() + int(a.xa * 12)
            py = center.y() + int(a.ya * 12)

            if a.urgence:
                color = QColor("green")
            else:
                color = QColor("#FFB43B")
            if self.selected_identifiant == a.identifiant:
                color = QColor("blue")

            if not self.plane_icon.isNull():
                transform = QTransform().rotate(-a.cap)
                icon = self.plane_icon
                rotated = icon.transformed(transform, Qt.SmoothTransformation)
                painter.drawPixmap(px - rotated.width() // 2, py - rotated.height() // 2, rotated)
            else:
                painter.setBrush(color)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(px - 6, py - 6, 12, 12)

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
            r = max(self.plane_icon.width(), self.plane_icon.height()) // 2 if not self.plane_icon.isNull() else 6
            if (px - ex) ** 2 + (py - ey) ** 2 <= r ** 2:
                if self.parent_window:
                    self.parent_window.select_plane_by_id(a.identifiant)
                break

    # --- Pixel-perfect check ---
    def is_outside(self, a):
        center = self.rect().center()
        px = center.x() + int(a.xa * 12)
        py = center.y() + int(a.ya * 12)
        radius = min(self.width(), self.height()) // 2 - 20
        return (px - center.x())**2 + (py - center.y())**2 > radius**2

# --- Main Window ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ATC Simulator")
        self.sim = Simulation()
        self.sim.charger_avions_test()
        self.selected_identifiant = None
        self.crash_count = 0
        self.total_generated = 0
        self.score = 0
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
        left = QVBoxLayout()

        # Stats
        stats_box = QGroupBox("STATS")
        stats_layout = QVBoxLayout()
        self.label_avions = QLabel(f"Avions générés: {self.total_generated}")
        self.label_crash = QLabel(f"Crashs: {self.crash_count}")
        self.label_score = QLabel(f"Score: {self.score}")
        stats_layout.addWidget(self.label_avions)
        stats_layout.addWidget(self.label_crash)
        stats_layout.addWidget(self.label_score)
        stats_box.setLayout(stats_layout)
        left.addWidget(stats_box)

        # Liste des avions
        self.liste_avions = QListWidget()
        self.liste_avions.itemClicked.connect(self.select_plane)
        left.addWidget(QLabel("AVIONS"))
        left.addWidget(self.liste_avions)

        # Radar
        self.radar = RadarWidget(parent_window=self)

        # Colonne droite
        right = QVBoxLayout()
        actions = QGroupBox("ACTIONS")
        a_layout = QVBoxLayout()

        self.label_selected = QLabel("Sélectionné : Aucun")
        a_layout.addWidget(self.label_selected)

        # Boutons contrôle et cap
        btn_up = QPushButton("⬆ Monter")
        btn_dn = QPushButton("⬇ Descendre")
        btn_speed_up = QPushButton("⬆ Accélérer")
        btn_speed_down = QPushButton("⬇ Ralentir")
        btn_cap_plus = QPushButton("+20°")
        btn_cap_minus = QPushButton("-20°")
        btn_land = QPushButton("✔ Atterrir")

        btn_up.clicked.connect(self.monter_avion)
        btn_dn.clicked.connect(self.descendre_avion)
        btn_speed_up.clicked.connect(self.accelerer_avion)
        btn_speed_down.clicked.connect(self.ralentir_avion)
        btn_cap_plus.clicked.connect(lambda: self.changer_cap(20))
        btn_cap_minus.clicked.connect(lambda: self.changer_cap(-20))
        btn_land.clicked.connect(self.atterrir_avion)

        for b in [btn_up, btn_dn, btn_speed_up, btn_speed_down, btn_cap_plus, btn_cap_minus, btn_land]:
            a_layout.addWidget(b)

        actions.setLayout(a_layout)
        right.addWidget(actions)

        layout.addLayout(left, 1)
        layout.addWidget(self.radar, 3)
        layout.addLayout(right, 1)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_timers(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.move_planes)
        self.timer.start(800)
        self.spawn_timer = QTimer()
        self.spawn_timer.timeout.connect(self.spawn_plane)
        self.spawn_timer.start(5000)

    # --- Génération d'avions ---
    def spawn_plane(self):
        letters = ''.join(random.choices(string.ascii_uppercase, k=2))
        digits = ''.join(random.choices(string.digits, k=3))
        ident = letters + digits

        angle = random.uniform(0, 360)
        distance = 8
        xa = distance * math.cos(math.radians(angle))
        ya = distance * math.sin(math.radians(angle))
        vitesse = random.randint(300, 750)
        cap = random.randint(0, 360)
        altitude = random.randint(2000, 9000)

        urgence = random.random() < 0.3
        a = Avion(ident, vitesse, cap, altitude, xa, ya, urgence)
        self.sim.espace.avions.append(a)
        self.total_generated += 1
        self.label_avions.setText(f"Avions générés: {self.total_generated}")
        self.liste_avions.addItem(ident)
        self.radar.update_positions(self.sim.espace.avions, self.selected_identifiant)

    # --- Déplacement et gestion ---
    def move_planes(self):
        dt = 5
        now = time.time()

        for a in self.sim.espace.avions[:]:
            # Déplacement
            a.move(dt)

            # Urgences
            if a.urgence and (now - a.spawn_time) > 10:
                self.sim.espace.avions.remove(a)
                self.crash_count += 1
                self.score -= 50
                self.label_crash.setText(f"Crashs: {self.crash_count}")
                self.label_score.setText(f"Score: {self.score}")
                if self.selected_identifiant == a.identifiant:
                    self.selected_identifiant = None
                continue

            # Hors radar, vitesse trop basse, altitude <= 0
            if self.radar.is_outside(a) or a.vitesse < 200 or a.altitude <= 0:
                self.sim.espace.avions.remove(a)
                self.score -= 20
                self.label_score.setText(f"Score: {self.score}")
                if self.selected_identifiant == a.identifiant:
                    self.selected_identifiant = None

        self.radar.update_positions(self.sim.espace.avions, self.selected_identifiant)
        self.update_selected_info()

    # --- Sélection d'avion ---
    def select_plane(self, item):
        self.selected_identifiant = item.text()
        self.update_selected_info()
        self.radar.update_positions(self.sim.espace.avions, self.selected_identifiant)

    def select_plane_by_id(self, ident):
        self.selected_identifiant = ident
        self.update_selected_info()
        self.radar.update_positions(self.sim.espace.avions, self.selected_identifiant)

    def update_selected_info(self):
        ident = self.selected_identifiant
        if ident:
            for a in self.sim.espace.avions:
                if a.identifiant == ident:
                    self.label_selected.setText(
                        f"Avion: {a.identifiant}\n"
                        f"Altitude: {a.altitude} ft\n"
                        f"Vitesse: {a.vitesse} km/h\n"
                        f"Cap: {a.cap}°\n"
                        f"Urgence: {'Oui' if a.urgence else 'Non'}\n"
                        f"Position: ({a.xa:.2f}, {a.ya:.2f})"
                    )
                    break
        else:
            self.label_selected.setText("Sélectionné : Aucun")

    # --- Contrôles ---
    def monter_avion(self): self.changer_altitude(1000)
    def descendre_avion(self): self.changer_altitude(-1000)
    def accelerer_avion(self): self.changer_vitesse(50)
    def ralentir_avion(self): self.changer_vitesse(-50)
    def changer_cap(self, delta):
        ident = self.selected_identifiant
        if ident:
            for a in self.sim.espace.avions:
                if a.identifiant == ident:
                    a.changement_cap(delta)
                    break
        self.update_selected_info()
        self.radar.update_positions(self.sim.espace.avions, self.selected_identifiant)
    def changer_altitude(self, delta):
        ident = self.selected_identifiant
        if ident:
            for a in self.sim.espace.avions:
                if a.identifiant == ident:
                    a.changement_altitude(delta)
                    break
        self.update_selected_info()
        self.radar.update_positions(self.sim.espace.avions, self.selected_identifiant)
    def changer_vitesse(self, delta):
        ident = self.selected_identifiant
        if ident:
            for a in self.sim.espace.avions:
                if a.identifiant == ident:
                    a.changement_vitesse(delta)
                    break
        self.update_selected_info()
        self.radar.update_positions(self.sim.espace.avions, self.selected_identifiant)

    # --- Atterrissage ---
    def atterrir_avion(self):
        ident = self.selected_identifiant
        if ident:
            for a in self.sim.espace.avions[:]:
                if a.identifiant == ident:
                    if a.atterrir(center_x=0, center_y=0, distance_max=10, altitude_max=2000):
                        self.sim.espace.avions.remove(a)
                        self.score += 100
                        self.label_score.setText(f"Score: {self.score}")
                        self.selected_identifiant = None
                    break
        self.radar.update_positions(self.sim.espace.avions, self.selected_identifiant)

# --- Programme principal ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.showMaximized()
    sys.exit(app.exec())



























