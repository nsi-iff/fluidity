import unittest
from should_dsl import should
from fluidity import StateMachine, state, transition


class Door(StateMachine):

    state('open')
    state('closed')
    state('broken')
    initial_state = 'closed'
    
    transition(from_='closed', event='open', to='open')
    transition(from_='open', event='close', to='closed')
    transition(from_='closed', event='crack', to='broken')
    
    def __init__(self):
        self.state_changes = []
        super(Door, self).__init__()
        
    def changing_state(self, from_, to):
        self.state_changes.append((from_, to))
    
    
class StateChangeNotificationSpec(unittest.TestCase):

    def test_notify_state_changes(self):
        door = Door()
        door.open()
        door.close()
        door.crack()
        
        door.state_changes |should| equal_to(
            [('closed', 'open'),
             ('open', 'closed'),
             ('closed', 'broken')])
    
