from PyQt5.QtCore import QTimer, QObject, pyqtSignal, pyqtSlot

class State(QObject):

    _exitCondition = False
    _configFileSectionName = 'States'

    def __init__(self, parsedConfig: dict[str, dict[str, str]], stateMachine, *, parent=None):
        super().__init__(parent)
        self._machine = stateMachine
        self._parsedConfig = parsedConfig
        self.readRelevantStateConfigVars(self._parsedConfig)

    @property
    def name(self):
        return 'null'

    # only function that "magically" adds instance vars (i.e. class member vars)
    # only hard-coded section, var names (e.g. iteratefreqhz) must match lower case keys in config.ini 
    def readRelevantStateConfigVars(self, parsedConfig: dict[str, dict[str, str]]):
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

    def __init__(self, parsedConfig: dict[str, dict[str, str]], stateMachine, *, parent=None):
        super().__init__(parsedConfig, stateMachine, parent=parent)
        self.readRelevantConfigVars(self._parsedConfig)
        self._sstimer = QTimer(self)
        self._sstimer.setSingleShot(True)
        self._sstimer.timeout.connect(self.timeout)

    @property
    def name(self):
        return 'welcome'

    def readRelevantConfigVars(self, parsedConfig: dict[str, dict[str, str]]):
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
        # TODO fully delete/reset singleshot timer so WelcomeState doesn't immediately exit if jumped to again
        print(f'{self.name} exiting...') # TODO remove, just for testing (also print() NOT thread-safe, use logging instead)

    def run(self):

        if (self._exitCondition):
            self.exit()
            return

        if (not self._sstimer.isActive()):
            self._sstimer.start(round(float(self._sstimerDurationSec)*1000.0))
            print(f'\nstate: {self.name}') # TODO remove, just for testing (also print() NOT thread-safe, use logging instead)
        

class HomeState(State):

    # TODO: connect signals to gui in StateMachine.makeConnections() 
    plungerStatusChanged = pyqtSignal(bool)
    compressionDrawerStatusChanged = pyqtSignal(bool)
    filtrateDrawerStatusChanged = pyqtSignal(bool)

    def __init__(self, parsedConfig: dict[str, dict[str, str]], stateMachine, *, parent=None):
        super().__init__(parsedConfig, stateMachine, parent=parent)
        self._plungerCheckPassed = False
        self._compressionDrawerCheckPassed = False
        self._filtrateDrawerCheckPassed = False
        self.readRelevantConfigVars(self._parsedConfig)
        self._iterateTimer = QTimer(self)
        self._iterateTimer.timeout.connect(self.iterate)
        # TODO define how sensors are read

    @property
    def name(self):
        return 'home'

    def readRelevantConfigVars(self, parsedConfig: dict[str, dict[str, str]]):
        configFile = parsedConfig['CONFIG_FILE_NAME'] if 'CONFIG_FILE_NAME' in parsedConfig else 'config file'
        if (self._configFileSectionName not in parsedConfig):
            raise Exception(f"'{self._configFileSectionName}' section not found in {configFile}...")
        try:
            # TODO add any other configurable parameters here
            self._plungerLimit = int(parsedConfig[self._configFileSectionName]['homescreenplungerlimit'])
            self._compressionDrawerLimit = int(parsedConfig[self._configFileSectionName]['homescreencompressiondrawerlimit'])
            self._filtrateDrawerLimit = int(parsedConfig[self._configFileSectionName]['homescreenfiltratedrawerlimit'])
        except:
            raise Exception(f"All required configurable parameters were not found under the '{self._configFileSectionName}' or 'DEFAULT' sections in {configFile}...")

    @pyqtSlot()
    def iterate(self):

        # read plunger sensor (TODO update with actual sensor reading in if statement, left like this just for testing)
        plungerSensorValue = 7
        if ((plungerSensorValue < self._plungerLimit) != self._plungerCheckPassed):
            self._plungerCheckPassed = (not self._plungerCheckPassed)
            self.plungerStatusChanged.emit(self._plungerCheckPassed)

        # read compression drawer sensor (TODO update with actual sensor reading in if statement, left like this just for testing)
        compressionDrawerSensorValue = 8
        if ((compressionDrawerSensorValue < self._compressionDrawerLimit) != self._filtrateDrawerCheckPassed):
            self._filtrateDrawerCheckPassed = (not self._filtrateDrawerCheckPassed)
            self.compressionDrawerStatusChanged.emit(self._filtrateDrawerCheckPassed)

        # read compression drawer sensor (TODO update with actual sensor reading in if statement, left like this just for testing)
        compressionDrawerSensorValue = 9
        if ((compressionDrawerSensorValue < self._filtrateDrawerLimit) != self._compressionDrawerCheckPassed):
            self._compressionDrawerCheckPassed = (not self._compressionDrawerCheckPassed)
            self.filtrateDrawerStatusChanged.emit(self._compressionDrawerCheckPassed)

        if (self._plungerCheckPassed and self._compressionDrawerCheckPassed and self._filtrateDrawerCheckPassed):
            self._exitCondition = True

    def exit(self):
        self._machine.setCurrentState('welcome') # TODO update once other states defined
        self._iterateTimer.stop()
        print(f'{self.name} exiting...') # TODO remove, just for testing (also print() NOT thread-safe, use logging instead)

    def run(self):
        
        if (self._exitCondition):
            self.exit()
            return

        if (not self._iterateTimer.isActive()):
            self.plungerStatusChanged.emit(self._plungerCheckPassed)
            self.compressionDrawerStatusChanged.emit(self._filtrateDrawerCheckPassed)
            self.filtrateDrawerStatusChanged.emit(self._compressionDrawerCheckPassed)
            self._iterateTimer.start(round(1000.0/(1.0*int(self._iterateFreqHz))))
            print(f'state: {self.name}') # TODO remove, just for testing (also print() NOT thread-safe, use logging instead)
