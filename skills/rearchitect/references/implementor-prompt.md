You are helping to carry out the rearchitecting plan in `@architecture-plan-path`, implementing the system described in `@feature-doc-path`. Your assignment is @implementor-assignment.

1. Carefully study the architecture plan and the relevant code files.
2. Draft a detailed plan for how you will make the changes described, including specific files, classes, functions, tests, etc. Guidelines:
    - Make note of anything you discover that needs changing, particularly if it affects the methods and classes you expose to the rest of the system.
    - Identify which parts of the existing code can be reused mostly or entirely intact, but don't compromise the new design for the sake of reusing old code.
    - Your test suite should consist mostly of integration tests. As much as possible, treat the internals of your assigned component as a black box. Test it through the same interfaces the rest of the system uses.
    - Wherever you need to do some precise or complex logic, plan to isolate it into its own class or method with no external dependencies, then write unit tests against it (an exception to the preceding rule).
