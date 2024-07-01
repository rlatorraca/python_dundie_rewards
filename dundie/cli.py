import pkg_resources
import rich_click as click
from rich import print
from rich.console import Console
from rich.table import Table

from dundie import core

click.rich_click.USE_RICH_MARKUP = True
click.rich_click.USE_MARKDOWN = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.SHOW_METAVARS_COLUMNS = True
click.rich_click.APPEND_METAVARS_HELP = True


@click.group()
@click.version_option(pkg_resources.get_distribution("dundie").version)
def main():
    """Dundier Mifflin Rewards System

    That is the system that controls Dundier Mifflin rewards

    """


@main.command()
@click.argument("filepath", type=click.Path(exists=True))
def load(filepath):
    """Load file from database

    ## Features
    - Validate data
    - Parse file
    - Load database

    """
    result = core.load(filepath)
    header = ["name", "department", "job title", "email"]
    for person in result:
        print("-" * 50)
        for key, value in zip(header, person.split(",")):
            print(f"[red]{key}[/]: {value.strip()}")
