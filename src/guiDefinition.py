import assets_rc_rc
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QGridLayout,
    QWidget,
    QStackedWidget,
    QGraphicsOpacityEffect
)

class WelcomePage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupPage()

    def setupPage(self):
        self.setObjectName("welcomePage")
        self._pageGraphic = self.setupPageGraphic(self)
        self._deviceName, self._softwareVersion = self.getDeviceDetails(self)
        self.retranslate()

    def setupPageGraphic(self, pageWidget: QWidget) -> QLabel:
        pageGraphic = QLabel(pageWidget)
        pageGraphic.setGeometry(QtCore.QRect(300, 70, 200, 200))
        pageGraphic.setStyleSheet("border-image: url(:/newPrefix/image_1.png);")
        pageGraphic.setText("")
        pageGraphic.setObjectName("welcomePageGraphic")
        return pageGraphic

    def getDeviceDetails(self, pageWidget: QWidget) -> tuple[QLabel, QLabel]:
        deviceFont = QtGui.QFont()
        deviceFont.setPointSize(20)
        deviceName = QLabel(pageWidget)
        deviceName.setGeometry(QtCore.QRect(300, 280, 201, 51))
        deviceName.setFont(deviceFont)
        deviceName.setStyleSheet("color: black;\n"
                                 "border-image:none;")
        deviceName.setAlignment(QtCore.Qt.AlignCenter)
        deviceName.setObjectName("deviceName")

        softwareFont = QtGui.QFont()
        softwareFont.setPointSize(16)
        softwareVersion = QLabel(pageWidget)
        softwareVersion.setGeometry(QtCore.QRect(300, 280, 201, 51))
        softwareVersion.setFont(softwareFont)
        softwareVersion.setStyleSheet("color: black;\n"
                                      "border-image:none;")
        softwareVersion.setAlignment(QtCore.Qt.AlignCenter)
        softwareVersion.setObjectName("softwareVersion")
        return (deviceName, softwareVersion)

    def retranslate(self):
        _translate = QtCore.QCoreApplication.translate
        self._deviceName.setText(_translate("MainWindow", "Device"))
        self._softwareVersion.setText(_translate("MainWindow", "Software Version 1.2.1"))



class GUIComponents(object):

    def __init__(self, mainWindow: QMainWindow):
        self._mainWindow = mainWindow
        self.setupUI()
        self.retranslate(self._mainWindow, self._pagesList)
        self.stackedWidget.setCurrentIndex(0)

    def setupUI(self):
        self._centralWidget, self._centralWidgetLayout = self.constructCentralWidget()
        self.modifyMainWindowAttributes(self._mainWindow, self._centralWidget)
        self._pagesList = self.constructPages()
        self.stackedWidget = self.constructStackedWidget(self._centralWidget, self._centralWidgetLayout, self._pagesList)

    def constructCentralWidget(self) -> tuple[QWidget, QGridLayout]:
        centralWidget = QWidget()
        centralWidget.setObjectName("centralWidget")
        gridLayout = QGridLayout(centralWidget)
        gridLayout.setContentsMargins(0, 0, 0, 0)
        gridLayout.setSpacing(0)
        gridLayout.setObjectName("centralWidgetGridLayout")
        return (centralWidget, gridLayout)

    def modifyMainWindowAttributes(self, mainWindow: QMainWindow, centralWidget: QWidget):
        mainWindow.resize(800, 400)
        mainWindow.setCentralWidget(centralWidget)
        mainWindow.setObjectName("mainWindow")
        mainWindow.setWindowTitle("Functionless Example GUI")
        # mainWindow.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        # mainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def constructPages(self) -> list[QWidget]:
        pages = list()
        pages.append(WelcomePage())
        # TODO add all pages
        return pages

    def constructStackedWidget(self, centralWidget: QWidget, gridLayout: QGridLayout, pages: list[QWidget]) -> QStackedWidget:
        stackedWidget = QStackedWidget(centralWidget)
        stackedWidget.setStyleSheet("background-color: white;")
        stackedWidget.setObjectName("stackedWidget")
        for page in pages:
            stackedWidget.addWidget(page)
        gridLayout.addWidget(stackedWidget, 0, 0, 1, 1)
        return stackedWidget

    def retranslate(self, mainWindow: QMainWindow, pages: list[QWidget]):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        for page in pages:
            page.retranslate()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = QMainWindow()
    gui = GUIComponents(win)
    win.show()
    sys.exit(app.exec_())
