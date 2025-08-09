"""Provides GitHub issue fetching functionality using the GitHub API.

Supports authentication via .netrc or GITHUB_TOKEN environment variable.
"""

from __future__ import annotations

import os
from netrc import netrc

import requests


class GitHubIssueFetcher:
    """Fetches a GitHub issue via the GitHub API.

    Supports .netrc or GITHUB_TOKEN.
    """

    def __init__(
        self,
        repo: str,
        issue_number: int,
        api_base: str = "https://api.github.com",
    ) -> None:
        """Initialize the GitHubIssueFetcher."""
        self.repo = repo
        self.issue_number = issue_number
        self.api_base = api_base.rstrip("/")
        self.session = requests.Session()

        token = os.environ.get("GITHUB_TOKEN") or self._get_token_from_netrc()
        if token:
            self.session.headers.update({"Authorization": f"token {token}"})

    def _get_token_from_netrc(self) -> str | None:
        try:
            auth = netrc().authenticators(self.api_base.replace("https://", ""))
            return auth[2] if auth else None
        except FileNotFoundError:
            return None

    def fetch(self) -> dict:
        """Fetch the specified GitHub issue as a dictionary."""
        url = f"{self.api_base}/repos/{self.repo}/issues/{self.issue_number}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
        return response.json()
