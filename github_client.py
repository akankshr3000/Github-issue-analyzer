import requests
import re
from typing import Dict, Optional, Any

GITHUB_API_BASE = "https://api.github.com"

def parse_repo_url(url: str) -> Optional[Dict[str, str]]:
    """
    Parses a GitHub repository URL to extract owner and repo name.
    Example: https://github.com/facebook/react -> {'owner': 'facebook', 'repo': 'react'}
    """
    pattern = r"github\.com/([^/]+)/([^/]+)"
    match = re.search(pattern, url)
    if match:
        return {"owner": match.group(1), "repo": match.group(2)}
    return None

def get_issue_details(owner: str, repo: str, issue_number: int) -> Dict[str, Any]:
    """
    Fetches issue details (title, body, comments) from GitHub API.
    """
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }

    # Fetch main issue data
    issue_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues/{issue_number}"
    print(f"Fetching issue from: {issue_url}")
    issue_resp = requests.get(issue_url, headers=headers)
    
    if issue_resp.status_code != 200:
        raise Exception(f"Failed to fetch issue: {issue_resp.status_code} - {issue_resp.text}")

    issue_data = issue_resp.json()

    # Fetch comments (limited to first 30 to avoid huge context)
    comments_url = issue_data.get("comments_url")
    comments_text = []
    
    if comments_url:
        print(f"Fetching comments from: {comments_url}")
        comments_resp = requests.get(comments_url, headers=headers)
        if comments_resp.status_code == 200:
            comments = comments_resp.json()
            for comment in comments[:10]: # Limit to first 10 comments for conciseness
                body = comment.get("body", "")
                user = comment.get("user", {}).get("login", "Unknown")
                if body:
                    comments_text.append(f"User {user}: {body}")
        else:
             print(f"Warning: Could not fetch comments: {comments_resp.status_code}")

    full_context = {
        "title": issue_data.get("title", ""),
        "body": issue_data.get("body", "") or "",
        "comments": "\n---\n".join(comments_text),
        "state": issue_data.get("state", ""),
        "user": issue_data.get("user", {}).get("login", "Unknown")
    }

    return full_context
