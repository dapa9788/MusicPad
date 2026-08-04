import json

class SoundBank:
    def __init__(self, filename):
        self.filename = filename
        with open(filename, "r") as file:
            self.data = json.load(file) #self.data becomes a dictionary that carries the data from the file
            
    def get_sound(self, pad):
        return self.data["pads"][str(pad)]

    def set_sound(self, pad, filename):
        self.data["pads"][str(pad)] = filename
        with open(self.filename, "w") as file:
            json.dump(self.data, file, indent=4)
