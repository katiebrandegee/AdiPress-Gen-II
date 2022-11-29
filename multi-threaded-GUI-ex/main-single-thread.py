import sys
import time
from guiComponents import GUIComponents
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow


class GUI(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.guiComponents = GUIComponents(self)
        self.setupUI()
        self.numClicks = 0

    def setupUI(self):
        self.setWindowTitle("Single-Threaded Example GUI")
        self.guiComponents.countBtn.clicked.connect(self.countClicks)
        self.guiComponents.longRunningBtn.clicked.connect(self.runLongTask)

    def reportProgress(self, n, duration):
        self.guiComponents.stepLabel.setText(f"Long-Running Step: {n}/{duration}")

    @pyqtSlot()
    def countClicks(self):
        self.numClicks += 1
        self.guiComponents.clicksLabel.setText(f"Counting: {self.numClicks} clicks")

    @pyqtSlot()
    def runLongTask(self):
        """Long-running task in 5 steps."""
        duration = 5
        for i in range(duration):
            time.sleep(1)
            self.reportProgress(i+1, duration)

app = QApplication(sys.argv)
gui = GUI()
gui.show()
sys.exit(app.exec())
