import pytest  # noqa
from machines.assembly_line_impl.main import AssemblyLine
from machines.defective.unreachable import AssemblyLineUnreachable
from machines.defective.sink import SimpleMachineWithSinkState
from machines.simple.simple_machine import SimpleMachine
from src.fsm_tester import FSMTester


def test_simple_machine():
    fsm_tester = FSMTester(
        fsm_module=SimpleMachine,
        final_state='Finish',
        dialect='pytransitions',
    )
    fsm_tester.run_tests()


@pytest.mark.xfail
def test_unreachable_state_machine():
    fsm_tester = FSMTester(
        AssemblyLineUnreachable,
        dialect='pytransitions',
        final_state='Finish',
    )
    fsm_tester.run_tests()


@pytest.mark.xfail
def test_sink_state_machine():
    fsm_tester = FSMTester(
        SimpleMachineWithSinkState,
        dialect='pytransitions',
        final_state='Finish',
    )
    fsm_tester.run_tests()


def test_assembly_line():
    fsm_tester = FSMTester(
        AssemblyLine,
        dialect='pytransitions',
        final_state='Finish',
    )
    fsm_tester.run_tests()
