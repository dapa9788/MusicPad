import time

class Recorder:
    def __init__(self):
        self.recording = False
        self.event_timestamps = []
        self.start_time = 0
    def start(self):
        self.recording = True
        self.event_timestamps = []
        self.start_time = time.time()
    def stop(self):
        self.recording = False
    def recordcheck(self, pad):
        if (self.recording):
            timestamp = time.time() - self.start_time
            self.event_timestamps.append({"time": timestamp, "pad": pad})
            print(self.event_timestamps)
    def get_events(self):
        return self.event_timestamps
