from transitions.extensions import GraphMachine


class SimpleMachine:
    states = ['A', 'B', 'C', 'Finish']

    transitions = [
        {'trigger': 'go_to_B', 'source': 'A', 'dest': 'B'},
        {'trigger': 'go_to_C', 'source': 'B', 'dest': 'C'},
        {'trigger': 'end_operation', 'source': 'C', 'dest': 'Finish'},
    ]

    def __init__(self):
        self.machine = GraphMachine(
            model=self,
            states=SimpleMachine.states,
            transitions=SimpleMachine.transitions,
            initial='A',
        )
