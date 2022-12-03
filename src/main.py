import sys
# from GUIDefinition import GUIComponents, GUITransitions
from configparser import ConfigParser
from PyQt5.QtCore import QTimer, QThread, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow


class GUI(QMainWindow):

    _iterateFreqHz = 1
    _configFile = "config.ini"

    _stateWelcome = "welcome"
    _stateHome = "home"
    _stateSettings = "settings"
    _stateCompression = "compression"
    _states = (_stateWelcome, _stateHome, _stateSettings, _stateCompression)

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.guiComponents = GUIComponents(self)
        # self.guiTransitions = GUITransitions(self)
        self.parseConfig()
        
        self.iterateTimer = QTimer(self)
        self.setupConnections()

        self.stateFns = {self._stateWelcome: self.stateWelcomeFn, self._stateHome: self.stateHomeFn}

        self.iterateLoops = 0
        self.state = self._stateWelcome
        self.iterateTimer.start(1000.0/self._iterateFreqHz)

    def parseConfig(self):
        self.parsedConfig = ConfigParser()
        self.parsedConfig.read(self._configFile)
        self.parsedConfig = {section: dict(self.parsedConfig.items(section)) for section in self.parsedConfig.sections()}
        print(f"state machine freq: {self.parsedConfig['StateMachine']['iteratefreqhz']}")
        for s in self.parsedConfig.keys():
            print(f'\nsection: {s}')
            for key in self.parsedConfig[s]:
                print(f'key: {key} value: {self.parsedConfig[s][key]}')
        # # TODO debug remove
        # print(self.parsedConfig.sections())
        # for section in self.parsedConfig.sections():
        #     print(f'\nsection: {section}')
        #     for key in self.parsedConfig[section]:
        #         print(f'key: {key} value: {self.parsedConfig[section][key]}')

    def setupConnections(self):
        self.iterateTimer.timeout.connect(self.iterate)

    def stateWelcomeFn(self):
        print('welcome fn')

    def stateHomeFn(self):
        print('home fn')

    def iterate(self):
        self.iterateLoops += 1
        print(' ')
        print(self.state)
        if (self.state in self.stateFns.keys()):
            self.stateFns[self.state]()
        else:
            print('false')
        self.state = self._stateSettings
        print(self.iterateLoops)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
