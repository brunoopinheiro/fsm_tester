from abc import ABC, abstractmethod
from entities import (
    FSMProtocol,
    FSMState,
    FSMTransition,
    TestCase,
)
from typing import List


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
    def mimic_attributes(self) -> set:
        """Reading the FSM implementation, returns the attributes that are not
        part of the FSM but are used in the FSM behavior.

        Returns:
            set: The attributes that are not part of the FSM but are used in
            the FSM behavior.
        """
        raise NotImplementedError
