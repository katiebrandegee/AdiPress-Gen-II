from PyQt5.QtCore import QTimer, QObject, pyqtSignal, pyqtSlot

class State(QObject):

    _exitCondition = False
    _configFileSectionName = 'States'

    def __init__(self, parsedConfig: dict, stateMachine, *, parent=None):
        super().__init__(parent)
        self._machine = stateMachine
        self._parsedConfig = parsedConfig
        self.readRelevantConfigVars(self._parsedConfig)

    @property
    def name(self):
        return 'null'

    # only function that "magically" adds instance vars (i.e. class member vars)
    # only hard-coded section, var names (e.g. iteratefreqhz) must match lower case keys in config.ini 
    def readRelevantConfigVars(self, parsedConfig: dict):
        configFile = parsedConfig['CONFIG_FILE_NAME'] if 'CONFIG_FILE_NAME' in parsedConfig else 'config file'
        if (self._configFileSectionName not in parsedConfig):
            raise Exception(f"'{self._configFileSectionName}' section not found in {configFile}...")
        try:
            # TODO add any other configurable parameters here
            self._iterateFreqHz = parsedConfig[self._configFileSectionName]['iteratefreqhz']
        except:
            raise Exception(f"All required configurable parameters were not found under the '{self._configFileSectionName}' or 'DEFAULT' sections in {configFile}...")

    def run(self):
        pass

    def exit(self):
        pass
    

class WelcomeState(State):

    def __init__(self, parsedConfig: dict, stateMachine, *, parent=None):
        super().__init__(parsedConfig, stateMachine, parent=parent)
        self.readRelevantConfigVars(self._parsedConfig)
        self._sstimer = QTimer(self)
        self._sstimer.setSingleShot(True)
        self._sstimer.timeout.connect(self.timeout)

    @property
    def name(self):
        return 'welcome'

    def readRelevantConfigVars(self, parsedConfig: dict):
        configFile = parsedConfig['CONFIG_FILE_NAME'] if 'CONFIG_FILE_NAME' in parsedConfig else 'config file'
        if (self._configFileSectionName not in parsedConfig):
            raise Exception(f"'{self._configFileSectionName}' section not found in {configFile}...")
        try:
            # TODO add any other configurable parameters here
            self._sstimerDurationSec = parsedConfig[self._configFileSectionName]['welcomescreendurationsec']
        except:
            raise Exception(f"All required configurable parameters were not found under the '{self._configFileSectionName}' or 'DEFAULT' sections in {configFile}...")

    @pyqtSlot()
    def timeout(self):
        self._exitCondition = True

    def exit(self):
        self._machine.setCurrentState('home')
        self._sstimer.stop()
        print(f'{self.name} exiting...') # TODO remove, just for testing (also print() NOT thread-safe, use logging instead)

    def run(self):

        if (self._exitCondition):
            self.exit()
            return

        if (not self._sstimer.isActive()):
            print(f'\nstate: {self.name}') # TODO remove, just for testing (also print() NOT thread-safe, use logging instead)
            self._sstimer.start(round(float(self._sstimerDurationSec)*1000.0))
        

class HomeState(State):

    def __init__(self, parsedConfig: dict, stateMachine, *, parent=None):
        super().__init__(parsedConfig, stateMachine, parent=parent)
        self.plungerCheckPassed = False
        self.compressionDrawerCheckPassed = False
        self.filtrateDrawerCheckPassed = False

    @property
    def name(self):
        return 'home'

    def exit(self):
        print(f'{self.name} exiting...') # TODO remove, just for testing (also print() NOT thread-safe, use logging instead)

    def run(self):
        
        if (self._exitCondition):
            self.exit()
            return

        print(f'state: {self.name}')

