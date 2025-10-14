"""
Lightweight GitHub REST v3 wrapper for Pull Requests, Comments, Labels, and Merge.
"""
from typing import Any, Dict, List, Optional
import os
import requests

class GitHubClient:
    def __init__(self, token: str, owner: str, repo: str) -> None:
        self.base = f"https://api.github.com/repos/{owner}/{repo}"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "github-pr-bot-python"
        })

    # ---- PRs ----
    def list_pull_requests(self, state: str = "open") -> List[Dict[str, Any]]:
        url = f"{self.base}/pulls"
        r = self.session.get(url, params={"state": state, "per_page": 100})
        r.raise_for_status()
        return r.json()

    def get_pull_request_files(self, pr_number: int) -> List[Dict[str, Any]]:
        url = f"{self.base}/pulls/{pr_number}/files"
        r = self.session.get(url)
        r.raise_for_status()
        return r.json()

    def merge_pull_request(self, pr_number: int, method: str = "squash", title: Optional[str] = None) -> Dict[str, Any]:
        url = f"{self.base}/pulls/{pr_number}/merge"
        payload = {"merge_method": method}
        if title:
            payload["commit_title"] = title
        r = self.session.put(url, json=payload)
        r.raise_for_status()
        return r.json()

    # ---- Comments (Issues API) ----
    def add_comment(self, pr_number: int, body: str) -> Dict[str, Any]:
        url = f"{self.base}/issues/{pr_number}/comments"
        r = self.session.post(url, json={"body": body})
        r.raise_for_status()
        return r.json()

    # ---- Labels ----
    def add_labels(self, pr_number: int, labels: List[str]) -> Dict[str, Any]:
        url = f"{self.base}/issues/{pr_number}/labels"
        r = self.session.post(url, json={"labels": labels})
        r.raise_for_status()
        return r.json()

    def remove_label(self, pr_number: int, label: str) -> None:
        # URL-encode label if needed
        from urllib.parse import quote
        url = f"{self.base}/issues/{pr_number}/labels/{quote(label)}"
        r = self.session.delete(url)
        # 200/204 are OK. 404 if label not present.
        if r.status_code not in (200, 204, 404):
            r.raise_for_status()
