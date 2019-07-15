import sys
from hashlib import md5
from pathlib import Path

import click

from .gistback import Gistback
from .gitAuth import update_gist

gist_dec = click.make_pass_decorator(Gistback)


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose mode.")
@click.version_option("0.1.0")
@click.pass_context
def cli(ctx, verbose: bool):
    ctx.obj = Gistback(click.echo)
    ctx.obj.read_config()
    ctx.obj.verbose = verbose


@cli.command()
@gist_dec
def init(gb: Gistback):
    """Initialize the program.
    """
    click.echo("------------------------------------")
    click.echo("Initializing gistback")
    click.echo(f"Settings dir at {gb.dir}")
    gb.initialize()
    click.echo(f"Gist Commit ID : {gb.config.get('commitId')}")
    click.echo("Completed")
    click.echo("------------------------------------")


@cli.command()
@click.argument("file_path", type=Path)
@click.option("-n", "--name", help="Name for the file")
@gist_dec
def add(gb: Gistback, file_path: Path, name):
    """Add file to backup list.
    """
    click.echo("------------------------------------")
    gb.add(file_path, name)


@cli.command()
@gist_dec
def ls(gb: Gistback):
    """List files to backup.
    """
    click.echo("------------------------------------")
    gb.list_files()
    click.echo("------------------------------------")


@cli.command()
@click.argument("index", type=int)
@click.confirmation_option()
@gist_dec
def remove(gb: Gistback, index: int):
    """Remove a file from backup list.
    """
    click.echo("------------------------------------")
    gb.remove_file(index, "fileList")
    click.echo("------------------------------------")


@cli.command()
@click.argument("index", type=int)
@click.confirmation_option()
@gist_dec
def unstage(gb: Gistback, index: int):
    """Unstage a file.
    """
    click.echo("------------------------------------")
    gb.remove_file(index, "newFiles")
    click.echo("------------------------------------")


@cli.command()
@gist_dec
def diff(gb: Gistback):
    """See which files have been changed.
    """
    click.echo("------------------------------------")
    gb.diff()
    click.echo("------------------------------------")


@cli.command()
@gist_dec
def staged(gb: Gistback):
    """List the files staged for backup.
    """
    click.echo("------------------------------------")
    gb.list_staged()
    click.echo("------------------------------------")


@cli.command()
@gist_dec
def test(gb: Gistback):
    """To test various stuff.
    """
    click.echo("------------------------------------")
    click.echo(gb.prep())
    click.echo("------------------------------------")


@cli.command()
@gist_dec
def run(gb: Gistback):
    """Run backup.
    """
    click.echo("------------------------------------")
    gb.run_backup()
    click.echo("------------------------------------")


if __name__ == "__main__":
    cli()

