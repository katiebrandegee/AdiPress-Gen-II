import sys
# from GUIDefinition import GUIComponents, GUITransitions
from statemachine import StateMachine
from configparser import ConfigParser
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow

class GUI(QMainWindow):

    aboutToQuit = pyqtSignal()

    _configFile = "config.ini"
    _threadNameStateMachine = 'StateMachine'
    _threadNameInterruptHandler = 'InterruptHandler'
    _additionalThreads = (_threadNameStateMachine, _threadNameInterruptHandler)

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.guiComponents = GUIComponents(self)
        # self.guiTransitions = GUITransitions(self)
        self._parsedConfig = self.parseConfig()

        self._otherThreads = self.constructThreads(self._additionalThreads)
        self._machine = self.constructStateMachine()
        # self._interruptHandler = self.constructInterruptHandler()
        self.setupConnections()

        # self.setupUI()
        # TODO define function for all startup behavior including below
        self._otherThreads[self._threadNameStateMachine].start()
        # self._otherThreads[self._threadNameInterruptHandler].start()

    def parseConfig(self) -> dict[str, dict[str, str]]:
        parsedConfig = ConfigParser()
        parsedConfig.read(self._configFile)
        parsedConfig = {section: dict(parsedConfig.items(section)) for section in parsedConfig.sections()}
        parsedConfig['CONFIG_FILE_NAME'] = self._configFile
        return parsedConfig

    def setupConnections(self):
        # TODO
        for thread in self._otherThreads.values():
            self.aboutToQuit.connect(thread.quit)

    def constructThreads(self, newThreadNames: tuple[str]) -> dict[str, QThread]:
        return {threadName: QThread() for threadName in newThreadNames}

    def constructStateMachine(self) -> StateMachine:
        # TODO check if QThread object within _otherThreads dict is actually valid
        if (self._threadNameStateMachine not in self._otherThreads):
            raise Exception("Thread for state machine could not be found...")

        machine = StateMachine(self._parsedConfig, self)
        newThread = self._otherThreads[self._threadNameStateMachine]
        machine.moveToThread(newThread)

        # TODO move to setupConnections()
        newThread.started.connect(machine.run)
        newThread.finished.connect(newThread.deleteLater)
        newThread.finished.connect(machine.deleteLater)
                
        return machine

    def closeEvent(self, event):
        print("closing")
        self.aboutToQuit.emit()
        # TODO ensure all threads finished and QObjects deleted




if __name__ == "__main__":
    # actual code here:
    # app = QApplication(sys.argv)
    # gui = GUI()
    # gui.show()
    # sys.exit(app.exec_())

    # temporary code just for testing stuff (TODO remove all code below and uncomment above)
    app = QApplication(sys.argv)
    gui = GUI()
    parsedConfig = ConfigParser()
    # SM = StateMachine(parsedConfig=gui._parsedConfig, gui=gui)
    # print(SM._firstStateName)
    # print(SM._states)
    # print(SM._states['welcome'].name)
    # print(SM._states['welcome']._machine)
    # print(SM._states['welcome']._parsedConfig)
    # print(SM.getStateNames())
    # print(SM.getStates())
    print(gui._otherThreads)
    gui.show()
    sys.exit(app.exec_())

