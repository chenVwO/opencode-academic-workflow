# OpenCode 学术工作流：AI 辅助写论文、做课件、数据分析

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.1.0-informational)](CHANGELOG.md)
[![Skills](https://img.shields.io/badge/skills-30-6f42c1)](.opencode/skills/)
[![Agents](https://img.shields.io/badge/agents-14-0366d6)](.opencode/agents/)
[![Windows](https://img.shields.io/badge/platform-Windows-0078d4)]()
[![中文](https://img.shields.io/badge/lang-中文-red)](README_CN.md)

> 将 [claude-code-my-workflow](https://github.com/pedrosantanna/claude-code-my-workflow) (v1.8.0) 移植至 **OpenCode**，完整适配 **Windows** 环境。

**AI 辅助学术工作流模板** — 专为学术写作、论文撰写、课件制作、数据分析设计。fork 即用，内置 30 个技能、14 个专业 Agent、24 条规则，以及一个自动管控审查-编译-验证循环的 TypeScript 插件。源自 Emory 大学博士课程（6 套课件，800+ 页幻灯片）。

适用于：**写论文** · **结课论文** · **毕业论文** · **学术论文** · **文献综述** · **LaTeX 论文** · **Quarto 论文** · **R 语言数据分析** · **Beamer 课件** · **可复现研究** · **论文润色** · **论文审稿**

[English](README_EN.md) | [中文](#)

---

## 目录

- [适用人群](#适用人群)
- [快速开始](#快速开始)
- [包含组件](#包含组件)
- [工作原理](#工作原理)
- [适用场景](#适用场景)
- [项目结构](#项目结构)
- [适配你的领域](#适配你的领域)
- [许可证](#许可证)

---

## 适用人群

| 身份 | 场景 | 推荐技能 |
|------|------|---------|
| **本科生 / 硕士生** | 结课论文、课程报告、毕业论文 | `/create-lecture` `/data-analysis` `/lit-review` `/proofread` |
| **博士生** | 学术论文、开题报告、博士论文 | `/review-paper --peer` `/seven-pass-review` `/preregister` `/verify-claims` |
| **教师 / 讲师** | 课件制作、学术演示、备课 | `/slide-excellence` `/pedagogy-review` `/translate-to-quarto` `/deploy` |
| **研究人员** | 文献综述、数据分析、可复现研究 | `/lit-review` `/data-analysis` `/audit-reproducibility` `/review-r` |
| **学生（通用）** | LaTeX 论文排版、参考文献管理、论文润色 | `/compile-latex` `/validate-bib` `/proofread` `/visual-audit` |

> 无论你在写**结课论文**、准备**毕业论文**、制作**学术 PPT**，还是跑**R 语言数据分析**，这个模板都能让 AI 帮你完成整套流程。

## 快速开始

### 先决条件

| 工具 | 用途 | 安装方式 |
|------|------|---------|
| [OpenCode](https://opencode.ai/download) | 核心引擎 | `npm install -g opencode-ai` 或 `choco install opencode` |
| git | 版本控制 | [git-scm.com](https://git-scm.com/downloads) |
| Python 3 | 内部检查脚本 | [python.org](https://www.python.org/) |
| XeLaTeX | Beamer 幻灯片编译 | [TeX Live](https://tug.org/texlive/) |
| [Quarto](https://quarto.org) | Web 幻灯片 | [quarto.org/docs/get-started](https://quarto.org/docs/get-started/) |
| R | 数据分析 (`/data-analysis`) | [r-project.org](https://www.r-project.org/) |

> **最低要求：** OpenCode + git + Python 3。如果只做文本/代码审查，无需安装 XeLaTeX 和 Quarto。

### 安装配置 (~5分钟)

```powershell
# 1. Fork 本仓库至你的 GitHub，然后克隆
git clone https://github.com/YOUR_USERNAME/opencode-academic-workflow.git
cd opencode-academic-workflow

# 2. 检查运行环境
.\scripts\validate-setup.ps1

# 3. 启动 OpenCode
opencode

# 4. 验证一切正常
/compile-latex HelloWorld    # 编译 Beamer 示例 → PDF
/deploy HelloWorld           # 渲染 Quarto 示例 → HTML
```

确认无误后，删除 `Slides/HelloWorld.tex` 和 `Quarto/HelloWorld.qmd`，开始你的正式工作。

---

## 包含组件

<details open>
<summary><b>30 个技能 · 14 个 Agent · 24 条规则 · 1 个自动插件</b></summary>

### 30 个技能 (`.opencode/skills/`)

Agent 通过 `skill` 工具按需加载技能，其中 15 个有面向用户的斜线命令。

| 分类 | 技能 |
|------|------|
| **幻灯片** | `/compile-latex` 编译、`/deploy` 部署、`/proofread` 校阅、`/visual-audit` 视觉审查、`/pedagogy-review` 教学审查、`/slide-excellence` 综合审查、`/create-lecture` 创建课件、`/translate-to-quarto` 格式转换、`/devils-advocate` 反方挑战 |
| **论文** | `/review-paper` 审稿（3种模式）、`/seven-pass-review` 七步审查、`/lit-review` 文献综述、`/respond-to-referees` 回复审稿人、`/preregister` 预注册 |
| **数据** | `/data-analysis` 数据分析、`/audit-reproducibility` 可复现性审计、`/review-r` R代码审查、`/validate-bib` 参考文献核验 |
| **研究** | `/research-ideation` 研究构思、`/interview-me` 研究访谈、`/verify-claims` 事实核验 |
| **质量** | `/qa-quarto` 对抗性QA、`/commit` 质量门控提交、`/deep-audit` 深度审计、`/checkpoint` 状态快照、`/context-status` 上下文状态、`/permission-check` 权限诊断 |
| **TikZ** | `/extract-tikz` 图表提取、`/new-diagram` 新建图表 |
| **元工具** | `/learn` 经验沉淀 |

### 14 个 Agent (`.opencode/agents/`)

可通过 `@agent-name` 调用，或由技能自动触发。

| Agent | 职责 |
|-------|------|
| `proofreader` | 语法、拼写、溢出、一致性校阅 |
| `slide-auditor` | 视觉效果布局审计 |
| `pedagogy-reviewer` | 13 维度教学质量审查 |
| `r-reviewer` | R 代码质量与可复现性 |
| `tikz-reviewer` | TikZ 图表严苛视觉审查 |
| `verifier` | 端到端编译验证 |
| `claim-verifier` | Post-Flight 事实核验（CoVe 链式验证） |
| `beamer-translator` | Beamer → Quarto 格式翻译 |
| `quarto-critic` | 对抗性 Beamer 与 Quarto 对比 QA |
| `quarto-fixer` | 根据 critic 报告执行修复 |
| `editor` | 期刊编辑（初审 + 审稿人指派 + 综合决策） |
| `domain-referee` | 领域实质内容评审（5 维加权） |
| `methods-referee` | 方法论评审（按论文类型分支） |
| `domain-reviewer` | 模板 — 根据你的专业领域自定义 |

### 1 个插件 (`.opencode/plugins/session-guard.ts`)

自动加载的 TypeScript 插件，替代原 Claude Code 的 6 个生命周期钩子：

- 上下文使用量监控（在 40/55/65/80/90% 时发出渐进警告）
- 编辑 `.tex`/`.qmd`/`.R` 文件后提醒编译/渲染验证
- 会话 IDLE 时提醒更新会话日志
- 上下文压缩时保留计划与日志状态

### 24 条规则 (`.opencode/instructions/`)

通过 `opencode.json` 的 `instructions` 字段加载，或由 Agent 按需读取。
</details>

---

## 工作原理

### 承包商模式

```
你描述一个任务
    ↓
OpenCode [规划] 方案
    ↓
你审核并批准计划
    ↓
OpenCode 调用相应的技能（skill）
    ↓
技能内运行：实现 → 验证 → 审查 → 修复 → 再验证 → 评分
    ↓
达到质量标准后返回摘要
```

### 三层验证架构

| 层级 | 模式 | 擅长场景 |
|------|------|---------|
| **对抗循环** | 两个 Agent 串行对抗 QA | 呈现与结构缺陷 |
| **跨工件审查** | 论文 ↔ 代码 依赖遍历 | 数值声明一致性 |
| **Post-Flight / CoVe** | 独立上下文验证器 | 事实虚构检测 |

### 质量阈值（建议性）

| 分数 | 关卡 | 含义 |
|------|------|------|
| 80 | 提交 | 可以保存 |
| 90 | PR | 可以发布 |
| 95 | 卓越 | 理想目标 |

由 `/commit` 技能强制执行（不达标则中断并要求确认）。无 git pre-commit 钩子。

---

## 适用场景

| 任务 | 如何使用 | 关键词 |
|------|---------|--------|
| **写论文 / 结课论文 / 毕业论文** | 文献综述 → 数据分析 → 稿件撰写 → 模拟审稿 → 论文润色，全流程 AI 辅助 | `结课论文` `毕业论文` `学术论文` `论文写作` |
| **论文审稿与润色** | 模拟同行评审（编辑 + 2 位匿名审稿人 + 综合决策），校阅语法/拼写/排版 | `论文审稿` `论文润色` `论文修改` |
| **文献综述** | 结构化文献检索、主题聚类、研究空白识别 | `文献综述` `参考文献` |
| **课件幻灯片（Beamer / Quarto）** | 创建、格式转换、多 Agent 审查、一键部署 | `Beamer` `Quarto` `PPT` `幻灯片` |
| **数据分析（R 语言）** | 端到端 R 流程，数据清洗 → 建模 → 可视化 → 导出，发表级输出 | `R语言` `数据分析` `回归分析` |
| **可复现研究** | 论文与代码交叉验证，数值一致性审计，AEA 合规打包 | `可复现性` `AEA` `研究审计` |
| **LaTeX 论文排版** | 3-pass XeLaTeX 编译、参考文献自动核验、TikZ 图表制作 | `LaTeX` `XeLaTeX` `TikZ` `排版` |

---

## 项目结构

```
opencode-academic-workflow/
├── AGENTS.md                  ← 会话入口（每次会话加载）
├── opencode.json              ← 配置：shell、模型、权限、规则引用
├── .opencode/
│   ├── agents/        (14)    ← 专业子 Agent
│   ├── skills/        (30)    ← 按需加载的工作流指引
│   ├── commands/      (15)    ← 面向用户的斜线命令
│   ├── instructions/  (24)    ← 规则与协议文件
│   ├── plugins/               ← session-guard.ts（自动钩子）
│   └── WORKFLOW_QUICK_REF.md  ← 工作流速查表
├── Slides/                    ← Beamer .tex 源文件
├── Quarto/                    ← RevealJS .qmd 镜像文件
├── Figures/                   ← 图片、TikZ SVG、R 输出
├── Preambles/header.tex       ← LaTeX 前导文件与主题
├── scripts/                   ← PowerShell + Python 工具
├── quality_reports/           ← 计划、规格、日志、检查点
├── templates/                 ← 会话日志、质量报告等模板
├── explorations/              ← 研究沙箱（快速通道：60 分阈值）
├── Bibliography_base.bib      ← 集中式参考文献库
├── README.md / README_CN.md
├── MEMORY.md / CHANGELOG.md
└── LICENSE
```

---

## 适配你的领域

1. **自定义领域评审 Agent** — `.opencode/agents/domain-reviewer.md` 提供了五维审查模板
2. **填写符号知识库** — `.opencode/instructions/knowledge-base-template.md`
3. **更新颜色方案** — `Preambles/header.tex` ↔ `Quarto/theme-template.scss` 双表面配色合同
4. **添加领域 R 语言陷阱** — `.opencode/instructions/r-code-conventions.md`
5. **设置探索目录** — `explorations/README.md`

---

## Windows 适配说明

| 原版 (Claude Code) | 移植版 (OpenCode) |
|---------------------|--------------------|
| `CLAUDE.md` | `AGENTS.md` |
| `.claude/settings.json` | `opencode.json` |
| `.claude/skills/` | `.opencode/skills/` |
| `.claude/agents/` | `.opencode/agents/` |
| `.claude/rules/` | `.opencode/instructions/` |
| `.claude/hooks/*.py` | `.opencode/plugins/session-guard.ts` |
| `*.sh` → `*.ps1` | PowerShell，无需 WSL |
| `TEXINPUTS=..:$TEXINPUTS` | `$env:TEXINPUTS="..\Preambles;$env:TEXINPUTS"` |

---

## 许可证

MIT License — 详见 [LICENSE](LICENSE)。

---

## 致谢

本项目移植自 [Pedro Sant'Anna](https://github.com/pedrosantanna) 的 `claude-code-my-workflow`（MIT 协议），源自 Emory 大学 Econ 730 博士课程。同行评审流程组件经许可适配自 [Hugo Sant'Anna 的 clo-author](https://github.com/hugosantanna/clo-author)。
