import states as States
from PyQt5.QtCore import QTimer, QObject, pyqtSignal, pyqtSlot

# NOTE: the only thing i dislike about this architecture is direct communication between GUI and states (i.e. not mediated by StateMachine)
#       cons:
#           it creates a weird cyclic dependency between GUI and StateMachine that is NOT a parent/child relationship
#           it makes the flow of data through the system less obvious (should be GUI <---> StateMachine <---> State(s) with no skip connections)
#       pros:
#           much more practical/efficient, and logical reason for direct connections very obvious to reader 
#           all issues could be avoided with single data broker, but that would be nightmarishly tedious and likely require another thread
#           cyclic dependency issue could be avoided by having GUI make direct connections to StateMachine._states, but doesn't totally make sense for GUI to have knowledge of anything more than state names <---> associated screens

class StateMachine(QObject):

    stateChangedSignal = pyqtSignal(str)

    _firstStateName = 'welcome' # TODO change
    _configFileSectionName = 'StateMachine'
    
    def __init__(self, parsedConfig: dict[str, dict[str, str]], gui, *, parent=None):
        super().__init__(parent)
        self._gui = gui
        self._parsedConfig = parsedConfig
        self.readRelevantConfigVars(self._parsedConfig)
        self._states = self.defineStateDict(self.constructStates(self._parsedConfig))
        if (not self.setCurrentState(self._firstStateName)):
            raise Exception(f"Could not set the state machine's first state to {self._firstStateName}...")
        self.prevStateName = self.currState.name
        self._iterateTimer = QTimer(self)
        self.makeConnections()        

    # only function that "magically" adds instance vars (i.e. class member vars)
    # only hard-coded section, var names (e.g. iteratefreqhz) must match lower case keys in config.ini 
    def readRelevantConfigVars(self, parsedConfig: dict[str, dict[str, str]]):
        configFile = parsedConfig['CONFIG_FILE_NAME'] if 'CONFIG_FILE_NAME' in parsedConfig else 'config file'
        if (self._configFileSectionName not in parsedConfig):
            raise Exception(f"'{self._configFileSectionName}' section not found in {configFile}...")
        try:
            # TODO add any other configurable parameters here
            self._iterateFreqHz = int(parsedConfig[self._configFileSectionName]['iteratefreqhz'])
        except:
            raise Exception(f"All required configurable parameters were not found under the '{self._configFileSectionName}' or 'DEFAULT' sections in {configFile}...")


    def constructStates(self, parsedConfig: dict[str, dict[str, str]]) -> tuple[States.State]:
        allStates = list()
        allStates.append(States.WelcomeState(parsedConfig=parsedConfig, stateMachine=self, parent=self))
        allStates.append(States.HomeState(parsedConfig=parsedConfig, stateMachine=self, parent=self))
        # TODO: add all states
        return tuple(allStates)

    def defineStateDict(self, allStates: tuple[States.State]) -> dict[str, States.State]:
        return {st.name: st for st in allStates}

    # make all signal/slot connections
    def makeConnections(self):
        self._iterateTimer.timeout.connect(self.iterate)
        # make all relevant connections between states and GUI
        # make all relevant connections between states and self
        # make all relevant connections between states and interrupt handler
        # DO NOT make all relevant connections between interrupt handler and self --> GUI thread's job
        # DO NOT make all relevant connections between GUI and self --> GUI thread's job

    # other than getters, ONLY function that should be called outside class (e.g. by GUI)
    # slot connected to QThread.started() so that StateMachine thread affinity set properly
    # then to actually start StateMachine, GUI just has to create its thread and call QThread.start()
    @pyqtSlot()
    def run(self):
        """Slot that begins state machine iteration process to continue indefinitely"""
        self._iterateTimer.start(round(1000.0/(1.0*self._iterateFreqHz)))

    # iterating (looping) at self._iterateFreqHz, using QTimer to loop allows signals/slots to execute in between loop iterations
    # self.currState modifiable within each State when State.exitCondition met
    @pyqtSlot()
    def iterate(self):
        self.currState.run()
        if (self.currState.name != self.prevStateName):
            self.stateChangedSignal.emit(self.currState.name)
            self.prevStateName = self.currState.name

    # only QMainWindow catches closeEvents, so connect signal from GUI(QMainWindow) to alert StateMachine for proper cleanup
    @pyqtSlot()
    def receiveCloseEvent(self):
        self._iterateTimer.stop()
        # potentially emit signal to states within machine

    def getStateNames(self) -> list[str]:
        """Get list of all state names as strings defined within the state machine"""
        return [stateName for stateName in self._states.keys()]

    def getStates(self) -> dict[str, States.State]:
        """Get dictionary of all states defined within the state machine of the form {stateName: stateObject}"""
        return self._states
        
    def setCurrentState(self, newStateName: str) -> bool:
        """Set current state within the state machine by providing its name as a string, returns boolean representing operation success"""
        if (newStateName not in self._states):
            return False
        self.currState = self._states[newStateName]
        return True
