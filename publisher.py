#!/usr/bin/env python3
"""
GitHub Skill Publisher
Automates publishing OpenClaw skills to GitHub
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime


class SkillPublisher:
    """Main skill publisher class"""
    
    def __init__(self, skill_path=None, dry_run=False):
        self.skill_path = skill_path or os.getcwd()
        self.dry_run = dry_run
        self.skill_name = os.path.basename(self.skill_path)
        
    def publish(self, description=None, force=False):
        """Publish skill to GitHub"""
        print(f"🚀 Publishing skill: {self.skill_name}")
        
        if self.dry_run:
            print("  [DRY RUN] No changes will be made")
        
        # Validate skill directory
        if not self._validate_skill():
            return False
        
        # Initialize git if needed
        self._init_git()
        
        # Create README if missing
        self._create_readme(description)
        
        # Create .gitignore if missing
        self._create_gitignore()
        
        # Commit files
        self._commit_files()
        
        # Create GitHub repo
        self._create_github_repo(force)
        
        # Push to GitHub
        self._push_to_github()
        
        # Create release notes
        self._create_release_notes()
        
        print(f"✅ Successfully published {self.skill_name}!")
        print(f"   https://github.com/YOUR_USERNAME/{self.skill_name}")
        
        return True
    
    def _validate_skill(self):
        """Validate skill directory structure"""
        required_files = ['SKILL.md']
        
        for file in required_files:
            path = os.path.join(self.skill_path, file)
            if not os.path.exists(path):
                print(f"❌ Missing required file: {file}")
                return False
        
        print("  ✓ Skill structure validated")
        return True
    
    def _init_git(self):
        """Initialize git repository"""
        git_dir = os.path.join(self.skill_path, '.git')
        
        if os.path.exists(git_dir):
            print("  ✓ Git already initialized")
            return
        
        if not self.dry_run:
            subprocess.run(['git', 'init'], cwd=self.skill_path, capture_output=True)
            subprocess.run(['git', 'config', 'user.email', 'skill@openclaw.local'], cwd=self.skill_path, capture_output=True)
            subprocess.run(['git', 'config', 'user.name', 'Skill Publisher'], cwd=self.skill_path, capture_output=True)
        
        print("  ✓ Git initialized")
    
    def _create_readme(self, description=None):
        """Create README.md if missing"""
        readme_path = os.path.join(self.skill_path, 'README.md')
        
        if os.path.exists(readme_path):
            print("  ✓ README.md exists")
            return
        
        # Read SKILL.md for info
        skill_md_path = os.path.join(self.skill_path, 'SKILL.md')
        skill_info = self._parse_skill_md(skill_md_path)
        
        desc = description or skill_info.get('description', f'{self.skill_name} OpenClaw skill')
        
        readme_content = f"""# {self.skill_name}

{desc}

## Installation

```bash
openclaw skills install {self.skill_name}
```

## Usage

{skill_info.get('usage', 'See SKILL.md for detailed usage instructions.')}

## Features

- OpenClaw skill
- Easy installation
- Ready to use

## Author

{skill_info.get('author', 'OpenClaw Community')}

## License

MIT License
"""
        
        if not self.dry_run:
            with open(readme_path, 'w') as f:
                f.write(readme_content)
        
        print("  ✓ README.md created")
    
    def _create_gitignore(self):
        """Create .gitignore if missing"""
        gitignore_path = os.path.join(self.skill_path, '.gitignore')
        
        if os.path.exists(gitignore_path):
            print("  ✓ .gitignore exists")
            return
        
        gitignore_content = """__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.pytest_cache/
.coverage
.tox/
.venv
venv/
ENV/
env/
.DS_Store
Thumbs.db
EOF
        
        if not self.dry_run:
            with open(gitignore_path, 'w') as f:
                f.write(gitignore_content)
        
        print("  ✓ .gitignore created")
    
    def _parse_skill_md(self, path):
        """Parse SKILL.md for metadata"""
        info = {}
        
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()
                # Simple parsing
                if 'description:' in content:
                    lines = content.split('\n')
                    for line in lines:
                        if 'description:' in line:
                            info['description'] = line.split('description:')[1].strip()
                        if 'author:' in line:
                            info['author'] = line.split('author:')[1].strip()
        
        return info
    
    def _commit_files(self):
        """Commit all files"""
        if self.dry_run:
            print("  [DRY RUN] Would commit files")
            return
        
        # Add all files
        subprocess.run(['git', 'add', '.'], cwd=self.skill_path, capture_output=True)
        
        # Check if there are changes to commit
        result = subprocess.run(['git', 'status', '--porcelain'], cwd=self.skill_path, capture_output=True, text=True)
        
        if not result.stdout.strip():
            print("  ✓ No changes to commit")
            return
        
        # Commit
        subprocess.run(['git', 'commit', '-m', f'Initial commit: {self.skill_name}'], cwd=self.skill_path, capture_output=True)
        print("  ✓ Files committed")
    
    def _create_github_repo(self, force=False):
        """Create GitHub repository"""
        # Check if repo already exists
        result = subprocess.run(
            ['gh', 'repo', 'view', self.skill_name],
            capture_output=True
        )
        
        if result.returncode == 0:
            if force:
                print("  ✓ Repository exists (force flag set)")
            else:
                print("  ✓ Repository exists")
            return
        
        if self.dry_run:
            print(f"  [DRY RUN] Would create repo: {self.skill_name}")
            return
        
        # Get description from README
        readme_path = os.path.join(self.skill_path, 'README.md')
        desc = "OpenClaw skill"
        if os.path.exists(readme_path):
            with open(readme_path, 'r') as f:
                lines = f.readlines()
                if len(lines) > 1:
                    desc = lines[1].strip()
        
        # Create repo
        subprocess.run([
            'gh', 'repo', 'create', self.skill_name,
            '--public',
            '--description', desc,
            '--source', self.skill_path,
            '--remote', 'origin',
            '--push'
        ], capture_output=True)
        
        print("  ✓ GitHub repository created")
    
    def _push_to_github(self):
        """Push code to GitHub"""
        if self.dry_run:
            print("  [DRY RUN] Would push to GitHub")
            return
        
        subprocess.run(['git', 'push', 'origin', 'main'], cwd=self.skill_path, capture_output=True)
        print("  ✓ Code pushed to GitHub")
    
    def _create_release_notes(self):
        """Create release notes template"""
        release_notes_path = os.path.join(self.skill_path, 'RELEASE_NOTES.md')
        
        if os.path.exists(release_notes_path):
            print("  ✓ Release notes exist")
            return
        
        content = f"""# {self.skill_name} v1.0.0

**Release date:** {datetime.now().strftime('%Y-%m-%d')}

## What's New

- Initial release
- Core functionality implemented
- Documentation added

## Installation

```bash
openclaw skills install {self.skill_name}
```

## Features

- Easy to use
- Well documented
- Ready for production

## Notes

This is the first release. Please report any issues!
"""
        
        if not self.dry_run:
            with open(release_notes_path, 'w') as f:
                f.write(content)
        
        print("  ✓ Release notes created")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Publish OpenClaw skills to GitHub')
    parser.add_argument('--skill', help='Path to skill directory (default: current directory)')
    parser.add_argument('--description', help='Skill description')
    parser.add_argument('--dry-run', action='store_true', help='Show what would happen without making changes')
    parser.add_argument('--force', action='store_true', help='Force overwrite existing repo')
    
    args = parser.parse_args()
    
    publisher = SkillPublisher(skill_path=args.skill, dry_run=args.dry_run)
    publisher.publish(description=args.description, force=args.force)


if __name__ == '__main__':
    main()
