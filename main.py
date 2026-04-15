#!/usr/bin/env python3
"""
MBTI Agent Personality — Give your AI coding agent a personality.
"""
from __future__ import annotations

import json
import os
import sys

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

from core.quiz import run_quiz
from core.matcher import get_recommendations, ALL_TYPES
from core.appender import apply_personality, TOOLS
from templates import ALL_TEMPLATES

console = Console()

# ── Locale loading ──────────────────────────────────────────────────────────

LOCALE_DIR = os.path.join(os.path.dirname(__file__), 'locales')

LANGUAGES = [
    ('en_US', 'English'),
    ('zh_TW', '繁體中文'),
    ('zh_CN', '简体中文'),
    ('ja_JP', '日本語'),
    ('ko_KR', '한국어'),
    ('es_ES', 'Español'),
    ('fr_FR', 'Français'),
    ('de_DE', 'Deutsch'),
]


def load_locale(code: str) -> dict:
    path = os.path.join(LOCALE_DIR, f'{code}.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


# ── Display helpers ──────────────────────────────────────────────────────────

def print_welcome(locale: dict):
    title = Text(locale['welcome_title'], style="bold cyan")
    subtitle = Text(locale['welcome_subtitle'], style="dim")
    combined = Text()
    combined.append(locale['welcome_title'], style="bold cyan")
    combined.append("\n")
    combined.append(locale['welcome_subtitle'], style="dim white")
    console.print(Panel(combined, box=box.DOUBLE_EDGE, padding=(1, 4)))
    console.print()


def print_personality_card(mbti: str, locale: dict, template: dict):
    name = locale['mbti_names'].get(mbti, mbti)
    desc = locale['mbti_short_desc'].get(mbti, '')
    ascii_art = template.get('ascii_art', '')
    signature = template.get('signature', '')

    console.print()
    console.print(Panel(
        f"[bold yellow]{ascii_art}[/bold yellow]\n"
        f"[bold white]{mbti} — {name}[/bold white]\n"
        f"[dim]{desc}[/dim]\n\n"
        f"[italic cyan]{signature}[/italic cyan]",
        box=box.ROUNDED,
        padding=(0, 2),
    ))
    console.print()


# ── Language selection ───────────────────────────────────────────────────────

def select_language() -> dict:
    choices = [f"{name}" for _, name in LANGUAGES]
    answer = questionary.select(
        "🌐 Select language / 選擇語言 / 言語を選択:",
        choices=choices,
    ).ask()

    if answer is None:
        sys.exit(0)

    idx = [name for _, name in LANGUAGES].index(answer)
    code = LANGUAGES[idx][0]
    return load_locale(code)


# ── MBTI input / quiz ────────────────────────────────────────────────────────

def ask_question(question_text: str, choices: list[str]) -> int:
    answer = questionary.select(question_text, choices=choices).ask()
    if answer is None:
        sys.exit(0)
    return choices.index(answer)


def get_user_mbti(locale: dict) -> str | None:
    """Returns user's own MBTI or None if unknown."""
    answer = questionary.select(
        locale['known_mbti_prompt'],
        choices=[
            locale['known_mbti_yes'],
            locale['known_mbti_quiz'],
            locale['known_mbti_browse'],
        ]
    ).ask()

    if answer is None:
        sys.exit(0)

    if answer == locale['known_mbti_yes']:
        while True:
            mbti = questionary.text(locale['enter_mbti']).ask()
            if mbti is None:
                sys.exit(0)
            mbti = mbti.strip().upper()
            if mbti in ALL_TYPES:
                return mbti
            console.print(f"[red]{locale['invalid_mbti']}[/red]")

    if answer == locale['known_mbti_quiz']:
        return None  # trigger quiz

    return 'BROWSE'  # trigger browse


def run_full_quiz(locale: dict) -> tuple[str, dict]:
    console.print(f"\n[bold]{locale['quiz_intro']}[/bold]\n")
    return run_quiz(locale, ask_question)


# ── Personality selection ────────────────────────────────────────────────────

def select_agent_personality(locale: dict, recommendations: list[str]) -> str:
    """Let user select from recommended types (or browse all). Handles back navigation."""
    while True:
        console.print(f"\n[bold cyan]{locale['recommendations_intro']}[/bold cyan]")

        # Show short preview of each recommendation
        choices = []
        for i, mbti in enumerate(recommendations, 1):
            name = locale['mbti_names'].get(mbti, mbti)
            desc = locale['mbti_short_desc'].get(mbti, '')
            label = f"{mbti} — {name}  |  {desc}"
            choices.append(questionary.Choice(title=label, value=mbti))

        # Add "browse all" option
        choices.append(questionary.Choice(title="[ Browse all 16 types ]", value='__browse__'))

        selected = questionary.select(
            locale['select_personality'],
            choices=choices,
        ).ask()

        if selected is None:
            sys.exit(0)

        if selected == '__browse__':
            result = browse_all_types(locale)
            if result == '__back__':
                # User pressed Back from browse — loop back to recommendations
                continue
            return result

        return selected


def browse_all_types(locale: dict) -> str:
    """Browse all 16 types. Returns '__back__' if user wants to go back."""
    choices = [questionary.Choice(title="← Back", value='__back__')]
    for mbti in ALL_TYPES:
        name = locale['mbti_names'].get(mbti, mbti)
        desc = locale['mbti_short_desc'].get(mbti, '')
        choices.append(questionary.Choice(title=f"{mbti} — {name}  |  {desc}", value=mbti))

    selected = questionary.select(
        locale['select_personality'],
        choices=choices,
    ).ask()

    if selected is None:
        sys.exit(0)
    return selected


# ── Tool + scope selection ───────────────────────────────────────────────────

def select_tools_and_scope(locale: dict) -> tuple[list[str], str]:
    tool_choices = [
        questionary.Choice(title=info['name'], value=key)
        for key, info in TOOLS.items()
    ]

    selected_tools = questionary.checkbox(
        locale['select_tools'],
        choices=tool_choices,
    ).ask()

    if selected_tools is None:
        sys.exit(0)

    if not selected_tools:
        console.print(f"[red]{locale['no_tools_selected']}[/red]")
        return select_tools_and_scope(locale)

    scope = questionary.select(
        locale['select_scope'],
        choices=[
            questionary.Choice(title=locale['scope_project'], value='project'),
            questionary.Choice(title=locale['scope_global'], value='global'),
        ]
    ).ask()

    if scope is None:
        sys.exit(0)

    return selected_tools, scope


# ── Apply personality ────────────────────────────────────────────────────────

def apply_to_tools(locale: dict, selected_tools: list[str], scope: str, mbti: str, template: dict):
    name = locale['mbti_names'].get(mbti, mbti)
    system_prompt = template['system_prompt']

    console.print()
    for tool_key in selected_tools:
        tool_name = TOOLS[tool_key]['name']
        console.print(locale['applying'].format(type=mbti, tool=tool_name))

        success, action, file_path = apply_personality(tool_key, scope, mbti, system_prompt)

        if action == 'appended':
            console.print(f"  [green]{locale['success_append'].format(path=file_path)}[/green]")
        else:
            console.print(f"  [yellow]{locale['success_update'].format(path=file_path)}[/yellow]")

    console.print()
    signature = template.get('signature', '')
    console.print(Panel(
        f"[bold green]{locale['done_title']}[/bold green]\n"
        f"{locale['done_message'].format(type=mbti, name=name)}\n\n"
        f"[italic]{signature}[/italic]",
        box=box.ROUNDED,
        padding=(1, 2),
    ))


# ── Main flow ────────────────────────────────────────────────────────────────

def main():
    # 1. Language selection
    locale = select_language()
    console.clear()
    print_welcome(locale)

    # 2. Initial menu → determine mode
    preference_scores = {}
    recommendations = []

    user_choice = get_user_mbti(locale)
    if user_choice is None:
        user_mbti, preference_scores = run_full_quiz(locale)
        console.print(f"\n[bold cyan]{locale['your_mbti_result'].format(type=user_mbti)}[/bold cyan]\n")
        recommendations = get_recommendations(user_mbti, preference_scores)
    elif user_choice != 'BROWSE':
        recommendations = get_recommendations(user_choice, preference_scores)
    # 'BROWSE' → recommendations stays [], pure browse mode

    # 3. Personality selection + preview + confirmation loop
    selected_mbti = None
    while True:
        # 3a. Pick a personality
        if recommendations:
            # select_agent_personality handles browse→Back→recommendations internally
            selected_mbti = select_agent_personality(locale, recommendations)
        else:
            # Pure browse mode
            selected_mbti = browse_all_types(locale)
            if selected_mbti == '__back__':
                # Back from browse → return to initial menu
                user_choice = get_user_mbti(locale)
                if user_choice is None:
                    user_mbti, preference_scores = run_full_quiz(locale)
                    console.print(f"\n[bold cyan]{locale['your_mbti_result'].format(type=user_mbti)}[/bold cyan]\n")
                    recommendations = get_recommendations(user_mbti, preference_scores)
                elif user_choice != 'BROWSE':
                    recommendations = get_recommendations(user_choice, preference_scores)
                # if 'BROWSE' again → stay in browse mode (recommendations stays [])
                continue

        # 3b. Preview selected personality
        template = ALL_TEMPLATES[selected_mbti]
        print_personality_card(selected_mbti, locale, template)

        # 3c. Confirm
        name = locale['mbti_names'].get(selected_mbti, selected_mbti)
        confirmed = questionary.confirm(
            locale['confirm_selection'].format(type=selected_mbti, name=name),
            default=True,
        ).ask()

        if confirmed is None:
            sys.exit(0)

        if confirmed:
            break
        # No → loop back: recommendations mode shows list again,
        #                  browse mode shows browse again (with Back → initial menu)

    # 4. Tool + scope selection
    selected_tools, scope = select_tools_and_scope(locale)

    # 6. Apply
    apply_to_tools(locale, selected_tools, scope, selected_mbti, template)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[dim]Cancelled.[/dim]")
        sys.exit(0)
