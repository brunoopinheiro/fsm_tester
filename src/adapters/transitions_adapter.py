# https://networkx.org/documentation/stable/
from adapters.base_adapter import (
    BaseAdapter,
    FSMState,
    FSMTransition,
    TestCase,
)
import networkx as nx
from tempfile import NamedTemporaryFile
from typing import List


class TransitionsAdapter(BaseAdapter):

    def get_test_cases(self):
        transitions = self.fsm.transitions
        test_cases = []
        for tr in transitions:
            source = tr['source']
            dest = tr['dest']
            trigger = tr['trigger']
            conditions = tr.get('conditions', None)
            unless = tr.get('unless', None)

            name = f"{source} -> {dest} by {trigger}"
            test_case = TestCase(
                name=name,
                source=source,
                dest=dest,
                trigger=trigger,
                condition=conditions,
                unless=unless,
            )

            test_cases.append(test_case)
        return test_cases

    def get_states(self) -> List[FSMState]:
        states = self.fsm.states
        fsm_states = []
        for state in states:
            name = state['name']
            on_enter = state.get('on_enter', None)
            on_exit = state.get('on_exit', None)

            fsm_state = FSMState(
                name=name,
                on_enter=on_enter,
                on_exit=on_exit,
            )
            fsm_states.append(fsm_state)
        return fsm_states

    def get_transitions(self):
        transitions = self.fsm.transitions
        fsm_transitions = []
        for tr in transitions:
            name = tr['trigger']
            source = tr['source']
            dest = tr['dest']
            conditions = tr.get('conditions', None)
            unless = tr.get('unless', None)
            before = tr.get('before', None)
            after = tr.get('after', None)

            fsm_transition = FSMTransition(
                name=name,
                source=source,
                destination=dest,
                conditions=conditions,
                unless=unless,
                before=before,
                after=after,
            )
            fsm_transitions.append(fsm_transition)
        return fsm_transitions

    def get_tree(self):
        # TODO: alterar dotfile com conditions etc
        with NamedTemporaryFile(mode='wt', delete_on_close=False) as fp:
            fp.write(self.fsm.get_graph().source)
            fp.close()

            graph = nx.drawing.nx_pydot.read_dot(fp.name)
        return graph
