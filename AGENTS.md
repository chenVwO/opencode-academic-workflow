# opencode-academic-workflow

**An academic AI-assisted workflow template for OpenCode, ported from claude-code-my-workflow (v1.8.0).**

---

## Core Principles

- **Plan first** — use plan mode before multi-file tasks; save plans to `quality_reports/plans/`
- **Verify after** — compile/render/run after every task; confirm output before claiming done
- **Single source of truth** — Beamer `.tex` is authoritative; Quarto `.qmd` derives from it
- **Quality gates** — score >= 80 to commit, >= 90 for PR (advisory)
- **[LEARN] tags** — when corrected, save `[LEARN:category] correct → wrong` to MEMORY.md

Cross-session context: MEMORY.md (committed). Past plans, specs, logs: `quality_reports/`.

---

## Folder Structure

```
opencode-academic-workflow/
├── AGENTS.md
├── opencode.json
├── .opencode/
│   ├── agents/          (14)
│   ├── skills/          (30)
│   ├── commands/        (15)
│   ├── instructions/    (24)
│   ├── plugins/         session-guard.ts (auto-loaded)
│   └── WORKFLOW_QUICK_REF.md
├── Memo.md / README.md / CHANGELOG.md
├── Slides/ Quarto/ Figures/ Preambles/
├── scripts/ (PowerShell + Python + R)
├── quality_reports/ (plans/ specs/ session_logs/ checkpoints/...)
├── explorations/
├── templates/ (+ tikz-snippets/)
└── master_supporting_docs/
```

---

## Commands (PowerShell)

```powershell
# LaTeX 3-pass
cd Slides
$env:TEXINPUTS="..\Preambles;$env:TEXINPUTS"
& xelatex -interaction=nonstopmode file.tex
$env:BIBINPUTS="..\$env:BIBINPUTS"; & bibtex file
& xelatex -interaction=nonstopmode file.tex
& xelatex -interaction=nonstopmode file.tex

# Deploy Quarto
& ".\scripts\sync-to-docs.ps1" [LectureN]

# Quality score
python scripts\quality-score.py Quarto\HelloWorld.qmd

# Palette sync (LaTeX ← SCSS)
& ".\scripts\check-palette-sync.ps1"
```

---

## Quality Thresholds (Advisory)

| Score | Checkpoint | Meaning |
|-------|------------|---------|
| 80    | Commit     | Good enough to save |
| 90    | PR         | Ready for deployment |
| 95    | Excellence | Aspirational |

Enforced by `/commit` skill (halts and asks for override). Not enforced by pre-commit hook.

---

## Skills Quick Reference

| Command | Description |
|---------|-------------|
| `/compile-latex [file]` | 3-pass XeLaTeX + bibtex |
| `/deploy [LectureN]` | Render Quarto + sync to docs/ |
| `/proofread [file]` | Grammar/typo/overflow review |
| `/visual-audit [file]` | Slide layout audit |
| `/pedagogy-review [file]` | Narrative, notation, pacing |
| `/qa-quarto [LectureN]` | Adversarial Beamer vs Quarto QA |
| `/slide-excellence [file]` | Multi-agent slide review |
| `/create-lecture` | Full lecture creation |
| `/review-paper [file]` | Manuscript review (3 modes) |
| `/data-analysis [dataset]` | End-to-end R analysis |
| `/commit [msg]` | Quality-gated commit |
| `/lit-review [topic]` | Literature search + synthesis |
| `/validate-bib` | Cross-reference citations |
| `/verify-claims [file]` | Chain-of-Verification fact-check |
| `/translate-to-quarto [file]` | Beamer → Quarto translation |

All 30 skills available; agent loads them on-demand via the `skill` tool. 14 subagents callable via `@agent-name`.

---

## Hooks (Plugin-Based)

All 6 lifecycle hooks from the original are handled automatically by `.opencode/plugins/session-guard.ts` — context monitoring, verify reminders, session-log nudges, notifications, and compaction context. No manual checklists needed.

---

## Current Project State

| Lecture | Beamer | Quarto | Key Content |
|---------|--------|--------|-------------|
| HelloWorld | Slides/HelloWorld.tex | Quarto/HelloWorld.qmd | Minimal deck to verify setup |
