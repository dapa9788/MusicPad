import time

class Recorder:
    def __init__(self):
        self.recording = False
        self.event_timestamps = []
        self.start_time = 0
        self.first_note_time = None
        self.loop_length = 0
    def start(self):
        self.recording = True
        self.event_timestamps = []
        self.first_note_time = None
        self.loop_length = 0
    def stop(self, bpm):
        self.recording = False
        if self.first_note_time is not None:
            raw_length = time.time() - self.first_note_time

            beat = 60 / bpm
            grid = beat / 4   # sixteenth notes
            self.loop_length = round(raw_length / grid) * grid
    def recordcheck(self, pad, bpm):
        if (self.recording):
            now = time.time()
            if self.first_note_time is None:
                self.first_note_time = now
            timestamp = now - self.first_note_time
            seconds_per_beat = 60/bpm
            beat = seconds_per_beat/4
            timestamp = round(timestamp/beat) * beat
            self.event_timestamps.append({"time": timestamp, "pad": pad})
            print(self.event_timestamps)
    def get_events(self):
        return self.event_timestamps
    def get_loop_time(self):
        return self.loop_length
