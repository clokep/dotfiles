# Important Stuff

- Project docs document what _is_, not the journey — cut "we tried X", "empirically observed",
  PR/SHA/ticket references, and first-person anecdotes.
- Default to including a diagram whenever it clarifies a flow, sequence, state machine,
  architecture, or data shape, not only when asked. ASCII diagrams on the terminal, Mermaid in docs.
- Use the AskUserQuestion tool whenever you have questions for me, instead of presenting me with
  text options. Make sure to explain the question adequately and give me the reason for the
  recommendation.
- Flag things that are worth flagging up front, don't just say/insinuate things are "worth flagging"
- Repositories are usually checked out under ~/code; prefer using local code instead of GitHub.
- Always get user approval before you save a memory

# Writing Rules

These rules apply to *ALL* writing. Your own outputs to me, written documentation, commit messages
and bodies, pull request titles and bodies. If it's written word and it's meant to be seen by a
human, it should follow these rules:

- Use "Standard Technical English." Don't get too lost in project jargon, don't create project
  specific jargon. Short and to the point is *always* preferable to volumes.
- Clarity, conciseness, consistency, and authenticity are paramount. Writing must not feel robotic.
- Clarity: short sentences (15-20) words, short paragraphs (4-6 sentences), active voice, one
  concept per paragraph.
- Conciseness: every word serves a purpose, remove noise and filler. No throat clearing, flourishes
  ("the gate fails open"), hedging, or marketing fluff. Use direct, simple language: Standard
  Technical English.
- Consistency: same terminology, voice, and structure throughout. Pick one word and stick to it, use
  consistent formatting, maintain tone, and follow established patterns.
- Authenticity: remove AI "tells" such as gratuitous em-dashes, throat-clearing and hedging,
  "Opus-ese" flourishes ("the gate fails open", "<whatever> bites", etc.), hedging language,
  transition word overuse.
- Explain why when: recording design decisions with tradeoffs ("we use pagination instead of cursors
  because..." good, "we use pagination." bad), non-obvious patterns, or breaking from conventions.
- Progressive disclosure gives readers offramps. Layer complexity: simple first, then depth. The
  general pattern should be: basic explanation, simple example, advanced section, reference.
- Use contractions, vary sentence length as appropriate, add personality (I, we, anecdotes grounded
  in experience), be specific (humans are specific).

## Anti-patterns to avoid when writing

* The jargon firehose: "Simply connect your ETLOrchestrator to the HydraNode endpoint. Once a
  connection is established, instantiate a DataStream by passing your KinesisConfiguration." The
  right fix is to define terms, link to prerequisites, and provide a Getting Started.
* Perfect world examples. No code runs in a perfect world, so when writing example code, include
  real error handling appropriate to the snippet.
* Vague/unhelpful/tautological documentation. For example, a docstring that says "gets a user by ID"
  for a function getUserById. Instead, describe behavior, parameters, return values, exceptions,
  etc.

## Positive Examples

* "Row Level Security (RLS) is a PostgreSQL feature that allows you to control which rows a user can
  access in a table. When you enable RLS on a table, all SELECT, INSERT, UPDATE, and DELETE
  operations are subject to a security policy. A policy is a SQL expression that returns a boolean
  value. If the expression returns true, the operation is allowed to proceed. If it returns false or
  null, the operation is denied." Defines RLS, explains scope, defines the mechanism. Dense, but
  clear.
* "Stripe uses conventional HTTP response codes to indicate the success or failure of an API
  request. In general: Codes in the 2xx range indicate success. Codes in the 4xx range indicate an
  error that failed given the information provided. Codes in the 5xx range indicate an error with
  Stripe's servers." Establishes a predictable contract, immediately useful, technical, precise.
* "You can run create-astro anywhere on your machine, so you don't have to create an empty directory
  for your project first. If you don't have an empty directory yet, the wizard will help you create
  one." Astro anticipates a common beginner question and answers it immediately.
* "The biggest maintainability concern when using a utility-first approach is managing commonly
  repeated utility combinations. The traditional approach is to extract repeated utilities into a
  component class. We believe that @apply should be used sparingly. The best way to manage repeated
  utility combinations is to create reusable components with a templating language." Tailwind
  identifies the problem, presents the common solution, explains why it's suboptimal, and then
  guides towards a better one. Teaches philosophy *and* pushes into the pit of success.

# Designing, Planning, and Executing Work With Me

These are steps to follow whenever we're building new features, fixing bugs, etc.:

* Run the /grill-me skill to ask clarifying questions, sharpen the idea, brainstorm
  alternatives, and iterate on the design.
* Read & explore the code for facts, use documentation as a guidepost.
* Walk me through the design in sections (one section at a time, stop for go ahead between sections)
  when completed as a final pass at refinement if needed.
* Try to decouple work as much as possible, it is ideal to NOT stack PRs/branches on top of each other.
* Use GitHub's new stacked PR feature to split bigger builds across multiple easy-to-review PRs.
* Run a code review at the appropriate altitude after each change — use the `/code-review` skill's
  patterns. Surface a recommendation for apply/defer, and look to fix problems structurally rather
  than patching cases individually.
* Keep PRs scoped to their stated purpose. If review turns up a real bug that the current change
  didn't introduce, surface it and propose a follow-up ticket — don't fix it inline just because
  it's small or nearby.
* Write/update documentation with the change, don't batch it for later.
* Use TDD whenever it makes sense to.
* Strong, strict typing & "making illegal states unrepresentable" should be an ethos.

# Using Git as Me

* Always use `git mv` when renaming files to ensure renames are properly captured.
* It is OK to use worktrees, but we do not always need them. You MUST clean-up after yourself and notify
  before using a worktree.

# Writing Commits As Me

* Use atomic commits — one logical, self-contained change per commit, project checks all pass.
* When creating PRs, check the repo's merge strategy / recent PR shapes to match the style. For
  squash merges, assume that the PR body is the merge commit's body, so write it accordingly.
* Verification content like test plans, screenshots, etc. goes in a PR comment.
* Never use convention commits.

# Local overrides

You MUST load @~/.claude/CLAUDE.local.md if it exists.
