from __future__ import annotations

from core.matcher import determine_mbti, PREFERENCE_WEIGHTS


def run_quiz(locale: dict, ask_fn) -> tuple[str, dict]:
    """
    Run the 10-question quiz.
    Returns (user_mbti, preference_scores).

    ask_fn(question, choices) -> int (index of selected choice)
    """
    questions = locale['questions']
    dim_scores = {'E': 0, 'I': 0, 'N': 0, 'S': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
    preference_scores = {}

    # Questions 0-4: determine user MBTI
    dimension_map = [
        # (answer_A_trait, answer_B_trait)
        ('I', 'E'),  # Q1: alone(I) vs social(E)
        ('N', 'S'),  # Q2: big picture(N) vs concrete(S)
        ('T', 'F'),  # Q3: logic(T) vs empathy(F)
        ('J', 'P'),  # Q4: structured(J) vs flexible(P)
        ('E', 'I'),  # Q5: think aloud(E) vs think first(I)
    ]

    for i in range(5):
        q = questions[i]
        answer = ask_fn(
            f"[{i+1}/10] {q['text']}",
            [q['choices'][0], q['choices'][1]]
        )
        trait_a, trait_b = dimension_map[i]
        if answer == 0:
            dim_scores[trait_a] += 1
        else:
            dim_scores[trait_b] += 1

    user_mbti = determine_mbti(dim_scores)

    # Questions 5-9: determine preferred agent style
    for i in range(5, 10):
        q = questions[i]
        answer = ask_fn(
            f"[{i+1}/10] {q['text']}",
            [q['choices'][0], q['choices'][1]]
        )
        weights = PREFERENCE_WEIGHTS.get(i, {}).get(answer, {})
        for trait, weight in weights.items():
            preference_scores[trait] = preference_scores.get(trait, 0) + weight

    return user_mbti, preference_scores
