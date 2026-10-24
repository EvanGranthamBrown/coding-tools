---
name: rearchitect
description: Overhaul a group of code files to make the code simpler, cleaner, and better designed. Activated on user request.
metadata:
  version: 0.1.0
  author: Evan Grantham-Brown
---
This skill ensures that the code base is kept clean, clear, and well-organized.

Area of focus: $ARGUMENTS

(If no area of focus is given, your focus is the entire code base.)

## 1. Safety Check
We want to start from a safe, committed base so the project can roll back if necessary. If `git status --porcelain` returns empty, everything is fine and you can proceed. If it shows untracked files and/or uncommitted changes:
- For each untracked file, decide whether you think it should be added or gitignored. Follow any clear project conventions that apply; otherwise, fall back to general best practices.
- If uncommitted changes would insert sensitive data (passwords, API keys, etc.) into a tracked file, or if project conventions dictate adding an untracked file that has sensitive data, tell the user which files are affected, then abort. Never commit sensitive data to git.
    - You do not need to abort for sensitive data that has already been committed. However, if you see any, warn the user.
- If no sensitive data will be added, tell the user which files your planned commit will add, delete, gitignore, or modify, then ask for permission to proceed.
- If the user grants permission, generate the commit with an appropriate message and proceed.
- If the user denies permission, abort.

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
- "@sample-architecture-plan": Absolute path to `references/sample-architecture.md`
- "@architecture-plan-path": `tmp/YYYYMMDD-hhmmss-architecture.md`

You may customize this prompt further if you think it's important.

Once the architect finishes its draft, review its work in light of your knowledge of the existing code base. Note any bugs or issues that you find. Also think about what would have to be changed to comply with the new design, and consider:

1. Has the user specifically given orders (to coding agents or in human-written documentation) not to go this route? If so, obey that directive unless the benefit is enormous or the user's stated reasons no longer apply. In those cases, ask the user for permission.
2. Does this change improve the current design, worsen it, or have no real impact either way? Avoid changes that don't lead to a clear improvement.
3. Has this change been tried before in this codebase? If so, why was it rejected last time? Don't move forward unless you're confident those problems won't recur.
4. How much risk is associated with this change? Will it require manual or time-consuming testing (beyond running a normal automated test suite), or a challenging deployment process? Keep in mind that the user has already accepted significant effort and risk by asking for a rearchitecting, so this should only be a deal-breaker if the effort/risk are very high and the benefit small.
5. Will this change dramatically increase the monetary cost (one-time or ongoing) of the system? If so, see if there's a way to avoid it. If not, and the user has not given you a specific budget, provide the user with an estimate of the cost increase and ask whether to proceed.

Based on this, suggest adjustments to the sub-agent, and answer any questions or concerns it has. If it says it can't implement a suggestion properly, note the fact and move on. Continue until you think the draft is in good shape (aside from any declined suggestions), keeping in mind that this is a high-level architectural document and doesn't have to cover every detail.

(If the sub-agent declined some of your suggestions, think about the reasons it gave for refusal. If you think it's wrong and you can safely implement those suggestions yourself, do so. Otherwise, leave it.)

## 4. Edit Architecture
Spin up an "editor" sub-agent and give it the prompt in `references/editor-prompt.md`, with the following string substitutions:

- "@feature-doc-path": Path to the feature doc
- "@architecture-plan-path": `tmp/YYYYMMDD-hhmmss-architecture.md`

You may customize this prompt further if you think it's important.

The editor agent will generate a list of improvements and suggestions. Consider each in light of what you've learned so far, and make those changes you agree with.

## 5. Draft Implementation Plans
The next step is to write detailed plans to carry out the overhaul. Identify the breakpoints where you can split the architecture into components that talk to each other through tightly defined interfaces. Add the list of components to the architecture plan, and specify what methods or classes each one exposes to the others.

Then, for each component, spin up a sub-agent and give it the prompt in `references/implementation-planner-prompt.md`. Make the following string substitutions:

- "@feature-doc-path": Path to the feature doc
- "@architecture-plan-path": `tmp/YYYYMMDD-hhmmss-architecture.md`
- "@implementor-assignment": The component assigned to this sub-agent