# Git Commands: From Zero to PR

## First-time setup
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

## Start a repo
git clone <repo-url>
cd <repo-folder>
git checkout -b feature/idp_insights

## Work and commit
git status
git add -A
git commit -m "dag deployment: add workflow and controller.json"

## Sync with remote
git pull --rebase origin development
# (Resolve any conflicts if prompted)
git push -u origin feature/idp_insights

## Open a Pull Request
# Go to GitHub → compare & create PR → fill PR template

## After review
git checkout development
git pull
git merge --no-ff feature/idp_insights
git push origin development

## Clean up
git branch -d feature/idp_insights
git push origin --delete feature/idp_insights
