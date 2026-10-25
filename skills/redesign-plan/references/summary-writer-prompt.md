Your task is to prepare an explanation of the rearchitecting plan in `@plan-directory/architecture.md`, which implements the system described in `@plan-directory/feature-doc.md`. This explanation will be presented to the user for review and approval. Assume the user is an experienced developer but is completely unfamiliar with the code base and the current architecture.

# Files
You'll use the following files:
- `@plan-directory/summary-scratch.md`: A scratch file where you plan out the explanation
- `@plan-directory/summary-draft.md`: The file where you'll write your first draft
- `@plan-directory/summary-review.md`: The file where a reviewer agent will note its concerns
- `@plan-directory/summary.md`: The final draft produced by a copy editor agent

# Content List
In your scratch file, make a list of the things your explanation needs to cover. This includes:

- The function and purpose of the system
- Each component of the planned architecture, its function, and how it interacts with the other components
- Which code is being preserved as-is from the current implementation, which is being rewritten or heavily modified, and which is being deleted altogether
- What new functionality is being written from scratch
- The most impactful and/or risky changes being made to the current implementation
- How the new code will be tested to ensure it works
- Anything noted in "User Review Items"
- Anything else the user should be aware of

# Write Introduction
In the first draft file, write the introduction, consisting of:

- A summary of what the system does and of the planned design (200 words or less).
- A diagram, tree, or nested list laying out the components of the design and their interactions. For each component, note what it is and does (30 words or less).
- A bulleted list with critical points for the user; major changes, significant risks, and decisions in "User Review Items." Each of these should be 30 words or less.

# Subsections
In your scratch file, record your thoughts on how to break up the detailed explanation into subsections. Options:

- Each component of the planned architecture is a subsection
- Each of the system's major functions is a subsection
- Something else

Choose the approach you think makes the most sense given the substance of the design. Try to keep each subsection as independent of the others as possible; ideally, you could present the subsections in any order and they would still make sense, though in practice this will likely be impossible.

In your scratch file, write another version of your content list, where you group the items into your chosen subsections.

# Sequencing
In your scratch file, record your thoughts on how to order the subsections. Considerations:

- Core functionality should usually come before secondary features
- If anything in Subsection A is required to understand Subsection B, A should precede B
- Simpler concepts should precede more difficult ones

Once you've decided how to order the subsections, record your thoughts on how to sequence the content items within each subsection. Order content items so each one builds on what came before; earlier items introduce the concepts needed to understand later ones.

In your scratch file, write a final outline, where you list the subsections in order and the content items in order within each.

# Write Explanation
In the first draft file, after the introduction, write the full explanation according to your outline. Then notify the caller that the first draft is done.

# Review
A reviewer agent will read your work and send you suggestions for improvement in `@plan-directory/summary-review.md`. You'll be notified when the review is ready. Consider its suggestions and make the changes you think are reasonable. Then notify the caller that you've finished your edits.

# Copy Edit and Final Draft
A copy editor agent will revise the explanation for clarity and concision, putting its work in `@plan-directory/summary.md`. When it's done, you'll be notified. Review its changes and make sure it didn't remove anything critical or introduce errors. If it did, you may restore the critical information; only do this if it's clearly necessary. Once you're finished, notify the caller that the final draft is ready.