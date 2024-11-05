from typing import Protocol, List, Dict


class FSMProtocol(Protocol):

    @property
    def states(self) -> List[Dict[str, str]]: ...

    @property
    def transitions(self) -> List[Dict[str, str]]: ...
