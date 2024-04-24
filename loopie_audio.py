from PyQt6 import QtCore, QtWidgets
import sys
import numpy as np
import pyaudio
import time
import scipy
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
        self.volMult = 5
        self.distOn = False
        self.clipAmount = 100.0
        self.tremOn = False
        self.tremolo_rate = 3.33 
        self.tremolo_depth = 0.5
        self.delayOn = False
        self.delayTime = 0.5
        self.oldDelayTime = 0.5 
        self.delayBuffer = np.zeros(int(self.rate * (self.delayTime)))
        self.delayIndex = 0

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
            if self.oldDelayTime != self.delayTime:
                self.delayBuffer = np.zeros(int(self.rate * (self.delayTime)))
                self.delayIndex = 0
                self.oldDelayTime = self.delayTime
            data = self.stream_in.read(self.chunk_size, exception_on_overflow=False)
            input_array = np.frombuffer(data, dtype=np.int16) 
            if self.distOn:
                input_array = self.apply_distortion(input_array)
            if self.tremOn:
                input_array = self.apply_tremolo(input_array)
            if self.delayOn:
                input_array = self.apply_delay(input_array)
            input_array = input_array * self.volMult
            self.stream_out.write(input_array.astype(np.int16).tobytes())
        self.finished.emit()


    def stop(self):
        self.running = False
        self.stream_in.stop_stream()
        self.stream_in.close()
        self.stream_out.stop_stream()
        self.stream_out.close()
        
        
    ### EFFECTS
    
    def apply_distortion(self, input_array):
        distorted_array = np.clip(input_array, -self.clipAmount, self.clipAmount) 
        return distorted_array * self.volMult
    
    def apply_tremolo(self, input_array):
        t = np.linspace(time.time(), time.time() + len(input_array) / self.rate, len(input_array))
        envelope = (1 - self.tremolo_depth) + self.tremolo_depth * np.sin(2 * np.pi * self.tremolo_rate * t)
        return input_array * envelope
    
    def apply_delay(self, input_array):
        output_array = np.empty_like(input_array)
        for i in range(len(input_array)):
            delayed_sample = self.delayBuffer[self.delayIndex]
            self.delayBuffer[self.delayIndex] = input_array[i] + delayed_sample * 0.5  
            output_array[i] = input_array[i] + delayed_sample  
            self.delayIndex = (self.delayIndex + 1) % len(self.delayBuffer)
        return output_array


    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    p = pyaudio.PyAudio()
    a = AudioThread(p, 1, 3, 4, 44100)
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