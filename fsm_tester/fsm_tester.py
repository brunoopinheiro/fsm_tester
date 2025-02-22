from unittest.runner import TextTestRunner
from unittest.case import TestCase
from unittest.suite import TestSuite
from pathlib import Path
from rich import terminal_theme
from rich.traceback import install
from fsm_tester.adapters import (
    AdapterFactory,
)
from fsm_tester.entities import FSMProtocol
from fsm_tester.components.graph_analyzer import GraphAnalyzer
from fsm_tester.components.machine_mocker import MachineMocker
from fsm_tester.components.rich_console import RichConsole as Console
from fsm_tester.typing import DIALECTS


class FSMTester():

    test_suites = [
        'unreachable_states_suite',
        'sink_states_suite',
        'nondeterministic_transition_suite',
        'machine_execution_suite',
        'deadlock_states_suite',
    ]

    def __init__(
        self,
        fsm_module: FSMProtocol,
        final_state: str,
        dialect: DIALECTS = 'pytransitions',
        expected_loops: int = 0,
        save_report: bool = False,
        report_dir: str = 'reports',
        verbosity=2,
        *args,
        **kwargs,
    ) -> None:
        if not isinstance(fsm_module, FSMProtocol):
            raise TypeError(
                'The FSM Module must implement the FSMProtocol.'
            )
        self.adapter = AdapterFactory.create_adapter(fsm_module, dialect)
        self.final_state = final_state
        self.graph = self.adapter.get_graph()
        self.console = Console(
            record=save_report,
        )
        self.save_report = save_report
        self.reports_path = Path(report_dir)
        self.reports_path.mkdir(exist_ok=True)
        self.test_runner = TextTestRunner(
            verbosity=verbosity,
            stream=self.console,
        )
        self.graph_analyzer = GraphAnalyzer(
            graph=self.graph,
            initial_state=self.adapter.initial_state,
            final_state=self.final_state,
        )
        self.machine_mocker = MachineMocker(
            adapter=self.adapter,
            expected_loops=expected_loops,
            final_state=final_state,
        )
        self.suites = list()
        self.suites.append(self.graph_analyzer.unreachable_states_suite())
        self.suites.append(self.graph_analyzer.sink_states_suite())
        self.suites.append(
            self.graph_analyzer.nondeterministic_transition_suite(
                transitions=self.adapter.get_transitions(),
            )
        )
        # maybe this part should be executed only if the graph tests pass
        self.suites.append(
            self.machine_mocker.unreachable_states_suite(),
        )
        self.exit = True

    @property
    def unreachable_states_suite(self) -> TestSuite:
        return self.graph_analyzer.unreachable_states_suite()

    @property
    def sink_states_suite(self) -> TestSuite:
        return self.graph_analyzer.sink_states_suite()

    @property
    def nondeterministic_transition_suite(self) -> TestSuite:
        return self.graph_analyzer.nondeterministic_transition_suite(
            transitions=self.adapter.get_transitions(),
        )

    @property
    def machine_execution_suite(self) -> TestSuite:
        return self.machine_mocker.unreachable_states_suite()

    @property
    def deadlock_states_suite(self) -> TestSuite:
        return self.machine_mocker.dead_lock_suite()

    def __getitem__(self, name):
        if name in FSMTester.test_suites:
            return super(FSMTester, self).__getattribute__(name)
        raise KeyError(f'{name} is not a valid test suite.')

    @staticmethod
    def _report_errors(fail_msg_base: str, failure_results: list) -> str:
        """Generates a summary of the errors found during the test run.

        Args:
            fail_msg_base (str): The base message to be displayed in the
                summary.
            failure_results (list): A list of the failures found during the
                test run.

        Returns:
            str: A summary of the errors found during the test run.
        """
        summary_info = f'[{fail_msg_base}]: '
        for failure in failure_results:
            summary_info += str(failure)
        return summary_info

    def run(self, test_suite: TestSuite):
        """Runs a test suite.

        Args:
            test_suite (TestSuite): A test suite to be run.
        """
        install(
            console=self.console,
            show_locals=True,
        )
        self.console.print(
            f'FSMTester: Running {test_suite.suite_name}...',
            justify='center',
            style='bold black on green',
        )
        self.console.print(
            '-----------------------------------\n\n',
            justify='center',
        )
        suite_results = list()
        failures = list()
        for test in test_suite:
            test: TestCase
            self.test = test
            result = self.test_runner.run(test)
            is_successful = result.wasSuccessful()
            if not is_successful:
                failures.append(test)
            suite_results.append(is_successful)
        errors_report = self._report_errors(test_suite.fail_msg, failures)
        if not all(suite_results) and self.save_report:
            self.console.save_html(
                f'{self.reports_path.resolve()}/report_{test_suite.suite_name}.html',  # noqa
                theme=terminal_theme.MONOKAI,
            )
        self.console.end_capture()
        assert all(suite_results), errors_report

    def run_tests(self):
        """Run all the test suites generated by the FSMTester."""
        for suite in self.suites:
            suite_results = list()
            failures = list()
            for test in suite:
                test: TestCase
                self.test = test
                result = self.test_runner.run(test)
                is_successful = result.wasSuccessful()
                if not is_successful:
                    failures.append(test)
                suite_results.append(is_successful)
            errors_report = self._report_errors(suite.fail_msg, failures)
            assert all(suite_results), errors_report
