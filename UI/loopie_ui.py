from PyQt6 import QtWidgets, uic
import sys
sys.path.append(".")

class LoopieUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/loopie.ui", self)
        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoopieUI()
    window.show()
    sys.exit(app.exec())