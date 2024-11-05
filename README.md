# TODO
- [X] Check Dead States
- [ ] Unreachable States (States that are not reachable from the initial state)
    - Could be solved by traversal and marking reachable states
- [ ] Unreachable Transitions (Transitions that are not reachable from the initial state)
    - Could be solved by traversal and marking reachable transitions
- [ ] Cycle Detection
    - Could be solved by traversal and marking visited states
    - Whenever a cycle is detected, it should increment the cycle count until it reaches a threshold that can be set by the user (default is 1). A failure should be reported if the cycle count exceeds the threshold.
