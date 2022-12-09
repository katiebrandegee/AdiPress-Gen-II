from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget 
)


class GUIComponents(object):
    
    def __init__(self, mainWindow: QMainWindow):

        self.mainWindow = mainWindow
        self.setupUI()

    def setupUI(self):
        
        # modify attributes of mainWindow
        self.mainWindow.setWindowTitle("Functionless Example GUI")
        self.mainWindow.resize(400, 150)
        self.centralWidget = QWidget()
        self.mainWindow.setCentralWidget(self.centralWidget)
        
        # create child widgets of mainWindow's centralWidget
        self.clicksLabel = QLabel("Counting: 0 clicks", self.centralWidget)
        self.clicksLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.stepLabel = QLabel("Long-Running Step: 0/0")
        self.stepLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.countBtn = QPushButton("Click me!", self.centralWidget)
        self.longRunningBtn = QPushButton("Long-Running Task!", self.centralWidget)

        # set the layout of mainWindow's centralWidget
        layout = QVBoxLayout()
        layout.addWidget(self.clicksLabel)
        layout.addWidget(self.countBtn)
        layout.addStretch()
        layout.addWidget(self.stepLabel)
        layout.addWidget(self.longRunningBtn)
        self.centralWidget.setLayout(layout)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = QMainWindow()
    gui = GUIComponents(win)
    win.show()
    sys.exit(app.exec_())
