import sys
# from guiDefinition import GUIComponents, GUITransitions
from uglyGuiDefinition import GUIComponents, GUITransitions
# from statemachine import StateMachine
from interrupthandler import InterruptHandler
from configparser import ConfigParser
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow

class GUI(QMainWindow):

    aboutToQuit = pyqtSignal()

    _configFile = 'config.ini'
    _threadNameStateMachine = 'StateMachine'
    _threadNameInterruptHandler = 'InterruptHandler'
    _additionalThreads = (_threadNameStateMachine, _threadNameInterruptHandler)

    _stateMachineExists = False
    _interruptHandlerExists = False

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parsedConfig = self.parseConfig()
        self._guiComponents = GUIComponents(self._parsedConfig, mainWindow=self)
        self._guiTransitions = GUITransitions(self._parsedConfig, mainWindow=self, guiComponents=self._guiComponents)

        self._otherThreads = self.constructThreads(self._additionalThreads)
        # self._machine = self.constructStateMachine()
        self._interruptHandler = self.constructInterruptHandler()
        self.setupConnections()

        # self.setupUI()
        # TODO --> potentially define function for all startup behavior including below
        self._otherThreads[self._threadNameStateMachine].start()
        self._otherThreads[self._threadNameInterruptHandler].start()

    def parseConfig(self) -> dict[str, dict[str, str]]:
        parsedConfig = ConfigParser()
        parsedConfig.read(self._configFile)
        parsedConfig = {section: dict(parsedConfig.items(section)) for section in parsedConfig.sections()}
        parsedConfig['CONFIG_FILE_NAME'] = self._configFile
        return parsedConfig

    def setupConnections(self):
        for thread in self._otherThreads.values():
            self.aboutToQuit.connect(thread.quit)
        
        if (self._stateMachineExists):
            self.aboutToQuit.connect(self._machine.receiveCloseEvent)
            self._machine.stateChangedSignal.connect(self.machineStateChanged)
        
        if (self._interruptHandlerExists):
            self.aboutToQuit.connect(self._interruptHandler.receiveCloseEvent)
            self._interruptHandler.emergencyStopSignal.connect(self.receiveEmergencyEvent)

        if (self._stateMachineExists and self._interruptHandlerExists):
            self._interruptHandler.emergencyStopSignal.connect(self._machine.receiveEmergencyEvent)

    @pyqtSlot(str, str)
    def machineStateChanged(self, newStateName: str, oldStateName: str):
        print(f"NEWSTATE: {newStateName}, OLDSTATE: {oldStateName}") # TODO remove
        self._guiTransitions.swapPages(newStateName, oldStateName)

    @pyqtSlot()
    def compressionStarted(self):
        oldStateName = "Compression"
        newStateName = "Compression2"
        print(f"NEWSTATE: {newStateName}, OLDSTATE: {oldStateName}") # TODO remove
        self._guiTransitions.swapPages(newStateName, oldStateName)
        
    @pyqtSlot(str, bool)
    def sampleSetupStatusChanged(self, sensorChecked: str, newCheckVal: bool):
        print(sensorChecked)
        newStyle = "border-radius: 10px;\nbackground-color: " + ("green;" if newCheckVal else "red;")
        if (sensorChecked == "plunger"):
            self._guiComponents.img_1_frame.setStyleSheet(newStyle)
        elif (sensorChecked == "compressionDrawer"):
            self._guiComponents.img_2_frame.setStyleSheet(newStyle)
        elif (sensorChecked == "filtrateDrawer"):
            self._guiComponents.img_3_frame.setStyleSheet(newStyle)
        elif (sensorChecked == "rfids"):
            self._guiComponents.img_4_frame.setStyleSheet(newStyle)

    def constructThreads(self, newThreadNames: tuple[str]) -> dict[str, QThread]:
        return {threadName: QThread() for threadName in newThreadNames}

    # def constructStateMachine(self) -> StateMachine:
    #     # TODO check if QThread object within _otherThreads dict is actually valid
    #     if (self._threadNameStateMachine not in self._otherThreads):
    #         raise Exception("Thread for state machine could not be found...")

    #     machine = StateMachine(self._parsedConfig, self)
    #     newThread = self._otherThreads[self._threadNameStateMachine]
    #     machine.moveToThread(newThread)

    #     # TODO move to setupConnections()
    #     newThread.started.connect(machine.run)
    #     newThread.finished.connect(newThread.deleteLater)
    #     newThread.finished.connect(machine.deleteLater)

    #     self._stateMachineExists = True
                
    #     return machine

    def constructInterruptHandler(self) -> InterruptHandler:
        # TODO check if QThread object within _otherThreads dict is actually valid
        if (self._threadNameInterruptHandler not in self._otherThreads):
            raise Exception("Thread for interrupt handler could not be found...")

        inthandler = InterruptHandler(self._parsedConfig, self)
        newThread = self._otherThreads[self._threadNameInterruptHandler]
        inthandler.moveToThread(newThread)

        # TODO move to setupConnections()
        newThread.started.connect(inthandler.run)
        newThread.finished.connect(newThread.deleteLater)
        newThread.finished.connect(inthandler.deleteLater)

        self._interruptHandlerExists = True

        return inthandler

    def closeEvent(self, event):
        print("closing") # TODO remove
        self.aboutToQuit.emit()
        # TODO ensure all threads finished and QObjects deleted

    @pyqtSlot()
    def receiveEmergencyEvent(self):
        print("emergency event received, closing") # TODO remove
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
    # print(gui._otherThreads)
    gui.show()
    sys.exit(app.exec_())

