import unittest
from should_dsl import should, should_not
from fluidity import StateMachine, state, transition
from fluidity import InvalidTransition


class MyMachine(StateMachine):

    initial_state = 'off'

    state('off', enter='inc_off')
    state('on', enter='inc_on')

    transition(from_='off', event='toggle', to='on')
    transition(from_='on', event='toggle', to='off')

    def __init__(self):
        self.off_count = 0
        self.on_count = 0
        super(MyMachine, self).__init__()

    def inc_off(self):
        self.off_count += 1

    def inc_on(self):
        self.on_count += 1


class MachineIndependence(unittest.TestCase):

    def test_two_machines_dont_share_transitions(self):
        machine_a = MyMachine()
        machine_b = MyMachine()

        machine_a.current_state |should| equal_to('off')
        machine_b.current_state |should| equal_to('off')

        machine_a.toggle()

        machine_a.current_state |should| equal_to('on')
        machine_b.current_state |should| equal_to('off')

    def test_two_machines_dont_share_actions(self):
        machine_a = MyMachine()
        machine_b = MyMachine()

        machine_a.on_count |should| equal_to(0)
        machine_b.on_count |should| equal_to(0)

        machine_a.toggle()

        machine_a.on_count |should| equal_to(1)
        machine_b.on_count |should| equal_to(0)



