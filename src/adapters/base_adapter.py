from abc import ABC, abstractmethod
from entities import TestCase, FSMProtocol
from typing import List


class BaseAdapter(ABC):

    def __init__(self, fsm: FSMProtocol):
        if not self.__assert_is_valid_fsm(fsm):
            raise ValueError("Invalid FSM provided.")
        self.fsm = fsm

    def __assert_is_valid_fsm(self, fsm) -> bool:
        has_states = hasattr(fsm, 'states')
        has_transitions = hasattr(fsm, 'transitions')
        is_valid_fsm = has_states and has_transitions
        return is_valid_fsm

    @abstractmethod
    def get_states(self):
        raise NotImplementedError

    @abstractmethod
    def get_transitions(self):
        raise NotImplementedError

    @abstractmethod
    def get_test_cases(self) -> List[TestCase]:
        raise NotImplementedError
