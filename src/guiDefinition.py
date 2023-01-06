import assets_rc
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

class Page(QWidget):

    _configFileSectionName = 'GuiPages'

    def __init__(self, parsedConfig: dict[str, dict[str, str]], *, parent=None):
        super().__init__(parent=parent)
        self._parsedConfig = parsedConfig
        self.readRelevantStateConfigVars(self._parsedConfig)

    @property
    def name(self):
        return 'null'

    def setupPage(self):
        pass

    # only function that "magically" adds instance vars (i.e. class member vars)
    # only hard-coded section, var names (e.g. iteratefreqhz) must match lower case keys in config.ini 
    def readRelevantStateConfigVars(self, parsedConfig: dict[str, dict[str, str]]):
        configFile = parsedConfig['CONFIG_FILE_NAME'] if 'CONFIG_FILE_NAME' in parsedConfig else 'config file'
        if (self._configFileSectionName not in parsedConfig):
            raise Exception(f"'{self._configFileSectionName}' section not found in {configFile}...")
        try:
            # add any other configurable parameters here
            self._deviceName = parsedConfig[self._configFileSectionName]['devicename']
            self._softwareVersion = parsedConfig[self._configFileSectionName]['softwareversion']
        except:
            raise Exception(f"All required configurable parameters were not found under the '{self._configFileSectionName}' or 'DEFAULT' sections in {configFile}...")



class WelcomePage(Page):

    def __init__(self, parsedConfig: dict[str, dict[str, str]], *, parent=None):
        super().__init__(parsedConfig, parent=parent)
        self.setupPage()

    def setupPage(self):
        self.setObjectName("welcomePage")
        self._pageGraphic = self.setupPageGraphic(self)
        self._deviceNameLabel, self._softwareVersionLabel = self.getDeviceDetails(self)
        self.retranslate()

    def setupPageGraphic(self, pageWidget: QWidget) -> QLabel:
        pageGraphic = QLabel(pageWidget)
        pageGraphic.setGeometry(QtCore.QRect(0, 0, 800, 480))
        pageGraphic.setStyleSheet("border-image: url(:/newPrefix/WelcomeScreen.jpg);")
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
        softwareVersion.setGeometry(QtCore.QRect(300, 320, 201, 51))
        softwareVersion.setFont(softwareFont)
        softwareVersion.setStyleSheet("color: black;\n"
                                      "border-image:none;")
        softwareVersion.setAlignment(QtCore.Qt.AlignCenter)
        softwareVersion.setObjectName("softwareVersion")
        return (deviceName, softwareVersion)

    def retranslate(self):
        _translate = QtCore.QCoreApplication.translate
        self._deviceNameLabel.setText(_translate("MainWindow", self._deviceName))
        self._softwareVersionLabel.setText(_translate("MainWindow", self._softwareVersion))
        # TODO maybe just remove these labels entirely
        self._deviceNameLabel.setVisible(False)
        self._softwareVersionLabel.setVisible(False)


class GUIComponents(object):

    def __init__(self, parsedConfig: dict[str, dict[str, str]], mainWindow: QMainWindow):
        self._mainWindow = mainWindow
        self._parsedConfig = parsedConfig
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
        pages.append(WelcomePage(self._parsedConfig))
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


# TODO update with underscores as appropriate for instance variables
class GUITransitions(object):

    def __init__(self, parsedConfig: dict[str, dict[str, str]], mainWindow: QMainWindow, guiComponents: GUIComponents):
        self.mainWindow = mainWindow
        self.guiComponents = guiComponents
        self._parsedConfig = parsedConfig

    def swapPages(self, newPage: str, currPage: str=None):
        if ((currPage and currPage not in self.guiComponents.pages.keys()) or newPage not in self.guiComponents.pages.keys()):
            if (currPage):
                raise Exception(f"Either new page name '{newPage}' or current page name '{currPage}' not found in list of defined pages...")
            else:
                raise Exception(f"New page name '{newPage}' not found in list of defined pages...")

        newPage = self.guiComponents.pages[newPage]
        if (currPage):
            oldPage = self.guiComponents.pages[currPage]
            self.slidePageUpOut(oldPage)
            self.fade(oldPage)
        self.slidePageUpIn(newPage)
        self.guiComponents.stackedWidget.setCurrentWidget(newPage)

    def slidePageUpIn(self, widget: QWidget):
        self.unfade(widget)
        self.animIn = QtCore.QPropertyAnimation(widget, b"geometry")
        self.animIn.setDuration(500)
        self.animIn.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
        self.animIn.setStartValue(QtCore.QRect(0, 100, 800, 480))
        self.animIn.setEndValue(QtCore.QRect(0, 0, 800, 480))
        self.animIn.start()

    def slidePageUpOut(self, widget: QWidget):
        self.unfade(widget)
        self.animOut = QtCore.QPropertyAnimation(widget, b"geometry")
        self.animOut.setDuration(500)
        self.animOut.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
        self.animOut.setStartValue(QtCore.QRect(0, 0, 800, 480))
        self.animOut.setEndValue(QtCore.QRect(0, -100, 800, 480))
        self.animOut.start()

    def fade(self, widget: QWidget):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)
        self.animFade = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animFade.setDuration(500)
        self.animFade.setStartValue(1)
        self.animFade.setEndValue(0)
        self.animFade.start()

    def unfade(self, widget: QWidget):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)
        self.animUnfade = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animUnfade.setDuration(500)
        self.animUnfade.setStartValue(0)
        self.animUnfade.setEndValue(1)
        self.animUnfade.start()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = QMainWindow()
    gui = GUIComponents(win)
    win.show()
    sys.exit(app.exec_())
