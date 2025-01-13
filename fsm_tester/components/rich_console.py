import sys
from rich.console import Console


class RichConsole(Console):
    """This class extends the Console class from the rich library.
    It adds a writeln method that is equivalent to the print method, intended
    to be used by the UnitTest Runner.

    Inherits:
        Console: The Console class from the rich library.
    """

    def __init__(self, *args, **kwargs):
        self.stream = sys.stderr
        super().__init__(*args, **kwargs)

    def __getattr__(self, attr):
        if attr in ('stream', '__getstate__'):
            raise AttributeError(attr)
        return getattr(self.stream, attr)

    def write(self, arg: str, *args, **kwargs):
        self.print(arg, *args, **kwargs)

    def writeln(self, arg: str, *args, **kwargs):
        if arg:
            self.write(arg)
        self.write('\n')
