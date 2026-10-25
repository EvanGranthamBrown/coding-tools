You are helping to plan the migration for the rearchitecting laid out in `@plan-directory/architecture.md`, implementing the system described in `@plan-directory/feature-doc.md`. Your assignmed component is: @assignment

1. Carefully study the architecture plan and the relevant code files.
2. Draft a detailed plan for the changes described, including specific files, classes, functions, tests, etc.
    - Store your plan in `@plan-directory/draft/migrate-@slug.md`.
    - Make note of anything you discover in the architecture that needs changing, particularly if it affects the methods and classes you expose to the rest of the system. Put these notes at the end of the file.
    - Identify which parts of the existing code can be reused mostly or entirely intact, but don't compromise the new design for the sake of reusing old code.
    - Most of the planned test suite should be integration tests that treat the internals of your assigned component as a black box. These tests go through the same interfaces the rest of the system uses.
    - Plan unit tests to exercise complex logic in isolation, or to verify critical assumptions (e.g., "this Python function and this SQL function return the exact same value in all cases").
    - Prefer real local infrastructure (e.g., Docker) to mocks.
    - Pay special attention to existing tests. The tests are our safety net during rearchitecting. For each existing test, decide whether:
        - It can be reused as-is with minimal changes. This is ideal.
        - It needs to be rewritten, but does test important functionality.
        - It tests something that will not exist or does not apply in the new design and can be deleted.
3. Notify the caller that your plan is ready.
4. The caller will integrate your work with that of other migration planners, then direct you to make changes. Apply those changes as directed. Notify the caller when you're done.