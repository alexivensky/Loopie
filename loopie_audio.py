from PyQt6 import QtCore
import sys
sys.path.append(".")

class AudioThread(QtCore.QThread):
    def __init__(self, stream_in, stream_out, chunk_size):
        super().__init__()
        self.stream_in = stream_in
        self.stream_out = stream_out
        self.chunk_size = chunk_size
        self.running = True

    def run(self):
        while self.running:
            data = self.stream_in.read(self.chunk_size)
            self.stream_out.write(data)
    
    def stop(self):
        self.running = False
    