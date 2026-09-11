import pygame
import os

class Pad:
    def __init__(self, number, filename, button):
        self.number = number
        self.filename = filename
        self.button = button

        if filename:
            self.sound = pygame.mixer.Sound(filename)
        else:
            self.sound = None
    def play(self):
        if self.sound:
            self.sound.play()
    def set_sound(self, filename):
        self.filename = filename
        self.sound = pygame.mixer.Sound(filename)

        name = os.path.splitext(os.path.basename(filename))[0]
        self.button.setText(name)