---
name: review-comments
description: Use when Patrick has review comments on his PR to work through, such as "we got a review", "look at the comments on PR 123", or a link to a review. Fetches every comment, groups duplicates, sorts them into priority buckets, then discusses them one at a time with background and options before changing anything. Invoke as /review-comments [PR number or URL].
user-invocable: true
---

# Review Comments

Work through review comments on Patrick's PR as a conversation, not a to-do list. The comments are
someone else's opinion of his code. Some are right, some miss context, and some are out of scope. He
decides each one, with enough background to decide well. Nothing changes until every comment has a
decision.

```
/review-comments
  ├─ 1. Fetch everything
  ├─ 2. Summary: group duplicates, sort into buckets, recommend per item
  │       └─ stop for go-ahead
  ├─ 3. Discuss one comment at a time  ◄─┐
  │       background, options, decision   │ next comment
  │       (no code changes) ──────────────┘
  ├─ 4. Apply the decisions, atomic commits
  └─ 5. Draft replies, post only with approval
```

This is a discussion. Don't use plan mode or `ExitPlanMode`, and don't write a plan file.

## Steps

### 1. Fetch

- PR: the number or URL from the arguments, else `gh pr view` for the current branch. Repos are under
  `~/code`; read local code rather than GitHub.
- Get all of it, with the GitHub MCP tools (`pull_request_read`: `get_reviews`, `get_review_comments`,
  `get_comments`), falling back to `gh api`:
  - review bodies, which often hold comments of their own
  - inline threads, with resolved and outdated state
  - general PR comments
- Note who commented. Prior comments from Patrick himself are his notes, not review feedback; list
  them separately.
- Read the code each comment points at, at the PR's head commit. Read enough around it to judge the
  comment, not only the line. A comment can be right about a line and wrong about the design.

### 2. Summary

Show this before discussing anything.

- **Group duplicates**: the same point made twice, whether on one line or several, is one item. List
  every thread it covers.
- **Bucket by priority**, most important first. Skip empty buckets.

| Bucket | What goes in it |
|---|---|
| 🔴 Bug or correctness | The code is wrong, loses data, or the reviewer found a real failure |
| 🟠 Should fix | Valid design, typing, test, or doc concerns for this PR |
| ❓ Question | The reviewer asks for an answer, or needs context |
| 🟢 Nit or style | Naming, taste, small cleanups |
| 🎫 Out of scope | A real problem this PR didn't introduce (propose a follow-up ticket) |
| ✅ Already handled | Resolved or outdated threads |

- For each item: number, one-line description, the reviewer's name, `file:line`, and a
  recommendation of **Apply**, **Reply**, **Ticket**, or **Skip**. Keep the reason to a clause.
- Order the discussion by bucket, then by how much the item affects the others. Say where one fix
  would settle several items.
- End with the count per bucket, and stop for his go-ahead.

### 3. Discuss, one at a time

Take one item per turn. Don't batch them, and don't use a single prompt for several items. For each:

1. **The comment**: quote it, with who said it and where. For a duplicate group, say which threads
   it covers.
2. **Background**: what the code does today and why. Include whatever Patrick needs to judge the
   comment and may not remember: the relevant code, how callers use it, what the repo's
   `CLAUDE.md`/`AGENTS.md` says, and what already exists elsewhere in the codebase. If the answer
   depends on something outside the repo, say what and how to check it.
3. **Is the reviewer right?** Give a plain verdict with the evidence. If they're wrong or missing
   context, say so and why.
4. **Options**: two to four real choices, each with its tradeoff and what the diff would look like.
   Include **Reply only** or **Skip** when it's a valid option. Add a diagram when it helps explain
   a flow or data shape.
5. **Recommendation**, with the reason.
6. **Ask** with `AskUserQuestion`, once the background is on screen. Put the key facts in the
   question text, so it stands on its own. The options match step 4. Then wait.

Record the decision and move on. Don't change code, commit, or post during this step. If an answer
changes how a later item should be handled (one fix settles several), say so and update that item.

If Patrick wants to change the approach, or asks what something means, answer in text and ask again.
If the question prompt is rejected, ask in plain text. Don't repeat the same prompt.

Fix problems structurally. If three comments point at one design problem, propose one change, not
three patches.

Keep the PR scoped. A real bug the PR didn't introduce is **Ticket**, even when it's small.

### 4. Apply

After the last decision, restate the list in a few lines (item, decision), then:

1. Make the change structurally. Update the docs and comments in the same change, and describe what
   the code is now, not the history.
2. Run the repo's lint and documented test command. If it fails for a reason the change didn't cause,
   stop and ask.
3. Commit with the sandbox disabled (GPG signing hangs otherwise). One logical change per commit, so
   each change maps to the comments it answers. Title it `<TICKET>: <what and why>`, taken from the
   branch name, and omit the prefix when the ticket is a placeholder or unknown. Never use
   Conventional Commits, and don't list files in the body.
4. Never push.

### 5. Reply

- Draft a reply for every thread: what changed (with the commit), why not, or the answer to the
  question. Short, direct, no filler. Use the PR author's voice (`patricks-voice` if it helps).
- Show the drafts. Post only the ones he approves, and don't resolve threads unless he says to. A
  duplicate thread gets a pointer to the thread that has the answer.
- For **Ticket** items, draft the title and body. Don't create them without approval.
- Remind him to check things outside the repo that a change might affect, such as dashboards and
  alerts when a metric is renamed.

## Common mistakes

- Skipping the summary and starting on the first comment.
- Presenting the comments as one plan document and asking for approval.
- Asking the question before the background is shown.
- A bare option list: "Apply / Skip / Reply". Each option needs its tradeoff.
- Agreeing with a reviewer without checking the code, or dismissing one without evidence.
- Fixing a comment inline during the discussion.
- Treating every comment as blocking. Most are nits or questions.
- Replying "done" to a duplicate thread instead of pointing at the one with the answer.
- Posting replies, resolving threads, or pushing without approval.

## Self-Check

- [ ] Every thread, review body, and general comment is in the summary or the already-handled list
- [ ] Duplicates are grouped, and each item has a bucket and a recommendation
- [ ] Waited for a go-ahead after the summary
- [ ] One item per turn, each with background, a verdict, options with tradeoffs, and a recommendation
- [ ] No code changed, committed, or posted before every item was decided
- [ ] Out-of-scope problems became ticket drafts, not inline fixes
- [ ] Replies drafted for every thread, and nothing posted without approval
