# define dictionary of {stateNames: state}
from statemachine import StateMachine
# import statemachine as smm
from PyQt5.QtCore import QTimer, QObject, pyqtSignal, pyqtSlot

class State(QObject):

    _exitCondition = False
    _iterateFreqHz = 10

    def __init__(self, machine: StateMachine, parsedConfig: dict, *, parent=None):
        super().__init__(parent)
        self._machine = machine
        self._parsedConfig = parsedConfig

    @property
    def name(self):
        return ''

    # # def defineParameters(self, machine: smm.StateMachine, parsedConfig: dict):
    # def defineParameters(self, machine: StateMachine, parsedConfig: dict):
    #     self._machine = machine
    #     self._parsedConfig = parsedConfig

    def run(self, machine):
        pass

    def iterate(self, machine):
        pass


class WelcomeState(State):

    def __init__(self, machine: StateMachine, parsedConfig: dict, *, parent=None):
        super().__init__(machine, parsedConfig, parent=parent)

    @property
    def name(self):
        return 'welcome'

    def runOnce(self, machine: StateMachine):
        print(f'state: {self.name}')


class HomeState(State):

    def __init__(self, machine: StateMachine, parsedConfig: dict, *, parent=None):
        super().__init__(machine, parsedConfig, parent=parent)
        self.plungerCheckPassed = False
        self.compressionDrawerCheckPassed = False
        self.filtrateDrawerCheckPassed = False

    @property
    def name(self):
        return 'home'

    def runOnce(self, machine: StateMachine):
        print(f'state: {self.name}')

