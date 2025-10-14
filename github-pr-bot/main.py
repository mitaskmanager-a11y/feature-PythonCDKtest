import argparse
import os
from dotenv import load_dotenv
from bot.github_api import GitHubClient

def env_or_fail(key: str) -> str:
    val = os.getenv(key)
    if not val:
        raise SystemExit(f"Missing required env var: {key}. Create .env from .env.example.")
    return val

def connect_client() -> GitHubClient:
    load_dotenv()
    token = env_or_fail("GITHUB_TOKEN")
    owner = env_or_fail("REPO_OWNER")
    repo = env_or_fail("REPO_NAME")
    return GitHubClient(token, owner, repo)

def cmd_list(args):
    client = connect_client()
    prs = client.list_pull_requests(state=args.state)
    if not prs:
        print("No pull requests found.")
        return
    print(f"=== {len(prs)} {args.state} PR(s) ===")
    for pr in prs:
        print(f"#{pr['number']:>4} | {pr['title']} | by {pr['user']['login']} | {pr['html_url']}")

def cmd_comment(args):
    client = connect_client()
    resp = client.add_comment(args.pr, args.body)
    print(f"Comment posted: {resp.get('html_url', 'OK')}")

def cmd_label(args):
    client = connect_client()
    if args.add:
        added = client.add_labels(args.pr, args.add)
        print("Labels now:", [l['name'] for l in added])
    if args.remove:
        for label in args.remove:
            client.remove_label(args.pr, label)
            print(f"Removed label: {label} (if it existed)")

def cmd_merge(args):
    client = connect_client()
    resp = client.merge_pull_request(args.pr, method=args.method, title=args.title)
    print("Merge result:", resp)

def build_parser():
    p = argparse.ArgumentParser(description="GitHub PR Bot CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="List pull requests")
    p_list.add_argument("--state", choices=["open", "closed", "all"], default="open")
    p_list.set_defaults(func=cmd_list)

    p_comment = sub.add_parser("comment", help="Post a PR comment")
    p_comment.add_argument("--pr", type=int, required=True, help="PR number")
    p_comment.add_argument("--body", type=str, required=True, help="Comment body text")
    p_comment.set_defaults(func=cmd_comment)

    p_label = sub.add_parser("label", help="Add or remove labels")
    p_label.add_argument("--pr", type=int, required=True, help="PR number")
    p_label.add_argument("--add", action="append", help="Label(s) to add (repeatable)")
    p_label.add_argument("--remove", action="append", help="Label(s) to remove (repeatable)")
    p_label.set_defaults(func=cmd_label)

    p_merge = sub.add_parser("merge", help="Merge a PR")
    p_merge.add_argument("--pr", type=int, required=True, help="PR number")
    p_merge.add_argument("--method", choices=["squash", "merge", "rebase"], default="squash")
    p_merge.add_argument("--title", type=str, help="Commit title (optional)")
    p_merge.set_defaults(func=cmd_merge)

    return p

if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
