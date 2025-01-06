# FSMTester
This tool was made as part of the evaluation process for the conclusion of the post-graduation course in Robotics and Artificial Inteligence at the "Residência em Robótica e Inteligência Artificial" program at CIn-UFPE (Centro de Informática da Universidade Federal de Pernambuco).

The tool is a Finite State Machine (FSM) tester, which is able to receive a FSM Model that defines its states and transitions, and tests the code for the following properties:
- Reachability
- Determinism
- Deadlocks

The tool is integrated with PyTest, and can be used to test the properties of the FSM Model with just a few lines of code.
```python
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
```

## Installation
!! TODO !! </br>
The tool was already developed using Poetry to ease the package management, but the installation process is not yet automated. The tool is not yet available on PyPi, so you need to clone the repository and install the dependencies manually.

## Supported Dialects
Currently, the tool supports supports only the [`pytransitions`](https://github.com/pytransitions/transitions) library, but the tool is designed to be easily extensible to other libraries. If you want to add support for a new library, you can create a class that inherits from the `BaseAdapter` class and implement the methods that are necessary to convert the FSM Model to the desired library, then add this support to the `create_adapter` method in the `AdapterFactory` class.

## Analysis
The tool uses an hybrid approach to analyze the FSM Model. It uses the NetworkX library to create a graph representation of the FSM Model, and then uses the graph to analyze the properties of the FSM Model.
Both the `Reachability` and the `Nondeterminism` properties are static analysis done from the graph representation of the FSM Model. The dynamic analysis is done by running the FSM Model with the aid of the unittest mocks, and checking the machine execution, both the `Deadlocks` and (again) the `Reachability` properties are checked in this phase.

## Testing a Machine Model with the Tool:
To test a FSM Model with the tool, you need to create a class that represents the FSM Model, having both the states and transitions defined.

```python
from transitions.extensions import GraphMachine


class SimpleMachine:
    states = ['A', 'B', 'C', 'Finish']

    transitions = [
        {'trigger': 'go_to_B', 'source': 'A', 'dest': 'B'},
        {'trigger': 'go_to_C', 'source': 'B', 'dest': 'C'},
        {'trigger': 'end_operation', 'source': 'C', 'dest': 'Finish'},
    ]

    def __init__(self):
        self.machine = GraphMachine(
            model=self,
            states=SimpleMachine.states,
            transitions=SimpleMachine.transitions,
            initial='A',
        )

```

With that defined, you have two possible approaches to test the FSM Model with the tool.

### Parametrized Test
The most direct and complete approach is to use the `pytest.mark.parametrize` decorator to run the test with all the test suites available in the tool.

```python
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

```

### Single Tests
If you want to test only a specific property of the FSM Model, you can use the `run` method of the `FSMTester` class, passing the desired test suite.

```python
import pytest  # noqa
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

```