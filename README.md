# github-skill-publisher

Tool for packaging and publishing OpenClaw skills to GitHub repositories.

## What It Does

Automates the process of creating a GitHub repo, pushing skill files, and configuring the repo for OpenClaw skill discovery.

## Usage

```bash
python publisher.py --skill-dir ./my-skill --repo-name my-skill-name
```

## Requirements

- GitHub CLI (`gh`) authenticated
- OpenClaw skill directory with `SKILL.md` and `_meta.json`

## Related

- [skill-factory](https://github.com/kbaker827/skill-factory)
- [skill-detector](https://github.com/kbaker827/skill-detector)
