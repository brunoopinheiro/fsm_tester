from dataclasses import dataclass
from typing import Optional, List, Union


@dataclass
class FSMState:

    name: str
    on_enter: Optional[List[Union[callable, str]]]
    on_exit: Optional[List[Union[callable, str]]]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
