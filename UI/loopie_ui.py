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
        self.tremBox.stateChanged.connect(self.toggleTremolo)
        
        self.p = pyaudio.PyAudio()
        
        self.inputIndex = 0
        self.outputIndex = 0
        
        self.audio_thread = None
        
        self.populateInputOutput()
        
        
        
    def populateInputOutput(self):
        for i in range(self.p.get_device_count()):
            device = self.p.get_device_info_by_index(i)
            if device['maxInputChannels']:
                self.deviceInputsCB.addItem(f"{device['name']}", i)
            if device['maxOutputChannels']:
                self.deviceOutputsCB.addItem(f"{device['name']}", i)
                
    def changeInputDevice(self, index):
        flag = 0
        if self.audio_thread is not None:
            if self.audio_thread.running:
                flag = 1
                self.audio_thread.stop()
        self.inputIndex = self.deviceInputsCB.itemData(index)
        self.audio_thread = AudioThread(self.p, self.inputIndex, self.outputIndex, CHUNK_SIZE, RATE)
        if flag:
            self.audio_thread.start()
    
    def changeOutputDevice(self, index):
        flag = 0
        if self.audio_thread is not None:
            if self.audio_thread.running:
                flag = 1
                self.audio_thread.stop()
        self.outputIndex = self.deviceOutputsCB.itemData(index)
        self.audio_thread = AudioThread(self.p, self.inputIndex, self.outputIndex, CHUNK_SIZE, RATE)
        if flag:
            self.audio_thread.start()
            
    def toggleAudio(self, value):
        if (value):
            self.audio_thread = AudioThread(self.p, self.inputIndex, self.outputIndex, CHUNK_SIZE, RATE)
            self.audio_thread.start()
        else:
            self.audio_thread.stop()
            
    def toggleDistortion(self, value):
        if self.audio_thread is not None:
            self.audio_thread.distOn = value
            
    def toggleTremolo(self, value):
        if self.audio_thread is not None:
            self.audio_thread.tremOn = value
    

        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoopieUI()
    window.show()
    sys.exit(app.exec())