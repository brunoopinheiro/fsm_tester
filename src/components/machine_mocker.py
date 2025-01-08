import networkx as nx
from unittest import TestSuite, TestCase
from unittest.mock import MagicMock
from src.typing import Adapter
from typing import List, Iterable


class MachineMocker:

    def __init__(
        self,
        adapter: Adapter,
        final_state: str,
        expected_loops: int = 0,
    ):
        self.adapter = adapter
        self.transitions = self.adapter.get_transitions()
        self.graph = self.adapter.get_graph()
        self.final_state = final_state
        self.expected_loops = expected_loops
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

    def execute_transition(
        self,
        source: str,
        dest: str,
    ) -> str:
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

        Returns:
            str: The name of the transition function that was executed.
        """
        transition = self.adapter.get_transition(source, dest)
        transition_function_ref = self.adapter.get_transition_function(
            transition=transition,
        )

        def callback(condition, mock):
            setattr(self.adapter.fsm, condition, mock)

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
        return transition.name

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

            def assert_function(*args, **kwargs):
                """Assert that the given path is reachable. This function will
                reset the FSM, then execute each of the transitions in the
                path, asserting that the state attribute of the machine is the
                expected state after each transition.
                """
                self.adapter.reset_fsm()
                traceback = list()
                for i in range(len(path) - 1):
                    source = path[i]
                    dest = path[i + 1]
                    # execute transition
                    t_name = self.execute_transition(
                        source=source,
                        dest=dest,
                    )
                    traceback.append(t_name)
                    errormsg = f'''Machine should have been in state {dest},
                                but is in state {getattr(self.adapter.fsm, self.adapter.state_attr)}
                                after executing {t_name}. \n Traceback: {traceback}'''  # noqa
                    assert getattr(
                        self.adapter.fsm,
                        self.adapter.state_attr,
                    ) == dest, errormsg

            return assert_function

        testsuite = TestSuite()
        setattr(
            testsuite,
            'fail_msg',
            'Unreachable States Detected in Execution',
        )
        setattr(
            testsuite,
            'suite_name',
            'unreachable_states_suite',
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

    def _find_loops(self) -> List[List[str]]:
        """Find all loops in the FSM. This method will use the networkx
        library to find all simple cycles in the FSM.

        Returns:
            List[List[str]]: A list of all loops in the FSM.
        """
        return list(nx.simple_cycles(self.graph))

    def _find_path(self, source: str, dest: str) -> List[str]:
        """Find a path from source to dest. This method will use the networkx
        library to find a simple path from source to dest.

        Args:
            source (str): The source state of the path.
            dest (str): The destination state of the path.

        Returns:
            List[str]: The path from source to dest.
        """
        return nx.shortest_path(
            self.graph,
            source=source,
            target=dest,
        )

    def _find_escape_path(self, source: str) -> List[str]:
        """Find an escape path from a loop. This method will find a path from
        the given destination state to the final state of the FSM. It tries to
        find a path to the final state, if it fails, it will find the shortest
        path from the destination state to the final state.

        Args:
            dest (str): The destination state of the loop.

        Returns:
            List[str]: The escape path from the loop.
        """
        # TODO: Try to find scape paths from each state in the loop
        try:
            paths = nx.shortest_path(
                self.graph,
                source=source,
            )
            recover_path = None
            if self.final_state in paths.keys():
                recover_path = paths[self.final_state]
            else:
                shortest_path = min(paths.values(), key=len)
                for path in paths.values():
                    if len(path) == shortest_path:
                        recover_path = path
            return recover_path
        except nx.exception.NodeNotFound:
            return list()

    def dead_lock_suite(self) -> TestSuite:
        """Generate test cases to check if there are dead lock states in the
        FSM. This method will first identify if there are any loops in the FSM,
        them check if the machine is able to escape the loop.

        Returns:
            TestSuite: A test suite containing test cases for each loop in the
                FSM.
        """

        def execute_path(path: List[str]) -> None:
            """Execute a path. This method will execute each of the transitions
            in the path, from the initial state to the final state, asserting
            that the state attribute of the machine is the expected state after
            each transition.

            Args:
                path (List[str]): A List of strings that represent the name of
                    the states in the path that should be executed by the
                    machine.
            """
            for i in range(len(path) - 1):
                source = path[i]
                dest = path[i + 1]
                self.execute_transition(
                    source=source,
                    dest=dest,
                )
            assert getattr(
                self.adapter.fsm,
                self.adapter.state_attr,
            ) == path[-1], f'Machine should have been in state {path[-1]}, but is in state {getattr(self.adapter.fsm, self.adapter.state_attr)}'  # noqa

        def _test_deadlock(loop: List[str]) -> callable:
            """Generate a test function that will check if the given loop is a
            dead lock. This function will first find a path from the initial
            state to the first state of the loop, then execute the path. After
            executing the path, the function will execute the loop N times,
            asserting that the machine is not in the loop after each execution.

            Args:
                loop (List[str]): A List of strings that represent the name of
                    the states in the loop that should be executed by the
                    machine.

            Returns:
                callable: The test function.
            """
            def assert_function(*args, **kwargs):
                """Assert that the given loop is not a dead lock. This function
                will first find a path from the initial state to the first
                state of the loop, then execute the path. After executing the
                path, the function will execute the loop N times, asserting
                that the machine is not in the loop after each execution.
                """
                self.adapter.reset_fsm()
                path_to_loop = self._find_path(
                    source=self.adapter.initial_state,
                    dest=loop[0],
                )
                escape_path = self._find_escape_path(
                    loop[-0],
                )
                if escape_path is None or len(escape_path) == 0:
                    assert False, f'Deadlock Detected in loop {loop}'
                execute_path(path_to_loop)
                for exec_n in range(self.expected_loops):
                    if exec_n > self.expected_loops:
                        assert False, f'Deadlock Detected in loop {loop}'
                    execute_path(loop)
                    self.execute_transition(
                        source=loop[-1],
                        dest=loop[0],
                    )
                    if exec_n == self.expected_loops - 1:
                        execute_path(escape_path)
                assert getattr(
                    self.adapter.fsm,
                    self.adapter.state_attr,
                ) not in loop, f'Machine should not be in loop {loop}, but is in state {getattr(self.adapter.fsm, self.adapter.state_attr)}, part of the following loop:\n {loop}'  # noqa

            return assert_function

        loops = self._find_loops()
        testsuite = TestSuite()
        setattr(
            testsuite,
            'fail_msg',
            'Deadlock Detected',
        )
        setattr(
            testsuite,
            'suite_name',
            'dead_lock_suite',
        )
        for loop in loops:
            testcase_name = f'test_deadlock_{loop}'
            _callable = _test_deadlock(loop)
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
