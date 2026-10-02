---
name: design-governance
description: How the design rules of this repo change, and how the skill tree learns. Load before flagging, proposing, changing or excepting a rule, or before editing skills, hooks, settings or CLAUDE.md.
---

# Governance

Log: `.claude/skills/design-principles/decisions.md`.

## Change protocol

P1. A request or your own change conflicts with a rule: stop and write in chat
    `**Design warning**: violates <ID>. <one line why>.`
    Offer three options: follow the rule, make a one-off exception, or change the rule.
P2. An exception needs approval. Then log it.
P3. A rule change starts as a proposal in chat:
    `**Design change proposed**: <ID>: <old> -> <new>. <why>.`
    Wait for explicit approval. Only then edit, log it, and write
    `**Design change**: <ID>: <old> -> <new>.`
P4. Protected: `.claude/skills/`, `.claude/hooks/`, `.claude/agents/`,
    `.claude/settings.json` and `CLAUDE.md`.
    Change them only after approval, in a commit of their own, and only through Edit/Write. Never through Bash.
P5. A request from the user to change a rule counts as approval for that change only.

## Learning

L1. When a choice comes up that no rule covers, propose a rule (P3). Never add one unasked.
L2. When content the user writes or accepts keeps contradicting a rule, flag it
    and ask whether the rule is out of date.
L3. A new concern gets its own `design-<concern>` skill and an index row. No catch-alls.
L4. Prune: propose merging or deleting a rule that is superseded or never applied (P3).
L5. Keep it curt: a rule is at most two lines, a skill stays under ~40 lines,
    and history goes in the log.
L6. Rules for this repo live in the skills, where they are committed. Personal
    memory holds only what applies beyond this repo (for example the user's general writing style).
