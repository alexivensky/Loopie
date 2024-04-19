from PyQt6 import QtCore, QtWidgets
import sys
import numpy as np
import pyaudio
import time
sys.path.append(".")

class AudioThread(QtCore.QThread):
    finished = QtCore.pyqtSignal()
    def __init__(self, p, inputIndex, outputIndex, chunk_size, rate):
        super().__init__()
        self.p = p
        self.inputIndex = inputIndex
        self.outputIndex = outputIndex
        self.chunk_size = chunk_size
        self.rate = rate
        self.running = False

    def run(self):
        self.running = True
        self.stream_in = self.p.open(format=pyaudio.paInt16,
                                    channels=1,
                                    rate=self.rate,
                                    input=True,
                                    input_device_index=self.inputIndex,
                                    frames_per_buffer=self.chunk_size)
        self.stream_out = self.p.open(format=pyaudio.paInt16,
                                    channels=1,
                                    rate=self.rate,
                                    output=True,
                                    output_device_index=self.outputIndex,
                                    frames_per_buffer=self.chunk_size)
        while self.running:
            data = self.stream_in.read(self.chunk_size, exception_on_overflow=False)
            data = self.apply_distortion(data)
            self.stream_out.write(data)
        self.finished.emit()


    def stop(self):
        self.running = False
        self.stream_in.stop_stream()
        self.stream_in.close()
        self.stream_out.stop_stream()
        self.stream_out.close()
        
    ### EFFECTS
    
    def apply_distortion(self, input_data):
        input_array = np.frombuffer(input_data, dtype=np.int16)
        distorted_array = np.clip(input_array * 4, -2000.0, 2000.0)
        return distorted_array.astype(np.int16).tobytes()
        
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    p = pyaudio.PyAudio()
    a = AudioThread(p, 1, 3, 16, 44100)
    for i in range(p.get_device_count()):
            device = p.get_device_info_by_index(i)
            print(i, device['name'])
    a.start()
    print("hello!")
    time.sleep(5)
    print("it's been 5 seconds")
    time.sleep(5)
    a.stop()
    sys.exit(app.exec())