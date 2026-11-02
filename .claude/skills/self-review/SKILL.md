---
name: self-review
description: Use when Patrick asks to self-review his own branch before opening or updating a PR. Wraps /code-review, adds his AGENTS.md rule checks and known blind spots, reports findings by priority, then applies the fix groups he picks. Invoke as /self-review [--uncommitted-only] [--effort <level>].
user-invocable: true
---

# Self-Review

Review Patrick's own branch the way he'd want a second pass: bugs first, sorted by how bad they are,
fixed structurally rather than one at a time. `/code-review` finds bugs; this skill adds the checks
`/code-review` doesn't know about (his AGENTS.md rules and what other reviewers keep catching on his
PRs), then puts it all in one report.

It's his branch, so be blunt. No hedging, no softening.

```
/self-review
  ├─ 1. Gather context
  ├─ 2. Bug hunt (/code-review)  ─┐
  ├─ 3. Rule checks               ├─ in parallel
  ├─ 4. Blind-spot checks        ─┘
  ├─ 5. Verify every finding
  ├─ 6. Report by priority
  ├─ 7. Ask about the next 3–4 most severe findings,  ◄─┐
  │       one question per finding, all in one prompt     │
  ├─ 8.   apply that batch, check, commit  ───────────────┘ next batch
  └─ 9. Squash fixups once every finding is decided
```

## Arguments

- `--uncommitted-only`: review only `git diff HEAD` and untracked files. Skip `$BASE...HEAD`.
- `--effort <level>`: passed to `/code-review`. Default `high`.

## Steps

### 1. Gather context

- Ticket: parse the ticket key (`[A-Z]+-\d+`) from the branch name. An all-zeros key (`ABC-0000`) is
  a placeholder and means no ticket.
- Conventions: read the repo's `CLAUDE.md`/`AGENTS.md` and the global instructions for commit
  title format, lint and test commands, and repo-specific invariants. Steps 3 and 8 use them.
- Base: `git fetch origin`, then set `$BASE` to `origin/<PR base branch>` (from
  `gh pr view --json baseRefName`), or `origin/<default branch>` when there's no PR. Never diff
  against the local `main`: it's often stale and drags upstream work into the review. Every step
  uses `$BASE`.
- Diffs: `git diff $BASE...HEAD` (committed) and `git diff HEAD` (uncommitted). Read each untracked
  file from `git status --porcelain`. Review it as new code if it belongs to the change. Otherwise
  it's a leftover. Remember which hunks are which; every finding gets tagged `[committed]` or
  `[uncommitted]`.
- Commits: `git log --format='%h %s%n%b' $BASE..HEAD`.
- History state, from `gh pr view --json isDraft,reviews,state` and whether the branch is pushed
  (`git rev-parse @{u}`). Record one of:
  - `rewritable`: the branch isn't pushed, and there's no PR or only a draft with no reviews.
  - `pushed`: the branch is pushed, but nobody has reviewed it.
  - `reviewed`: a non-draft PR, or any review at all.

  Never plan anything that rewrites commits already on the remote, since that needs a force-push.
  Commits made locally during this review can still be changed before they're pushed.

### 2. Bug hunt

Invoke the `code-review` skill with the effort level and `$BASE` as the target, so it reviews the
same diff as steps 3 and 4. It runs in the background; do steps 3 and 4 while it runs, then wait
for its notification. Never predict its results. It may skip its own verification pass, so treat
its output as candidates for step 5, not findings.

### 3. Rule checks

Run every check. Each one needs a concrete hit (file and line), not a vibe.

- **Docs**: behavior, config, or an interface changed, but the docs that describe that area didn't.
  Grep `CLAUDE.md`, `AGENTS.md`, `README*`, and `docs/` for the module, flow, or service the change
  touches. A doc that now lists an incomplete set (flows, services, modules) counts.
- **Scope**: hunks unrelated to the ticket. A real bug the branch didn't introduce goes to the
  follow-up lane, not a fix.
- **Callee contracts**: for each existing function the new code calls, read how that function
  fails. Does it throw, return an error, or log and resolve? Does "resolved" mean "done", or only
  "queued"? When the new caller depends on a guarantee the callee doesn't give (for example, it acks,
  retries, or dead-letters based on success), that's a finding. If the callee's behavior predates
  the branch, put it in 🎫.
- **Typing**: types that are stale next to their usage (an interface missing fields the code
  reads), `any`, or loose `string`s where a union or enum makes bad states unrepresentable.
- **Tests**: each behavior change has a test that would fail without it.
- **Commits**: each commit is atomic, titled `<TICKET>: ...` when there's a ticket, not a
  Conventional Commit (`feat:`, `fix(x):`), and never uses a placeholder key in a title. Also flag
  merge commits from the base (rebase instead), commits that are empty against `$BASE` because the
  work already landed upstream, and commit bodies that no longer match the code. On a `pushed` or
  `reviewed` branch, fixing these means a force-push. Say so in the finding and recommend
  **Defer**.
- **Repo invariants**: anything the repo's `CLAUDE.md`/`AGENTS.md` says must hold (patterns to use,
  modules to go through, things that don't mean what they look like).
- **Comments**: comments and docstrings are true *after* this change, aren't tautological ("gets a
  user by ID"), and follow the writing rules (no AI tells, no flourishes). A comment that lies is a
  correctness finding, not a nit.
- **Leftovers**: untracked scratch files, debug logging, `console.log`, `.only` in tests, TODOs with
  no ticket.

### 4. Blind-spot checks

These are what other reviewers catch most often on Patrick's PRs. All are mandatory.

- **Dropped assertions** (the biggest one): when a test file changes, compare the old and new
  assertions hunk by hunk. Flag every dropped tag, field, metric name, or check, and every swapped
  name. A refactor that loses an assertion is a 🟠, not a nit.
- **Stale names after a rename**: grep the repo for the old identifier in code, JSDoc, metric names,
  log messages, and docs. Skip this check when nothing was renamed.
- **Schema vs. type drift**: fields in a JSON schema or event schema that the TypeScript type is
  missing, or the reverse.
- **Unhandled rejections**: new async paths, fire-and-forget promises, or event handlers with no
  `try`/`catch`.
- **Metric cardinality**: label values that come from input (message properties, user IDs, error
  strings) instead of a fixed set.
- **Shutdown and timeouts**: close order, what still runs after a timeout, and whether timeouts
  conflict with each other or with the deployment's termination grace period.

### 5. Verify

Read the code behind every finding, including the ones from `/code-review`. Drop anything that
doesn't hold. If a finding depends on something outside the repo (a producer contract, deployed
config), keep it and mark it **needs confirmation** with the exact question to ask. Bucket it by
its worst outcome if the answer goes the wrong way. Unconfirmed data loss is still 🔴.

### 6. Report

Start with a summary, before any findings:

```
## Summary
**Verdict:** <Not ready to merge | Ready after fixes | Ready to merge> — <one sentence why>
| 🔴 n | 🟠 n | 🟢 n | 🎫 n |
- <The 1–3 findings that matter most, one line each, with their numbers>
- <Recommended structural fix, if any, and which findings it covers>
- <Open questions from "needs confirmation", if any>
```

Keep the summary under ten lines. Then list the findings.

Group findings into these buckets, most severe first. Skip empty buckets.

| Bucket | What goes in it |
|---|---|
| 🔴 Fix before merge | Data loss, crashes, leaks, production stability |
| 🟠 Fix in this PR | Edge-case correctness, comments that lie, dropped assertions, missing or stale docs |
| 🟢 Types & hygiene | Typing, naming, leftovers, commit titles, small cleanups |
| 🎫 Follow-up ticket | Real bugs this branch didn't introduce |

Number findings across the whole report. Each finding is:

```
**N. <Bold title stating the problem>** (`path/to/file.ts:123`) [committed]
<2–4 sentences: what's wrong, the concrete failure, and the fix.>
```

Tags, added after the location where they apply:

- `[committed]` or `[uncommitted]`, always.
- `Structural: covers #A, #B` on the refactor, and `Structural: fixed by #M` on each finding it
  fixes. The refactor gets its own number, in the bucket of its most severe covered finding, and
  can list several locations. Prefer it over patching each finding.
- **needs confirmation**, from step 5.

After the findings, list in one line each: candidates dropped in step 5 and why, and checks that
came up clean. This shows what was checked, not only what failed.

Add one short `★ Insight` paragraph only if a finding teaches something reusable.

### 7. Decide

Decide in batches. Take the 3–4 most severe undecided findings, in report order, and ask one
`AskUserQuestion` with one question per finding (the tool allows four). One question for a whole
bucket, or for the whole report, is too much to decide at once. A question per finding also lets
Patrick drop or reshape a single finding.

Each question restates its finding (the problem, the concrete failure, the fix) so it stands on its
own. Say when its fix covers another finding, or is covered by one, but still ask about each finding
separately. Options: **Apply**, **Defer**, **Ticket**. Put the recommended option first with
"(Recommended)" and say why in its description. Recommend **Ticket** for the follow-up lane. Don't
use text questions.

An answer may reject a finding or explain that it's by design. Drop that finding. If a commit body
or comment caused the misread, note it so a later finding (commits, comments) fixes it.

Finish step 8 for a batch before asking about the next one.

### 8. Apply

Runs once per batch, right after Patrick decides it, for the findings he picked **Apply** (or
**Ticket**, for item 5).

1. Fix structurally. If a `Structural` refactor covers several findings, do the refactor once, not
   the patches, and add a test for each finding it covers.
2. Update the docs for every fix in the same commit as the fix. Grep the same places as the Docs
   check for anything the fix makes stale, including code comments and docstrings near the change.
   Follow the global writing rules: document what *is*, not the history of the fix.
3. Run the repo's lint command and its documented test command, exactly as the repo documents
   it. Don't build a narrower test invocation or work around a failing bootstrap; if the
   documented command fails for a reason other than the change, stop and ask. Fix failures the change caused before committing. If they still fail, stop and report
   the output.
4. Commit with the sandbox disabled (GPG signing hangs otherwise). How depends on the history
   state from step 1:
   - `rewritable`: `git commit --fixup=<sha>` for each fix, where `<sha>` is the last commit that
     touched those lines (fewer rebase conflicts). Don't squash yet; step 9 does it once.
   - `pushed`: `git commit --fixup=<sha>` as above, but never squash them. They push as a
     fast-forward, and a squash-merged PR folds them in.
   - `reviewed`: new atomic commits titled `<TICKET>: <what and why>`. Omit the prefix when the
     ticket is a placeholder or missing.
5. For each **Ticket** finding, draft the ticket title and body. Don't create it without approval.
6. Never push.

Then go back to step 7 for the next batch.

### 9. Squash

Only for `rewritable` branches, and only after every finding is decided. Skip it for `pushed` and
`reviewed` branches. Squashing once keeps the history rewrite in one place, and a commit-history
finding may change how it's done.

Squash with `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash $BASE`. That also drops merge commits
from the base and replays the branch onto `$BASE`. If the rebase conflicts, run `git rebase --abort`
and report it.

## Common mistakes

- Reporting `/code-review` output without verifying it. Every finding gets read against the code.
- Filing a pre-existing bug as 🔴 because it's bad. If this branch didn't introduce it, it's 🎫.
- Patching three symptoms of one design problem instead of tagging them `Structural`.
- Skipping the assertion diff because "the tests pass". Dropped assertions always pass.
- Diffing against the local `main`. Use `$BASE`.
- Trusting that an existing callee does what its name says. Check how it fails before relying on
  its success.
- Hedging ("might be worth considering"). State the problem and the fix.
- Asking about a whole bucket, or every bucket, in one question. Ask one question per finding, 3–4
  findings at a time.
- Starting work before every question in the batch is answered.

## Self-Check

- [ ] The report opens with the summary: verdict, counts, top findings, open questions
- [ ] Every finding has a `file:line` and a `[committed]`/`[uncommitted]` tag
- [ ] Every finding was verified against the code
- [ ] Blind-spot checks ran, including the assertion diff for every changed test file
- [ ] Pre-existing bugs are in 🎫, not fixed inline
- [ ] Questions asked in batches of 3–4 findings, one question per finding, most severe first,
      each with a recommendation; each batch applied before the next is asked
- [ ] Missing or stale docs are 🟠, not 🟢
- [ ] Every applied fix updated its docs in the same commit
- [ ] Nothing applied, committed, or ticketed without Patrick picking it
