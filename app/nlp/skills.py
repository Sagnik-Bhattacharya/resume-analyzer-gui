import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]  # app/
SKILLS_PATH = BASE_DIR / "data" / "skills.json"


def load_skills() -> set:
    with open(SKILLS_PATH, "r", encoding="utf-8") as f:
        return set(json.load(f))

SKILLS = load_skills()

def extract_skills(text: str) -> list:
    found = set()

    for skill in SKILLS:
        if skill.lower() in text:
            found.add(skill)

    return sorted(found)
