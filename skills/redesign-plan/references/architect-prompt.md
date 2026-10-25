Your task is to draft a high-level architecture for the code system described in `@plan-directory/feature-doc.md`. Follow the example in `@sample-architecture-plan` and write your output to `@plan-directory/architecture.md`.

- Do NOT look at any files in this repo other than `@plan-directory/feature-doc.md` and `@sample-architecture-plan`. Your goal is to envision a logical, unified architecture for this system, as if it were a greenfield project, without being prejudiced by the current implementation.
- Your design may use any of the technologies listed under "Technologies." You do not *have* to use them. Only include other technologies if you see no feasible way to do it with the ones listed.
- Keep the top-level "Description" and "Purpose" of the system in mind at all times.
- Make sure your design delivers all of the "Functionality" items under each Duty.
- "Components" breaks the design down into discrete components which communicate through well-defined interfaces.
- "Complications" lists problems that actually occurred, or that are very likely to occur, based on a naive implementation. Factor them into your design and document how each one is resolved.

Once you complete the document, report back to the caller, which will reply with suggestions for improvement. You may now look at other files in the repository if you need to. If you agree with a suggestion, implement it. If you don't agree, have concerns, or see opportunities to improve further, discuss it with the caller and try to reach a resolution. If, after discussion, you don't believe you can implement a suggestion properly, tell the caller and provide your reasons, then move on.

The caller may reply with additional suggestions; address them as above. Continue until you get no further requests.