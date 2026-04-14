# MBTI Agent Personality

> 快速為你的 AI 程式助手設定人格 · Instantly give your AI coding agent a personality

---

## 中文說明

### 這是什麼？

靈感來自和朋友聊天聊到 AI agent 的「個性」，這個小工具讓你用 MBTI 人格框架，為自己的 AI 程式助手設定一套專屬的個性與溝通風格。

不同的人有不同的工作偏好 — 有人喜歡直話直說、有人需要溫暖鼓勵、有人想要創意激盪。現在你的 agent 也可以有對應的性格。

### 功能特色

- **10 題測驗**：前 5 題測自己的人格，後 5 題測你喜歡的 agent 風格，自動推薦最互補的 MBTI 人格
- **16 種 MBTI 人格模板**：每種人格都有專屬的 system prompt、溝通風格與簽名語錄
- **支援多種主流工具**：Cursor、Claude Code、Kiro、Windsurf、GitHub Copilot、Antigravity、VS Code、Zed
- **Project / Global 兩種套用範圍**
- **Append 不覆蓋**：使用標記區塊，不破壞現有設定，可重複執行更換人格
- **8 種語言支援**：繁體中文、簡體中文、English、日本語、한국어、Español、Français、Deutsch

### 安裝與使用

```bash
pip install -r requirements.txt
python main.py
```

### 流程說明

1. **選擇語言**
2. **輸入 MBTI 或進行測驗**
   - 已知自己的 MBTI → 直接輸入，系統推薦互補的 agent 人格（1~3 種）
   - 不知道 → 完成 10 題測驗，系統根據你的類型和偏好自動推薦
   - 想自選 → 瀏覽全部 16 種類型
3. **預覽人格**：查看 ASCII 圖案、描述和 system prompt 風格
4. **選擇工具**：多選你想設定的 coding 工具
5. **選擇範圍**：Project（當前目錄）或 Global（全域）
6. **套用**：以 append 方式寫入設定檔，不覆蓋現有內容

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

### 人格配對邏輯

工具背後使用 MBTI 認知功能理論的互補配對，例如：

- **INTJ 使用者** → 推薦 ENFP、ENTP、INFP 作為 agent（互補型激發創意）
- **ENFP 使用者** → 推薦 INTJ、INFJ、ENTJ（提供結構與策略）
- **ISTJ 使用者** → 推薦 ESFP、ESTP、ISFP（帶來靈活與活力）

後 5 題的偏好答案會進一步微調推薦排序。

### 相依套件

- `questionary` — 互動式 CLI 介面
- `rich` — 終端機美化輸出

---

## English

### What is this?

Inspired by a conversation about AI agent "personalities," this small tool lets you configure your AI coding assistant with an MBTI-based personality — shaping how it communicates, codes, and gives feedback.

Different people have different working styles. Some prefer direct, no-nonsense feedback. Others need encouragement. Some want creative sparks. Now your agent can match.

### Features

- **10-question quiz**: 5 questions about you, 5 about your preferred agent style — auto-recommends the most complementary MBTI personalities
- **16 MBTI personality templates**: Each with a unique system prompt, communication style, and signature quote
- **Supports major coding tools**: Cursor, Claude Code, Kiro, Windsurf, GitHub Copilot, Antigravity, VS Code, Zed
- **Project or Global scope**
- **Append, never overwrite**: Uses tagged blocks — safe to re-run to switch personalities
- **8 languages**: English, 繁體中文, 简体中文, 日本語, 한국어, Español, Français, Deutsch

### Installation & Usage

```bash
pip install -r requirements.txt
python main.py
```

### How it works

1. **Select language**
2. **Enter your MBTI or take the quiz**
   - Know your type → enter it, get 1–3 complementary agent recommendations
   - Don't know → complete 10 questions, get auto-recommendations based on your type + style preferences
   - Just browsing → view all 16 types
3. **Preview the personality**: ASCII art, description, and system prompt style
4. **Select tools**: Multi-select which coding tools to configure
5. **Select scope**: Project (current directory) or Global (all projects)
6. **Apply**: Appended to config files without overwriting existing content

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

### Matching logic

Uses MBTI cognitive function compatibility theory, for example:

- **INTJ user** → recommends ENFP, ENTP, INFP as agent (complementary types that spark creativity)
- **ENFP user** → recommends INTJ, INFJ, ENTJ (provides structure and strategy)
- **ISTJ user** → recommends ESFP, ESTP, ISFP (brings flexibility and energy)

The final 5 quiz questions further refine the ranking based on your preferred agent style.

### Dependencies

- `questionary` — interactive CLI prompts
- `rich` — beautiful terminal output

### License

MIT
