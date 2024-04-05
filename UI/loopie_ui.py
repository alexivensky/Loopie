from PyQt6 import QtWidgets, uic
import pyaudio
import sys
sys.path.append(".")

CHUNK_SIZE = 1024

class LoopieUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/loopie.ui", self)
        
        self.p = pyaudio.PyAudio()
        
        self.stream_in = self.p.open(format=pyaudio.paInt16,
                   channels=1,
                   rate=44100,
                   input=True,
                   frames_per_buffer=CHUNK_SIZE)
        self.stream_out = self.p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    output=True,
                    frames_per_buffer=CHUNK_SIZE)

        
        self.populateInputOutput()
        
    def populateInputOutput(self):
        for i in range(self.p.get_device_count()):
            device = self.p.get_device_info_by_index(i)
            if device['maxInputChannels']:
                self.deviceInputsCB.addItem(f"{device['name']}", i)
            if device['maxOutputChannels']:
                self.deviceOutputsCB.addItem(f"{device['name']}", i)
        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoopieUI()
    window.show()
    sys.exit(app.exec())