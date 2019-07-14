import sys

import click

from utils import Gistback
from pathlib import Path
from hashlib import md5

gist_dec = click.make_pass_decorator(Gistback)


@click.group()
@click.version_option("0.1.0")
@click.pass_context
def cli(ctx):
    ctx.obj = Gistback(click.echo)
    ctx.obj.read_config()
    # ctx.obj.verbose = verbose


@cli.command()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose mode.")
@gist_dec
def init(gb, verbose):
    """Initialize the program.

    """
    click.echo("Initializing gistback")
    click.echo(f"Settings dir at {gb.dir}")
    gb.initialize()
    click.echo(f"Gist Commit ID : {gb.config.get('commitId')}")
    click.echo("Completed")


@cli.command()
@click.argument("file_path", type=Path)
@gist_dec
def add(gb: Gistback, file_path: Path):
    """Add file to backup list.

    """
    click.echo(f"Path to file is {file_path}")
    gb.add(file_path)
    click.echo("File added successfully")


@cli.command()
@gist_dec
def list(gb: Gistback):
    """List files to backup.

    """
    gb.list_files()
    click.echo("------------------------------------")


@cli.command()
@click.argument("index", type=int)
@click.confirmation_option()
@gist_dec
def remove(gb: Gistback, index):
    """Remove a file from backup list.

    """
    gb.remove_file(index)
    click.echo("------------------------------------")


if __name__ == "__main__":
    cli()
