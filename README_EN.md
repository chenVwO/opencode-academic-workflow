# opencode-academic-workflow

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.1.0-informational)](CHANGELOG.md)
[![Skills](https://img.shields.io/badge/skills-30-6f42c1)](.opencode/skills/)
[![Agents](https://img.shields.io/badge/agents-14-0366d6)](.opencode/agents/)
[![Windows](https://img.shields.io/badge/platform-Windows-0078d4)]()

> Port of [claude-code-my-workflow](https://github.com/pedrosantanna/claude-code-my-workflow) (v1.8.0) to **OpenCode** with full **Windows** compatibility.

**AI-assisted academic workflow template** — fork once, get 30 skills, 14 specialized agents, 24 rules, and a TypeScript plugin that automates the review-compile-verify loop. Originally developed for an Emory University PhD course (6 lecture decks, 800+ slides), now ported to OpenCode.

[English](#) | [中文](README.md)

---

## Table of Contents

- [Quick Start](#quick-start)
- [What's Included](#whats-included)
- [How It Works](#how-it-works)
- [Use Cases](#use-cases)
- [Project Structure](#project-structure)
- [Adapting for Your Field](#adapting-for-your-field)
- [License](#license)

---

## Quick Start

### Prerequisites

| Tool | Required For | Install |
|------|-------------|---------|
| [OpenCode](https://opencode.ai/download) | Everything | `npm install -g opencode-ai` or `choco install opencode` |
| git | Version control | [git-scm.com](https://git-scm.com/downloads) |
| Python 3 | Internal checkers | [python.org](https://www.python.org/) |
| XeLaTeX | Beamer compilation | [TeX Live](https://tug.org/texlive/) |
| [Quarto](https://quarto.org) | Web slides | [quarto.org/docs/get-started](https://quarto.org/docs/get-started/) |
| R | Data analysis (`/data-analysis`) | [r-project.org](https://www.r-project.org/) |

> **Minimum:** OpenCode + git + Python 3. R and XeLaTeX are optional if you only do text/code review work.

### Setup (~5 minutes)

```powershell
# 1. Fork this repo on GitHub (click "Fork"), then clone
git clone https://github.com/YOUR_USERNAME/opencode-academic-workflow.git
cd opencode-academic-workflow

# 2. Check your environment
.\scripts\validate-setup.ps1

# 3. Start OpenCode
opencode

# 4. Verify everything works
/compile-latex HelloWorld    # Compile Beamer sample → PDF
/deploy HelloWorld           # Render Quarto sample → HTML
```

After confirmation, delete `Slides/HelloWorld.tex` and `Quarto/HelloWorld.qmd` and start your real work.

---

## What's Included

<details open>
<summary><b>30 Skills · 14 Agents · 24 Rules · 1 Auto-Plugin</b></summary>

### 30 Skills (`.opencode/skills/`)

Agent loads skills on-demand via the `skill` tool. 15 have user-facing slash commands.

| Category | Skills |
|----------|--------|
| **Slides** | `/compile-latex`, `/deploy`, `/proofread`, `/visual-audit`, `/pedagogy-review`, `/slide-excellence`, `/create-lecture`, `/translate-to-quarto`, `/devils-advocate` |
| **Papers** | `/review-paper`, `/seven-pass-review`, `/lit-review`, `/respond-to-referees`, `/preregister` |
| **Data** | `/data-analysis`, `/audit-reproducibility`, `/review-r`, `/validate-bib` |
| **Research** | `/research-ideation`, `/interview-me`, `/verify-claims` |
| **Quality** | `/qa-quarto`, `/commit`, `/deep-audit`, `/checkpoint`, `/context-status`, `/permission-check` |
| **TikZ** | `/extract-tikz`, `/new-diagram` |
| **Meta** | `/learn` |

### 14 Agents (`.opencode/agents/`)

Callable via `@agent-name` or invoked automatically by skills.

| Agent | Role |
|-------|------|
| `proofreader` | Grammar, typos, overflow, consistency |
| `slide-auditor` | Visual layout audit |
| `pedagogy-reviewer` | 13-pattern teaching quality review |
| `r-reviewer` | R code quality & reproducibility |
| `tikz-reviewer` | TikZ diagram visual critique |
| `verifier` | End-to-end compilation verification |
| `claim-verifier` | Post-Flight CoVe fact-checking |
| `beamer-translator` | Beamer → Quarto translation |
| `quarto-critic` | Adversarial Beamer vs Quarto QA |
| `quarto-fixer` | Implements critic fixes |
| `editor` | Journal editor (desk + referee selection + decision) |
| `domain-referee` | Substance referee (5-dim weighted) |
| `methods-referee` | Methodology referee (paper-type branching) |
| `domain-reviewer` | Template — customize for your field |

### 1 Plugin (`.opencode/plugins/session-guard.ts`)

Auto-loaded TypeScript plugin replacing all 6 Claude Code hooks:

- Context usage monitoring (warnings at 40/55/65/80/90%)
- Verify reminders after editing `.tex`/`.qmd`/`.R` files
- Session-log update reminders at idle
- Compaction context preservation

### 24 Rules (`.opencode/instructions/`)

Loaded via `opencode.json` or read on-demand by agents.
</details>

---

## How It Works

### The Contractor Pattern

```
You describe a task
    ↓
OpenCode [PLANS] the approach
    ↓
You approve the plan
    ↓
OpenCode invokes the right skill
    ↓
Skill runs: implement → verify → review → fix → re-verify → score
    ↓
Returns summary when quality standards are met
```

### Three Verification Layers

| Layer | Pattern | Best For |
|-------|---------|----------|
| **Critic-Fixer** | Two agents in serial adversarial loop | Presentation & structural bugs |
| **Cross-Artifact** | Paper ↔ code dependency traversal | Numeric claim consistency |
| **Post-Flight / CoVe** | Fresh-context verifier, never sees draft | Factual hallucination detection |

### Quality Thresholds (Advisory)

| Score | Gate | Meaning |
|-------|------|---------|
| 80 | Commit | Good enough to save |
| 90 | PR | Ready for deployment |
| 95 | Excellence | Aspirational |

Enforced by `/commit` skill (halts + asks for override). No pre-commit hook.

---

## Use Cases

| Task | How This Helps |
|------|---------------|
| Lecture slides (Beamer/Quarto) | Creation, translation, multi-agent review, deploy |
| Research papers | Lit review, manuscript review, simulated peer review |
| Data analysis | End-to-end R pipeline, publication-ready output |
| Replication packages | AEA-compliant packaging, reproducibility audit |
| Presentations | Visual audit, pedagogy review, cognitive load check |
| Proposals | Structured drafting with adversarial critique |

---

## Project Structure

```
opencode-academic-workflow/
├── AGENTS.md                  ← Session entrypoint (loaded every session)
├── opencode.json              ← Config: shell, model, permissions, instructions
├── .opencode/
│   ├── agents/        (14)    ← Specialized subagents
│   ├── skills/        (30)    ← On-demand workflow instructions
│   ├── commands/      (15)    ← User-facing slash commands
│   ├── instructions/  (24)    ← Rules & protocols
│   ├── plugins/               ← session-guard.ts (auto hooks)
│   └── WORKFLOW_QUICK_REF.md
├── Slides/                    ← Beamer .tex sources
├── Quarto/                    ← RevealJS .qmd mirrors
├── Figures/                   ← Images, TikZ SVGs, R outputs
├── Preambles/header.tex       ← LaTeX preamble & theme
├── scripts/                   ← PowerShell + Python utilities
├── quality_reports/           ← Plans, specs, logs, checkpoints
├── templates/                 ← Session-log, quality-report, etc.
├── explorations/              ← Research sandbox (fast-track: 60 pts)
├── Bibliography_base.bib
├── README.md / README.md
├── MEMORY.md / CHANGELOG.md
└── LICENSE
```

---

## Adapting for Your Field

1. **Customize the domain reviewer** — `.opencode/agents/domain-reviewer.md` has a 5-lens template
2. **Fill in notation knowledge base** — `.opencode/instructions/knowledge-base-template.md`
3. **Update the color palette** — `Preambles/header.tex` ↔ `Quarto/theme-template.scss`
4. **Add field-specific R pitfalls** — `.opencode/instructions/r-code-conventions.md`
5. **Set up exploration folder** — `explorations/README.md`

---

## Windows Notes

| Original (Claude Code) | This Port (OpenCode) |
|------------------------|----------------------|
| `CLAUDE.md` | `AGENTS.md` |
| `.claude/settings.json` | `opencode.json` |
| `.claude/skills/` | `.opencode/skills/` |
| `.claude/agents/` | `.opencode/agents/` |
| `.claude/rules/` | `.opencode/instructions/` |
| `.claude/hooks/*.py` | `.opencode/plugins/session-guard.ts` |
| `*.sh` → `*.ps1` | PowerShell, no WSL needed |
| `TEXINPUTS=..:$TEXINPUTS` | `$env:TEXINPUTS="..\Preambles;$env:TEXINPUTS"` |

---

## License

MIT License — see [LICENSE](LICENSE).

---

## Acknowledgments

This is a port of [Pedro Sant'Anna](https://github.com/pedrosantanna)'s `claude-code-my-workflow` (MIT), originally extracted from Econ 730 at Emory University. The peer-review pipeline is adapted from [Hugo Sant'Anna's clo-author](https://github.com/hugosantanna/clo-author) with permission.
