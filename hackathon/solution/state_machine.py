from transitions import Machine


class StateMachine(object):
    states = ['mode1', 'mode2']
    transitions = [
        {'trigger': 'off', 'source': 'mode1', 'dest': 'mode2'},
        {'trigger': 'on', 'source': 'mode2', 'dest': 'mode1'}
    ]

    def __init__(self):
        self.machine = Machine(self, states=StateMachine.states, transitions=StateMachine.transitions, initial='mode1')


class Handler(object):
    state_machine = StateMachine()

    def process(self, msg):
        return self.state_machine.state

