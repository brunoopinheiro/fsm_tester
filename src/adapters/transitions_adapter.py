# https://networkx.org/documentation/stable/
from tempfile import NamedTemporaryFile
import networkx as nx
from adapters.base_adapter import BaseAdapter, TestCase


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

    def get_states(self):
        ...

    def get_transitions(self):
        ...

    def get_tree(self):
        with NamedTemporaryFile(mode='wt', delete_on_close=False) as fp:
            fp.write(self.fsm.get_graph().source)
            fp.close()

            graph = nx.drawing.nx_pydot.read_dot(fp.name)
        return graph
