from abc import ABC, abstractmethod
from pathlib import Path


class BaseStyle(ABC):
    """Abstract base class for PDF styling."""

    def __init__(self, title: str, content: str, labels: list[str]) -> None:
        """Initialize the base style."""
        self.title = title
        self.content = content
        self.labels = labels

    @abstractmethod
    def render_html(self) -> str:
        """Render the HTML for the styled PDF."""
        pass


class GitHubStyle(BaseStyle):
    """GitHub-like PDF style with dark/light mode."""

    def __init__(
        self,
        title: str,
        content: str,
        labels: list[str],
        dark: bool = False,  # noqa: FBT001
    ) -> None:
        """Initialize GitHubStyle."""
        super().__init__(title, content, labels)
        self.dark = dark

    def render_html(self) -> str:
        """Render the HTML for the GitHub-styled PDF."""
        css_file = (
            Path("markdown-dark.css")
            if self.dark
            else Path("markdown-light.css")
        )
        if not css_file.is_file():
            exception_msg = f"CSS file not found: {css_file}"
            raise FileNotFoundError(exception_msg)

        github_css = css_file.read_text(encoding="utf-8")

        background = "#0d1117" if self.dark else "#ffffff"
        foreground = "#c9d1d9" if self.dark else "#24292f"

        return f"""
        <html>
            <head>
                <meta charset="utf-8">
                <style>
                    @page {{
                        margin: 0;
                        background: {background};
                    }}
                    body.markdown-body {{
                        background: {background};
                        color: {foreground};
                    }}
                    {github_css}
                </style>
            </head>
            <body class="markdown-body">
                <h1>{self.title}</h1>
                <p><strong>Labels:</strong> {", ".join(self.labels)}</p>
                <hr>
                {self.content}
            </body>
        </html>
        """


class CustomCSSStyle(BaseStyle):
    """Custom PDF style using a user-provided CSS file."""

    def __init__(
        self, title: str, content: str, labels: list[str], css_path: Path
    ) -> None:
        """Initialize CustomCSSStyle."""
        super().__init__(title, content, labels)
        self.css_path = css_path
        self.margin = "1cm"

    def render_html(self) -> str:
        """Render the HTML for the custom CSS-styled PDF."""
        if not self.css_path.is_file():
            exception_msg = f"CSS file not found: {self.css_path}"
            raise FileNotFoundError(exception_msg)

        custom_css = self.css_path.read_text(encoding="utf-8")

        return f"""
        <html>
            <head>
                <meta charset="utf-8">
                <style>
                    @page {{
                        margin: {self.margin};
                    }}
                    {custom_css}
                </style>
            </head>
            <body>
                <h1>{self.title}</h1>
                <p><strong>Labels:</strong> {", ".join(self.labels)}</p>
                <hr>
                {self.content}
            </body>
        </html>
        """
