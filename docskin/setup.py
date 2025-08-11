"""Setup utilities for the docskin CLI.

This module defines a :class:`SetupInstaller` which orchestrates the
installation of system packages required by WeasyPrint, ensures the
`uv` package manager is present, and synchronises Python dependencies
from the project's ``pyproject.toml``.  It also exposes a
``run_setup`` convenience function used by the CLI.
"""

from __future__ import annotations

import platform
import shutil
import subprocess

import click


class SetupInstaller:
    """Install system and Python dependencies for docskin.

    This installer encapsulates the logic for checking the host platform,
    installing system libraries required by WeasyPrint and other
    dependencies, ensuring the ``uv`` package manager is present, and
    syncing Python dependencies defined in ``pyproject.toml``.  Each
    step is implemented as a separate method to facilitate testing
    and extension.
    """

    def __init__(self) -> None:
        """Initialise a new installer instance."""
        self.platform = platform.system()

    def install_system_dependencies(self) -> None:
        """Install system packages required by WeasyPrint.

        On Debian/Ubuntu-based systems, this method will attempt to
        install ``libcairo2``, ``libpango-1.0-0``, ``libgdk-pixbuf2.0-0``
        and ``libffi-dev`` using ``apt-get``.  If ``apt-get`` or
        ``sudo`` is unavailable, or if the command fails, a message
        is printed and the method returns without raising an exception.
        For unsupported platforms, a notice is shown to the user.
        """
        if self.platform != "Linux":
            click.echo(
                "⚠️  Automatic system dependency installation is only "
                "supported on Linux.  Please install the required "
                "libraries manually on your system.",
            )
            return

        apt_get = shutil.which("apt-get")
        if apt_get is None:
            click.echo(
                "⚠️  apt-get not found.  Please install the system "
                "dependencies manually: libcairo2 libpango-1.0-0 "
                "libgdk-pixbuf2.0-0 libffi-dev.",
            )
            return

        try:
            click.echo("[1/4] Installing system dependencies for WeasyPrint..")
            # Update package lists quietly
            sudo_path = shutil.which("sudo") or "sudo"
            subprocess.run([sudo_path, apt_get, "update", "-qq"], check=True)
            subprocess.run(
                [
                    sudo_path,
                    apt_get,
                    "install",
                    "-y",
                    "fonts-noto-color-emoji",
                    "fonts-noto-core",
                    "libcairo2",
                    "libpango-1.0-0",
                    "libgdk-pixbuf2.0-0",
                    "libffi-dev",
                ],
                check=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            # In test environments or where sudo is unavailable, avoid failing
            click.echo(
                "⚠️  Failed to install system dependencies automatically.  "
                "Please install them manually.",
            )

    def run(self) -> None:
        """Perform the full setup sequence.

        This method orchestrates the installation steps and prints a
        summary upon completion.
        """
        click.echo("\n========== Docskin Environment Setup ==========")
        self.install_system_dependencies()
        click.echo("\n✅ Setup complete!\n")
        click.echo(
            (
                "To activate your environment later, run: "
                "source .venv/bin/activate"
            ),
        )


def run_setup() -> None:
    """Convenience wrapper to execute the installer from the CLI."""
    installer = SetupInstaller()
    installer.run()
