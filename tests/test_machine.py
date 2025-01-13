import pytest  # noqa
from machines.assembly_line_impl.main import AssemblyLine
from fsm_tester.fsm_tester import FSMTester


@pytest.fixture
def fsm_tester():
    return FSMTester(
        AssemblyLine,
        dialect='pytransitions',
        final_state='Finish',
        expected_loops=3,
    )


def test_unreachable_states_suite(fsm_tester):
    suite = fsm_tester.unreachable_states_suite
    fsm_tester.run(suite)


def test_sink_states_suite(fsm_tester):
    suite = fsm_tester.sink_states_suite
    fsm_tester.run(suite)


def test_nondeterministic_transition_suite(fsm_tester):
    suite = fsm_tester.nondeterministic_transition_suite
    fsm_tester.run(suite)


def test_machine_execution_suite(fsm_tester):
    suite = fsm_tester.machine_execution_suite
    fsm_tester.run(suite)


def test_deadlock_states_suite(fsm_tester):
    suite = fsm_tester.deadlock_states_suite
    fsm_tester.run(suite)
