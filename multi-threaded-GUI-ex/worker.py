import time
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class Worker(QObject):

    # define signals (must be defined as class attributes like done here)
    finished = pyqtSignal()
    progress = pyqtSignal(int, int)

    @pyqtSlot()
    def run(self):
        """Long-running task."""
        duration = 5
        for i in range(duration):
            time.sleep(1)
            self.progress.emit(i+1, duration)
        self.finished.emit()
