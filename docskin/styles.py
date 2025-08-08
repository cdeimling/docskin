from abc import ABC, abstractmethod
from pathlib import Path


class BaseStyle(ABC):
    def __init__(self, title: str, content: str, labels: list[str]):
        self.title = title
        self.content = content
        self.labels = labels

    @abstractmethod
    def render_html(self) -> str:
        pass


class GitHubStyle(BaseStyle):
    def __init__(self, title, content, labels, dark=False):
        super().__init__(title, content, labels)
        self.dark = dark

    def render_html(self) -> str:
        css_file = "markdown-dark.css" if self.dark else "markdown-light.css"
        try:
            with open(css_file) as f:
                github_css = f.read()
        except FileNotFoundError:
            github_css = "/* CSS file not found */"

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
                <p><strong>Labels:</strong> {', '.join(self.labels)}</p>
                <hr>
                {self.content}
            </body>
        </html>
        """


class CustomCSSStyle(BaseStyle):
    def __init__(self, title:str, content:str, labels:list[str], css_path: Path):
        super().__init__(title, content, labels)
        self.css_path = css_path
        self.margin = "1cm"

    def render_html(self) -> str:
        try:
            with open(self.css_path) as f:
                custom_css = f.read()
        except FileNotFoundError:
            custom_css = "/* custom CSS file not found */"

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
                <p><strong>Labels:</strong> {', '.join(self.labels)}</p>
                <hr>
                {self.content}
            </body>
        </html>
        """
