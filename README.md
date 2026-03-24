# 📄 docskin

[![Build Status](https://github.com/cdeimling/docskin/actions/workflows/ci.yml/badge.svg)](https://github.com/cdeimling/docskin/actions)
[![image](https://img.shields.io/pypi/v/ruff.svg)](https://pypi.python.org/pypi/ruff)
[![Security Status](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PyPI Version](https://img.shields.io/pypi/v/docskin?style=flat-square)](https://pypi.org/project/docskin/)
<!-- Pytest Coverage Comment:Begin -->

<!-- Pytest Coverage Comment:End -->

Style your **doc**uments - convert Markdown files and GitHub issues into styled PDF documents in your corporate **skin** – with full support for CSS themes, logos, and directory processing.

## 🔧 Installation

```bash
uv sync
```

or in development mode:

```bash
uv sync --editable .
```

# 🚀 Usage

### 📁 Convert Markdown Files in a Directory

Converts **all `.md` files in a directory** to PDF format.

```bash
docskin md-dir \
  --input ./docs \
  --output ./pdfs \
  --css-style assets/markdown-dark.css \
  --logo assets/bosch-logo.png
```

### 📄 Convert a Single Markdown File

Converts a single file to PDF format.

```bash
docskin md \
  --input README.md \
  --output README.pdf \
  --css-style assets/minimal.css
```

### 🐙 Convert GitHub Issue to PDF

Converts a GitHub issue (e.g. on Bosch DevCloud) to PDF.

```bash
docskin github \
  --repo aos-stakeholder-tools/recompute-driving-cluster \
  --issue 197 \
  --api-base https://github.boschdevcloud.com/api/v3 \
  --output issue-197.pdf \
  --css-style assets/markdown-dark.css
```

## 🎨 Styling

Use any CSS file to define the appearance of the resulting PDFs.

Example styles:

- `assets/markdown-dark.css` – GitHub Dark Theme
- `assets/minimal.css` – Simple light theme
- `assets/bosch.css` – Bosch Corporate Design (experimental)

### 🖼️ Logo (optional)

Add a logo at the top of the PDF with `--logo path/to/logo.png`.

## 📦 CLI Overview

The `docskin` CLI provides the following commands:

- **setup**
  Installs all required Python and system dependencies for docskin, including WeasyPrint and its Linux libraries.
  Example:
  ```bash
  docskin setup
  ```

- **md**
  Converts a single Markdown file to a styled PDF.
  Uses the MarkdownHTMLExtractor for parsing, StyleManager for HTML/CSS rendering, and WeasyPrint for PDF export.
  Example:
  ```bash
  docskin md --input README.md --output README.pdf --css-style assets/minimal.css
  ```

- **md-dir**
  Recursively converts all Markdown files in a directory (and subdirectories) to PDFs, preserving the folder structure.
  Example:
  ```bash
  docskin md-dir --input ./docs --output ./pdfs --css-style assets/markdown-dark.css
  ```

- **github**
  Fetches a GitHub issue and converts it to a styled PDF. Supports custom API endpoints and authentication for private repos.
  Example:
  ```bash
  docskin github --repo owner/repo --issue 42 --output issue-42.pdf --css-style assets/markdown-dark.css
  ```

---

## 💡 Notes

- GitHub APIs use `.netrc` for authentication (if private repos).
- For Bosch internal: Use `--api-base https://github.boschdevcloud.com/api/v3`

## 📜 License and Third-Party Software

`docskin` is licensed under the MIT License – see [LICENSE.txt](LICENSE.txt) for details.

This software uses [WeasyPrint](https://weasyprint.org/) for PDF rendering.  
WeasyPrint is licensed under the BSD 3-Clause License, and depends on system libraries such as Cairo, Pango, HarfBuzz, GDK-Pixbuf, and GLib, which are licensed under the LGPL or MIT licenses.

Some CSS files in `assets/` are adapted from  
[sindresorhus/github-markdown-css](https://github.com/sindresorhus/github-markdown-css),  
which is licensed under the MIT License.

The file `assets/github.svg.png` is adapted from
[Primer Octicons](https://github.com/primer/octicons?tab=readme-ov-file),
which is licensed under the MIT License.

The full license texts for `docskin` and the bundled third-party components are included in the [LICENSE.txt](LICENSE.txt) file in this repository.



## �️ Updated File Structure

```text
docskin/
├── cli.py                # CLI entry point (Click commands: setup, md, md-dir, github)
├── converter.py          # MarkdownHTMLExtractor, MarkdownPdfRenderer, orchestration
├── github_api.py         # GitHub issue fetching
├── styles.py             # StyleManager: CSS loading & HTML rendering
├── setup.py              # Dependency installation logic
assets/
├── markdown-dark.css     # GitHub Dark Theme CSS [3rd party](https://github.com/sindresorhus/github-markdown-css)
├── markdown-light.css    # GitHub Light Theme CSS [3rd party](https://github.com/sindresorhus/github-markdown-css)
├── minimal.css           # Minimal light theme CSS
tests/
├── resources/
│   ├── markdown/         # Test Markdown files
├── test_cli.py           # CLI integration tests
```

## Architecture

The architecture of `docskin` is designed to be modular and extensible. The main components are:

![docskin architecture](docs/architecture.svg)

- **CLI**: The command-line interface for user interaction.
- **MarkdownHTMLExtractor**: Extracts HTML from Markdown files.
- **StyleManager**: Manages CSS styles and applies them to the HTML.
- **PDFExporter**: Handles the conversion of styled HTML to PDF.
- **GitHubIssueFetcher**: Fetches GitHub issues for conversion.


## 🧜 Mermaid Diagram Support

docskin automatically renders [Mermaid](https://mermaid.js.org/) diagrams
embedded in Markdown files.  Write standard fenced code blocks tagged
`mermaid` and the diagrams will appear as crisp SVG graphics in the output
PDF:

````markdown
```mermaid
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Do it]
    B -->|No| D[Skip it]
```
````

Supported diagram types include flowcharts, sequence diagrams, class diagrams,
Gantt charts, and all other types supported by the
[mermaid.ink](https://mermaid.ink) rendering service.

> **Note:** Diagram rendering requires an internet connection to reach
> `https://mermaid.ink`.  When the service is unreachable the diagram source
> is preserved as a plain-text `<pre>` block so the rest of the document still
> renders correctly.

## 🛠️ TODO / Ideas

- PDF metadata (author, title, etc.)
- Generate TOC
- Bundle multiple issues
- Integrate Highlight.js

---

Made with ❤️ by a senior engineer passionate about open source.
