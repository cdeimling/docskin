"""Main entry point for the docskin CLI application."""

import sys

from docskin.cli import cli


def main() -> None:
    """Entry point for the docskin CLI application.

    Invokes the CLI interface with the specified program name and disables
    standalone mode.
    """
    cli(prog_name="docskin", standalone_mode=False)


if __name__ == "__main__":
    sys.exit(main())
