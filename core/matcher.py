from __future__ import annotations

# MBTI compatibility matrix
# For each user MBTI, lists recommended agent personalities (complementary types)
# Based on cognitive function theory and commonly cited compatibility pairs

COMPATIBILITY = {
    'INTJ': ['ENFP', 'ENTP', 'INFP'],
    'INTP': ['ENTJ', 'ENFJ', 'INTJ'],
    'ENTJ': ['INTP', 'INFP', 'ENFP'],
    'ENTP': ['INFJ', 'INTJ', 'ENFJ'],
    'INFJ': ['ENTP', 'ENFP', 'INTJ'],
    'INFP': ['ENTJ', 'ENFJ', 'ENTP'],
    'ENFJ': ['INTP', 'INFP', 'ISFP'],
    'ENFP': ['INTJ', 'INFJ', 'ENTJ'],
    'ISTJ': ['ESFP', 'ESTP', 'ISFP'],
    'ISFJ': ['ESTP', 'ESFP', 'ISTP'],
    'ESTJ': ['ISFP', 'INFP', 'ISTP'],
    'ESFJ': ['ISTP', 'ISFP', 'INTP'],
    'ISTP': ['ESFJ', 'ESTJ', 'ENFJ'],
    'ISFP': ['ESTJ', 'ESFJ', 'ENTJ'],
    'ESTP': ['ISFJ', 'ISTJ', 'INFJ'],
    'ESFP': ['ISTJ', 'ISFJ', 'INTJ'],
}

ALL_TYPES = list(COMPATIBILITY.keys())

# Trait mapping for preferred agent style scoring (Q6-Q10)
# Each question maps answers to MBTI trait preferences
# Format: {question_index: {answer_index: {trait: weight}}}
PREFERENCE_WEIGHTS = {
    5: {0: {'T': 2}, 1: {'F': 2}},           # Q6: direct vs diplomatic
    6: {0: {'N': 2}, 1: {'S': 2}},           # Q7: big picture vs detail
    7: {0: {'N': 1, 'E': 1}, 1: {'S': 1, 'I': 1}},  # Q8: proactive vs responsive
    8: {0: {'J': 1, 'T': 1}, 1: {'P': 1, 'F': 1}},  # Q9: formal vs casual
    9: {0: {'N': 1, 'P': 1}, 1: {'S': 1, 'J': 1}},  # Q10: creative vs methodical
}

# Trait profile for each MBTI type (used to score against preferences)
TYPE_TRAITS = {
    'INTJ': {'I': 1, 'N': 2, 'T': 2, 'J': 1},
    'INTP': {'I': 1, 'N': 2, 'T': 2, 'P': 1},
    'ENTJ': {'E': 1, 'N': 2, 'T': 2, 'J': 1},
    'ENTP': {'E': 1, 'N': 2, 'T': 1, 'P': 1},
    'INFJ': {'I': 1, 'N': 2, 'F': 2, 'J': 1},
    'INFP': {'I': 1, 'N': 2, 'F': 2, 'P': 1},
    'ENFJ': {'E': 1, 'N': 1, 'F': 2, 'J': 1},
    'ENFP': {'E': 1, 'N': 2, 'F': 2, 'P': 1},
    'ISTJ': {'I': 1, 'S': 2, 'T': 2, 'J': 1},
    'ISFJ': {'I': 1, 'S': 2, 'F': 2, 'J': 1},
    'ESTJ': {'E': 1, 'S': 2, 'T': 2, 'J': 1},
    'ESFJ': {'E': 1, 'S': 2, 'F': 2, 'J': 1},
    'ISTP': {'I': 1, 'S': 2, 'T': 2, 'P': 1},
    'ISFP': {'I': 1, 'S': 2, 'F': 2, 'P': 1},
    'ESTP': {'E': 1, 'S': 2, 'T': 2, 'P': 1},
    'ESFP': {'E': 1, 'S': 2, 'F': 2, 'P': 1},
}


def get_recommendations(user_mbti: str, preference_scores: dict) -> list[str]:
    """
    Returns top 1-3 recommended agent MBTI types based on:
    1. Compatibility with user's MBTI
    2. User's preferred agent style (from Q6-Q10)
    """
    candidates = COMPATIBILITY.get(user_mbti, ALL_TYPES[:3])

    # Score each candidate against user's preferred style
    scored = []
    for mbti in candidates:
        score = 0
        traits = TYPE_TRAITS.get(mbti, {})
        for trait, weight in preference_scores.items():
            score += traits.get(trait, 0) * weight
        scored.append((mbti, score))

    # Sort by score descending, keep original order for ties
    scored.sort(key=lambda x: -x[1])
    return [t for t, _ in scored]


def determine_mbti(scores: dict) -> str:
    """Convert dimension scores to MBTI type string."""
    e_i = 'E' if scores.get('E', 0) >= scores.get('I', 0) else 'I'
    n_s = 'N' if scores.get('N', 0) >= scores.get('S', 0) else 'S'
    t_f = 'T' if scores.get('T', 0) >= scores.get('F', 0) else 'F'
    j_p = 'J' if scores.get('J', 0) >= scores.get('P', 0) else 'P'
    return f"{e_i}{n_s}{t_f}{j_p}"
