import unittest
from should_dsl import should
from fluidity import StateMachine, state, transition
from fluidity import GuardNotSatisfied

footsteps = []


class Foo:
  def bar(self):
      footsteps.append('exit looking')


foo = Foo()

def enter_falling_function():
    footsteps.append('enter falling')


class JumperGuy(StateMachine):
    state('looking', enter=lambda jumper: jumper.append('enter looking'),
                     exit=foo.bar)
    state('falling', enter=enter_falling_function)
    initial_state = 'looking'

    transition(from_='looking', event='jump', to='falling',
               action=lambda jumper: jumper.append('action jump'),
               guard=lambda jumper: jumper.append('guard jump') is None)

    def __init__(self):
        StateMachine.__init__(self)

    def append(self, text):
        footsteps.append(text)


class CallableSupport(unittest.TestCase):

    def test_every_callback_can_be_a_callable(self):
        '''every callback can be a callable'''
        guy = JumperGuy()
        guy.jump()
        footsteps |should| have(5).elements
        footsteps |should| include_all_of([
            'enter looking', 'exit looking', 'enter falling',
            'action jump', 'guard jump'])

    def test_it_should_deny_state_change_if_guard_callable_returns_false(self):
        class Door(StateMachine):
            state('open')
            state('closed')
            initial_state = 'closed'
            transition(from_='closed', event='open', to='open',
                       guard=lambda d: not door.locked)
            def locked(self):
                return self.locked

        door = Door()
        door.locked = True
        door.open |should| throw(GuardNotSatisfied)


if __name__ == '__main__':
    unittest.main()

