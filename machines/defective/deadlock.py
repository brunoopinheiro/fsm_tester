from transitions.extensions import GraphMachine


class DeadlockMachine:
    states = ['A', 'B', 'C', 'D', 'E', 'F', 'Finish']

    transitions = [
        {'trigger': 'go_to_B', 'source': 'A', 'dest': 'B'},
        {'trigger': 'go_to_C', 'source': 'B', 'dest': 'C'},
        {'trigger': 'go_to_D', 'source': 'C', 'dest': 'D'},
        {'trigger': 'go_to_E', 'source': 'D', 'dest': 'E'},
        {'trigger': 'go_to_F', 'source': 'E', 'dest': 'F', 'unless': 'is_defective'},  # noqa
        {'trigger': 'defective_op', 'source': 'E', 'dest': 'C', 'conditions': 'is_defective'},  # noqa
        {'trigger': 'end_operation', 'source': 'F', 'dest': 'Finish'},
    ]

    def __init__(self):
        self.machine = GraphMachine(
            model=self,
            states=DeadlockMachine.states,
            transitions=DeadlockMachine.transitions,
            initial='A',
        )
        self.defective = False

    def is_defective(self):
        return self.defective

    def trigger_defective(self):
        self.defective = True
