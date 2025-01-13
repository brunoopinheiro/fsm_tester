from rich.console import Console


class RichConsole(Console):
    """This class extends the Console class from the rich library.
    It adds a writeln method that is equivalent to the print method, intended
    to be used by the UnitTest Runner.

    Inherits:
        Console: The Console class from the rich library.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def write(self, message: str, *args, **kwargs):
        self.print(message, *args, **kwargs)
