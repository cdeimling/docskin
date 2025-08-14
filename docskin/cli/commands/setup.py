"""CLI command for setting up the docskin environment.

This module defines the 'setup' command, which installs necessary system and
Python dependencies by delegating to the run_setup helper.
"""

import click

from docskin.core.setup import run_setup


@click.command(name="setup")
def setup_command() -> None:
    """Install the necessary ubuntu system dependencies."""
    run_setup()
