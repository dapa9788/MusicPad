import sys
import pygame #sound audios
import os #filename stuff
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QFileDialog
from PySide6.QtCore import Qt, QTimer
from bank import SoundBank
from recorder import Recorder

class MusicPad(QWidget):
    def __init__(self):
        super().__init__() #initializes QWidget
        self.bank = SoundBank("banks/default.json")
        self.selected_pad = None
        self.buttons = {}
        self.recorder = Recorder()
        self.is_playing = False #for looping


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
                    name = os.path.splitext(os.path.basename(sound))[0] # fix filename
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
        record_button = QPushButton("Record")
        record_button.clicked.connect(self.start_recording)
        play_button = QPushButton("Play")
        play_button.clicked.connect(self.play_recording)
        stop_button = QPushButton("Stop")
        stop_button.clicked.connect(self.stop_recording)

        layout.addWidget(record_button, 5, 0)
        layout.addWidget(play_button, 5, 1, 1, 2)  # spans two columns
        layout.addWidget(stop_button, 5, 3)

        layout.addWidget(change_button, 4, 0, 1, 4)

    def pad_pressed(self, number):
        self.selected_pad = number
        self.recorder.recordcheck(number)
        sound = self.bank.get_sound(number)
        if sound:
            pygame.mixer.Sound(sound).play()
        #print(sound)

    def play_pad(self, number):
        self.selected_pad = number
        sound = self.bank.get_sound(number)
        if sound:
            pygame.mixer.Sound(sound).play()

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
    def start_recording(self):
        self.recorder.start()
        print("Started Recording:")
    

    def stop_recording(self):
        self.recorder.stop()
        self.is_playing = False
        #print("Stopped Recording:")

    def play_recording(self):
        print("Playing..." + str(self.recorder.get_events()))
        if self.recorder.recording:
            self.recorder.stop()
        self.is_playing = True
        events = self.recorder.get_events()
        for event in events:
            QTimer.singleShot(int(event["time"]*1000), lambda pad=event["pad"]: self.play_pad(pad))
        if events:
            loop_time = int(self.recorder.get_loop_time()*1000)
            print(loop_time)

            QTimer.singleShot(loop_time,lambda: self.play_recording() if self.is_playing else None)
            

app = QApplication(sys.argv) #QApplication is my entire applicaiton
pygame.mixer.init()
pygame.mixer.set_num_channels(64)
window = MusicPad() #QUI object

window.show() #Open the window

sys.exit(app.exec())