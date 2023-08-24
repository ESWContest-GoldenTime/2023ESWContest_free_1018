from collections import deque

class VideoBuffer:
    def __init__(self, max_frames=300):
        self.frames = deque(maxlen=max_frames)

    def add_frame(self, frame):
        self.frames.append(frame)

    def get_all_frames(self):
        return list(self.frames)

    def clear(self):
        self.frames.clear()