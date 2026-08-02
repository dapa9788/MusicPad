import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout

class MusicPad(QWidget):
    def __init__(self):
        super().__init__() #initializes QWidget

        self.setWindowTitle("Music Pad")
        self.adjustSize()

        layout = QGridLayout()
        layout.setSpacing(3)
        layout.setContentsMargins(10, 10, 10, 10)

        for row in range(4):
            for col in range(4):
                pad_number = row * 4 + col + 1

                button = QPushButton(str(pad_number))
                button.setFixedSize(90, 90)
                button.clicked.connect(
                    lambda checked, num=pad_number: self.pad_pressed(num)
                )

                layout.addWidget(button, row, col)

        self.setLayout(layout)

    def pad_pressed(self, number):
        print(f"Pad {number} pressed")

app = QApplication(sys.argv) #QApplication is my entire applicaiton
window = MusicPad() #QUI object
window.setWindowTitle("Music Pad")

window.show() #Open the window

sys.exit(app.exec())