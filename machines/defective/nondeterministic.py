from transitions.extensions import GraphMachine


class NondeterministicMachine:
    states = ['A', 'B', 'C', 'D', 'E', 'F', 'Finish']

    transitions = [
        {'trigger': 'go_to_B', 'source': 'A', 'dest': 'B'},
        {'trigger': 'go_to_C', 'source': 'B', 'dest': 'C'},
        {'trigger': 'go_to_D', 'source': 'C', 'dest': 'D'},
        {'trigger': 'go_to_E', 'source': 'D', 'dest': 'E'},
        {'trigger': 'go_to_F', 'source': 'E', 'dest': 'F'},
        {'trigger': 'end_operation', 'source': 'E', 'dest': 'Finish'},
    ]

    def __init__(self):
        self.machine = GraphMachine(
            model=self,
            states=NondeterministicMachine.states,
            transitions=NondeterministicMachine.transitions,
            initial='A',
        )
