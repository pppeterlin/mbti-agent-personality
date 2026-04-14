import os
import re

# Marker format used to identify the personality block in config files
MARKER_START = "<!-- AGENT_PERSONALITY_START: {mbti} -->"
MARKER_END = "<!-- AGENT_PERSONALITY_END -->"
MARKER_PATTERN = re.compile(
    r'<!-- AGENT_PERSONALITY_START: [A-Z]+ -->.*?<!-- AGENT_PERSONALITY_END -->',
    re.DOTALL
)

# Tool definitions: name, project-level path, global path
TOOLS = {
    'cursor': {
        'name': 'Cursor',
        'project': '.cursor/rules/agent-personality.mdc',
        'global': os.path.expanduser('~/.cursor/rules/agent-personality.mdc'),
    },
    'claude': {
        'name': 'Claude Code',
        'project': 'CLAUDE.md',
        'global': os.path.expanduser('~/.claude/CLAUDE.md'),
    },
    'kiro': {
        'name': 'Kiro',
        'project': '.kiro/steering/agent-personality.md',
        'global': os.path.expanduser('~/.kiro/agents/agent-personality.md'),
    },
    'windsurf': {
        'name': 'Windsurf',
        'project': '.windsurf/rules/agent-personality.md',
        'global': os.path.expanduser('~/.codeium/windsurf/memories/global_rules.md'),
    },
    'copilot': {
        'name': 'GitHub Copilot',
        'project': '.github/copilot-instructions.md',
        'global': os.path.expanduser('~/.copilot/copilot-instructions.md'),
    },
    'antigravity': {
        'name': 'Antigravity',
        'project': '.antigravity/rules.md',
        'global': os.path.expanduser('~/.antigravity/rules.md'),
    },
    'zed': {
        'name': 'Zed',
        'project': '.rules',
        'global': os.path.expanduser('~/.config/zed/rules.md'),
    },
    'vscode': {
        'name': 'VS Code (Copilot)',
        'project': '.github/copilot-instructions.md',
        'global': os.path.expanduser('~/.copilot/copilot-instructions.md'),
    },
}


def build_personality_block(mbti: str, system_prompt: str) -> str:
    """Build the personality block to append/replace in config files."""
    start = MARKER_START.format(mbti=mbti)
    lines = [
        start,
        "",
        system_prompt.strip(),
        "",
        MARKER_END,
    ]
    return "\n".join(lines)


def apply_personality(tool_key: str, scope: str, mbti: str, system_prompt: str) -> tuple[bool, str]:
    """
    Apply personality to a tool config file.
    scope: 'project' or 'global'
    Returns (success, message).
    """
    tool = TOOLS[tool_key]
    file_path = tool[scope]

    # Resolve project path relative to cwd
    if scope == 'project':
        file_path = os.path.join(os.getcwd(), file_path)

    # Ensure parent directory exists
    parent = os.path.dirname(file_path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    new_block = build_personality_block(mbti, system_prompt)

    # Read existing content
    existing_content = ""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()

    # Replace existing block or append
    if MARKER_PATTERN.search(existing_content):
        updated_content = MARKER_PATTERN.sub(new_block, existing_content)
        action = 'updated'
    else:
        separator = "\n\n" if existing_content and not existing_content.endswith("\n\n") else ""
        if existing_content and not existing_content.endswith("\n"):
            separator = "\n\n"
        updated_content = existing_content + separator + new_block + "\n"
        action = 'appended'

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    return True, action, file_path
