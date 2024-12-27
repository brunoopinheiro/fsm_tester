import pytest
from machines.assembly_line_impl.main import AssemblyLine
from src.fsm_tester import FSMTester


@pytest.fixture
def fsm_tester():
    return FSMTester(
        AssemblyLine,
        dialect='pytransitions',
        final_state='Finish',
        expected_loops=3,
    )


@pytest.mark.parametrize(
    'suite',
    FSMTester.test_suites,
)
def test_assembly_line(fsm_tester, suite):
    suite = fsm_tester[suite]
    fsm_tester.run(suite)
