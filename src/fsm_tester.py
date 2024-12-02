import networkx as nx

from unittest import TestSuite, TestCase
from unittest.runner import TextTestRunner
from src.adapters import (
    BaseAdapter,
    TransitionsAdapter,
)
from src.entities import FSMProtocol
from typing import Literal


DIALECTS = Literal['pytransitions', 'python-statemachine']


class FSMTester():

    def __initiate_adapter(
        self,
        fsm_module: FSMProtocol,
        dialect: DIALECTS,
    ) -> BaseAdapter:
        """With the given FSM module and dialect, return the appropriate
        adapter that will be used to interpret the FSM module.

        Args:
            fsm_module (FSMProtocol): The FSM Module implementation under test.
            dialect (DIALECTS): The dialect of the FSM module.

        Raises:
            NotImplementedError: For State Machine implementations not yet
                implemented.
            ValueError: For dialects not recognized.

        Returns:
            BaseAdapter: The adapter that will be used to interpret the FSM
        """
        if dialect == 'pytransitions':
            return TransitionsAdapter(fsm_module)
        elif dialect == 'python-statemachine':
            raise NotImplementedError(
                'Python State Machine not implemented yet.')
        else:
            raise ValueError('Dialect not recognized.')

    def unreachable_states(self) -> TestSuite:
        """Generate test cases to check if there are unreachable states in the
        FSM.

        Returns:
            TestSuite: A test suite containing test cases for each state in the
                FSM.
        """

        def test_case_name(state: str) -> str:
            """Generate a test case name for the given state.

            Args:
                state (str): The state to generate a test case name for.

            Returns:
                str: The test case name.
            """
            return f"test_unreachable_{state}"

        def test_unreachable(state: str) -> callable:
            """Generate a test function that will check if the given state is
            unreachable.

            Args:
                state (str): The state to check for reachability.

            Returns:
                callable: The test function.
            """
            def assert_function(*args, **kwargs):
                assert nx.has_path(
                        self.graph,
                        source=self.adapter.initial_state,
                        target=state,
                    )
            return assert_function

        testsuite = TestSuite()
        setattr(
            testsuite,
            'fail_msg',
            'Unreachable States Detected',
        )
        for state in self.graph.nodes:
            testcase_name = test_case_name(state)
            _callable = test_unreachable(state)
            _callable.__name__ = testcase_name
            setattr(
                TestCase,
                f'{testcase_name}',
                _callable,
            )
            testcase = TestCase(
                testcase_name,
            )
            testcase._class_cleanups = list()
            testsuite.addTest(testcase)
        return testsuite

    def sink_states(self) -> TestSuite:

        def test_case_name(state: str) -> str:
            return f"test_sink_{state}"

        def test_sink(state: str, final_state: str) -> callable:
            def assert_function(*args, **kwargs):
                is_endstate = state == final_state
                successors = list(self.graph.successors(state))
                has_successors = len(successors) > 0
                escape_path = list()
                for s_state in successors:
                    has_escape = nx.has_path(
                        self.graph,
                        source=s_state,
                        target=final_state,
                    )
                    if s_state == final_state:
                        has_escape = True
                    escape_path.append(has_escape)
                assert (is_endstate is True or
                        (has_successors is True
                         and all(escape_path)))
            return assert_function

        testsuite = TestSuite()
        setattr(
            testsuite,
            'fail_msg',
            'Sink States Detected',
        )
        for state in self.graph.nodes:
            testcase_name = test_case_name(state)
            _callable = test_sink(state, self.final_state)
            _callable.__name__ = testcase_name
            setattr(
                TestCase,
                f'{testcase_name}',
                _callable,
            )
            testcase = TestCase(
                testcase_name,
            )
            testcase._class_cleanups = list()
            testsuite.addTest(testcase)
        return testsuite

    def __init__(
        self,
        fsm_module: FSMProtocol,
        final_state: str,
        dialect: DIALECTS = 'pytransitions',
        verbosity=2,
        *args,
        **kwargs,
    ) -> None:
        self.adapter = self.__initiate_adapter(fsm_module, dialect)
        self.final_state = final_state
        self.graph = self.adapter.get_graph()
        self.test_runner = TextTestRunner(
            verbosity=verbosity,
        )
        self.suites = list()
        unreachable_states_suite = self.unreachable_states()
        self.suites.append(unreachable_states_suite)
        sink_states_suite = self.sink_states()
        self.suites.append(sink_states_suite)
        self.exit = True

    @staticmethod
    def _report_errors(fail_msg_base: str, failure_results: list) -> str:
        summary_info = fail_msg_base
        for failure in failure_results:
            summary_info += str(failure)
        return summary_info

    def run_tests(self):
        """Run all the test suites generated by the FSMTester."""
        for suite in self.suites:
            suite_results = list()
            failures = list()
            for test in suite:
                self.test = test
                result = self.test_runner.run(test)
                is_successful = result.wasSuccessful()
                if not is_successful:
                    failures.append(test)
                suite_results.append(is_successful)
            errors_report = self._report_errors(suite.fail_msg, failures)
            assert all(suite_results), errors_report
