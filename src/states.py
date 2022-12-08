from PyQt5.QtCore import QTimer, QObject, pyqtSignal, pyqtSlot

class State(QObject):

    _nullInt = -1
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
            self._iterateFreqHz = int(parsedConfig[self._configFileSectionName]['iteratefreqhz'])
        except:
            raise Exception(f"All required configurable parameters were not found under the '{self._configFileSectionName}' or 'DEFAULT' sections in {configFile}...")

    def enter(self):
        pass

    def exit(self):
        pass

    def run(self):
        pass
    

class WelcomeState(State):

    def __init__(self, parsedConfig: dict[str, dict[str, str]], stateMachine, *, parent=None):
        super().__init__(parsedConfig, stateMachine, parent=parent)
        self.readRelevantConfigVars(self._parsedConfig)
        self._sstimer = QTimer(self)
        self._sstimer.timeout.connect(self.timeout)

    @property
    def name(self):
        return 'Welcome'

    def readRelevantConfigVars(self, parsedConfig: dict[str, dict[str, str]]):
        configFile = parsedConfig['CONFIG_FILE_NAME'] if 'CONFIG_FILE_NAME' in parsedConfig else 'config file'
        if (self._configFileSectionName not in parsedConfig):
            raise Exception(f"'{self._configFileSectionName}' section not found in {configFile}...")
        try:
            # TODO add any other configurable parameters here
            self._sstimerDurationSec = float(parsedConfig[self._configFileSectionName]['welcomescreendurationsec'])
        except:
            raise Exception(f"All required configurable parameters were not found under the '{self._configFileSectionName}' or 'DEFAULT' sections in {configFile}...")

    @pyqtSlot()
    def timeout(self):
        self._exitCondition = True

    def enter(self):
        self._exitCondition = False
        self._sstimer.start(round(self._sstimerDurationSec*1000.0))
        print(f'\nstate: {self.name}') # TODO remove, just for testing (also print() NOT thread-safe, use logging instead)

    def exit(self):
        newStateName = 'MachineSetup'
        if (not self._machine.setCurrentState(newStateName)): 
            raise Exception(f"Could not change current state of state machine to state named '{newStateName}'...")
        self._sstimer.stop()
        print(f'{self.name} exiting...') # TODO remove, just for testing (also print() NOT thread-safe, use logging instead)

    def run(self):
        
        if (not self._sstimer.isActive()):
            self.enter()

        if (self._exitCondition):
            self.exit()        


class MachineSetupState(State):

    deviceHomedStatusChanged = pyqtSignal(bool)
    loadCellsTaredStatusChanged = pyqtSignal(bool)

    def __init__(self, parsedConfig: dict[str, dict[str, str]], stateMachine, *, parent=None):
        super().__init__(parsedConfig, stateMachine, parent=parent)
        self._deviceHomed = False
        self._loadCellsTared = False
        self._calibrationCurrentMeasured = False
        self.readRelevantConfigVars(self._parsedConfig)
        self._iterateTimer = QTimer(self)
        self._iterateTimer.timeout.connect(self.iterate)
        # TODO define how sensors are read

    @property
    def name(self):
        return 'MachineSetup'

    def readRelevantConfigVars(self, parsedConfig: dict[str, dict[str, str]]):
        configFile = parsedConfig['CONFIG_FILE_NAME'] if 'CONFIG_FILE_NAME' in parsedConfig else 'config file'
        if (self._configFileSectionName not in parsedConfig):
            raise Exception(f"'{self._configFileSectionName}' section not found in {configFile}...")
        try:
            # TODO add any other configurable parameters here
            self._actuatorVerticalDist = float(parsedConfig[self._configFileSectionName]['machinesetupscreenverticalactuatordistinches'])
        except:
            raise Exception(f"All required configurable parameters were not found under the '{self._configFileSectionName}' or 'DEFAULT' sections in {configFile}...")

    def iterate(self):

        # TODO read device homed
        deviceHomed = True
        if (deviceHomed != self._deviceHomed):
            self._deviceHomed = (not self._deviceHomed)
            self.deviceHomedStatusChanged.emit(self._deviceHomed)

        if (not self._deviceHomed):
            return

        # TODO potentially emit second signal to prompt user to "take everything out"
        # TODO tare load cells
        self._loadCellsTared = True

        # TODO move actuator up and down an measure calibration current
        self._calibrationCurrentMeasured = True

        if (self._loadCellsTared and self._calibrationCurrentMeasured):
            self._exitCondition = True

    def enter(self):
        self._exitCondition = False
        self._deviceHomed = False
        self._loadCellsTared = False
        self._calibrationCurrentMeasured = False
        self.deviceHomedStatusChanged.emit(self._deviceHomed)
        self.loadCellsTaredStatusChanged.emit(self._loadCellsTared)
        self._iterateTimer.start(round(1000.0/(1.0*self._iterateFreqHz)))
        print(f'\nstate: {self.name}') # TODO remove, just for testing (also print() NOT thread-safe, use logging instead)

    def exit(self):
        newStateName = 'SampleSetup'
        if (not self._machine.setCurrentState(newStateName)): 
            raise Exception(f"Could not change current state of state machine to state named '{newStateName}'...")
        self._iterateTimer.stop()
        print(f'{self.name} exiting...') # TODO remove, just for testing (also print() NOT thread-safe, use logging instead)

    def run(self):
        
        if (not self._iterateTimer.isActive()):
            self.enter()

        if (self._exitCondition):
            self.exit()


class SampleSetupState(State):

    # TODO: connect signals to gui in StateMachine.makeConnections() 
    plungerStatusChanged = pyqtSignal(bool)
    compressionDrawerStatusChanged = pyqtSignal(bool)
    filtrateDrawerStatusChanged = pyqtSignal(bool)

    def __init__(self, parsedConfig: dict[str, dict[str, str]], stateMachine, *, parent=None):
        super().__init__(parsedConfig, stateMachine, parent=parent)
        self._plungerCheckPassed = False
        self._compressionDrawerCheckPassed = False
        self._filtrateDrawerCheckPassed = False
        self._consumableRFID = self._nullInt
        self._filtrateRFID = self._nullInt
        self.readRelevantConfigVars(self._parsedConfig)
        self._iterateTimer = QTimer(self)
        self._iterateTimer.timeout.connect(self.iterate)
        # TODO define how sensors are read

    @property
    def name(self):
        return 'SampleSetup'

    def readRelevantConfigVars(self, parsedConfig: dict[str, dict[str, str]]):
        configFile = parsedConfig['CONFIG_FILE_NAME'] if 'CONFIG_FILE_NAME' in parsedConfig else 'config file'
        if (self._configFileSectionName not in parsedConfig):
            raise Exception(f"'{self._configFileSectionName}' section not found in {configFile}...")
        try:
            # TODO add any other configurable parameters here
            self._plungerLimit = int(parsedConfig[self._configFileSectionName]['samplesetupscreenplungerlimit'])
            self._compressionDrawerLimit = int(parsedConfig[self._configFileSectionName]['samplesetupscreencompressiondrawerlimit'])
            self._filtrateDrawerLimit = int(parsedConfig[self._configFileSectionName]['samplesetupscreenfiltratedrawerlimit'])
        except:
            raise Exception(f"All required configurable parameters were not found under the '{self._configFileSectionName}' or 'DEFAULT' sections in {configFile}...")

    @pyqtSlot()
    def iterate(self):

        # read plunger sensor (TODO update with actual sensor reading in if statement, left like this just for testing)
        plungerSensorValue = 5
        if ((plungerSensorValue < self._plungerLimit) != self._plungerCheckPassed):
            self._plungerCheckPassed = (not self._plungerCheckPassed)
            self.plungerStatusChanged.emit(self._plungerCheckPassed)

        # read compression drawer sensor (TODO update with actual sensor reading in if statement, left like this just for testing)
        compressionDrawerSensorValue = 6
        if ((compressionDrawerSensorValue < self._compressionDrawerLimit) != self._compressionDrawerCheckPassed):
            self._compressionDrawerCheckPassed = (not self._compressionDrawerCheckPassed)
            self.compressionDrawerStatusChanged.emit(self._compressionDrawerCheckPassed)

        # read compression drawer sensor (TODO update with actual sensor reading in if statement, left like this just for testing)
        filtrateDrawerSensorValue = 7
        if ((filtrateDrawerSensorValue < self._filtrateDrawerLimit) != self._filtrateDrawerCheckPassed):
            self._filtrateDrawerCheckPassed = (not self._filtrateDrawerCheckPassed)
            self.filtrateDrawerStatusChanged.emit(self._filtrateDrawerCheckPassed)

        # read consumable RFID (TODO update with actual RFID reading in if statement, left like this just for testing)
        if (self._compressionDrawerCheckPassed):
            self._consumableRFID = 8

        # read consumable RFID (TODO update with actual RFID reading in if statement, left like this just for testing)
        if (self._filtrateDrawerCheckPassed):
            self._filtrateRFID = 9

        allChecksPassed = (self._plungerCheckPassed and self._compressionDrawerCheckPassed and self._filtrateDrawerCheckPassed)
        allRfIdsRead = (self._consumableRFID != self._nullInt and self._filtrateRFID != self._nullInt)

        if (allChecksPassed and allRfIdsRead):
            # TODO: lock trays and store sample weight
            self._exitCondition = True

    def enter(self):
        self._exitCondition = False
        self._plungerCheckPassed = False
        self._filtrateDrawerCheckPassed = False
        self._compressionDrawerCheckPassed = False
        self._consumableRFID = self._nullInt
        self._filtrateRFID = self._nullInt
        self.plungerStatusChanged.emit(self._plungerCheckPassed)
        self.compressionDrawerStatusChanged.emit(self._filtrateDrawerCheckPassed)
        self.filtrateDrawerStatusChanged.emit(self._compressionDrawerCheckPassed)
        self._iterateTimer.start(round(1000.0/(1.0*self._iterateFreqHz)))
        print(f'\nstate: {self.name}') # TODO remove, just for testing (also print() NOT thread-safe, use logging instead)

    def exit(self):
        newStateName = 'Compression'
        if (not self._machine.setCurrentState(newStateName)): 
            raise Exception(f"Could not change current state of state machine to state named '{newStateName}'...")
        self._iterateTimer.stop()
        print(f'{self.name} exiting...') # TODO remove, just for testing (also print() NOT thread-safe, use logging instead)

    def run(self):
        
        if (not self._iterateTimer.isActive()):
            self.enter()

        if (self._exitCondition):
            self.exit()


class CompressionState(State):

    goButtonPressedEvent = pyqtSignal()

    def __init__(self, parsedConfig: dict[str, dict[str, str]], stateMachine, *, parent=None):
        super().__init__(parsedConfig, stateMachine, parent=parent)
        self._goButtonPressed = False
        self.readRelevantConfigVars(self._parsedConfig)
        self._iterateTimer = QTimer(self)
        self._iterateTimer.timeout.connect(self.iterate)
        # TODO define how sensors are read

    @property
    def name(self):
        return 'Compression'

    def readRelevantConfigVars(self, parsedConfig: dict[str, dict[str, str]]):
        configFile = parsedConfig['CONFIG_FILE_NAME'] if 'CONFIG_FILE_NAME' in parsedConfig else 'config file'
        if (self._configFileSectionName not in parsedConfig):
            raise Exception(f"'{self._configFileSectionName}' section not found in {configFile}...")
        try:
            # TODO add any other configurable parameters here
            self._currentLimit = int(parsedConfig[self._configFileSectionName]['compressionscreencurrentlimit'])
            self._dwellDurationSec = float(parsedConfig[self._configFileSectionName]['compressionscreendwelldurationsec'])
        except:
            raise Exception(f"All required configurable parameters were not found under the '{self._configFileSectionName}' or 'DEFAULT' sections in {configFile}...")

    def iterate(self):

        # TODO: check if go button pressed
        if (self._goButtonPressed):
            self.goButtonPressedEvent.emit()

        # TODO define rest of state (and probably do goButtonStatusChanged for signal instead)
        self._exitCondition = True

    def enter(self):
        self._exitCondition = False
        self._goButtonPressed = False
        self._iterateTimer.start(round(1000.0/(1.0*self._iterateFreqHz)))
        print(f'\nstate: {self.name}') # TODO remove, just for testing (also print() NOT thread-safe, use logging instead)

    def exit(self):
        newStateName = 'Welcome'
        if (not self._machine.setCurrentState(newStateName)): 
            raise Exception(f"Could not change current state of state machine to state named '{newStateName}'...")
        self._iterateTimer.stop()
        print(f'{self.name} exiting...') # TODO remove, just for testing (also print() NOT thread-safe, use logging instead)

    def run(self):
        
        if (not self._iterateTimer.isActive()):
            self.enter()

        if (self._exitCondition):
            self.exit()

