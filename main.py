import sys
import pygame #sound audios
import os #filename stuff
import time
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QFileDialog, QSpinBox
from PySide6.QtCore import Qt, QTimer
from bank import SoundBank
from recorder import Recorder
from pad import Pad

class MusicPad(QWidget):
    def __init__(self):
        super().__init__() #initializes QWidget
        self.bank = SoundBank("banks/default.json")
        self.selected_pad = None
        self.pads = {}
        self.recorder = Recorder()
        self.is_playing = False #for looping
        self.bpm = 145
        self.song_start = 0
        self.loop_number = 0
        self.last_loop_time = None


        self.setWindowTitle("Music Pad")
        self.adjustSize()

        layout = QGridLayout()
        layout.setSpacing(3)
        layout.setContentsMargins(10, 10, 10, 10)
        change_button = QPushButton("Change Pad Sound")
        change_button.pressed.connect(self.change_sound)
        record_button = QPushButton("Record")
        record_button.pressed.connect(self.start_recording)
        play_button = QPushButton("Play")
        play_button.pressed.connect(self.play_recording)
        stop_button = QPushButton("Stop")
        stop_button.pressed.connect(self.stop_recording)
        library_button = QPushButton("Sound Library")
        library_button.pressed.connect(self.open_sound_library)

        bpm_input = QSpinBox()
        bpm_input.setRange(40, 300)
        bpm_input.setValue(self.bpm)

        bpm_button = QPushButton("Set BPM")
        bpm_button.pressed.connect(lambda: self.change_bpm(bpm_input.value()))

        layout.addWidget(record_button, 6, 0)
        layout.addWidget(play_button, 6, 1, 1, 2)  # spans two columns
        layout.addWidget(stop_button, 6, 3)
        layout.addWidget(bpm_input, 0, 1)
        layout.addWidget(bpm_button, 0, 2)
        layout.addWidget(library_button, 5, 0, 1, 2)
        layout.addWidget(change_button, 5, 2, 1, 2)

        for row in range(4):
            for col in range(4):
                pad_number = row * 4 + col + 1
                sound = self.bank.get_sound(pad_number)
                if sound:
                    name = os.path.splitext(os.path.basename(sound))[0] # fix filename
                    button = QPushButton(name)
                else:
                    button = QPushButton("[empty]")
                self.pads[pad_number] = Pad(pad_number, sound, button)
                button.setFixedSize(90, 90)
                button.pressed.connect(
                    lambda num=pad_number: self.pad_pressed(num)
                )

                layout.addWidget(button, row+1, col)

        self.setLayout(layout)


    def pad_pressed(self, number):
        self.selected_pad = number
        self.recorder.recordcheck(number, self.bpm)
        self.pads[number].play()
        #print(sound)

    def play_pad(self, number):
        self.selected_pad = number
        sound = self.bank.get_sound(number)
        self.pads[number].play()

    def change_sound(self):
        if self.selected_pad is None:
            print("Select a pad first.")
            return
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Choose Sound",
            "sounds",
            "Audio Files (*.wav)"
        )

        if file:
            self.bank.set_sound(self.selected_pad, file)
            name = os.path.splitext(os.path.basename(file))[0] #fix the text of the button
            self.pads[self.selected_pad].set_sound(file)
            #print("Done.")
    def start_recording(self):
        self.recorder.start()
        print("Started Recording:")
    

    def stop_recording(self):
        self.recorder.stop(self.bpm)
        self.is_playing = False
        #print("Stopped Recording:")

    def play_recording(self):
        start = time.perf_counter()
        print("play_recording started:", start)
        if self.recorder.recording:
            self.recorder.stop(self.bpm)
        self.is_playing = True
        events = self.recorder.get_events()
        self.loop_number = 0
        self.song_start = time.perf_counter()
        for event in events:
            QTimer.singleShot(round(event["time"] * 1000), lambda pad=event["pad"]: self.play_pad(pad))
            print("Scheduled note after:", time.perf_counter() - self.song_start)
        self.play_loop() #hardcoded fix later
        print("Total play_recording overhead:", time.perf_counter() - start)

    def change_bpm(self, bpm):
        self.bpm = bpm
        print("Changed BPM")

    def play_loop(self): #Created scheduled timings so that if delay, next loop will compensate
        if not self.is_playing:
            return
        for event in self.recorder.get_events():
            QTimer.singleShot(int(event["time"] * 1000), lambda pad=event["pad"]: self.play_pad(pad))
        self.loop_number += 1
        loop_length = self.recorder.get_loop_time()
        target = self.song_start + self.loop_number * loop_length
        delay = max(0, target - time.perf_counter())
        QTimer.singleShot(int(delay * 1000), self.play_loop)

    def open_sound_library(self):
        self.sound_library = QWidget()
        self.sound_library.setWindowTitle("Sound Library")
        self.sound_library.setFixedSize(500, 400)

        layout = QGridLayout()

        sounds = self.get_all_sounds()

        categories = {}

        for category, sound in sounds:
            if category not in categories:
                categories[category] = []
            categories[category].append(sound)

        row = 0

        for category, category_sounds in categories.items():
            category_label = QPushButton(category)
            category_label.setEnabled(False)
            layout.addWidget(category_label, row, 0, 1, 3)
            row += 1

            for index, sound in enumerate(category_sounds):
                name = os.path.splitext(os.path.basename(sound))[0]

                button = QPushButton(f"▶ {name}")
                button.pressed.connect(
                    lambda sound=sound: self.preview_sound(sound)
                )

                col = index % 3

                layout.addWidget(button, row, col)

                if col == 2:
                    row += 1

            if len(category_sounds) % 3 != 0:
                row += 1

        self.sound_library.setLayout(layout)
        self.sound_library.show()

    def preview_sound(self, sound):
        pygame.mixer.Sound(sound).play()

    def get_all_sounds(self):
        sounds = []

        for category in os.listdir("sounds"):
            category_path = os.path.join("sounds", category)

            if os.path.isdir(category_path):
                for filename in os.listdir(category_path):
                    if filename.lower().endswith(".wav"):
                        filepath = os.path.join(category_path, filename)
                        sounds.append((category, filepath))

        return sounds

app = QApplication(sys.argv) #QApplication is my entire applicaiton
pygame.mixer.init()
pygame.mixer.set_num_channels(64)
window = MusicPad() #QUI object

window.show() #Open the window

sys.exit(app.exec())