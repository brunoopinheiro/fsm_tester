from abc import ABC, abstractmethod
from fsm_tester.entities import (
    FSMProtocol,
    FSMState,
    FSMTransition,
    TestCase,
)
from typing import List, Union
from networkx import MultiDiGraph, MultiGraph


class BaseAdapter(ABC):

    def __init__(self, fsm: FSMProtocol):
        if not self.__assert_is_valid_fsm(fsm):
            raise ValueError("Invalid FSM provided.")
        self.fsm = fsm()

    def __assert_is_valid_fsm(self, fsm: FSMProtocol) -> bool:
        """Asserts that the provided FSM is valid.

        Args:
            fsm (FSMProtocol): The FSM to validate.

        Returns:
            bool: True if the FSM is valid, False otherwise.
        """
        has_states = hasattr(fsm, 'states')
        has_transitions = hasattr(fsm, 'transitions')
        is_valid_fsm = has_states and has_transitions
        return is_valid_fsm

    @property
    @abstractmethod
    def initial_state(self) -> str:
        """Returns the initial state of the FSM.

        Returns:
            str: The name for the initial state of the FSM.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def state_attr(self) -> str:
        """Returns the internal reference that holds the current state of the
        machine."""
        raise NotImplementedError

    @abstractmethod
    def get_states(self) -> List[FSMState]:
        """Returns the states of the FSM.

        Returns:
            List[FSMState]: The states of the FSM.
        """
        raise NotImplementedError

    @abstractmethod
    def get_transitions(self) -> List[FSMTransition]:
        """Returns the transitions of the FSM.

        Returns:
            List[FSMTransition]: The transitions of the FSM.
        """
        raise NotImplementedError

    @abstractmethod
    def get_transition(self, source: str, dest: str) -> FSMTransition:
        """Returns the transition from source to dest.

        Args:
            source (str): The source state of the transition.
            dest (str): The destination state of the transition.

        Returns:
            FSMTransition: The transition from source to dest.
        """
        raise NotImplementedError

    @abstractmethod
    def get_test_cases(self) -> List[TestCase]:
        """Builds and returns the test cases for the FSM.

        Returns:
            List[TestCase]: The test cases for the FSM.
        """
        raise NotImplementedError

    @abstractmethod
    def get_methods(self) -> set:
        """Reading the FSM implementation, returns the methods that are not
        part of the FSM but are used in the FSM behavior.

        Returns:
            set: The methods that are not part of the FSM but are used in the
            FSM behavior.
        """
        raise NotImplementedError

    @abstractmethod
    def mimic_attributes(self, callback: callable) -> set:
        """Reading the FSM implementation, returns the attributes that are not
        part of the FSM but are used in the FSM behavior.

        Args:
            callback (callable): The callback to use to insert the attributes
                in the parent class.

        Returns:
            set: The attributes that are not part of the FSM but are used in
            the FSM behavior.
        """
        raise NotImplementedError

    @abstractmethod
    def get_graph(self) -> Union[MultiGraph, MultiDiGraph]:
        """Returns the graph representation of the FSM.

        Returns:
            DiGraph: The graph representation of the FSM.
        """
        raise NotImplementedError

    @abstractmethod
    def get_transition_function(self, transition: FSMTransition) -> callable:
        """Returns the transition function for the given transition.

        Args:
            transition (FSMTransition): The transition to get the function for.

        Returns:
            callable: The transition function.
        """
        raise NotImplementedError

    @abstractmethod
    def reset_fsm(self) -> None:
        """Resets the FSM to the initial state."""
        raise NotImplementedError
