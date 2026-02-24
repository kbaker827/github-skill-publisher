---
name: github-skill-publisher
version: 1.0.0
description: One-command GitHub publishing for OpenClaw skills. Automates git init, commit, push, and repo creation.
author: Kyle Baker
---

# GitHub Skill Publisher

**Publish OpenClaw skills to GitHub with a single command.**

## What It Does

Automates the entire GitHub publishing workflow:
1. Initializes git repository
2. Creates comprehensive README
3. Generates release notes
4. Commits all files
5. Creates GitHub repository
6. Pushes code
7. Creates GitHub release

## Usage

```bash
# Publish current skill directory
skill-publish

# Publish specific skill
skill-publish --skill /path/to/skill

# Publish with custom description
skill-publish --description "My awesome skill"

# Dry run (see what would happen)
skill-publish --dry-run

# Force overwrite existing repo
skill-publish --force
```

## Features

- ✨ One-command publishing
- 📝 Auto-generated README template
- 🏷️ Automatic release notes
- 🔐 Safe (dry-run mode)
- 📦 Creates proper .gitignore
- 🎨 Professional repo structure
