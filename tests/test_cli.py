from __future__ import annotations

import os
import sys
import types
import unittest
from pathlib import Path

from click.testing import CliRunner

# Ensure that the project root (which contains the `docskin` package) is on
# `sys.path`. When running tests directly, the current working directory
# changes into the isolated filesystem created by Click's test runner, so
# Python may not find the `docskin` package without this adjustment.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _prepare_stubs(tmp_path: Path) -> None:
    """Prepare stub modules for markdown and weasyprint and insert into sys.

    The `markdown` stub simply wraps the passed text in a paragraph, and the
    `weasyprint` stub writes a PDF-like file to the provided output. If the
    output path is a directory, it writes `output.pdf` inside that directory.
    """

    # Stub markdown module
    def markdown_func(text: str, **kwargs) -> str:
        return f"<p>{text}</p>"

    markdown_stub = types.SimpleNamespace(markdown=markdown_func)

    # Stub weasyprint.HTML object
    class PDFStub:
        def __init__(self, string: str | None = None) -> None:
            self.string = string

        def write_pdf(self, output) -> None:
            p = Path(output)
            # if path is a directory, create a default PDF inside
            if p.exists() and p.is_dir():
                out_file = p / "output.pdf"
            else:
                # ensure parent directory exists
                p.parent.mkdir(parents=True, exist_ok=True)
                out_file = p
            out_file.write_text("PDF content")

    # weasyprint stub exposing an HTML factory
    weasyprint_stub = types.SimpleNamespace(
        HTML=lambda string=None: PDFStub(string)
    )
    # Insert stub modules into sys.modules
    sys.modules["markdown"] = markdown_stub
    sys.modules["weasyprint"] = weasyprint_stub


class TestDocskinCLI(unittest.TestCase):
    def setUp(self):
        # Prepare isolated directory for each test
        self.runner = CliRunner()

    def test_md_command_creates_pdf(self) -> None:
        with self.runner.isolated_filesystem():
            tmp_path = Path.cwd()
            # prepare stub modules
            _prepare_stubs(tmp_path)
            # after stubs, import CLI
            import docskin.cli

            # create markdown file
            md_file = tmp_path / "sample.md"
            md_file.write_text("# Heading\nThis is a *test*.")
            # create dummy CSS style
            css_file = tmp_path / "style.css"
            css_file.write_text("body { color: black; }")
            # output directory
            output_dir = tmp_path / "outdir" / md_file.with_suffix(".pdf").name
            # Create the output directory ahead of time so that the stub
            # understands it's a directory and writes into output.pdf within it.
            output_dir.mkdir(parents=True)
            # run CLI
            result = self.runner.invoke(
                docskin.cli.main,
                [
                    "md",
                    "--input",
                    str(md_file),
                    "--output",
                    str(output_dir),
                    "--css-style",
                    str(css_file),
                ],
            )
            self.assertEqual(result.exit_code, 0, msg=result.output)
            # The stub writes output.pdf into the directory
            pdf_file = output_dir / "output.pdf"
            self.assertTrue(pdf_file.exists(), "PDF file was not created")

    def test_md_dir_command_multiple_files(self) -> None:
        with self.runner.isolated_filesystem():
            tmp_path = Path(os.getcwd())
            # prepare stub modules
            _prepare_stubs(tmp_path)
            import docskin.cli

            # create directory with markdown files
            input_dir = tmp_path / "mds"
            input_dir.mkdir(parents=True)
            (input_dir / "first.md").write_text("First file content")
            (input_dir / "second.md").write_text("Second file content")
            # dummy CSS
            css_file = tmp_path / "style.css"
            css_file.write_text("body { color: black; }")
            output_dir = tmp_path / "output"
            # run CLI
            result = self.runner.invoke(
                docskin.cli.main,
                [
                    "md-dir",
                    "--input",
                    str(input_dir),
                    "--output",
                    str(output_dir),
                    "--css-style",
                    str(css_file),
                ],
            )
            self.assertEqual(result.exit_code, 0, msg=result.output)
            # verify two pdfs exist
            first_pdf = output_dir / "first.pdf"
            second_pdf = output_dir / "second.pdf"
            self.assertTrue(first_pdf.exists(), "First PDF missing")
            self.assertTrue(second_pdf.exists(), "Second PDF missing")

    def test_md_dir_empty_directory(self) -> None:
        with self.runner.isolated_filesystem():
            tmp_path = Path(os.getcwd())
            _prepare_stubs(tmp_path)
            import docskin.cli

            # empty directory
            input_dir = tmp_path / "empty"
            input_dir.mkdir(parents=True)
            css_file = tmp_path / "style.css"
            css_file.write_text("body { color: black; }")
            output_dir = tmp_path / "out"
            result = self.runner.invoke(
                docskin.cli.main,
                [
                    "md-dir",
                    "--input",
                    str(input_dir),
                    "--output",
                    str(output_dir),
                    "--css-style",
                    str(css_file),
                ],
            )
            self.assertEqual(result.exit_code, 0, msg=result.output)
            # message should indicate no markdown files found
            self.assertIn("No Markdown files found", result.output)

    def test_github_command_creates_pdf(self) -> None:
        with self.runner.isolated_filesystem():
            tmp_path = Path(os.getcwd())
            _prepare_stubs(tmp_path)
            # Import CLI after stubs
            # monkeypatch GitHubIssueFetcher.fetch to return a fake issue
            from unittest.mock import patch

            from docskin import cli as docskin_cli

            fake_issue = {
                "title": "Fake Issue",
                "body": "# Title\nThis is **bold** text.",
                "labels": [{"name": "bug"}, {"name": "enhancement"}],
            }
            # dummy css
            css_file = tmp_path / "style.css"
            css_file.write_text("body { color: black; }")
            output_file = tmp_path / "issue.pdf"
            with patch(
                "docskin.github_api.GitHubIssueFetcher.fetch",
                return_value=fake_issue,
            ):
                result = self.runner.invoke(
                    docskin_cli.main,
                    [
                        "github",
                        "--repo",
                        "dummy/repo",
                        "--issue",
                        "1",
                        "--output",
                        str(output_file),
                        "--css-style",
                        str(css_file),
                    ],
                )
            self.assertEqual(result.exit_code, 0, msg=result.output)
            self.assertTrue(output_file.exists(), "GitHub PDF not created")
            self.assertEqual(result.exit_code, 0, msg=result.output)
            self.assertTrue(output_file.exists(), "GitHub PDF not created")
