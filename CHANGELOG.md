# Changelog

## v0.1.0 — 2026-05-10 (Initial Port)

### Ported from claude-code-my-workflow (v1.8.0)

Initial port of the academic workflow template from Claude Code to OpenCode, with full Windows compatibility.

### Added

- **`AGENTS.md`** — OpenCode entry point (replaces `CLAUDE.md`)
- **`opencode.json`** — configuration with PowerShell shell, permissions, instructions
- **`.opencode/agents/`** (14 agents) — all original agent prompts in OpenCode YAML frontmatter format
- **`.opencode/skills/`** (30 skills) — all original skill workflows, bash commands converted to PowerShell
- **`.opencode/commands/`** (15 commands) — user-facing slash commands for common workflows
- **`.opencode/instructions/`** (24 rules) — all original rules, YAML frontmatter removed, paths updated
- **`.opencode/plugins/session-guard.ts`** — TypeScript plugin replacing all 6 Claude Code hooks
- **`scripts/*.ps1`** — PowerShell scripts replacing bash (validate-setup, sync-to-docs, palette check, surface sync)
- **`README.md`, `MEMORY.md`** — documentation with port-specific notes

### Windows Adaptation

- All shell commands converted from bash to PowerShell syntax
- `$env:VAR` for environment variables, `;` separator for path lists
- `& executable` operator for calling executables
- `python` (not `python3`) for Python scripts
- Path separators: `\\` (PowerShell also accepts `/`)
- Plugin-based hooks via `@opencode-ai/plugin` (no Python lifecycle scripts)
- No WSL required — runs natively on Windows

### Component Counts

- **30 skills** (1:1 port from original)
- **14 agents** (1:1 port from original)
- **24 rules** (1:1 port from original)
- **1 plugin** (replaces 6 hooks)
- **4 PowerShell scripts** (replaces 4 bash scripts)
