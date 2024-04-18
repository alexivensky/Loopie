from PyQt6 import QtCore
import sys
import numpy as np
import pyaudio
sys.path.append(".")

class AudioThread(QtCore.QThread):
    def __init__(self, p, input_device_index, output_device_index, chunk_size, rate):
        super().__init__()
        self.p = p
        self.input_device_index = input_device_index
        self.output_device_index = output_device_index
        self.chunk_size = chunk_size
        self.rate = rate
        self.running = False

    def run(self):
        self.running = True
        self.stream_in = self.p.open(format=pyaudio.paInt16,
                                     channels=1,
                                     rate=self.rate,
                                     input=True,
                                     input_device_index=self.input_device_index,
                                     frames_per_buffer=self.chunk_size)
        self.stream_out = self.p.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=self.rate,
                                      output=True,
                                      output_device_index=self.output_device_index,
                                      frames_per_buffer=self.chunk_size)
        while self.running:
            data = self.stream_in.read(self.chunk_size, exception_on_overflow=False)
            self.stream_out.write(data)

    def stop(self):
        self.running = False
        self.stream_in.stop_stream()
        self.stream_in.close()
        self.stream_out.stop_stream()
        self.stream_out.close()
    