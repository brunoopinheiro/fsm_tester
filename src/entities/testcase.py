from dataclasses import dataclass


@dataclass
class TestCase:

    name: str
    source: str
    dest: str
    trigger: str
    condition: list | None = None
    unless: list | None = None

    def __str__(self):
        return f"FSM Test: {self.name}"
