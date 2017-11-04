from transitions import Machine
from hackathon.utils.utils import ResultsMessage, PVMode


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
        if not msg.grid_status and self.state_machine.state == 'mode1':
            self.state_machine.off()
        elif msg.grid_status and self.state_machine.state == 'mode2':
            self.state_machine.on()

        if self.state_machine.state == 'mode1':
            pv_mode = PVMode.OFF
        elif self.state_machine.state == 'mode2':
            pv_mode = PVMode.ON

        res = ResultsMessage(data_msg=msg,
                             load_one=True,
                             load_two=True,
                             load_three=True,
                             power_reference=0.0,
                             pv_mode=pv_mode)

        print('BamBam: {}'.format(res))
        return res
