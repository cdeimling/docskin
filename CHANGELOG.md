# 📝 Changelog

All notable changes to this project will be documented in this file.

## [0.2.4](https://github.com/cdeimling/docskin/compare/v0.2.3...v0.2.4) (2025-08-12)


### Bug Fixes

* [#1](https://github.com/cdeimling/docskin/issues/1) workflow dispatch bugfixing ([66ed110](https://github.com/cdeimling/docskin/commit/66ed110bf5e8a8e52d69af7f45734c4cffb0400b))


### Documentation

* [#1](https://github.com/cdeimling/docskin/issues/1) update coverage badge ([8e3f629](https://github.com/cdeimling/docskin/commit/8e3f629ea60fdb798692fa90867fe539cdbbe60e))

## [0.2.3](https://github.com/cdeimling/docskin/compare/v0.2.2...v0.2.3) (2025-08-12)


### Bug Fixes

* [#1](https://github.com/cdeimling/docskin/issues/1) conditional publishing ([f79e6f3](https://github.com/cdeimling/docskin/commit/f79e6f314cb02fe922a13c207ebfbced1cba9546))
* [#1](https://github.com/cdeimling/docskin/issues/1) conditional publishing ([439afa6](https://github.com/cdeimling/docskin/commit/439afa67228319ef5860f67fcdb2df5641930e44))


### Documentation

* [#1](https://github.com/cdeimling/docskin/issues/1) update coverage badge ([28bb4b3](https://github.com/cdeimling/docskin/commit/28bb4b3bb29242c065524e22bcd728efe4073df4))

## [0.2.2](https://github.com/cdeimling/docskin/compare/v0.2.1...v0.2.2) (2025-08-12)


### Documentation

* [#1](https://github.com/cdeimling/docskin/issues/1) update coverage badge ([2b9523e](https://github.com/cdeimling/docskin/commit/2b9523e91a05d4079a957527cc6e132b3261cf28))

## [0.2.1](https://github.com/cdeimling/docskin/compare/v0.2.0...v0.2.1) (2025-08-12)


### Bug Fixes

* [#1](https://github.com/cdeimling/docskin/issues/1) auto-release ([b7bd73d](https://github.com/cdeimling/docskin/commit/b7bd73dcf306d57deb5a33a929c3d829702bc316))
* [#1](https://github.com/cdeimling/docskin/issues/1) auto-release ([0f4cf92](https://github.com/cdeimling/docskin/commit/0f4cf92c45afd8ec6051b8a603350e429a82683c))


### Documentation

* [#1](https://github.com/cdeimling/docskin/issues/1) update coverage badge ([367bf74](https://github.com/cdeimling/docskin/commit/367bf74a6b8a766cdc00155407d86a0a10180454))

## [0.2.0](https://github.com/cdeimling/docskin/compare/v0.1.0...v0.2.0) (2025-08-12)


### Features

* [#1](https://github.com/cdeimling/docskin/issues/1) enable auto-publishing ([fa3a4a8](https://github.com/cdeimling/docskin/commit/fa3a4a81c0ce57f54b9cdaf2f4fef4785f6627d8))
* [#1](https://github.com/cdeimling/docskin/issues/1) enable auto-publishing ([5ad3e5a](https://github.com/cdeimling/docskin/commit/5ad3e5a7a463a1ff844b7ebd107c68b96d2ebe46))

## 0.1.0 (2025-08-12)


### Bug Fixes

* [#1](https://github.com/cdeimling/docskin/issues/1) adaptation of coverage badge inclusion ([a412114](https://github.com/cdeimling/docskin/commit/a412114aed7499adad505f4ade642224588471e5))
* [#1](https://github.com/cdeimling/docskin/issues/1) adaptation of coverage badge inclusion ([052b637](https://github.com/cdeimling/docskin/commit/052b6376a2bd4732d957eb2af11215b4d1fe08a6))
* [#1](https://github.com/cdeimling/docskin/issues/1) implement coverage badge fix ([e576b4f](https://github.com/cdeimling/docskin/commit/e576b4f8c48d19efb85759c2fe9abf7cef6ec8ad))
* [#1](https://github.com/cdeimling/docskin/issues/1) implement coverage badge fix ([6ce5009](https://github.com/cdeimling/docskin/commit/6ce500905debd37712139c876c510a0a150d0d4f))
* [#1](https://github.com/cdeimling/docskin/issues/1) release-please action ([f406535](https://github.com/cdeimling/docskin/commit/f4065358d9855d88907e67475a85df8b9cb85a84))
* [#1](https://github.com/cdeimling/docskin/issues/1) release-please action ([062f888](https://github.com/cdeimling/docskin/commit/062f888a947051bd60d7d38c37ab887c027d231c))
* [#1](https://github.com/cdeimling/docskin/issues/1) release-please-pipeline ([0440803](https://github.com/cdeimling/docskin/commit/044080354225ec671ee88c5b6cc5e09a0a14bcb0))
* [#1](https://github.com/cdeimling/docskin/issues/1) release-please-pipeline ([dcf84a0](https://github.com/cdeimling/docskin/commit/dcf84a0e37f3864b24c1da9765b1f434bc318a1b))


### Documentation

* update coverage badge ([9451d17](https://github.com/cdeimling/docskin/commit/9451d170eb1945eb4a99b7b80a9b61d01e8af738))

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
