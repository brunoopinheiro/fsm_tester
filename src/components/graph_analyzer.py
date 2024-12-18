import networkx as nx

from entities import FSMTransition
from networkx import MultiDiGraph, MultiGraph
from unittest import TestSuite, TestCase
from typing import Union, List


class GraphAnalyzer:

    def __init__(
        self,
        graph: Union[MultiDiGraph, MultiGraph],
        initial_state: str,
        final_state: str,
    ):
        self.graph = graph
        self.initial_state = initial_state
        self.final_state = final_state

    def unreachable_states_suite(self) -> TestSuite:
        """Generate test cases to check if there are unreachable states in the
        FSM.

        Returns:
            TestSuite: A test suite containing test cases for each state in the
                FSM.
        """

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
                        source=self.initial_state,
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
            testcase_name = f'test_unreachable_{state}'
            _callable = test_unreachable(state)
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

    def sink_states_suite(self) -> TestSuite:
        """Generate test cases to check if there are sink states in the
        FSM.

        Returns:
            TestSuite: A test suite containing test cases for each state in the
                FSM.
        """

        def test_sink(state: str) -> callable:
            """Generate a test function that will check if the given state is
            a sink state.

            Args:
                state (str): The state to check for being a sink state.

            Returns:
                callable: The test function.
            """
            def assert_function(*args, **kwargs):
                is_endstate = state == self.final_state
                successors = list(self.graph.successors(state))
                has_successors = len(successors) > 0
                escape_path = list()
                for s_state in successors:
                    has_escape = nx.has_path(
                        self.graph,
                        source=state,
                        target=self.final_state,
                    )
                    if not has_escape:
                        escape_path.append(s_state)
                assert not is_endstate or not has_successors or escape_path
            return assert_function

        testsuite = TestSuite()
        setattr(
            testsuite,
            'fail_msg',
            'Sink States Detected',
        )
        for state in self.graph.nodes:
            testcase_name = f'test_sink_{state}'
            _callable = test_sink(state)
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

    def nondeterministic_transition_suite(
        self,
        transitions: List[FSMTransition],
    ) -> TestSuite:
        """Generate test cases to check if there are nondeterministic
        transitions in the FSM.

        Args:
            transitions (List[FSMTransition]): The list of transitions in the
                FSM. Expected to be acquired from the FSMAdapter.

        Returns:
            TestSuite: A test suite containing test cases for each state in the
                FSM.
        """
        def nondeterministic(
            transition1: FSMTransition,
            transition2: FSMTransition,
        ) -> bool:
            """Check if two transitions are nondeterministic, by comparing
            their set of conditions, unless, before, and after definitions.
            NOTE: This function might be better suited to be a method of the
            `Adapter` class.

            Args:
                transition1 (FSMTransition): The first transition to compare.
                transition2 (FSMTransition): The second transition to compare.

            Returns:
                bool: True if the transitions are nondeterministic, False
                    otherwise.
            """
            if (
                transition1.conditions == transition2.conditions
                and transition1.unless == transition2.unless
                and transition1.before == transition2.before
                and transition1.after == transition2.after
            ):
                return True
            return False

        def test_nondeterministic(
            state: str,
        ) -> callable:
            """Generate a test function that will check if the given state has
            nondeterministic transitions.
            A transition is nondeterministic if there are two transitions from
            the same source state with no clear differentiation between the
            conditions that allow them to be triggered.

            Args:
                state (str): The state to check for nondeterministic
                    transitions.

            Returns:
                callable: The test function.
            """
            src_transitions = [
                t for t in transitions if t.source == state
            ]
            nondet_tr = list()
            for tr in src_transitions:
                subset = [tr2 for tr2 in src_transitions if tr2 != tr]
                for tr2 in subset:
                    if nondeterministic(tr, tr2):
                        if tr not in nondet_tr:
                            nondet_tr.append(tr)
                        if tr2 not in nondet_tr:
                            nondet_tr.append(tr2)

            def assert_function(*args, **kwargs):
                assert len(nondet_tr) == 0
            return assert_function

        testsuite = TestSuite()
        setattr(
            testsuite,
            'fail_msg',
            'Nondeterministic Transitions Detected',
        )
        for state in self.graph.nodes:
            testcase_name = f'test_nondeterministic_{state}'
            _callable = test_nondeterministic(state)
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
