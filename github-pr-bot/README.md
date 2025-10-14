# GitHub PR Bot (Python) — VS Code Mini Project

Automate common **Pull Request** tasks from your local machine using **Python**:
- List open PRs
- Post comments (e.g., after lint/unit checks)
- Add or remove labels automatically
- Merge PRs (squash/merge/rebase) once checks pass

> Ideal for data-engineering repos (Glue, Lambda, Step Functions, PL/pgSQL) where you want a simple local tool to review and merge PRs after validation.

---

## 🧰 Prerequisites
- Python 3.8+
- A GitHub Personal Access Token (classic) with `repo` scope (or a fine-grained PAT with “Pull requests: Read & Write”, “Issues: Read & Write”).
- `pip` installed

---

## 🚀 Quick Start

1) **Clone** this project (or unzip the archive):  
```bash
cd your/work/dir
# if you downloaded the zip:
unzip github-pr-bot.zip -d github-pr-bot
cd github-pr-bot
```

2) **Install dependencies**:
```bash
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
```

3) **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your repo details + token
```

`.env`:
```
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
REPO_OWNER=your-github-user-or-org
REPO_NAME=your-repo-name
```

4) **Try it out**:
```bash
# List open PRs
python main.py list

# Add a comment
python main.py comment --pr 2 --body "✅ Lint passed. Ready to merge."

# Add labels
python main.py label --pr 2 --add "AWS Glue" --add "ETL"

# Remove labels
python main.py label --pr 2 --remove "WIP"

# Merge (squash|merge|rebase)
python main.py merge --pr 2 --method squash --title "Automated merge after checks"
```

---

## 🧪 Optional: Local checks before comment/merge
You can wire any local validation step (unit tests, lint, security scan) and then post the result as a PR comment. A simple lint task is provided:

```bash
# Windows PowerShell
scripts\lint.ps1

# macOS/Linux
bash scripts/lint.sh
```

---

## 🧩 VS Code Integration
- **Run / Debug**: `F5` starts `main.py list`. Use the `launch.json` dropdown to pick other common commands.  
- **Tasks**: `Ctrl/Cmd + Shift + B` to run “Lint”.  
- Formatting: basic Black + isort settings included.

---

## 🔒 Security Notes
- Store your PAT in `.env` **never commit it**.
- Fine-grained PATs are recommended; scope only to the target repository when possible.

---

## 🧭 Git Commands Cheat Sheet (local → remote)

```bash
# one-time: initialize your repo and push
git init
git branch -M main
git remote add origin https://github.com/<owner>/<repo>.git
git add .
git commit -m "feat: add github pr bot mini project"
git push -u origin main

# create a feature branch
git checkout -b feature/pr-automation
# edit files, then:
git add .
git commit -m "feat: wire label + merge commands"
git push -u origin feature/pr-automation

# open a PR (via GitHub UI) from feature/pr-automation → main
# then use this tool locally to comment/label/merge.
```

---

## 📁 Project Structure
```
github-pr-bot/
├─ .vscode/
│  ├─ launch.json
│  └─ settings.json
├─ bot/
│  ├─ __init__.py
│  └─ github_api.py
├─ scripts/
│  ├─ lint.ps1
│  └─ lint.sh
├─ .env.example
├─ .gitignore
├─ main.py
├─ pyproject.toml
├─ requirements.txt
└─ README.md
```

---

## 🧠 How it works (high-level)
- `bot/github_api.py` wraps **GitHub REST v3** endpoints for PRs, issues (comments), and labels.
- `main.py` provides a CLI with subcommands: `list`, `comment`, `label`, `merge`.
- All config comes from `.env` via `python-dotenv` to avoid hard-coding.

---

## 📜 License
MIT
