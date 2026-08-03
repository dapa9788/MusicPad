import sys
import pygame #sound audios
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout
from bank import SoundBank

class MusicPad(QWidget):
    def __init__(self):
        super().__init__() #initializes QWidget
        self.bank = SoundBank("banks/default.json")


        self.setWindowTitle("Music Pad")
        self.adjustSize()

        layout = QGridLayout()
        layout.setSpacing(3)
        layout.setContentsMargins(10, 10, 10, 10)

        for row in range(4):
            for col in range(4):
                pad_number = row * 4 + col + 1
                sound = self.bank.get_sound(pad_number)
                if sound:
                    button = QPushButton(sound)
                else:
                    button = QPushButton("[empty]")
                button.setFixedSize(90, 90)
                button.clicked.connect(
                    lambda checked, num=pad_number: self.pad_pressed(num)
                )

                layout.addWidget(button, row, col)

        self.setLayout(layout)

    def pad_pressed(self, number):
        sound = self.bank.get_sound(number)
        if sound:
            pygame.mixer.Sound(sound).play()
        #print(sound)

app = QApplication(sys.argv) #QApplication is my entire applicaiton
pygame.mixer.init()
window = MusicPad() #QUI object

window.show() #Open the window

sys.exit(app.exec())