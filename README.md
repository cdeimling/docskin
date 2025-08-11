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

- GitHub APIs use `.netrc` for authentication (if private repos).
- For Bosch internal: Use `--api-base https://github.boschdevcloud.com/api/v3`

## 📜 License and Third-Party Software

`docskin` is licensed under the MIT License – see [LICENSE.txt](LICENSE.txt) for details.

This software uses [WeasyPrint](https://weasyprint.org/) for PDF rendering.  
WeasyPrint is licensed under the BSD 3-Clause License, and depends on system libraries such as Cairo, Pango, HarfBuzz, GDK-Pixbuf, and GLib, which are licensed under the LGPL or MIT licenses.

Some CSS files in `assets/` are adapted from  
[sindresorhus/github-markdown-css](https://github.com/sindresorhus/github-markdown-css),  
which is licensed under the MIT License.

The full license texts for `docskin` and the bundled third-party components are included in the [LICENSE.txt](LICENSE.txt) file in this repository.


## 📁 Structure

```text
docskin/
├── cli.py             # CLI definition via Click
├── styles.py          # CSS styles & HTML renderer
├── github_api.py      # GitHub API support
├── ...
assets/
├── markdown-dark.css   # 3rd Party CSS [sindresorhus/github-markdown-css](https://github.com/sindresorhus/github-markdown-css)
├── markdown-light.css   # 3rd Party CSS [sindresorhus/github-markdown-css](https://github.com/sindresorhus/github-markdown-css)
├── minimal.css
```

## 🛠️ TODO / Ideas

- PDF metadata (author, title, etc.)
- Generate TOC
- Bundle multiple issues
- Integrate Highlight.js

---

Made with ❤️ by a senior engineer passionate about open source.
