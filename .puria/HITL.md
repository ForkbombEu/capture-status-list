# HITL.md

## ⚠️ Human In The Loop

This file contains observations that require human validation.

It is a controlled buffer between:

- agent discovery
- human decision
- doctrine (`PURIA.md`)

---

## Rules

- entries are NOT authoritative
- entries MUST NOT influence agent decisions
- this file is **write-only for agents**
- only humans may promote entries into `PURIA.md`

Agents MUST:

- append new valid observations
- NEVER modify or delete existing entries
- keep entries minimal and factual

---

## Constraints

Only add an entry if:

- the pattern appears at least twice
- it may impact architecture, naming, or workflow

If unsure:

→ DO NOT add  
→ DO NOT assume

---

## Entry Template

- id: hitl-XXXX
- observation:
- location:
- evidence:
- rationale:

---

## Entries

- id: hitl-0001
- observation: `PURIA.md` mandates a neubrutalist design system, while `.puria/design/DESIGN.md` is the Credimi brand specification, which is calm, flat, hairline-bordered and explicitly forbids the neubrutalist traits (thick borders, hard offset shadows, square corners).
- location: `PURIA.md` "Design Source"; `.puria/design/DESIGN.md`
- evidence: `PURIA.md` requires "thick, explicit borders", "hard offset shadows", "square or near-square corners"; `.puria/design/DESIGN.md` §7 requires a 6px canonical radius and "almost flat" elevation, and §15 forbids shadows on cards by default.
- rationale: Both documents are declared authoritative for design. The UI follows `.puria/design/DESIGN.md`, because `PURIA.md` names `.puria/design/DESIGN.md` the source of truth for design when present, and because this repository is a Credimi Extra whose brand is set by the `credimi-extras-template` repository. A human must decide whether `PURIA.md` keeps the neubrutalist clause for Credimi Extras repositories.
- id: hitl-0002
- observation: `PURIA.md` requires formatting through a repository-defined formatter before every commit, but `mise.toml` only defines `gofmt` for Go. The repository's active codebase is Python, and no Python formatter (e.g., black, ruff format) task is defined.
- location: `mise.toml` `[tasks.format]`; `PURIA.md` "Git Behavior" pre-commit validation
- evidence: `mise.toml` format task is `gofmt -w .` only; CI (`ci.yml`) runs `mise run fix` (Go) but no Python format/lint step; pytest is the only Python validation.
- rationale: Python commits cannot satisfy the "run the repository-defined formatter" requirement as written. A human should decide whether to add a Python formatter task (e.g., `ruff format` / `black`) to `mise.toml` and CI.
