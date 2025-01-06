from transitions.extensions import GraphMachine


class UnreachableMachine:
    states = [
        {'name': 'Start', 'on_enter': ['print_state']},
        {'name': 'Idle', 'on_enter': ['print_state']},
        {'name': 'SelectPart', 'on_enter': ['print_state']},
        {'name': 'CheckPart', 'on_enter': ['print_state']},
        {'name': 'RejectPart', 'on_enter': ['print_state', 'count_rejected_parts']},  # noqa
        {'name': 'PlacePart', 'on_enter': ['print_state']},
        {'name': 'BuildProduct', 'on_enter': ['print_state']},
        {'name': 'Unused', 'on_enter': ['print_state']},
        {'name': 'InspectBuild', 'on_enter': ['print_state']},
        {'name': 'BoxProduct', 'on_enter': ['print_state']},
        {'name': 'Calibrate', 'on_enter': ['print_state']},
        {'name': 'ReturnHome', 'on_enter': ['print_state']},
        {'name': 'Complete', 'on_enter': ['print_state']},
    ]

    transitions = [
        {'trigger': 'start', 'source': 'Start', 'dest': 'Idle'},
        {'trigger': 'command_received', 'source': 'Idle', 'dest': 'SelectPart'},  # noqa
        {'trigger': 'part_selected', 'source': 'SelectPart', 'dest': 'CheckPart'},  # noqa

        {'trigger': 'part_checked', 'source': 'CheckPart', 'dest': 'PlacePart',  # noqa
         'unless': ['is_defective_part']},
        {'trigger': 'part_checked', 'source': 'CheckPart', 'dest': 'RejectPart',  # noqa
         'conditions': ['is_defective_part']},

        {'trigger': 'part_placed', 'source': 'PlacePart', 'dest': 'BuildProduct'},  # noqa
        {'trigger': 'product_built', 'source': 'BuildProduct', 'dest': 'InspectBuild'},  # noqa
        {'trigger': 'build_inspected', 'source': 'InspectBuild', 'dest': 'BoxProduct'},  # noqa

        {'trigger': 'part_rejected', 'source': 'RejectPart', 'dest': 'ReturnHome'},  # noqa

        {'trigger': 'max_defective_parts', 'source': 'ReturnHome', 'dest': 'Calibrate',  # noqa
         'conditions': ['max_rejections']},
        {'trigger': 'not_max_defective_parts', 'source': 'ReturnHome', 'dest': 'Idle',  # noqa
         'unless': ['max_rejections']},

        {'trigger': 'product_boxed', 'source': 'BoxProduct', 'dest': 'Complete'},  # noqa
        {'trigger': 'calibration_done', 'source': 'Calibrate', 'dest': 'Complete'}  # noqa

    ]

    def __init__(self):
        self.part_checked_flag = False
        self.defective_parts_limit = 2
        self.rejected_parts_count = 0

        self.machine = GraphMachine(
            model=self,
            states=UnreachableMachine.states,
            transitions=UnreachableMachine.transitions,
            initial='Start', graph_engine='graphviz')

    def print_state(self):
        print('Current state: ' + self.state + '\n')

    def count_rejected_parts(self):
        self.rejected_parts_count += 1

    def is_defective_part(self):
        return self.part_checked_flag

    def max_rejections(self):
        return self.rejected_parts_count == self.defective_parts_limit
