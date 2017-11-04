from transitions import Machine
from hackathon.utils.utils import ResultsMessage, PVMode


class StateMachine(object):
    states = [
        'on_good_full' , 'on_good_half' , 'on_good_empty',
        'on_bad_full'  , 'on_bad_half'  , 'on_bad_empty',
        'off_good_full', 'off_good_half', 'off_good_empty',
        'off_bad_full' , 'off_bad_half' , 'off_bad_empty'
    ]

    transitions = [
        # on_good_full
        {'trigger': 'off',   'source': 'on_good_full',  'dest': 'off_good_full'},
        {'trigger': 'bad',   'source': 'on_good_full',  'dest': 'on_bad_full'},
        {'trigger': 'half',  'source': 'on_good_full',  'dest': 'on_good_half'},

        # on_good_half
        {'trigger': 'full',  'source': 'on_good_half',  'dest': 'on_good_full'},
        {'trigger': 'empty', 'source': 'on_good_half',  'dest': 'on_good_empty'},
        {'trigger': 'bad',   'source': 'on_good_half',  'dest': 'on_bad_half'},
        {'trigger': 'off',   'source': 'on_good_half',  'dest': 'off_good_half'},

        # on_good_empty
        {'trigger': 'half',  'source': 'on_good_empty', 'dest': 'on_good_half'},
        {'trigger': 'bad',   'source': 'on_good_empty', 'dest': 'on_bad_empty'},
        {'trigger': 'off',   'source': 'on_good_empty', 'dest': 'off_good_empty'},

        # on_bad_full
        {'trigger': 'good',  'source': 'on_bad_full',   'dest': 'on_good_full'},
        {'trigger': 'half',  'source': 'on_bad_full',   'dest': 'on_bad_half'},
        {'trigger': 'off',   'source': 'on_bad_full',   'dest': 'off_bad_full'},

        # on_bad_half
        {'trigger': 'full',  'source': 'on_bad_half',   'dest': 'on_bad_full'},
        {'trigger': 'good',  'source': 'on_bad_half',   'dest': 'on_good_half'},
        {'trigger': 'empty', 'source': 'on_bad_half',   'dest': 'on_bad_empty'},
        {'trigger': 'off',   'source': 'on_bad_half',   'dest': 'off_bad_half'},

        # on_bad_empty
        {'trigger': 'good',  'source': 'on_bad_empty',  'dest': 'on_good_empty'},
        {'trigger': 'half',  'source': 'on_bad_empty',  'dest': 'on_bad_half'},
        {'trigger': 'off',   'source': 'on_bad_empty',  'dest': 'off_bad_empty'},

        # off_good_full
        {'trigger': 'half', 'source': 'off_good_full', 'dest': 'off_good_half'},
        {'trigger': 'on', 'source': 'off_good_full', 'dest': 'on_good_full'},
        {'trigger': 'bad', 'source': 'off_good_full', 'dest': 'off_bad_full'},

        # off_good_half
        {'trigger': 'full', 'source': 'off_good_half', 'dest': 'off_good_full'},
        {'trigger': 'empty', 'source': 'off_good_half', 'dest': 'off_good_empty'},
        {'trigger': 'on', 'source': 'off_good_half', 'dest': 'on_good_half'},
        {'trigger': 'bad', 'source': 'off_good_half', 'dest': 'off_bad_half'},

        # off_good_empty
        {'trigger': 'half', 'source': 'off_good_empty', 'dest': 'off_half_empty'},
        {'trigger': 'on', 'source': 'off_good_empty', 'dest': 'on_good_empty'},
        {'trigger': 'bad', 'source': 'off_good_empty', 'dest': 'off_bad_empty'},

        # off_bad_full
        {'trigger': 'half', 'source': 'off_bad_full', 'dest': 'off_bad_half'},
        {'trigger': 'on', 'source': 'off_bad_full', 'dest': 'on_bad_full'},
        {'trigger': 'good', 'source': 'off_bad_full', 'dest': 'off_good_full'},

        # off_bad_half
        {'trigger': 'full', 'source': 'off_bad_half', 'dest': 'off_bad_full'},
        {'trigger': 'empty', 'source': 'off_bad_half', 'dest': 'off_bad_empty'},
        {'trigger': 'on', 'source': 'off_bad_half', 'dest': 'on_bad_half'},
        {'trigger': 'good', 'source': 'off_bad_half', 'dest': 'off_good_half'},

        # off_bad_empty
        {'trigger': 'half', 'source': 'off_bad_empty', 'dest': 'off_bad_half'},
        {'trigger': 'on', 'source': 'off_bad_empty', 'dest': 'on_bad_empty'},
        {'trigger': 'good', 'source': 'off_bad_empty', 'dest': 'off_good_empty'},
    ]

    def __init__(self):
        self.machine = Machine(self, states=StateMachine.states, transitions=StateMachine.transitions, initial='mode1')


class Handler(object):
    state_machine = StateMachine()

    def process(self, msg):
        # pitam se da li se promenila mreza

        # pitam se da li se promenio odnos cena
        # pitam se da li se popunjenost baterije promenila



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
