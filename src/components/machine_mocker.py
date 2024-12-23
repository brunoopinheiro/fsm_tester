import networkx as nx
from unittest import TestSuite, TestCase
from unittest.mock import MagicMock
from src.typing import Adapter
from typing import List, Iterable


class MachineMocker:

    def __init__(
        self,
        adapter: Adapter,
    ):
        self.adapter = adapter
        self.transitions = self.adapter.get_transitions()
        self.graph = self.adapter.get_graph()
        callback = lambda attr_name, attr_value: setattr(self, attr_name, attr_value)  # noqa
        self.adapter.mimic_attributes(callback)

    @staticmethod
    def mock_ensemble(
        callable_ensemble: Iterable[str],
        callback: callable,
        expected_return_value: any = None,
    ) -> None:
        """Given a set of callables that needed to be mocked, and a callback
        function that will be called to inject the mock objects, this method
        will create the mock objects and inject them into the callback.

        Args:
            callback (callable): A function that will be called to inject the
                mock objects.
            callable_ensemble (Iterable[str]): A set of callables that need to
                be mocked.
        """
        callable_ensemble = list(callable_ensemble)
        for callable_ in callable_ensemble:
            mock = MagicMock(return_value=expected_return_value)
            callback(callable_, mock)

    def unreachable_states_suite(self) -> TestSuite:
        """Generate test cases to check if there are unreachable states in the
        FSM. This method will generate a test function for each state in the
        FSM, checking if the state is reachable from the initial state.

        Returns:
            TestSuite: A test suite containing test cases for each state in the
                FSM.
        """

        def test_path(path: List[str]) -> callable:
            """Generate a test function that will check if the given path is
            reachable. This function will execute each of the transitions in
            the path, from the initial state to the final state, asserting
            that the state attribute of the machine is the expected state
            after each transition.

            Args:
                path (List[str]): The path to check for reachability.

            Returns:
                callable: The test function.
            """

            def execute_transition(
                source: str,
                dest: str,
                adapter: Adapter,
            ) -> None:
                """Execute a transition from source to dest. This function
                shall execute each of the `before` functions in the transition
                definition, then mock the `conditions` and `unless` functions
                to allow the transition to happen, execute the transition
                and then execute each of the `after` functions in the
                transition definition.

                Args:
                    source (str): The source state of the transition.
                    dest (str): The destination state of the transition.
                    adapter (Adapter): The adapter for the FSM.
                """
                transition = adapter.get_transition(source, dest)
                transition_function_ref = adapter.get_transition_function(
                    transition=transition,
                )

                def callback(condition, mock):
                    setattr(self, condition, mock)

                # for before in transition.before:
                #     func = getattr(
                #         self,
                #         before,
                #     )
                #     func()
                if transition.conditions is not None:
                    self.mock_ensemble(
                        callback=callback,
                        callable_ensemble=transition.conditions,
                        expected_return_value=True,
                    )
                if transition.unless is not None:
                    self.mock_ensemble(
                        callback=callback,
                        callable_ensemble=transition.unless,
                        expected_return_value=False,
                    )
                transition_function_ref()
                # for after in transition.after:
                #     func = getattr(
                #         self,
                #         after,
                #     )
                #     func()

            def assert_function(*args, **kwargs):
                """Assert that the given path is reachable. This function will
                reset the FSM, then execute each of the transitions in the
                path, asserting that the state attribute of the machine is the
                expected state after each transition.
                """
                self.adapter.reset_fsm()
                for i in range(len(path) - 1):
                    source = path[i]
                    dest = path[i + 1]
                    # execute transition
                    execute_transition(
                        source=source,
                        dest=dest,
                        adapter=self.adapter,
                    )
                    assert getattr(
                        self.adapter.fsm,
                        self.adapter.state_attr,
                    ) == dest, f'Machine should have been in state {dest}, but is in state {getattr(self.adapter.fsm, self.adapter.state_attr)}'  # noqa

            return assert_function

        testsuite = TestSuite()
        setattr(
            testsuite,
            'fail_msg',
            'Unreachable States Detected in Execution',
        )
        for state in self.graph.nodes:
            paths = list(nx.all_simple_paths(
                self.graph,
                self.adapter.initial_state,
                state,
            ))
            for idx, path in enumerate([path for path in paths
                                        if len(path) > 1]):
                testcase_name = f'test_transition_{idx}_to_{state}'
                _callable = test_path(path)
                _callable.__name__ = testcase_name
                setattr(
                    TestCase,
                    testcase_name,
                    _callable,
                )
                testcase = TestCase(
                    testcase_name,
                )
                testcase._class_cleanups = list()
                testsuite.addTest(testcase)
        return testsuite
