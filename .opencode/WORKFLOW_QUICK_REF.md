# Workflow Quick Reference

**Model:** Contractor (you direct, OpenCode orchestrates)

---

## The Loop

```
Your instruction
    ↓
[PLAN] (if multi-file or unclear) → Show plan → Your approval
    ↓
[EXECUTE] Implement, verify, done
    ↓
[REPORT] Summary + what's ready
    ↓
Repeat
```

---

## Quality Gates (Advisory)

| Score | Action |
|-------|--------|
| >= 80 | Ready to commit |
| < 80  | Fix blocking issues |

---

## Common Commands

| Command | What It Does |
|---------|-------------|
| `/compile-latex [file]` | 3-pass XeLaTeX + bibtex |
| `/deploy [LectureN]` | Render Quarto + sync to docs/ |
| `/commit [msg]` | Quality-gated commit |
| `/proofread [file]` | Grammar/typo/overflow |
| `/slide-excellence [file]` | Multi-agent slide review |
| `/qa-quarto [LectureN]` | Adversarial Beamer vs Quarto QA |
| `/review-paper [file]` | Manuscript review |
| `/data-analysis [dataset]` | End-to-end R analysis |

---

## Non-Negotiables

- **Plan first** — no multi-file work without a plan
- **Verify after** — compile/render/run after every task
- **Single source of truth** — Beamer `.tex` is authoritative

---

## Hooks (Auto)

All 6 lifecycle hooks are handled automatically by `.opencode/plugins/session-guard.ts`:
- Context usage monitoring (progressive warnings at 40/55/65/80/90%)
- Verify reminders after editing `.tex`/`.qmd`/`.R` files
- Session-log update nudges at idle
- Compaction context preservation (plan + log state injected on compact)

---

## Exploration Mode

For experimental work in `explorations/`:
- 60/100 quality threshold (vs 80/100 for production)
- No plan needed — just a research value check
