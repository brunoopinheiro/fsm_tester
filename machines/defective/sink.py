from transitions.extensions import GraphMachine


class SimpleMachineWithSinkState:
    states = ['A', 'B', 'C', 'Sink', 'Finish']

    transitions = [
        {'trigger': 'go_to_B', 'source': 'A', 'dest': 'B'},
        {'trigger': 'go_to_C', 'source': 'B', 'dest': 'C'},
        {'trigger': 'end_operation', 'source': 'B', 'dest': 'Finish'},
        {'trigger': 'go_to_Sink', 'source': 'C', 'dest': 'Sink'},
        {'trigger': 'retry', 'source': 'Sink', 'dest': 'Sink'},
        {'trigger': 'restart', 'source': 'Sink', 'dest': 'C'},
    ]

    def __init__(self):
        self.machine = GraphMachine(
            model=self,
            states=SimpleMachineWithSinkState.states,
            transitions=SimpleMachineWithSinkState.transitions,
            initial='A',
        )
