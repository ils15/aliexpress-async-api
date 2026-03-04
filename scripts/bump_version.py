#!/usr/bin/env python3
"""
Automatic semantic versioning based on commit messages
Implements: MAJOR (breaking), MINOR (features), PATCH (fixes)
"""
import os
import re
from pathlib import Path
from typing import Tuple


def get_current_version() -> str:
    """Read version from pyproject.toml"""
    pyproject = Path("pyproject.toml").read_text()
    match = re.search(r'version = "(\d+\.\d+\.\d+)"', pyproject)
    if match:
        return match.group(1)
    return "1.0.0"


def parse_version(version: str) -> Tuple[int, int, int]:
    """Parse version string to tuple"""
    parts = version.split(".")
    return int(parts[0]), int(parts[1]), int(parts[2])


def format_version(major: int, minor: int, patch: int) -> str:
    """Format version tuple to string"""
    return f"{major}.{minor}.{patch}"


def detect_bump_type(commit_message: str) -> str:
    """
    Detect version bump type from commit message
    Returns: 'major', 'minor', 'patch', or 'none'
    """
    commit_lower = commit_message.lower()
    
    # Breaking change = MAJOR
    if "breaking change" in commit_lower or "feat!" in commit_lower:
        return "major"
    
    # Feature = MINOR
    if commit_lower.startswith("feat("):
        return "minor"
    
    # Fix/Refactor = PATCH
    if commit_lower.startswith("fix(") or commit_lower.startswith("refactor("):
        return "patch"
    
    # Docs/tests = no publish
    return "none"


def bump_version(current: str, bump_type: str) -> str:
    """Apply version bump"""
    if bump_type == "none":
        return current
    
    major, minor, patch = parse_version(current)
    
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    
    return format_version(major, minor, patch)


def update_version_in_pyproject(new_version: str) -> None:
    """Update version in pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    
    # Replace version
    content = re.sub(
        r'version = "\d+\.\d+\.\d+"',
        f'version = "{new_version}"',
        content
    )
    
    pyproject_path.write_text(content)


def update_version_in_init(new_version: str) -> None:
    """Update __version__ in __init__.py"""
    init_path = Path("aliexpress_async_api/__init__.py")
    if init_path.exists():
        content = init_path.read_text()
        content = re.sub(
            r'__version__ = "\d+\.\d+\.\d+"',
            f'__version__ = "{new_version}"',
            content
        )
        init_path.write_text(content)


def main():
    """Main entrypoint"""
    # Get commit message from environment (GitHub Actions)
    commit_msg = os.environ.get("GIT_COMMIT_MESSAGE", "")
    
    # Detect bump type
    bump_type = detect_bump_type(commit_msg)
    
    # Skip if no version bump needed
    if bump_type == "none":
        print(f"ℹ️ Skipping version bump (commit type: {commit_msg.split(':')[0]})")
        return
    
    # Get current version
    current_version = get_current_version()
    print(f"📦 Current version: {current_version}")
    
    # Calculate new version
    new_version = bump_version(current_version, bump_type)
    print(f"🆙 Bumping {bump_type}: {current_version} → {new_version}")
    
    # Update files
    update_version_in_pyproject(new_version)
    update_version_in_init(new_version)
    
    # Output for GitHub Actions
    with open(os.environ.get("GITHUB_OUTPUT", "/dev/null"), "a") as f:
        f.write(f"version={new_version}\n")
        f.write(f"should_publish={bump_type != 'none'}\n")
    
    print(f"✅ Version updated to {new_version}")


if __name__ == "__main__":
    main()
