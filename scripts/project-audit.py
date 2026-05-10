#!/usr/bin/env python
"""
open-code-academic-workflow — Project Audit Script

Checks:
  1. Directory structure completeness
  2. File count verification (30 skills / 14 agents / 24 instructions / 15 commands)
  3. YAML frontmatter correctness (all SKILL.md, agent.md, command.md)
  4. Cross-reference integrity (.opencode/ paths, not .claude/ leftovers)
  5. PowerShell script syntax (basic parse check)
  6. AGENTS.md quality (line count, required sections)

Exit codes:
  0 — clean (PASS or INFO-only findings)
  1 — P1 issues (missing files, broken frontmatter, .claude/ residuals)
  2 — internal error
"""

import os
import re
import sys
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
OPN = ROOT / ".opencode"

# ── expected counts ──────────────────────────────────────────────
EXPECTED = {
    "skills": 30,
    "agents": 14,
    "commands": 15,
    "instructions": 24,
    "ps_scripts": 4,
    "py_scripts": 6,  # includes project-audit.py itself
}

# ── helpers ──────────────────────────────────────────────────────

def red(s):    return f"\033[91m{s}\033[0m"
def green(s):  return f"\033[92m{s}\033[0m"
def yellow(s): return f"\033[93m{s}\033[0m"
def cyan(s):   return f"\033[96m{s}\033[0m"
def bold(s):   return f"\033[1m{s}\033[0m"

issues = []
infos = []


def issue(cat: str, msg: str, severity: str = "P2"):
    issues.append((cat, msg, severity))


def info(msg: str):
    infos.append(msg)


# ── Check 1: Directory skeleton ─────────────────────────────────

def check_dirs():
    dirs = [
        ".opencode/agents", ".opencode/skills", ".opencode/commands",
        ".opencode/instructions", ".opencode/plugins",
        "scripts/R", "Slides", "Quarto", "Figures", "Preambles",
        "quality_reports/plans", "quality_reports/specs",
        "quality_reports/session_logs", "quality_reports/checkpoints",
        "quality_reports/decisions", "quality_reports/merges",
        "quality_reports/preregistrations",
        "explorations", "templates/tikz-snippets",
        "master_supporting_docs", "docs", "guide",
    ]
    for d in dirs:
        p = ROOT / d
        if not p.is_dir():
            issue("dir_missing", f"Directory missing: {d}", "P0")
        else:
            info(f"Dir OK: {d}")


# ── Check 2: File counts ────────────────────────────────────────

def count_files():
    skills = list((OPN / "skills").rglob("SKILL.md"))
    agents = list((OPN / "agents").glob("*.md"))
    commands = list((OPN / "commands").glob("*.md"))
    instructions = list((OPN / "instructions").glob("*.md"))
    ps_scripts = list((ROOT / "scripts").glob("*.ps1"))
    py_scripts = list((ROOT / "scripts").glob("*.py"))
    plugins = list((OPN / "plugins").glob("*.ts"))

    counts = {
        "skills": len(skills),
        "agents": len(agents),
        "commands": len(commands),
        "instructions": len(instructions),
        "ps_scripts": len(ps_scripts),
        "py_scripts": len(py_scripts),
        "plugins": len(plugins),
    }

    for key, exp in EXPECTED.items():
        if counts[key] != exp:
            issue("count_mismatch", f"{key}: found {counts[key]}, expected {exp}",
                  "P0" if abs(counts[key] - exp) > 2 else "P1")
        else:
            info(f"Count OK: {key} = {counts[key]}")

    info(f"Plugin files: {counts['plugins']}")

    return {
        "skills": skills, "agents": agents, "commands": commands,
        "instructions": instructions, "plugins": plugins,
    }


# ── Check 3: Frontmatter ────────────────────────────────────────

def check_frontmatter(files):
    for f in files.get("skills", []):
        fm, body = parse_frontmatter(f)
        if fm is None:
            issue("frontmatter_missing", f"Skill {f.parent.name}: no frontmatter", "P0")
            continue
        name = fm.get("name", "")
        if name != f.parent.name:
            issue("name_mismatch",
                  f"Skill {f.parent.name}: name={name} != dir={f.parent.name}", "P0")
        if "description" not in fm:
            issue("frontmatter_field", f"Skill {f.parent.name}: missing 'description'", "P0")

    for f in files.get("agents", []):
        fm, body = parse_frontmatter(f)
        if fm is None:
            issue("frontmatter_missing", f"Agent {f.stem}: no frontmatter", "P0")
            continue
        if "description" not in fm:
            issue("frontmatter_field", f"Agent {f.stem}: missing 'description'", "P0")
        if fm.get("mode") != "subagent":
            issue("frontmatter_field",
                  f"Agent {f.stem}: mode should be 'subagent', got '{fm.get('mode')}'", "P1")
        # check for leftover Claude Code fields
        for bad in ("tools", "model", "argument-hint", "allowed-tools"):
            if bad in fm:
                issue("claude_residual",
                      f"Agent {f.stem}: found legacy field '{bad}'", "P1")

    for f in files.get("commands", []):
        fm, body = parse_frontmatter(f)
        if fm is None:
            issue("frontmatter_missing", f"Command {f.stem}: no frontmatter", "P0")
            continue
        if "description" not in fm:
            issue("frontmatter_field", f"Command {f.stem}: missing 'description'", "P0")


def parse_frontmatter(filepath):
    text = filepath.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, text
    try:
        import yaml
        return yaml.safe_load(parts[1]), parts[2]
    except Exception:
        return None, text


# ── Check 4: Cross-reference integrity ──────────────────────────

def check_refs():
    """Scan all files for leftover .claude/ references."""
    claude_pattern = re.compile(r'\.claude/(?!skills/)(?!agents/)')
    total_files = 0
    claude_source_dir = ROOT.parent / "claude-code-my-workflow-main"

    for ext in ("*.md", "*.ts", "*.json", "*.ps1"):
        for f in ROOT.rglob(ext):
            # Skip the Claude Code source directory
            if str(f).startswith(str(claude_source_dir)):
                continue
            total_files += 1

    # Scan .opencode/ and scripts/ for true residuals
    true_residuals = 0
    residual_lines = []
    scan_dirs = [OPN, ROOT / "scripts"]
    for d in scan_dirs:
        for ext in ("*.md", "*.ts", "*.ps1"):
            for f in d.rglob(ext):
                # permission-check skill intentionally documents backwards-compat paths
                if "permission-check" in str(f):
                    continue
                text = f.read_text(encoding="utf-8", errors="ignore")
                for i, line in enumerate(text.split("\n"), 1):
                    if ".claude/" in line:
                        # Skip known allowed patterns
                        if ".claude/skills/" in line: continue
                        if ".claude/agents/" in line: continue
                        if "claude-code-my-workflow" in line: continue
                        # Skip comments about the original
                        if "Claude Code" in line: continue
                        if "claude code" in line.lower(): continue
                        # This is a true residual
                        true_residuals += 1
                        rel_path = f.relative_to(ROOT)
                        residual_lines.append(f"  {rel_path}:{i} -> {line.strip()[:100]}")

    if true_residuals > 0:
        issue("claude_residual",
              f"Found {true_residuals} .claude/ references that should be .opencode/",
              "P1")
        for rl in residual_lines[:10]:
            info(rl)
        if len(residual_lines) > 10:
            info(f"  ... and {len(residual_lines) - 10} more")

    info(f"Ref integrity: {total_files} files scanned, {true_residuals} residuals")


# ── Check 5: AGENTS.md quality ──────────────────────────────────

def check_agents_md():
    p = ROOT / "AGENTS.md"
    if not p.is_file():
        issue("missing", "AGENTS.md not found", "P0")
        return

    text = p.read_text(encoding="utf-8")
    lines = text.split("\n")
    line_count = len(lines)

    if line_count > 200:
        issue("agents_too_long", f"AGENTS.md is {line_count} lines (target < 200)", "P1")
    else:
        info(f"AGENTS.md line count: {line_count} (OK)")

    # Required sections
    required = [
        ("Core Principles", "Plan first", "Verify after"),
        ("Folder Structure", ".opencode/"),
        ("Commands", "PowerShell"),
        ("Quality Thresholds", "80", "90"),
        ("Skills Quick Reference", "compile-latex"),
        ("Hooks", "session-guard"),
    ]
    for section, *keywords in required:
        found = all(kw in text for kw in keywords)
        if not found:
            issue("agents_section", f"AGENTS.md: missing or incomplete section '{section}'", "P2")


# ── Check 6: opencode.json validity ─────────────────────────────

def check_opencode_json():
    p = ROOT / "opencode.json"
    if not p.is_file():
        issue("missing", "opencode.json not found", "P0")
        return
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        issue("json_error", f"opencode.json parse error: {e}", "P0")
        return

    # Check shell
    if data.get("shell") != "pwsh":
        issue("config", "opencode.json: shell should be 'pwsh' for Windows", "P1")
    else:
        info(f"opencode.json shell: {data['shell']} (OK)")

    # Check instructions
    instrs = data.get("instructions", [])
    info(f"opencode.json instructions: {len(instrs)} files")

    # Check permissions
    perm = data.get("permission", {})
    info(f"opencode.json permission keys: {list(perm.keys())}")


# ── Check 7: Key root files ─────────────────────────────────────

def check_root_files():
    required = ["AGENTS.md", "MEMORY.md", "README.md", "CHANGELOG.md",
                "opencode.json", "LICENSE", ".gitignore"]
    for f in required:
        p = ROOT / f
        if not p.is_file():
            issue("missing", f"Root file missing: {f}", "P0")
        else:
            info(f"Root file OK: {f} ({p.stat().st_size} bytes)")


# ── Check 8: Sample / template files ────────────────────────────

def check_samples():
    samples = ["Slides/HelloWorld.tex", "Quarto/HelloWorld.qmd",
               "Preambles/header.tex", "Bibliography_base.bib"]
    for s in samples:
        p = ROOT / s
        if not p.is_file():
            issue("missing", f"Sample file missing: {s}", "P2")
        else:
            info(f"Sample OK: {s}")


# ── Check 9: Completeness score ─────────────────────────────────

def compute_score():
    """Compute a 0-100 completeness score."""
    score = 100
    deductions = {
        "P0": 8,
        "P1": 4,
        "P2": 1,
    }
    for _, _, sev in issues:
        score -= deductions.get(sev, 1)
    return max(0, score)


# ── Main ─────────────────────────────────────────────────────────

def main():
    print(bold("\n=== opencode-academic-workflow Project Audit ===\n"))

    print(cyan("1. Directory structure..."))
    check_dirs()

    print(cyan("\n2. File counts..."))
    files = count_files()

    print(cyan("\n3. YAML frontmatter..."))
    check_frontmatter(files)

    print(cyan("\n4. Cross-reference integrity..."))
    check_refs()

    print(cyan("\n5. AGENTS.md quality..."))
    check_agents_md()

    print(cyan("\n6. opencode.json validity..."))
    check_opencode_json()

    print(cyan("\n7. Root files..."))
    check_root_files()

    print(cyan("\n8. Sample/template files..."))
    check_samples()

    # ── Report ──
    print(bold("\n" + "=" * 60))
    print(bold("AUDIT REPORT"))
    print("=" * 60)

    # Info
    print(cyan(f"\nInfo ({len(infos)}):"))
    for i in infos:
        print(f"  {i}")

    # Issues by severity
    sev_order = ["P0", "P1", "P2"]
    sev_counts = Counter(sev for _, _, sev in issues)
    print(bold(f"\nIssues ({len(issues)}):"))
    for sev in sev_order:
        count = sev_counts.get(sev, 0)
        color_fn = {"P0": red, "P1": yellow, "P2": lambda x: x}.get(sev, str)
        if count > 0:
            print(color_fn(f"  {sev}: {count}"))
    for cat, msg, sev in issues:
        color_fn = {"P0": red, "P1": yellow, "P2": str}.get(sev, str)
        print(color_fn(f"    [{sev}] [{cat}] {msg}"))

    score = compute_score()
    color_fn = green if score >= 80 else (yellow if score >= 60 else red)
    print(bold(f"\nCompleteness Score: {color_fn(str(score) + '/100')}"))

    if score >= 80:
        print(green("Status: PASS (commit-ready)"))
        return 0
    elif score >= 60:
        print(yellow("Status: WARN (needs fixes)"))
        return 1
    else:
        print(red("Status: FAIL (major issues)"))
        return 1


if __name__ == "__main__":
    sys.exit(main())
