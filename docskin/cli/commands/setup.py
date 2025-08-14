"""CLI command for setting up the docskin environment.

This module defines the 'setup' command, which installs necessary system and
Python dependencies by delegating to the run_setup helper.
"""

import click

from docskin.setup import run_setup


@click.command(name="setup")
def setup_command() -> None:
    """Install the necessary system and Python dependencies.

    This command executes a series of steps to prepare the
    environment for ``docskin``.  It delegates to the
    :func:`run_setup` helper, which in turn uses the
    :class:`SetupInstaller` class to perform installation tasks in
    a safe and platform‑aware manner.
    """
    run_setup()
