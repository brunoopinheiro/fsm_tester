from transitions.extensions import GraphMachine


class SinkStateMachine:
    states = ['A', 'B', 'C', 'D', 'E', 'G', 'F']

    transitions = [
        {'trigger': 'go_to_B', 'source': 'A', 'dest': 'B'},
        {'trigger': 'go_to_C', 'source': 'B', 'dest': 'C'},
        {'trigger': 'go_to_D', 'source': 'C', 'dest': 'D'},
        {'trigger': 'go_to_E', 'source': 'D', 'dest': 'E'},
        {'trigger': 'go_to_G', 'source': 'E', 'dest': 'G', 'unless': 'is_defective'},  # noqa
        {'trigger': 'defective_op', 'source': 'E', 'dest': 'F'},
        {'trigger': 'end_operation', 'source': 'G', 'dest': 'A'},
        {'trigger': 'retry_F', 'source': 'F', 'dest': 'F'},
    ]

    def __init__(self):
        self.machine = GraphMachine(
            model=self,
            states=SinkStateMachine.states,
            transitions=SinkStateMachine.transitions,
            initial='A',
        )
        self.defective = False

    def is_defective(self):
        return self.defective

    def trigger_defective(self):
        self.defective = True
