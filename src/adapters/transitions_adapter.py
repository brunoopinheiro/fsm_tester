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

    def __init__(self, fsm):
        super().__init__(fsm)
        self.__initial_state = self.fsm.machine.initial

    @property
    def initial_state(self) -> str:
        # documentation provided by base_adapter.py
        return self.__initial_state

    def get_test_cases(self):
        # documentation provided by base_adapter.py
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
        # documentation provided by base_adapter.py
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
        # documentation provided by base_adapter.py
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

    def __get_state_methods(self):
        state_methods = set()
        for state in self.fsm.states:
            on_enter = state.get('on_enter', None)
            on_exit = state.get('on_exit', None)
            if on_enter is not None:
                for callback in on_enter:
                    state_methods.add(callback)
            if on_exit is not None:
                for callback in on_exit:
                    state_methods.add(callback)
        return state_methods

    def __get_transition_methods(self):
        transition_methods = set()
        for transition in self.fsm.transitions:
            conditions = transition.get('conditions', None)
            unless = transition.get('unless', None)
            if conditions is not None:
                for condition in conditions:
                    transition_methods.add(condition)
            if unless is not None:
                for condition in unless:
                    transition_methods.add(condition)
        return transition_methods

    def get_methods(self) -> set:
        # documentation provided by base_adapter.py
        state_methods = self.__get_state_methods()
        transition_methods = self.__get_transition_methods()
        return state_methods.union(transition_methods)

    def __runtime_evaluators(self, runtime_methods: set):
        model_logic = [state.get('name', None)
                       for state in self.fsm.states]
        for method in model_logic:
            runtime_methods.add(f'is_{method}')
            runtime_methods.add(f'may_{method}')
            runtime_methods.add(f'may_to_{method}')
            runtime_methods.add(f'to_{method}')

    def __declared_transitions(self, runtime_methods: set):
        for transition in self.fsm.transitions:
            trigger = transition.get('trigger', None)
            runtime_methods.add(trigger)
            runtime_methods.add(f'may_{trigger}')

    def __transitions_runtime_methods(self):
        runtime_methods = set()
        self.__runtime_evaluators(runtime_methods)
        self.__declared_transitions(runtime_methods)
        runtime_methods.add('trigger')
        runtime_methods.add('may_trigger')
        return runtime_methods

    def mimic_attributes(self) -> set:
        # documentation provided by base_adapter.py
        stolen_methods = set()
        runtime_methods = self.__transitions_runtime_methods()
        for attribute in dir(self.fsm):
            not_magic = not (attribute.startswith('__')
                             and attribute.endswith('__'))
            not_runtime_methods = attribute not in runtime_methods
            condition = (not_magic and not_runtime_methods)
            if condition:
                setattr(self, attribute, getattr(self.fsm, attribute))
                stolen_methods.add(attribute)
        return stolen_methods

    def get_tree(self):
        # TODO: alterar dotfile com conditions etc
        with NamedTemporaryFile(mode='wt', delete_on_close=False) as fp:
            fp.write(self.fsm.get_graph().source)
            fp.close()

            graph = nx.drawing.nx_pydot.read_dot(fp.name)
        return graph
