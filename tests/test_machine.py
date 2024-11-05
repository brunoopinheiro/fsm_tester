import pytest  # noqa
from unittest.mock import Mock
from enum import Enum
from entities.testcase import TestCase
from src.assembly_line_impl.main import AssemblyLine
from typing import List


class LibAdapters(Enum):
    """Enumeration of all available adapters."""
    TRANSITIONS = 1
    PYTHON_STATEMACHINE = 2


class TestAssemblyLine:
    """Tests the AssemblyLine class, ensuring that all states are reachable and
    that the machine transitions between states correctly.
    """

    def setup_class(self):
        self.fsm = AssemblyLine()
        self.reachable_states = set()

    def setup_method(self):
        self.reachable_states.clear()

    def _generate_individual_transitions(self) -> List[TestCase]:
        """Generates individual test cases for each transition in the machine.

        Returns:
            List[TestCase]: A list of test cases for each transition in the
            machine.
        """
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

    def _test_machine_execution(self, test_case: TestCase, monkeypatch):
        """Tests the machine execution for a given test case. It mocks the
        conditions of the machine and ensures that the machine transitions
        to the expected state.

        Args:
            test_case (TestCase): The test case to be executed.
            monkeypatch (MonkeyPatch): The monkeypatch fixture.
        """
        statemachine: AssemblyLine = self.fsm
        if test_case.condition is not None:
            for condition in test_case.condition:
                spec = f'{statemachine.__module__}.{condition}'
                cmock = Mock(
                    spec=spec,
                    return_value=True,
                    name=condition,
                )
                monkeypatch.setattr(statemachine, condition, cmock)
            setattr(statemachine, 'state', test_case.source)
            statemachine.trigger(test_case.trigger)
            assert statemachine.state == test_case.dest
            self.reachable_states.add(test_case.dest)

            for condition in test_case.condition:
                spec = f'{statemachine.__module__}.{condition}'
                cmock = Mock(
                    spec=spec,
                    return_value=False,
                    name=condition,
                )
                monkeypatch.setattr(statemachine, condition, cmock)
            setattr(statemachine, 'state', test_case.source)
            statemachine.trigger(test_case.trigger)
            assert statemachine.state != test_case.dest
        else:
            setattr(statemachine, 'state', test_case.source)
            statemachine.trigger(test_case.trigger)
            assert statemachine.state == test_case.dest
            self.reachable_states.add(test_case.dest)

    def test_machine_states(self, monkeypatch):
        """Tests the machine states, ensuring that all states are reachable.
        Additionally, it tests the individual transitions between states.
        """
        self.reachable_states.add(self.fsm.machine.initial)
        test_cases = self._generate_individual_transitions()
        for test_case in test_cases:
            self._test_machine_execution(test_case, monkeypatch)
        assert self.reachable_states == set(self.fsm.machine.states)
