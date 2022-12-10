from PyQt5.QtCore import QTimer, QObject, pyqtSignal, pyqtSlot
import RPi.GPIO as GPIO
import busio
import board
import adafruit_ads1x15.ads1115 as ADS 
from adafruit_ads1x15.analog_in import AnalogIn
from hx711 import HX711
import RFID
import config 
import pymongo
import socket
import datetime
import sched


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
    plungerStatusChanged = pyqtSignal(str, bool)
    compressionDrawerStatusChanged = pyqtSignal(str, bool)
    filtrateDrawerStatusChanged = pyqtSignal(str, bool)
    rfidStatusChanged = pyqtSignal(str, bool)

    def __init__(self, parsedConfig: dict[str, dict[str, str]], stateMachine, *, parent=None):
        super().__init__(parsedConfig, stateMachine, parent=parent)
        self._plungerCheckPassed = False
        self._compressionDrawerCheckPassed = False
        self._filtrateDrawerCheckPassed = False
        self._rfidChecksPassed = False
        self._consumableRFID = self._nullInt
        self._filtrateRFID = self._nullInt
        self.readRelevantConfigVars(self._parsedConfig)
        self._iterateTimer = QTimer(self)
        self._iterateTimer.timeout.connect(self.iterate)
        # TODO define how sensors are read
        self.plungerSensor, self.compressionDrawerSensor, self.filtrateDrawerSensor, self.nfc = self.setupSampleSetupSensors()

        # TODO remove below, just for testing slots in GUI
        self.testPlungerVal = 5000000
        self.testCompressionDrawerVal = 6000000
        self.testFiltrateDrawerVal = 7000000
        QTimer.singleShot(6000, lambda: self.testConditions1())
        QTimer.singleShot(8000, lambda: self.testConditions2())
        QTimer.singleShot(10000, lambda: self.testConditions3())

    def setupSampleSetupSensors(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        ads5V = ADS.ADS1115(i2c, address=0x49)
        plungerSensor = AnalogIn(ads5V, ADS.P0)
        compressionDrawerSensor = AnalogIn(ads5V, ADS.P1)
        filtrateDrawerSensor = AnalogIn(ads5V, ADS.P2)

        #RFID
        GPIO.setup(self._consumableRFID_RST, GPIO.OUT)
        GPIO.setup(self._filtrateRFID_RST, GPIO.OUT)
        nfc = RFID.NFC()
        nfc.addBoard("consumableRFID",self._consumableRFID_RST)
        nfc.addBoard("filtrateRFID",self._filtrateRFID_RST)

        return plungerSensor, compressionDrawerSensor, filtrateDrawerSensor


    # TODO remove, just for testing slots in GUI
    def testConditions1(self):
        self.testPlungerVal = 5

    # TODO remove, just for testing slots in GUI
    def testConditions2(self):
        self.testCompressionDrawerVal = 6

    # TODO remove, just for testing slots in GUI
    def testConditions3(self):
        self.testFiltrateDrawerVal = 6

    @property
    def name(self):
        return 'SampleSetup'

    def readRelevantConfigVars(self, parsedConfig: dict[str, dict[str, str]]):
        configFile = parsedConfig['CONFIG_FILE_NAME'] if 'CONFIG_FILE_NAME' in parsedConfig else 'config file'
        if (self._configFileSectionName not in parsedConfig):
            raise Exception(f"'{self._configFileSectionName}' section not found in {configFile}...")
        try:

            # TODO add any other configurable parameters here
            self._plungerimit = int(parsedConfig[self._configFileSectionName]['plungersensorlim'])
            self._compressionDrawerLimit = int(parsedConfig[self._configFileSectionName]['compressiondrawerlim'])
            self._filtrateDrawerLimit = int(parsedConfig[self._configFileSectionName]['filtratedrawerlimit'])
            self._consumableRFID_RST = int(parsedConfig[self._configFileSectionName]['consumablerfid_rst'])
            self._filtrateRFID_RST = int(parsedConfig[self._configFileSectionName]['filtraterfid_rst'])
            self._consumableGain = int(parsedConfig[self._configFileSectionName]['consumablegain'])
            self._filtrateGain = int(parsedConfig[self._configFileSectionName]['filtrategain'])


        except:
            raise Exception(f"All required configurable parameters were not found under the '{self._configFileSectionName}' or 'DEFAULT' sections in {configFile}...")

    @pyqtSlot()
    def iterate(self):

        # read plunger sensor (TODO update with actual sensor reading in if statement, left like this just for testing)
        plungerSensorValue = self.plungerSensor.value
        if ((plungerSensorValue < self._plungerLimit) != self._plungerCheckPassed):
            self._plungerCheckPassed = (not self._plungerCheckPassed)
            self.plungerStatusChanged.emit("plunger", self._plungerCheckPassed)

        # read compression drawer sensor (TODO update with actual sensor reading in if statement, left like this just for testing)
        compressionDrawerSensorValue = self.compressionDrawerSensor.value
        if ((compressionDrawerSensorValue < self._compressionDrawerLimit) != self._compressionDrawerCheckPassed):
            self._compressionDrawerCheckPassed = (not self._compressionDrawerCheckPassed)
            self.compressionDrawerStatusChanged.emit("compressionDrawer", self._compressionDrawerCheckPassed)

        # read compression drawer sensor (TODO update with actual sensor reading in if statement, left like this just for testing)
        filtrateDrawerSensorValue = self.compressionDrawerSensor.value
        if ((filtrateDrawerSensorValue < self._filtrateDrawerLimit) != self._filtrateDrawerCheckPassed):
            self._filtrateDrawerCheckPassed = (not self._filtrateDrawerCheckPassed)
            self.filtrateDrawerStatusChanged.emit("filtrateDrawer", self._filtrateDrawerCheckPassed)

        allChecksPassed = (self._plungerCheckPassed and self._compressionDrawerCheckPassed and self._filtrateDrawerCheckPassed)

        # read consumable RFID (TODO update with actual RFID reading in if statement, left like this just for testing)
        if (self._compressionDrawerCheckPassed):
            self._consumableRFID = self.nfc.read("consumableRFID")

        # read consumable RFID (TODO update with actual RFID reading in if statement, left like this just for testing)
        if (self._filtrateDrawerCheckPassed):
            self._filtrateRFID = self.nfc.read("filtateRFID")
        # make sure that nullInt is representative of what you get when theres no card
        allRfIdsRead = (self._consumableRFID != self._nullInt and self._filtrateRFID != self._nullInt)
        if (allRfIdsRead != self._rfidChecksPassed):
            self._rfidChecksPassed = (not self._rfidChecksPassed)
            self.rfidStatusChanged.emit("rfids", self._rfidChecksPassed)

        if (allChecksPassed and allRfIdsRead):
            # TODO: lock trays and store sample weight
            self._exitCondition = True

    def enter(self):
        self._exitCondition = False
        self._plungerCheckPassed = False
        self._filtrateDrawerCheckPassed = False
        self._compressionDrawerCheckPassed = False
        self._rfidChecksPassed = False
        self._consumableRFID = self._nullInt
        self._filtrateRFID = self._nullInt
        self.plungerStatusChanged.emit("plunger", self._plungerCheckPassed)
        self.compressionDrawerStatusChanged.emit("compressionDrawer", self._filtrateDrawerCheckPassed)
        self.filtrateDrawerStatusChanged.emit("filtrateDrawer", self._compressionDrawerCheckPassed)
        self.rfidStatusChanged.emit("rfids", self._rfidChecksPassed)
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
        self._goButtonPressedFlag = False
        self._compressionLimitReached = False
        self.readRelevantConfigVars(self._parsedConfig)
        self._iterateTimer = QTimer(self)
        self._iterateTimer.timeout.connect(self.iterate)
        self.pwmDown, self.pwmUp, self.currentSensor = self.setupCompressionSensors()
        # TODO define how sensors are read

    @property
    def name(self):
        return 'Compression'

    def setupCompressionSensors(self):
        # Actuator Setup
        GPIO.setup(self._UP_PWM, GPIO.OUT)
        GPIO.setup(self._DOWN_PWM, GPIO.OUT)
        GPIO.setup(self._UP_EN, GPIO.OUT)
        GPIO.setup(self._DOWN_EN, GPIO.OUT)

        GPIO.output(self._UP_EN, GPIO.HIGH)
        GPIO.output(self._DOWN_EN, GPIO.HIGH)

        # set these better later
        pwmUp = GPIO.PWM(self._UP_PWM, 50)
        pwmDown = GPIO.PWM(self._DOWN_PWM, 50)

        pwmUp.start(0)
        pwmDown.start(0)

        # Current sensor setup
        i2c = busio.I2C(board.SCL, board.SDA)
        ads3V = ADS.ADS1115(i2c)
        currentSensor = AnalogIn(ads3V, ADS.P0)

        # Load Cells
        loadCell1 = HX711(dout_pin=21, pd_sck_pin=18, channel='A', gain = gain1)
        loadCell2 = HX711(dout_pin=19, pd_sck_pin=26, channel='A', gain = gain2)


        return pwmDown, pwmUp, currentSensor



    def readRelevantConfigVars(self, parsedConfig: dict[str, dict[str, str]]):
        configFile = parsedConfig['CONFIG_FILE_NAME'] if 'CONFIG_FILE_NAME' in parsedConfig else 'config file'
        if (self._configFileSectionName not in parsedConfig):
            raise Exception(f"'{self._configFileSectionName}' section not found in {configFile}...")
        try:
            # TODO add any other configurable parameters here
            self._currentLimit = int(parsedConfig[self._configFileSectionName]['compressionscreencurrentlimit'])
            self._dwellDurationSec = float(parsedConfig[self._configFileSectionName]['compressionscreendwelldurationsec'])
            self._UP_PWM = int(parsedConfig[self._configFileSectionName]['up_pwm'])
            self._DOWN_PWM = int(parsedConfig[self._configFileSectionName]['down_pwm'])
            self._UP_EN = int(parsedConfig[self._configFileSectionName]['up_en'])
            self._DOWN_EN = int(parsedConfig[self._configFileSectionName]['down_en'])
            self._endPin = int(parsedConfig[self._configFileSectionName]['endpin'])
            self._homePin = int(parsedConfig[self._configFileSectionName]['homepin'])
            self._encoder = int(parsedConfig[self._configFileSectionName]['encoder']) 
            self._consumableGain = int(parsedConfig[self._configFileSectionName]['consumablegain']) 
            self._filtrateGain = int(parsedConfig[self._configFileSectionName]['filtrategain']) 

        except:
            raise Exception(f"All required configurable parameters were not found under the '{self._configFileSectionName}' or 'DEFAULT' sections in {configFile}...")

    def iterate(self):
        
        # TODO: check if go button pressed
        # check what current sensor reads when nothing is moving
        # chekc to see if loop executes fast enough for polling go Buttun instead of interrupt
        if (self._goButtonPressed and not self._compressionLimitReached):
            self._goButtonPressedFlag = True
            if (not self._goButtonPressedFlag):
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

