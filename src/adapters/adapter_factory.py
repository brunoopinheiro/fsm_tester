from src.adapters.base_adapter import BaseAdapter
from src.adapters.transitions_adapter import TransitionsAdapter
from src.entities import FSMProtocol
from src.typing import DIALECTS


class AdapterFactory:
    """Factory class for creating the appropriate adapter for the given FSM
    module and dialect.
    """

    @staticmethod
    def create_adapter(
        fsm_module: FSMProtocol,
        dialect: DIALECTS,
    ) -> BaseAdapter:
        """With the given FSM module and dialect, return the appropriate
        adapter that will be used to interpret the FSM module.

        Args:
            fsm_module (FSMProtocol): The FSM Module implementation under test.
            dialect (DIALECTS): The dialect of the FSM module.

        Raises:
            NotImplementedError: For State Machine implementations not yet
                implemented.
            ValueError: For dialects not recognized.

        Returns:
            BaseAdapter: The adapter that will be used to interpret the FSM
        """
        if dialect == 'pytransitions':
            return TransitionsAdapter(fsm_module)
        elif dialect == 'python-statemachine':
            raise NotImplementedError(
                'Python State Machine not implemented yet.')
        else:
            raise ValueError('Dialect not recognized.')
