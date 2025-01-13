from typing import Protocol, List, Dict, runtime_checkable


@runtime_checkable
class FSMProtocol(Protocol):
    """TODO: Needs to be better structured. Should specify the necessary
    organization for a Machine Implementation to be tested."""

    @property
    def states(self) -> List[Dict[str, str]]: ...

    @property
    def transitions(self) -> List[Dict[str, str]]: ...

    def __instancecheck__(self, instance) -> bool:
        """Check if the instance has the necessary attributes to be considered
        a FSM Module.

        Args:
            instance (Any): The instance to be checked.

        Returns:
            bool: True if the instance has the necessary attributes, False
                otherwise.
        """
        has_states = hasattr(instance, 'states')
        has_transitions = hasattr(instance, 'transitions')
        return has_states and has_transitions
