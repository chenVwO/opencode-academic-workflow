import type { Plugin } from "@opencode-ai/plugin"
import { readFileSync, writeFileSync, existsSync, statSync, mkdirSync } from "fs"
import { join } from "path"

interface State {
  toolCalls?: number
  shownThresholds?: number[]
  fileNudges?: Record<string, number>
  lastLogCheck?: number
}

function statePath(projectDir: string): string {
  const dir = join(projectDir, "quality_reports", "session_logs", ".plugin-state")
  return join(dir, "session-guard.json")
}

function loadState(projectDir: string): State {
  const p = statePath(projectDir)
  if (!existsSync(p)) return {}
  try { return JSON.parse(readFileSync(p, "utf-8")) }
  catch { return {} }
}

function saveState(projectDir: string, state: State): void {
  const p = statePath(projectDir)
  mkdirSync(join(p, ".."), { recursive: true })
  writeFileSync(p, JSON.stringify(state, null, 2))
}

export const SessionGuard: Plugin = async ({ worktree, client }) => {
  if (!worktree) return {}

  return {
    "tool.execute.after": async (input) => {
      const state = loadState(worktree)
      const toolCalls = (state.toolCalls ?? 0) + 1
      state.toolCalls = toolCalls

      const pct = Math.min((toolCalls / 150) * 100, 100)

      // context-monitor: progressive threshold warnings
      const thresholds = [40, 55, 65, 80, 90]
      for (const t of thresholds) {
        if (pct >= t && !((state.shownThresholds ?? []).includes(t))) {
          state.shownThresholds = [...(state.shownThresholds ?? []), t]
          const msg = t >= 90 ? `[session-guard] Context at ${pct.toFixed(0)}% — critical, finish current task`
            : t >= 80 ? `[session-guard] Context at ${pct.toFixed(0)}% — compaction approaching`
            : `[session-guard] Context at ${pct.toFixed(0)}% — consider saving state or using /learn`
          await client.app.log({ body: { service: "session-guard", level: pct >= 80 ? "warn" : "info", message: msg }})
        }
      }

      // verify-reminder: after editing .tex/.qmd/.R, suggest compile
      if ((input.tool === "edit" || input.tool === "write") && input.args?.filePath) {
        const fp: string = input.args.filePath
        if (/\.(tex|qmd|R)$/i.test(fp)) {
          const nudges = state.fileNudges ?? {}
          const lastNudge = nudges[fp] ?? 0
          if (Date.now() - lastNudge > 300_000) {
            nudges[fp] = Date.now()
            state.fileNudges = nudges
            const action = fp.endsWith(".tex") ? "compile with XeLaTeX"
              : fp.endsWith(".qmd") ? "render with Quarto"
              : "run with Rscript"
            await client.app.log({ body: { service: "session-guard", level: "info", message: `[verify-reminder] ${fp} changed — ${action} before marking task done` }})
          }
        }
      }

      saveState(worktree, state)
    },

    "session.idle": async () => {
      const state = loadState(worktree)
      const logDir = join(worktree, "quality_reports", "session_logs")
      const logs = existsSync(logDir) ? readFileSync(logDir, "utf-8") : ""

      const now = Date.now()
      if (state.lastLogCheck && (now - state.lastLogCheck) < 600_000) return
      state.lastLogCheck = now

      // Check if session log exists and is recent
      let newestLogTime = 0
      if (existsSync(logDir)) {
        const files = readFileSync(logDir, "utf-8").split("\n").filter(Boolean)
        for (const f of files) {
          const full = join(logDir, f)
          if (existsSync(full)) {
            const mtime = statSync(full).mtimeMs
            if (mtime > newestLogTime) newestLogTime = mtime
          }
        }
      }

      if (newestLogTime === 0) {
        await client.app.log({ body: { service: "session-guard", level: "info", message: "[log-reminder] No session log found — consider creating one in quality_reports/session_logs/" }})
      } else if (now - newestLogTime > 3600_000) {
        await client.app.log({ body: { service: "session-guard", level: "info", message: "[log-reminder] Session log may need updating (last modified > 1 hour ago)" }})
      }

      saveState(worktree, state)
    },

    "experimental.session.compacting": async (_input, output) => {
      output.context = output.context ?? []
      output.context.push(`## Session Guard (auto-injected)
Before continuing after compaction:
1. Re-read active plan from quality_reports/plans/ if one was in progress
2. Re-read most recent session log from quality_reports/session_logs/
3. Confirm MEMORY.md has any pending [LEARN] entries committed`)
    },
  }
}