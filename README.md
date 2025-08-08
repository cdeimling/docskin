# 📄 docskin

[![Build Status](https://github.com/cdeimling/docskin/actions/workflows/ci.yml/badge.svg)](https://github.com/cdeimling/docskin/actions)
[![Coverage Status](https://img.shields.io/codecov/c/github/cdeimling/docskin?style=flat-square)](https://codecov.io/gh/cdeimling/docskin)
[![PyPI Version](https://img.shields.io/pypi/v/docskin?style=flat-square)](https://pypi.org/project/docskin/)

Convert **Markdown files** and **GitHub issues** into styled PDF documents – with full support for CSS themes, logos, and directory processing.

## 🔧 Installation

```bash
uv sync
```

or in development mode:

```bash
uv sync --editable .
```

## 🚀 Usage

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

```bash
docskin --help
```

```text
Usage: docskin [OPTIONS] COMMAND [ARGS]...

  📄 Convert Markdown or GitHub issues to styled PDF files.

Options:
  --help  Show this message and exit.

Commands:
  md       Convert a local Markdown file to PDF with optional theming.
  md-dir   Convert all Markdown files in a directory to PDF.
  github   Convert a GitHub issue to PDF.
```

## 💡 Notes

- CSS is based on the GitHub style from [sindresorhus/github-markdown-css](https://github.com/sindresorhus/github-markdown-css)
- GitHub APIs use `.netrc` for authentication (if private repos).
- For Bosch internal: Use `--api-base https://github.boschdevcloud.com/api/v3`

## 📁 Structure

```text
docskin/
├── cli.py             # CLI definition via Click
├── styles.py          # CSS styles & HTML renderer
├── github_api.py      # GitHub API support
├── ...
assets/
├── markdown-dark.css
├── minimal.css
├── bosch.css
```

## 🛠️ TODO / Ideas

- PDF metadata (author, title, etc.)
- Generate TOC
- Bundle multiple issues
- Integrate Highlight.js

---

Made with ❤️ by your Markdown ↔ PDF Toolkit
