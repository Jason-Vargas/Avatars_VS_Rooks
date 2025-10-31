from PyQt6.QtWidgets import QApplication, QLabel
import sys
print("[sanity] import ok")
app = QApplication(sys.argv)
print("[sanity] qapp ok")
lbl = QLabel("Hola, PyQt6 👋"); lbl.resize(240, 80); lbl.show()
print("[sanity] show ok")
sys.exit(app.exec())
