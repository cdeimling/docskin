import requests
import os
from netrc import netrc


class GitHubIssueFetcher:
    """Fetches a GitHub issue via the GitHub API (supports .netrc or GITHUB_TOKEN)."""

    def __init__(self, repo: str, issue_number: int, api_base: str = "https://api.github.com"):
        self.repo = repo
        self.issue_number = issue_number
        self.api_base = api_base.rstrip("/")
        self.session = requests.Session()

        token = os.environ.get("GITHUB_TOKEN") or self._get_token_from_netrc()
        if token:
            self.session.headers.update({"Authorization": f"token {token}"})

    def _get_token_from_netrc(self):
        try:
            auth = netrc().authenticators(self.api_base.replace("https://", ""))
            return auth[2] if auth else None
        except FileNotFoundError:
            return None

    def fetch(self) -> dict:
        url = f"{self.api_base}/repos/{self.repo}/issues/{self.issue_number}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
