from PyQt6 import QtWidgets, uic
import pyaudio
import sys
sys.path.append(".")

from loopie_audio import *

CHUNK_SIZE = 256
RATE = 44100

class LoopieUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/loopie.ui", self)
        
        # UI Signals
        self.deviceInputsCB.currentIndexChanged.connect(self.changeInputDevice)
        self.deviceOutputsCB.currentIndexChanged.connect(self.changeOutputDevice)
        self.onCheck.stateChanged.connect(self.toggleAudio)
        self.distBox.stateChanged.connect(self.toggleDistortion)
        
        self.p = pyaudio.PyAudio()
        
        self.inputIndex = 0
        self.outputIndex = 0
        
        self.stream_in = None
        self.stream_out = None
        
        self.audio_thread = None
        
        self.populateInputOutput()
        
        
        
    def populateInputOutput(self):
        for i in range(self.p.get_device_count()):
            device = self.p.get_device_info_by_index(i)
            if device['maxInputChannels']:
                self.deviceInputsCB.addItem(f"{device['name']}", i)
                if i == self.inputIndex: 
                    self.inputChannels = device['maxInputChannels']
            if device['maxOutputChannels']:
                self.deviceOutputsCB.addItem(f"{device['name']}", i)
                if i == self.outputIndex: 
                    self.outputChannels = device['maxOutputChannels']
                
    def changeInputDevice(self, index):
        self.inputIndex = self.deviceInputsCB.itemData(index)
        if self.stream_in is not None:
            self.stream_in.stop_stream()
            self.stream_in.close()
        self.stream_in = self.p.open(format=pyaudio.paInt16,
                                     channels=1,
                                     rate=RATE,
                                     input=True,
                                     input_device_index=self.inputIndex,
                                     frames_per_buffer=CHUNK_SIZE)
        if self.onCheck.isChecked():
            self.stream_in.start_stream()
    
    def changeOutputDevice(self, index):
        self.outputIndex = self.deviceOutputsCB.itemData(index)
        if self.stream_out is not None:
            self.stream_out.stop_stream()
            self.stream_out.close()
        self.stream_out = self.p.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=RATE,
                                      output=True,
                                      output_device_index=self.outputIndex,
                                      frames_per_buffer=CHUNK_SIZE)
        if self.onCheck.isChecked():
            self.stream_out.start_stream()
            
    def toggleAudio(self, value):
        if (value):
            self.audio_thread = AudioThread(self.p, self.inputIndex, self.outputIndex, CHUNK_SIZE, RATE)
            self.audio_thread.start()
        else:
            self.audio_thread.stop()
            
    def toggleDistortion(self, value):
        if self.audio_thread is not None:
            self.audio_thread.distOn = value
    

        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoopieUI()
    window.show()
    sys.exit(app.exec())