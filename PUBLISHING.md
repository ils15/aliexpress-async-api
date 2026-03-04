# 🚀 PyPI Publishing Automation Guide

## Overview

This project uses **fully automated** publishing to PyPI with:
- ✅ Semantic versioning (MAJOR.MINOR.PATCH)
- ✅ Automatic changelog generation
- ✅ GitHub Actions CI/CD pipeline
- ✅ GitHub Releases with release notes
- ✅ Zero manual intervention

---

## How It Works

### Automatic Publishing Flow

```
Developer Push → Tests → Version Bump → Build → Publish to PyPI
                                    ↓
                          GitHub Release Created
```

### Versioning Rules

| Commit Type | Example | Version Bump |
|------------|---------|------------|
| `feat(...)` | Add new feature | MINOR (1.0 → 1.1) |
| `fix(...)` | Bug fix | PATCH (1.0 → 1.0.1) |
| `BREAKING CHANGE` | API breaking change | MAJOR (1.0 → 2.0) |
| `docs(...)` | Documentation | None (no publish) |
| `test(...)` | Test changes | None (no publish) |
| `refactor(...)` | Code refactoring | PATCH (1.0 → 1.0.1) |

---

## Setting Up PyPI Token

### Step 1: Create PyPI Account (if needed)
1. Go to https://pypi.org/
2. Register account
3. Verify email

### Step 2: Create API Token
1. Go to Account Settings → API Tokens
2. Click "Create token for aliexpress-async-api"
3. Scope: **Project (aliexpress-async-api)**
4. Copy token (only shown once): `pypa-XXXXXXXXXXXXXX`

### Step 3: Add to GitHub Secrets
1. Go to Repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: Paste the token from Step 2
3. Save

---

## Publishing Workflow

### Automatic (Recommended)

Simply push to master with a proper commit message:

```bash
# Feature (will bump MINOR)
git commit -m "feat(new-feature): Add webhook filtering"
git push origin master
# ↓ GitHub Actions automatically:
#   1. Runs tests
#   2. Bumps version 1.0.0 → 1.1.0
#   3. Generates changelog
#   4. Publishes to PyPI
#   5. Creates GitHub Release

# Bug fix (will bump PATCH)
git commit -m "fix(auth): Handle token expiration"
git push origin master
# ↓ Automatically publishes as version 1.0.1

# Breaking change (will bump MAJOR)
git commit -m "feat(api): Redesign endpoint architecture

BREAKING CHANGE: Endpoint classes now use different signatures"
git push origin master
# ↓ Automatically publishes as version 2.0.0
```

### Manual (if needed)

```bash
# Build locally
python -m pip install build twine
python -m build

# Test on TestPyPI first
twine upload --repository test-pypi dist/*
# Test: pip install -i https://test.pypi.org/simple/ aliexpress-async-api

# Upload to real PyPI
twine upload dist/*
```

---

## Commit Message Format

### Required Format (Conventional Commits)

```
type(scope): description

Optional: longer explanation
Optional: BREAKING CHANGE: explanation
```

### Examples

✅ **Good:**
```
feat(endpoints): Add categories endpoint
fix(logging): Handle None values in log_request
refactor(models): Simplify product dataclass
```

❌ **Bad:**
```
fixed bugs
update code
v1.0.1
```

---

## GitHub Actions Workflow

### File: `.github/workflows/publish.yml`

**Triggered on:** Push to `master` with changes to:
- `aliexpress_async_api/`
- `tests/`
- `pyproject.toml`
- `.github/workflows/publish.yml`

**Jobs:**
1. **Test** - Run 103 tests, enforce 85% coverage
2. **Version** - Detect commit type, bump version
3. **Changelog** - Generate CHANGELOG.md
4. **Build** - Create wheel + sdist
5. **Publish** - Upload to PyPI
6. **Release** - Create GitHub Release with notes

### Status

Check workflow status:
- https://github.com/ils15/aliexpress-async-api/actions
- Each push shows build status

---

## Changelog Management

### Automatic Generation

Changelog is generated automatically from commits:
- Parses conventional commit format
- Groups by: Features, Fixes, Refactoring, etc.
- Updates `CHANGELOG.md` on each release
- Syncs with GitHub Releases

### File: `CHANGELOG.md`

Format:
```markdown
## [1.1.0] - 2026-03-05

### Features
- New webhook filtering support
- Added rate limiting decorators

### Bug Fixes
- Fixed token expiration handling

### Refactoring
- Simplified endpoint architecture
```

---

## Version Bumping

### File: `scripts/bump_version.py`

**Updates:**
- `pyproject.toml` - Project version
- `aliexpress_async_api/__init__.py` - `__version__` constant
- `CHANGELOG.md` - New release section

**How it works:**
1. Reads last commit message
2. Detects: feat → MINOR, fix → PATCH, BREAKING → MAJOR
3. Calculates new version
4. Updates files
5. Outputs version for GitHub Actions

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-04 | Production release - 5 advanced features, 103 tests |
| 1.1.0 | (future) | Next feature release (MINOR bump) |
| 1.0.1 | (future) | Next bug fix (PATCH bump) |

---

## Using the Package

### Installation

```bash
# Latest version
pip install aliexpress-async-api

# Specific version
pip install aliexpress-async-api==1.0.0

# Development
pip install -e ".[dev]"
```

### Checking Installed Version

```python
import aliexpress_async_api
print(aliexpress_async_api.__version__)  # "1.0.0"
```

---

## Troubleshooting

### Workflow didn't publish

**Check:**
1. Tests passed? (Check in Actions tab)
2. Commit message follows format? (e.g., `feat(...):`)
3. PYPI_API_TOKEN secret is set? (Settings → Secrets)
4. Changes are in `aliexpress_async_api/`? (Paths filter)

### Version didn't bump

**Check:**
1. Commit message starts with valid type: `feat`, `fix`, `refactor`
2. Scope is in parentheses: `feat(scope):`
3. Description is present: `feat(scope): description`

### PyPI token expired

**Fix:**
1. Create new token on pypi.org
2. Update PYPI_API_TOKEN secret in GitHub
3. Re-push code

---

## Best Practices

✅ **Do:**
- Use conventional commits
- Write clear commit messages
- Include scope in commits: `feat(endpoints): ...`
- Pin dependencies in future releases
- Test locally before pushing

❌ **Don't:**
- Mix multiple features in one commit
- Use vague messages like "fix"
- Push to master without tests passing
- Manually edit version numbers
- Merge without proper commit messages

---

## FAQ

**Q: What if I don't want to publish?**
- Use commit types like `docs:`, `test:`, `chore:` → no publish

**Q: Can I skip automatic publishing?**
- Yes, use `[skip-ci]` in commit message
- Or edit workflow to require manual approval

**Q: How often can I publish?**
- As often as you have features/fixes
- Each feature = new MINOR version
- Each fix = new PATCH version

**Q: Can I revert a version?**
- Yes, push new fix with revert commit
- Or delete release on GitHub + PyPI (advanced)

**Q: How to test without publishing?**
- Run locally: `python -m build && twine check dist/*`
- Push with `docs:` or `test:` type (won't publish)

---

## Next Steps

1. ✅ PyPI token configured
2. ✅ GitHub Actions workflow ready
3. ✅ Version bumping scripts ready
4. ✅ Changelog automation ready

**You're all set!** 🎉

Just commit with proper message format and GitHub Actions handles the rest.
