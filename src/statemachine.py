import states
# from states import WelcomeState, HomeState # TODO include rest of states
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

    _firstStateName = 'welcome' # TODO change

    stateChangedSignal = pyqtSignal(str)

    def __init__(self, parsedConfig: dict, *, parent=None):
        super().__init__(parent)
        self._parsedConfig = parsedConfig
        self.readRelevantConfigVars(self._parsedConfig)
        self._states = self.defineStateDict((states.WelcomeState(self, self._parsedConfig, parent=self), states.HomeState(self, self._parsedConfig, parent=self)))
        # self._states = self.defineStateDict((sm.WelcomeState(parent=self), sm.HomeState(parent=self)))
        self.currState = self._states[self._firstStateName]
        self.prevStateName = self.currState.name
        self._iterateTimer = QTimer(self)
        self.makeConnections()        

    # only function that "magically" adds instance vars (i.e. class member vars)
    # only hard-coded section, var names (e.g. iteratefreqhz) must match lower case keys in config.ini 
    def readRelevantConfigVars(self, parsedConfig: dict):
        self._iterateFreqHz = parsedConfig['StateMachine']['iteratefreqhz']

    def defineStateDict(self, states: tuple) -> dict:
        return {st.name: st for st in states}

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
        self._iterateTimer.start(self._iterateFreqHz)

    # iterating (looping) at self._iterateFreqHz, using QTimer to loop allows signals/slots to execute in between loop iterations
    # self.currState modifiable within each State when State.exitCondition met
    @pyqtSlot()
    def iterate(self):
        self.currState.run(self)
        if (self.currState.name != self.prevStateName):
            self.stateChangedSignal.emit(self.currState.name)
            self.prevStateName = self.currState.name

    # only QMainWindow catches closeEvents, so connect signal from GUI(QMainWindow) to alert StateMachine for proper cleanup
    @pyqtSlot()
    def receiveCloseEvent(self):
        self._iterateTimer.stop()
        # potentially emit signal to states within machine


# TODO remove --> for testing only
if __name__ == "__main__":
    from configparser import ConfigParser
    parsedConfig = ConfigParser()
    parsedConfig.read("config.ini")
    parsedConfig = {section: dict(parsedConfig.items(section)) for section in parsedConfig.sections()}
    SM = StateMachine(parsedConfig)
    print(SM._firstStateName)
    print(SM._states)
    print(SM._states['welcome'].name)
    print(SM._states['welcome']._machine)
    print(SM._states['welcome']._parsedConfig)

