from fsm_tester.adapters import BaseAdapter
from typing import Literal, TypeVar


Adapter = TypeVar('Adapter', bound=BaseAdapter)
DIALECTS = Literal['pytransitions', 'python-statemachine']
