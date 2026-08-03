import json

class SoundBank:
    def __init__(self, filename):
        with open(filename, "r") as file:
            self.data = json.load(file) #self.data becomes a dictionary that carries the data from the file
            
    def get_sound(self, pad):
        return self.data["pads"][str(pad)]