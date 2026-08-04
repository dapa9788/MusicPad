import sys
import pygame #sound audios
import os #filename stuff
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QFileDialog
from PySide6.QtCore import Qt
from bank import SoundBank

class MusicPad(QWidget):
    def __init__(self):
        super().__init__() #initializes QWidget
        self.bank = SoundBank("banks/default.json")
        self.selected_pad = None
        self.buttons = {}


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
                    name = os.path.splitext(os.path.basename(sound))[0]
                    button = QPushButton(name)
                else:
                    button = QPushButton("[empty]")
                self.buttons[pad_number] = button
                button.setFixedSize(90, 90)
                button.clicked.connect(
                    lambda checked, num=pad_number: self.pad_pressed(num)
                )

                layout.addWidget(button, row, col)

        self.setLayout(layout)
        change_button = QPushButton("Change Pad Sound")
        change_button.clicked.connect(self.change_sound)

        layout.addWidget(change_button, 4, 0, 1, 4)

    def pad_pressed(self, number):
        self.selected_pad = number
        sound = self.bank.get_sound(number)
        if sound:
            pygame.mixer.Sound(sound).play()
        #print(sound)

    def change_sound(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Choose Sound",
            "sounds",
            "Audio Files (*.wav)"
        )

        if file:
            self.bank.set_sound(self.selected_pad, file)
            name = os.path.splitext(os.path.basename(file))[0] #fix the text of the button
            self.buttons[self.selected_pad].setText(name)
            #print("Done.")


app = QApplication(sys.argv) #QApplication is my entire applicaiton
pygame.mixer.init()
pygame.mixer.set_num_channels(64)
window = MusicPad() #QUI object

window.show() #Open the window

sys.exit(app.exec())