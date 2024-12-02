from typing import Protocol, List, Dict


class FSMProtocol(Protocol):
    """TODO: Needs to be better structured. Should specify the necessary
    organization for a Machine Implementation to be tested."""

    @property
    def states(self) -> List[Dict[str, str]]: ...

    @property
    def transitions(self) -> List[Dict[str, str]]: ...
