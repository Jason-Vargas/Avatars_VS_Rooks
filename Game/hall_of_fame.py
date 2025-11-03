import json
import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
)
from PyQt6.QtCore import Qt


SCORES_FILE = "scores.json"
MAX_SCORES = 5


class HallOfFameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🏆 Hall of Fame")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()
        title = QLabel("🏅 Mejores Jugadores 🏅")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        # Tabla
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Jugador", "Puntaje", "Oleada"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        # Botón cerrar
        close_btn = QPushButton("Cerrar")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        self.setLayout(layout)
        self.load_scores()

    def load_scores(self):
        """Carga los puntajes del archivo"""
        if not os.path.exists(SCORES_FILE):
            return

        with open(SCORES_FILE, "r") as f:
            scores = json.load(f)

        # Ordenar por puntaje descendente
        scores.sort(key=lambda s: s["score"], reverse=True)
        self.table.setRowCount(len(scores))

        for i, s in enumerate(scores[:MAX_SCORES]):
            self.table.setItem(i, 0, QTableWidgetItem(s["name"]))
            self.table.setItem(i, 1, QTableWidgetItem(str(s["score"])))
            self.table.setItem(i, 2, QTableWidgetItem(str(s["wave"])))


def save_score(name, score, wave):
    """Guarda un nuevo puntaje en el archivo JSON"""
    scores = []

    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "r") as f:
            scores = json.load(f)

    scores.append({"name": name, "score": score, "wave": wave})
    scores.sort(key=lambda s: s["score"], reverse=True)
    scores = scores[:MAX_SCORES]

    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f, indent=4)
