from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from hall_of_fame import save_score


class PlayerNameDialog(QDialog):
    def __init__(self, score, wave, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Guardar puntaje")
        self.setFixedSize(300, 200)
        self.score = score
        self.wave = wave

        layout = QVBoxLayout()
        label = QLabel(f"Tu puntaje: {score}\nOleada alcanzada: {wave}")
        layout.addWidget(label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ingresa tu nombre...")
        layout.addWidget(self.name_input)

        save_btn = QPushButton("Guardar")
        save_btn.clicked.connect(self.save)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def save(self):
        name = self.name_input.text().strip()
        if not name:
            name = "Anónimo"
        save_score(name, self.score, self.wave)
        self.accept()