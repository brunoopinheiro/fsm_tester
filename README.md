# TODO
- [X] Check Dead States
- [ ] Unreachable States (States that are not reachable from the initial state)
    - Could be solved by traversal and marking reachable states
- [ ] Unreachable Transitions (Transitions that are not reachable from the initial state)
    - Could be solved by traversal and marking reachable transitions
- [ ] Cycle Detection
    - Could be solved by traversal and marking visited states
    - Whenever a cycle is detected, it should increment the cycle count until it reaches a threshold that can be set by the user (default is 1). A failure should be reported if the cycle count exceeds the threshold.


# Notes
- https://networkx.org/documentation/stable/
    - Used to get the graph representation of the state machine
    - read documentation to check if it can be used to solve the problems mentioned in the TODO section