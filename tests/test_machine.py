import pytest
from unittest.mock import Mock
from src.testcase import TestCase
from src.assembly_line_impl.main import AssemblyLine
from typing import List


# TODO: Conditions and Unless Mocks
# TODO: Tree Traversal to check whole FSM Path
# TODO: Obj Oriented Project Structure


def _generate_test_parameters(fsm) -> List[TestCase]:
    transitions = fsm.transitions
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


fsm = AssemblyLine()


@pytest.mark.parametrize(
    'test_case',
    [test_case for test_case in _generate_test_parameters(fsm)]
)
def test_machine_execution(test_case: TestCase, monkeypatch):
    statemachine: AssemblyLine = fsm
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
