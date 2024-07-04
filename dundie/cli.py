# import json
import pkg_resources
import rich_click as click
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

    table = Table(title="Dundie Mifflin Reward - Associates")
    headers = ["name", "department", "job title", "created", "email"]
    for header in headers:
        table.add_column(header, style="magenta", justify="center")

    result = core.load(filepath)
    for person in result:
        table.add_row(*[str(value) for value in person.values()])

    console = Console()
    console.print(table)
