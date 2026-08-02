import sys
from PySide6.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv) #QApplication is my entire applicaiton
window = QWidget() #QUI object
window.setWindowTitle("Music Pad")

window.show() #Open the window

sys.exit(app.exec())