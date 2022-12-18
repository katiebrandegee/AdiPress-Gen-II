from PyQt5.QtCore import QTimer, QObject, pyqtSignal, pyqtSlot

class InterruptHandler(QObject):

    emergencyStopSignal = pyqtSignal()
    
    _configFileSectionName = 'InterruptHandler'

    def __init__(self, parsedConfig: dict[str, dict[str, str]], gui, *, parent=None):
        super().__init__(parent)
        self._gui = gui
        self._parsedConfig = parsedConfig
        self._estopPressed = False
        self.readRelevantConfigVars(self._parsedConfig)
        self._iterateTimer = QTimer(self)
        self.makeConnections()

    def readRelevantConfigVars(self, parsedConfig: dict[str, dict[str, str]]):
        configFile = parsedConfig['CONFIG_FILE_NAME'] if 'CONFIG_FILE_NAME' in parsedConfig else 'config file'
        if (self._configFileSectionName not in parsedConfig):
            raise Exception(f"'{self._configFileSectionName}' section not found in {configFile}...")
        try:
            self._iterateFreqHz = int(parsedConfig[self._configFileSectionName]['iteratefreqhz'])
        except:
            raise Exception(f"All required configurable parameters were not found under the '{self._configFileSectionName}' or 'DEFAULT' sections in {configFile}...")

    def makeConnections(self):
        self._iterateTimer.timeout.connect(self.iterate)

    @pyqtSlot()
    def run(self):
        """Slot that begins interrupt handler iteration process to continue indefinitely"""
        self.resetEStop()
        self._iterateTimer.start(round(1000.0/(1.0*self._iterateFreqHz)))

    @pyqtSlot()
    def iterate(self):
        # TODO check if estop pressed 
        if (self._estopPressed):
            self.emergencyStopSignal.emit()

    def resetEStop(self):
        self._estopPressed = False

    @pyqtSlot()
    def receiveCloseEvent(self):
        self._iterateTimer.stop()
