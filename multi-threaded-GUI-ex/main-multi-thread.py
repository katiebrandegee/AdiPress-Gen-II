import sys
from worker import Worker
from guiComponents import GUIComponents
from PyQt5.QtCore import QThread, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow


class GUI(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.guiComponents = GUIComponents(self)
        self.setupUI()
        self.numClicks = 0

    def setupUI(self):
        self.setWindowTitle("Multi-Threaded Example GUI")
        self.guiComponents.countBtn.clicked.connect(self.countClicks)
        self.guiComponents.longRunningBtn.clicked.connect(self.runLongTask)

    @pyqtSlot(int, int)
    def reportProgress(self, n, duration):
        self.guiComponents.stepLabel.setText(f"Long-Running Step: {n}/{duration}")

    @pyqtSlot()
    def countClicks(self):
        self.numClicks += 1
        self.guiComponents.clicksLabel.setText(f"Counting: {self.numClicks} clicks")

    @pyqtSlot()
    def runLongTask(self):
        """Long-running task in 5 steps."""
        
        # disable button that starts long-running task
        self.guiComponents.longRunningBtn.setEnabled(False)

        # create worker on new thread
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        # connect signals and slots related to startUp/cleanUp of worker and thread
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(lambda: self.guiComponents.longRunningBtn.setEnabled(True))
        self.thread.finished.connect(lambda: self.guiComponents.stepLabel.setText(f"Long-Running Step: 0/0"))

        # connect signals and slots related to exchange of data between threads
        self.worker.progress.connect(self.reportProgress)

        # start worker task on new thread
        self.thread.start()

app = QApplication(sys.argv)
gui = GUI()
gui.show()
sys.exit(app.exec_())
