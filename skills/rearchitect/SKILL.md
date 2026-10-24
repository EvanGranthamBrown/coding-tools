---
name: rearchitect
description: Overhaul a group of code files to make the code simpler, cleaner, and better designed. Activate after implementing substantial new features, or on user request.
metadata:
  version: 0.1.0
  author: Evan Grantham-Brown
---
This skill ensures that the code base is kept clean, clear, and well-organized.

Area of focus: $ARGUMENT

(If no area of focus is given, your focus is the entire code base.)

## 1. Safety Check
Run `git status --porcelain` and verify that it returns nothing.
If it returns non-empty, you'll need to add or gitignore any untracked files, then commit all changes, so you have a stable base to roll back to. If the user activated this skill and `git status --porcelain` shows changes you didn't make, get confirmation from the user before proceeding.

## 2. Draft Feature Doc
Go through the code and write a "feature doc." This brief document describes the essential functions of the system, but NOT implementation details. A zero-context agent will use the feature doc to design an "ideal architecture" for the system, and we do not want it influenced by the present implementation. See `references/sample-feature-doc.md` for an example.

- Store the document in `tmp/YYYYMMDD-hhmmss-feature-doc.md`.
- If the code base is large, you may delegate review to 1-10 sub-agents. Don't do this unless you need to.
- Ignore commented-out code and unreachable code.
- If there is a spec or roadmap, include functionality which is clearly and definitely on the roadmap. Do NOT include "nice to haves," brainstorming output, experimental features, or vague future plans.

### Feature Doc Elements
- **Overview:**
    - **Name:** A name encapsulating the code under review. No more than 5 words.
    - **Description:** Summarize the core function of the code under review. No more than 30 words.
    - **Purpose:** Describe why this function needs to be performed. No more than 30 words.
- **Technologies:** List the technologies chosen for this system. This includes physical or virtual infrastructure, languages, storage, communications protocols, AI models, code libraries, etc. Only list technologies used by the code under review. Do not specify how any given technology is used.
- **Duties:** Group the functions of this system into high-level "duties."
    - **Functionality:** List the specific tasks that must be performed as part of this duty.
        - Avoid specifying *how* any task is performed.
        - Do not mention any specific technology, detailed algorithm, or code component (function, class, module, etc.).
    - **Complications:** Review tests, code comments, and git history to find unexpected problems which forced design changes.
        - List issues which were actually encountered in development. Include the short hash of the first git commit which references or addresses the issue. Sort issues by commit timestamp. 
        - Include cost, complexity, and performance considerations, not just correctness issues.
        - If you find code changes addressing a hypothetical scenario, with no indication that the scenario actually happened, assess whether that scenario is likely and/or impactful enough to justify altering the design. If in doubt, leave it out.
        - Summarize the problem only. Do NOT describe how it was solved. Avoid language which hints at a particular solution.

## 3. Draft Greenfield Architecture
Spin up an "architect" sub-agent with no context. Give it the prompt in `references/architect-prompt.md`, with the following string substitutions:

- "@feature-doc-path": Path to the feature doc
- "@sample-output": Absolute path to `references/sample-architecture.md`
- "@output-path": `tmp/YYYYMMDD-hhmmss-architecture.md`

You may customize this prompt further if you think it's important.