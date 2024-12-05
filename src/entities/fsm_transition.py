from dataclasses import dataclass
from src.entities import FSMState
from typing import Optional, List, Union


WILDCARD_ALL = '*'
WILDCARD_SAME = '='


@dataclass
class FSMTransition:

    name: str
    source: Union[FSMState, str, List[Union[FSMState, str]]]
    destination: Union[FSMState, str]
    conditions: Optional[List[Union[callable, str]]]
    unless: Optional[List[Union[callable, str]]]
    before: Optional[List[Union[callable, str]]]
    after: Optional[List[Union[callable, str]]]

    def __str__(self):
        return f'{self.name}: {self.name} -> {self.destination}'

    def __repr__(self):
        return self.name

    def __eq__(self, value):
        if isinstance(value, FSMTransition):
            return (self.name == value.name
                    and self.source == value.source
                    and self.destination == value.destination)
        return False
