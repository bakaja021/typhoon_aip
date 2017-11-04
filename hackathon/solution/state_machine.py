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
        {'trigger': 'half',  'source': 'off_good_full', 'dest': 'off_good_half'},
        {'trigger': 'on',    'source': 'off_good_full', 'dest': 'on_good_full'},
        {'trigger': 'bad',   'source': 'off_good_full', 'dest': 'off_bad_full'},

        # off_good_half
        {'trigger': 'full',  'source': 'off_good_half', 'dest': 'off_good_full'},
        {'trigger': 'empty', 'source': 'off_good_half', 'dest': 'off_good_empty'},
        {'trigger': 'on',    'source': 'off_good_half', 'dest': 'on_good_half'},
        {'trigger': 'bad',   'source': 'off_good_half', 'dest': 'off_bad_half'},

        # off_good_empty
        {'trigger': 'half',  'source': 'off_good_empty', 'dest': 'off_half_empty'},
        {'trigger': 'on',    'source': 'off_good_empty', 'dest': 'on_good_empty'},
        {'trigger': 'bad',   'source': 'off_good_empty', 'dest': 'off_bad_empty'},

        # off_bad_full
        {'trigger': 'half',  'source': 'off_bad_full', 'dest': 'off_bad_half'},
        {'trigger': 'on',    'source': 'off_bad_full', 'dest': 'on_bad_full'},
        {'trigger': 'good',  'source': 'off_bad_full', 'dest': 'off_good_full'},

        # off_bad_half
        {'trigger': 'full',  'source': 'off_bad_half', 'dest': 'off_bad_full'},
        {'trigger': 'empty', 'source': 'off_bad_half', 'dest': 'off_bad_empty'},
        {'trigger': 'on',    'source': 'off_bad_half', 'dest': 'on_bad_half'},
        {'trigger': 'good',  'source': 'off_bad_half', 'dest': 'off_good_half'},

        # off_bad_empty
        {'trigger': 'half',  'source': 'off_bad_empty', 'dest': 'off_bad_half'},
        {'trigger': 'on',    'source': 'off_bad_empty', 'dest': 'on_bad_empty'},
        {'trigger': 'good',  'source': 'off_bad_empty', 'dest': 'off_good_empty'},
    ]

    def __init__(self):
        self.machine = Machine(self, states=StateMachine.states,
                               transitions=StateMachine.transitions, initial='on_bad_half')


class Handler(object):
    state_machine = StateMachine()

    def process(self, msg):
        state, price, battery = self.state_machine.state.split('_')

        # Ask if network changed status
        curr_state = 'on' if msg.grid_status else 'off'
        if curr_state != state:
            if state == 'on':
                self.state_machine.off()
            else:
                self.state_machine.on()

        # Ask if prices changed
        if msg.selling_price == msg.buying_price and price == 'bad' or \
                                msg.selling_price < msg.buying_price and price == 'good':
            if price == 'bad':
                self.state_machine.good()
            else:
                self.state_machine.bad()

        # Ask if fullness changed
        if msg.bessSOC > 0.9:
            curr_battery = 'full'
        elif 0.25 <= msg.bessSOC <= 0.9:
            curr_battery = 'half'
        else:
            curr_battery = 'empty'

        if curr_battery != battery:
            if battery != 'half':
                self.state_machine.half()
            else:
                if curr_battery == 'full':
                    self.state_machine.full()
                else:
                    self.state_machine.empty()


        # For different states send different controls
        if self.state_machine.state == 'on_good_full':
            pow_ref = 6.0
        elif self.state_machine.state == 'on_good_half':
            pow_ref = 3.0
        elif self.state_machine.state == 'on_good_empty':
            pow_ref = 0.0
        elif self.state_machine.state == 'on_bad_full':
            pow_ref = 0.0
        elif self.state_machine.state == 'on_bad_half':
            pow_ref = 0.0
        elif self.state_machine.state == 'on_bad_empty':
            pow_ref = -3.0
        elif self.state_machine.state == 'off_good_full':
            pow_ref = 3.0
        elif self.state_machine.state == 'off_good_half':
            pow_ref = 0.0
        elif self.state_machine.state == 'off_good_empty':
            pow_ref = 0.0
        elif self.state_machine.state == 'off_bad_full':
            pow_ref = 0.0
        elif self.state_machine.state == 'off_bad_half':
            pow_ref = 0.0
        else: #'off_bad_empty'
            pow_ref = 0.0

        pow_ref = 0.0
        # Prepare response
        res = ResultsMessage(data_msg=msg,
                             load_one=True,
                             load_two=True,
                             load_three=True,
                             power_reference=pow_ref,
                             pv_mode=PVMode.ON)

        print('BamBam: {}'.format(msg))
        print(self.state_machine.state)
        print("=" * 50)
        return res
