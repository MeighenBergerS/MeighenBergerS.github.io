---
name: design-docs
description: The README, docs/ and the comment headers of the data files. Load when editing README.md, anything in docs/, or the comment block at the top of a data file.
---

# Docs

G1. The README is for the owner only: what the repo is, the build commands,
    where to edit what. One screen, no tutorial.
G2. How to fill a data file lives in the comment block at the top of that
    file, not in the README.
G3. `docs/` holds guides that people and tools follow (`news-style.md`). A
    rule for Claude goes in a skill, and the skill links to the guide.
G4. When a command, a path or a workflow step changes, the README and the
    affected skill change in the same commit.
