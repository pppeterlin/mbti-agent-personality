# MBTI Agent Personality

> 快速為你的 AI 程式助手設定人格 · Instantly give your AI coding agent a personality

---

## 中文說明

### 這是什麼？

靈感來自和朋友聊天聊到 AI agent 的「個性」，這個小工具讓你用 MBTI 人格框架，為自己的 AI 程式助手設定一套專屬的個性與溝通風格。

不同的人有不同的工作偏好 — 有人喜歡直話直說、有人需要溫暖鼓勵、有人想要創意激盪。現在你的 agent 也可以有對應的性格。

### 功能特色

- **16 種 MBTI 人格模板**：每種人格都有專屬的 system prompt、溝通風格與簽名語錄
- **支援多種主流工具**：Cursor、Claude Code、Kiro、Windsurf、GitHub Copilot、Antigravity、VS Code、Zed
- **Project / Global 兩種套用範圍**
- **Append 不覆蓋**：使用標記區塊，不破壞現有設定，可重複執行更換人格
- **8 種語言支援**：繁體中文、簡體中文、English、日本語、한국어、Español、Français、Deutsch
- **不知道 MBTI？** 直接進入測驗即可，或自行瀏覽全部 16 種人格選擇

### 安裝與使用

```bash
pip install -r requirements.txt
python main.py
```

### 設定檔位置

| 工具 | Project 路徑 | Global 路徑 |
|------|-------------|------------|
| Cursor | `.cursor/rules/agent-personality.mdc` | `~/.cursor/rules/agent-personality.mdc` |
| Claude Code | `CLAUDE.md` | `~/.claude/CLAUDE.md` |
| Kiro | `.kiro/steering/agent-personality.md` | `~/.kiro/agents/agent-personality.md` |
| Windsurf | `.windsurf/rules/agent-personality.md` | `~/.codeium/windsurf/memories/global_rules.md` |
| GitHub Copilot | `.github/copilot-instructions.md` | `~/.copilot/copilot-instructions.md` |
| Antigravity | `.antigravity/rules.md` | `~/.antigravity/rules.md` |
| VS Code | `.github/copilot-instructions.md` | `~/.copilot/copilot-instructions.md` |
| Zed | `.rules` | `~/.config/zed/rules.md` |

### 相依套件

- `questionary` — 互動式 CLI 介面
- `rich` — 終端機美化輸出

---

## English

### What is this?

Inspired by a conversation about AI agent "personalities," this small tool lets you configure your AI coding assistant with an MBTI-based personality — shaping how it communicates, codes, and gives feedback.

Different people have different working styles. Some prefer direct, no-nonsense feedback. Others need encouragement. Some want creative sparks. Now your agent can match.

### Features

- **16 MBTI personality templates**: Each with a unique system prompt, communication style, and signature quote
- **Supports major coding tools**: Cursor, Claude Code, Kiro, Windsurf, GitHub Copilot, Antigravity, VS Code, Zed
- **Project or Global scope**
- **Append, never overwrite**: Uses tagged blocks — safe to re-run to switch personalities
- **8 languages**: English, 繁體中文, 简体中文, 日本語, 한국어, Español, Français, Deutsch
- **Don't know your MBTI?** Just take the quiz — or browse all 16 types and pick one yourself

### Installation & Usage

```bash
pip install -r requirements.txt
python main.py
```

### Config file locations

| Tool | Project path | Global path |
|------|-------------|------------|
| Cursor | `.cursor/rules/agent-personality.mdc` | `~/.cursor/rules/agent-personality.mdc` |
| Claude Code | `CLAUDE.md` | `~/.claude/CLAUDE.md` |
| Kiro | `.kiro/steering/agent-personality.md` | `~/.kiro/agents/agent-personality.md` |
| Windsurf | `.windsurf/rules/agent-personality.md` | `~/.codeium/windsurf/memories/global_rules.md` |
| GitHub Copilot | `.github/copilot-instructions.md` | `~/.copilot/copilot-instructions.md` |
| Antigravity | `.antigravity/rules.md` | `~/.antigravity/rules.md` |
| VS Code | `.github/copilot-instructions.md` | `~/.copilot/copilot-instructions.md` |
| Zed | `.rules` | `~/.config/zed/rules.md` |

### Dependencies

- `questionary` — interactive CLI prompts
- `rich` — beautiful terminal output

### License

MIT
