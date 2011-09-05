import unittest
from should_dsl import should, should_not
from fluidity import StateMachine, state, transition


class JumperGuy(StateMachine):
    state('looking')
    state('falling')
    initial_state = 'looking'
    transition(from_='looking', event='jump', to='falling')


class BooleanStateGettersSpec(unittest.TestCase):

    def it_has_boolean_getters_for_the_states(self):
        guy = JumperGuy()
        guy |should| respond_to('is_looking')
        guy |should| respond_to('is_falling')
        guy.current_state |should| equal_to('looking')
        guy |should| be_looking
        guy |should_not| be_falling

        guy.jump()
        guy |should_not| be_looking
        guy |should| be_falling

