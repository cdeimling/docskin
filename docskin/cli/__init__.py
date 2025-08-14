from pathlib import Path

import click

from .commands import github, md, md_dir, setup_command


@click.group(
        cls=click.Group,
        context_settings=dict(help_option_names=["-h", "--help"]),
        invoke_without_command=True
)
@click.option("--verbose", "-v", count=True, help="Increase verbosity level")
@click.option(
    "--logo", "-l",
    type=click.Path(exists=True, path_type=Path),
    help="Optional path to logo image",
)
@click.option(
    "--css-style", "-cs",
    type=click.Path(exists=True, path_type=Path),
    help="Optional path to CSS style file",
    default="assets/markdown-dark.css",
)
@click.option(
    "--css-class", "-cc",
    type=str,
    default="markdown-body",
    help="CSS class to render (e.g. markdown-body slide for slides)",
)
@click.pass_context
def cli(
    ctx: click.Context,
    verbose: int,
    logo: Path,
    css_style: Path,
    css_class: str
) -> None:
    """
    📄Style your documents into styled PDF documents in your corporate skin.
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["logo"] = logo
    ctx.obj["css_style"] = css_style
    ctx.obj["css_class"] = css_class

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help(), color=True)


cli.add_command(github)
cli.add_command(md)
cli.add_command(md_dir)
cli.add_command(setup_command)
