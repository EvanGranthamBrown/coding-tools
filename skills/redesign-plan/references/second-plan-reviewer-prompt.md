Your task is to review and critique the rearchitecting plan in `@plan-directory/architecture.md` and the migration plan in `@plan-directory/migration.md`, implementing the system described in `@plan-directory/feature-doc.md`. Consider the following:

- Do you see any obvious bugs or flaws?
- Are there areas of the plans that seem overly complex or convoluted? Can they be simplified?
- Does each file and module have a well-defined responsibility? Is any piece of the system doing too much?
- Where present, review names of files, classes, methods, etc. Does each name succinctly and accurately convey the function of the named thing? Can names be made shorter without losing clarity?
- Does the architecture decompose cleanly into components, where each component only talks to the others through a few tightly defined interfaces? If not, what can be changed in order to make it so?
- Where abstractions are used, do they serve a purpose or are they just introducing needless layers of indirection?
- Is the architecture plan consistent with the migration plan?
- What risks does the migration plan present? What mitigations are in place for those risks, and are they adequate?
- How much downtime does migration involve? How can it be minimized?

Compile a list of proposed improvements and return it to the caller. The caller will make the final decision on which changes to implement.