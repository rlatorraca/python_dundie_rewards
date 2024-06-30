import argparse

from dundie.core import load  # noqa


def main():
    parser = argparse.ArgumentParser(
        description="Dunder Mifflin Rewards CLI", epilog="a simple command-line interface for rewards management"
    )
    parser.add_argument(
        "subcommand",
        type=str,
        help="Action to execute",
        choices=("load", "show", "send"),
        default=help,
    )
    parser.add_argument("filepath", type=str, help="Path for loading file", default=None)

    args = parser.parse_args()  # Catch arguments typed from command line

    try:
        # Call globals load / show / send function using globals attribute -> args.subcommand
        # Passing (args.filepath) typed from command line
        print(*globals()[args.subcommand](args.filepath), sep="\n", end="")
    except KeyError:
        print("Invalid 'subcommand' argument")
