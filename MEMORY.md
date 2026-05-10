# Project Memory

## OpenCode Port

[LEARN:port] OpenCode uses TypeScript plugins for lifecycle hooks (`@opencode-ai/plugin`), not Python scripts. Plugin events `tool.execute.after`, `session.idle`, and `experimental.session.compacting` cover all 6 Claude Code hook behaviors in a single file.

[LEARN:port] OpenCode skills have NO `allowed-tools` or `argument-hint` frontmatter. Tool restrictions are set at the agent level via `permission` in `opencode.json`.

[LEARN:port] OpenCode subagents (`mode: subagent`) inherit the calling agent's model by default — no `model: inherit` needed.

[LEARN:port] PowerShell script conventions: `$env:VAR` for environment variables, `& executable` for calling executables, `;` as path separator in env vars (not `:`).

[LEARN:port] OpenCode does NOT path-scope rules like Claude Code. All rules are in `.opencode/instructions/` and loaded via `opencode.json` `instructions` field or read on-demand by the agent.

## Windows-Specific

[LEARN:windows] `python` not `python3` on Windows (Python launcher `py` is also available).

[LEARN:windows] OpenCode shell setting `"shell": "pwsh"` uses PowerShell 5.1+. All paths use `\` separator (PowerShell also accepts `/`).

[LEARN:windows] `tui.toast.show` in plugins is cross-platform — no need for `osascript`/`notify-send` on Windows.

[LEARN:windows] Desktop notifications via `msg` command work but `tui.toast.show` is preferred for in-app context.

## Workflow Patterns

[LEARN:workflow] Requirements specification phase catches ambiguity before planning → reduces rework 30-50%. Use spec-then-plan for complex/ambiguous tasks.

[LEARN:workflow] Plans, specs, and session logs must live on disk (not just in conversation) to survive compaction and session boundaries.

## Documentation Standards

[LEARN:documentation] When adding new features, update BOTH README and AGENTS.md immediately to prevent documentation drift.

[LEARN:documentation] Always document new templates in README's "What's Included" section.

## Quality Gates

[LEARN:quality] Quality gates are advisory at the harness level — the `/commit` skill runs checks and halts on failure, but there is no git pre-commit hook that blocks a direct `git commit`.

## Verification Architecture

[LEARN:verification] Three complementary verification patterns:
1. Critic-fixer loop — two agents, serial, adversarial (best for presentation bugs)
2. Cross-artifact review — horizontal dependency traversal (paper ↔ code consistency)
3. Post-Flight / CoVe — single agent, fresh-context fork (factual hallucination detection)
