"""
Install every skill in this repo's skills/ directory into ~/.claude/skills/,
replacing any existing skill with the same name.

Usage: python3 install.py
"""

import shutil
from pathlib import Path

REPO_SKILLS_DIR: Path = Path(__file__).resolve().parent / "skills"
USER_SKILLS_DIR: Path = Path.home() / ".claude" / "skills"
IGNORED_FILES = shutil.ignore_patterns(".DS_Store")


def find_skill_dirs(skills_dir: Path) -> list[Path]:
    return sorted(path.parent for path in skills_dir.glob("*/SKILL.md"))


def install_skill(skill_dir: Path, target_root: Path) -> Path:
    target: Path = target_root / skill_dir.name
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(skill_dir, target, ignore=IGNORED_FILES)
    return target


def main() -> None:
    skill_dirs: list[Path] = find_skill_dirs(REPO_SKILLS_DIR)
    if not skill_dirs:
        raise RuntimeError(f"No skills found in {REPO_SKILLS_DIR}")

    USER_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    for skill_dir in skill_dirs:
        target: Path = install_skill(skill_dir, USER_SKILLS_DIR)
        print(f"Installed {skill_dir.name} -> {target}")
    print(f"Installed {len(skill_dirs):,} skill(s).")


if __name__ == "__main__":
    main()
