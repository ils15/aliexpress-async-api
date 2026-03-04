#!/usr/bin/env python3
"""
Generate structured CHANGELOG.md from git history
Parses conventional commits and organizes by type
"""
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict


def get_git_logs(since_tag: str = None) -> List[str]:
    """Get git log since last tag"""
    cmd = ["git", "log", "--oneline", "--format=%s|%b"]
    
    if since_tag:
        cmd.append(f"{since_tag}..HEAD")
    else:
        # Get all commits if no tags
        cmd.append("--all")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip().split("\n") if result.stdout else []
    except subprocess.CalledProcessError:
        return []


def parse_commit(commit_line: str) -> Dict[str, str]:
    """Parse conventional commit"""
    subject = commit_line.split("|")[0]
    
    # Parse: type(scope): description
    match = re.match(r"^(feat|fix|docs|test|refactor|perf|chore)\((.*?)\):\s?(.*)", subject)
    if match:
        return {
            "type": match.group(1),
            "scope": match.group(2),
            "desc": match.group(3),
            "full": subject
        }
    
    return {"type": "other", "scope": "", "desc": subject, "full": subject}


def categorize_commits(commits: List[str]) -> Dict[str, List[str]]:
    """Categorize commits by type"""
    categories = {
        "Breaking Changes": [],
        "Features": [],
        "Bug Fixes": [],
        "Performance": [],
        "Refactoring": [],
        "Documentation": [],
        "Other": []
    }
    
    for commit in commits:
        if not commit:
            continue
        
        parsed = parse_commit(commit)
        commit_type = parsed["type"]
        
        entry = f"- {parsed['desc']}"
        if parsed["scope"]:
            entry = f"- **{parsed['scope']}**: {parsed['desc']}"
        
        if "breaking" in commit.lower():
            categories["Breaking Changes"].append(entry)
        elif commit_type == "feat":
            categories["Features"].append(entry)
        elif commit_type == "fix":
            categories["Bug Fixes"].append(entry)
        elif commit_type == "perf":
            categories["Performance"].append(entry)
        elif commit_type == "refactor":
            categories["Refactoring"].append(entry)
        elif commit_type == "docs":
            categories["Documentation"].append(entry)
        else:
            categories["Other"].append(entry)
    
    # Remove empty categories
    return {k: v for k, v in categories.items() if v}


def generate_changelog(version: str, commits: List[str]) -> str:
    """Generate changelog section"""
    change_date = datetime.now().strftime("%Y-%m-%d")
    categories = categorize_commits(commits)
    
    changelog = f"## [{version}] - {change_date}\n\n"
    
    for category, items in categories.items():
        if items:
            changelog += f"### {category}\n"
            changelog += "\n".join(items) + "\n\n"
    
    return changelog


def update_changelog_file(new_section: str) -> None:
    """Update CHANGELOG.md with new section"""
    changelog_path = Path("CHANGELOG.md")
    
    if changelog_path.exists():
        content = changelog_path.read_text()
        # Insert after header and before first version
        lines = content.split("\n")
        
        # Find first version line
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith("## ["):
                insert_idx = i
                break
        
        # Insert new section
        lines.insert(insert_idx, new_section)
        changelog_path.write_text("\n".join(lines))
    else:
        # Create new changelog
        header = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

"""
        changelog_path.write_text(header + new_section)


def main():
    """Main entrypoint"""
    # Get latest tag
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
            check=False
        )
        last_tag = result.stdout.strip() if result.returncode == 0 else None
    except:
        last_tag = None
    
    # Get commits since last tag
    commits = get_git_logs(last_tag)
    
    if not commits or not any(commits):
        print("ℹ️ No commits to process")
        return
    
    # Get version from environment (set by bump_version.py)
    version = os.environ.get("VERSION", "1.0.0")
    
    # Generate changelog
    new_section = generate_changelog(version, commits)
    
    # Update file
    update_changelog_file(new_section)
    
    print(f"✅ Changelog updated for version {version}")
    print(f"📝 Changes:\n{new_section}")


if __name__ == "__main__":
    main()
