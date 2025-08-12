# 📝 Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

- Refactored architecture: clear separation between MarkdownHTMLExtractor, StyleManager, PDFExporter, MarkdownPdfRenderer, and GitHubIssuePdfRenderer.
- CLI now supports four main commands: `setup`, `md`, `md-dir`, and `github`.
- Improved file structure and documentation.
- Added support for custom CSS themes and logo integration.
- Directory conversion (`md-dir`) now preserves folder structure for PDFs.
- Enhanced error handling and logging.
- Updated dependencies and configuration for Python 3.9+.
- Added SVG architecture diagram to documentation.
- Improved test coverage and CI integration.

## [0.1.0] – 2025-08-11

- Initial release: Convert Markdown files and GitHub issues to styled PDF documents.
- Support for GitHub API authentication and custom endpoints.
- Basic CSS theming and logo support.
- CLI commands for single file, directory, and GitHub issue conversion.
- MIT License.

---

For older changes, see previous commits in the repository.