from transitions import Machine
from hackathon.utils.utils import ResultsMessage, PVMode


class StateMachine(object):
    states = [
        'on_empty_none',  'on_empty_third', 'on_empty_secthr',
        'on_half_none',   'on_half_third',  'on_half_secthr',
        'on_full_none',   'on_full_third', 'on_full_secthr',

        'off_empty_none', 'off_empty_third', 'off_empty_secthr',
        'off_half_none',  'off_half_third', 'off_half_secthr',
        'off_full_none',  'off_full_third', 'off_full_secthr'
    ]

    transitions = [
        # on_empty_none
        {'trigger': 'off', 'source': 'on_empty_none', 'dest': 'off_empty_none'},
        {'trigger': 'half', 'source': 'on_empty_none', 'dest': 'on_half_none'},
        {'trigger': 'third', 'source': 'on_empty_none', 'dest': 'on_empty_third'},
        # on_empty_third
        {'trigger': 'off', 'source': 'on_empty_third', 'dest': 'off_empty_third'},
        {'trigger': 'half', 'source': 'on_empty_third', 'dest': 'on_half_third'},
        {'trigger': 'none', 'source': 'on_empty_third', 'dest': 'on_empty_none'},
        {'trigger': 'secthr', 'source': 'on_empty_third', 'dest': 'on_empty_secthr'},
        # on_empty_secthr
        {'trigger': 'off', 'source': 'on_empty_secthr', 'dest': 'off_empty_secthr'},
        {'trigger': 'half', 'source': 'on_empty_secthr', 'dest': 'on_half_secthr'},
        {'trigger': 'third', 'source': 'on_empty_secthr', 'dest': 'on_empty_third'},
        # on_half_none
        {'trigger': 'off', 'source': 'on_half_none', 'dest': 'off_half_none'},
        {'trigger': 'full', 'source': 'on_half_none', 'dest': 'on_full_none'},
        {'trigger': 'empty', 'source': 'on_half_none', 'dest': 'on_empty_none'},
        {'trigger': 'third', 'source': 'on_half_none', 'dest': 'on_half_third'},
        # on_half_third
        {'trigger': 'off', 'source': 'on_half_third', 'dest': 'off_half_third'},
        {'trigger': 'full', 'source': 'on_half_third', 'dest': 'on_full_third'},
        {'trigger': 'empty', 'source': 'on_half_third', 'dest': 'on_empty_third'},
        {'trigger': 'none', 'source': 'on_half_third', 'dest': 'on_half_none'},
        {'trigger': 'secthr', 'source': 'on_half_third', 'dest': 'on_half_secthr'},
        # on_half_secthr
        {'trigger': 'off', 'source': 'on_half_secthr', 'dest': 'off_half_secthr'},
        {'trigger': 'full', 'source': 'on_half_secthr', 'dest': 'on_full_secthr'},
        {'trigger': 'empty', 'source': 'on_half_secthr', 'dest': 'on_empty_secthr'},
        {'trigger': 'third', 'source': 'on_half_secthr', 'dest': 'on_half_third'},
        # on_full_none
        {'trigger': 'off', 'source': 'on_full_none', 'dest': 'off_full_none'},
        {'trigger': 'half', 'source': 'on_full_none', 'dest': 'on_half_none'},
        {'trigger': 'third', 'source': 'on_full_none', 'dest': 'on_full_third'},
        # on_full_third
        {'trigger': 'off', 'source': 'on_full_third', 'dest': 'off_full_third'},
        {'trigger': 'half', 'source': 'on_full_third', 'dest': 'on_half_third'},
        {'trigger': 'secthr', 'source': 'on_full_third', 'dest': 'on_full_secthr'},
        {'trigger': 'none', 'source': 'on_full_third', 'dest': 'on_full_none'},
        # on_full_secthr
        {'trigger': 'off', 'source': 'on_full_secthr', 'dest': 'off_full_secthr'},
        {'trigger': 'half', 'source': 'on_full_secthr', 'dest': 'on_half_secthr'},
        {'trigger': 'third', 'source': 'on_full_secthr', 'dest': 'on_full_third'},
        # off_empty_none
        {'trigger': 'on', 'source': 'off_empty_none', 'dest': 'on_empty_none'},
        {'trigger': 'half', 'source': 'off_empty_none', 'dest': 'off_half_none'},
        {'trigger': 'third', 'source': 'off_empty_none', 'dest': 'off_empty_third'},
        # off_empty_third
        {'trigger': 'on', 'source': 'off_empty_third', 'dest': 'on_empty_third'},
        {'trigger': 'half', 'source': 'off_empty_third', 'dest': 'off_half_third'},
        {'trigger': 'secthr', 'source': 'off_empty_third', 'dest': 'off_empty_secthr'},
        {'trigger': 'none', 'source': 'off_empty_third', 'dest': 'off_empty_none'},
        # off_empty_secthr
        {'trigger': 'on', 'source': 'off_empty_secthr', 'dest': 'on_empty_secthr'},
        {'trigger': 'half', 'source': 'off_empty_secthr', 'dest': 'off_half_secthr'},
        {'trigger': 'third', 'source': 'off_empty_secthr', 'dest': 'off_empty_third'},
        # off_half_none
        {'trigger': 'on', 'source': 'off_half_none', 'dest': 'on_half_none'},
        {'trigger': 'full', 'source': 'off_half_none', 'dest': 'off_full_none'},
        {'trigger': 'empty', 'source': 'off_half_none', 'dest': 'off_empty_none'},
        {'trigger': 'third', 'source': 'off_half_none', 'dest': 'off_half_third'},
        # off_half_third
        {'trigger': 'on', 'source': 'off_half_third', 'dest': 'on_half_third'},
        {'trigger': 'full', 'source': 'off_half_third', 'dest': 'off_full_third'},
        {'trigger': 'empty', 'source': 'off_half_third', 'dest': 'off_empty_third'},
        {'trigger': 'secthr', 'source': 'off_half_third', 'dest': 'off_half_secthr'},
        {'trigger': 'none', 'source': 'off_half_third', 'dest': 'off_half_none'},
        # off_half_secthr
        {'trigger': 'on', 'source': 'off_half_secthr', 'dest': 'on_half_secthr'},
        {'trigger': 'full', 'source': 'off_half_secthr', 'dest': 'off_full_secthr'},
        {'trigger': 'empty', 'source': 'off_half_secthr', 'dest': 'off_empty_secthr'},
        {'trigger': 'third', 'source': 'off_half_secthr', 'dest': 'off_half_third'},
        # off_full_none
        {'trigger': 'on', 'source': 'off_full_none', 'dest': 'on_full_none'},
        {'trigger': 'half', 'source': 'off_full_none', 'dest': 'off_half_none'},
        {'trigger': 'third', 'source': 'off_full_none', 'dest': 'off_full_third'},
        # off_full_third
        {'trigger': 'on', 'source': 'off_full_third', 'dest': 'on_full_third'},
        {'trigger': 'half', 'source': 'off_full_third', 'dest': 'off_half_third'},
        {'trigger': 'secthr', 'source': 'off_full_third', 'dest': 'off_full_secthr'},
        {'trigger': 'none', 'source': 'off_full_third', 'dest': 'off_full_none'},
        # off_full_secthr
        {'trigger': 'on', 'source': 'off_full_secthr', 'dest': 'on_full_secthr'},
        {'trigger': 'half', 'source': 'off_full_secthr', 'dest': 'off_half_secthr'},
        {'trigger': 'third', 'source': 'off_full_secthr', 'dest': 'off_full_third'}
    ]

    def __init__(self):
        self.machine = Machine(self, states=StateMachine.states,
                               transitions=StateMachine.transitions, initial='on_half_none')


class Handler(object):
    state_machine = StateMachine()
    third_cons = 0
    sec_cons = 0
    total_cons = 0

    def process(self, msg):
        state, battery, disabled = self.state_machine.state.split('_')

        # Ask if network changed status
        curr_state = 'on' if msg.grid_status else 'off'
        if curr_state != state:
            if state == 'on':
                self.state_machine.off()
            else:
                self.state_machine.on()

        # Ask if fullness changed
        if msg.bessSOC > 0.8:
            curr_battery = 'full'
        elif 0.2 <= msg.bessSOC <= 0.8:
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

        # Ask if some devices should be powered on or off
        if state == 'on':
            if disabled == 'secthr':
                self.state_machine.third()
            elif disabled == 'third':
                self.state_machine.none()

        else:
            if msg.bessOverload and disabled == 'none':
                self.state_machine.third()

            elif msg.bessOverload and disabled == 'third':
                self.state_machine.secthr()

            elif not msg.bessOverload and msg.bessPower > float(0) and disabled == 'secthr':
                self.state_machine.third()

            elif not msg.bessOverload and msg.bessPower > float(0) and disabled == 'third':
                self.state_machine.none()

        # For different states send different controls
        if self.state_machine.state.startswith('on'):
            if self.state_machine.state == 'on_empty_none':
                load_two = True
                load_three = True
                if msg.buying_price == float(8):
                    if msg.solar_production > float(0.5):
                        pow_ref = 0.0
                    else:
                        pow_ref = -3.0
                else:
                    pow_ref = -6.0

            elif self.state_machine.state == 'on_empty_third':
                load_two = True
                load_three = False
                if msg.buying_price == float(8):
                    if msg.solar_production > float(0.5):
                        pow_ref = 0.0
                    else:
                        pow_ref = -3.0
                else:
                    pow_ref = -6.0

            elif self.state_machine.state == 'on_empty_secthr':
                load_two = False
                load_three = False
                if msg.buying_price == float(8):
                    if msg.solar_production > float(0.5):
                        pow_ref = 0.0
                    else:
                        pow_ref = -3.0
                else:
                    pow_ref = -6.0

            elif self.state_machine.state == 'on_half_none':
                load_two = True
                load_three = True
                if msg.buying_price == float(8):
                    if msg.solar_production > 0.5:
                        pow_ref = 0.0
                    else:
                        pow_ref = -2.0
                elif msg.selling_price == float(3):
                    pow_ref = 2.0
                else:
                    pow_ref = 0.0

            elif self.state_machine.state == 'on_half_third':
                load_two = True
                load_three = False
                if msg.buying_price == float(8):
                    if msg.solar_production > 0.5:
                        pow_ref = 0.0
                    else:
                        pow_ref = -2.0
                elif msg.selling_price == float(3):
                    pow_ref = 2.0
                else:
                    pow_ref = 0.0

            elif self.state_machine.state == 'on_half_secthr':
                load_two = False
                load_three = False
                if msg.buying_price == float(8):
                    if msg.solar_production > 0.5:
                        pow_ref = 0.0
                    else:
                        pow_ref = -2.0
                elif msg.selling_price == float(3):
                    pow_ref = 2.0
                else:
                    pow_ref = 0.0

            elif self.state_machine.state == 'on_full_none':
                load_two = True
                load_three = True
                pow_ref = 0.0

            elif self.state_machine.state == 'on_full_third':
                load_two = True
                load_three = False
                if msg.buying_price == float(8):
                    pow_ref = 2.0
                else:
                    pow_ref = 0.0

            elif self.state_machine.state == 'on_full_secthr':
                load_two = False
                load_three = False
                if msg.buying_price == float(8):
                    pow_ref = 2.0
                else:
                    pow_ref = 0.0
        else:
            pow_ref = 0.0
            if self.state_machine.state == 'off_empty_none':
                load_two = True
                load_three = True

            elif self.state_machine.state == 'off_empty_third':
                load_two = True
                load_three = False

            elif self.state_machine.state == 'off_empty_secthr':
                load_two = False
                load_three = False

            elif self.state_machine.state == 'off_half_none':
                load_two = True
                load_three = True
            elif self.state_machine.state == 'off_half_third':
                load_two = True
                load_three = False

            elif self.state_machine.state == 'off_half_secthr':
                load_two = False
                load_three = False

            elif self.state_machine.state == 'off_full_none':
                load_two = True
                load_three = True

            elif self.state_machine.state == 'off_full_third':
                load_two = True
                load_three = False

            elif self.state_machine.state == 'off_full_secthr':
                load_two = False
                load_three = False


        # Prepare response
        res = ResultsMessage(data_msg=msg,
                             load_one=True,
                             load_two=load_two,
                             load_three=load_three,
                             power_reference=pow_ref,
                             pv_mode=PVMode.ON)

        print('BamBam: {}'.format(res))
        print(self.state_machine.state)
        print(self.third_cons)
        print(self.sec_cons)
        print("=" * 50)
        return res
