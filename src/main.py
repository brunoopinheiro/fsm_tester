from machines.assembly_line_impl.main import AssemblyLine
from adapters.transitions_adapter import TransitionsAdapter


adapter = TransitionsAdapter(AssemblyLine)
graph = adapter.get_graph()
print(type(graph))
print(graph)
print()
