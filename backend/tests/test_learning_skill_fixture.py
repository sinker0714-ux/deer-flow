from pathlib import Path

from deerflow.skills.loader import load_skills
from deerflow.skills.parser import parse_skill_file


def _learning_skills_root() -> Path:
    return Path(__file__).resolve().parents[1] / "examples" / "learning_skills"


def test_learning_repository_reading_skill_fixture_parses():
    skill_file = _learning_skills_root() / "public" / "repository-reading-assistant" / "SKILL.md"

    skill = parse_skill_file(skill_file, category="public", relative_path=Path("repository-reading-assistant"))

    assert skill is not None
    assert skill.name == "repository-reading-assistant"
    assert "DeerFlow backend" in skill.description


def test_learning_repository_reading_skill_fixture_loads_with_container_path():
    skills = load_skills(skills_path=_learning_skills_root(), use_config=False, enabled_only=False)
    by_name = {skill.name: skill for skill in skills}

    skill = by_name["repository-reading-assistant"]

    assert skill.category == "public"
    assert skill.get_container_file_path() == "/mnt/skills/public/repository-reading-assistant/SKILL.md"
