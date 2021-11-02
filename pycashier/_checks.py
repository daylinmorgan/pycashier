import sys
from shutil import which

from rich.table import Table

from .console import console


def pre_run_check(tools):

    tools_exist = {name: is_tool(name) for name in tools}
    if False in tools_exist.values():
        console.print("\n[red bold] FAILED PRE-RUN CHECKS!!\n")
        table = Table(title="Pre-run Dependency Check")
        table.add_column("package", justify="right")
        table.add_column("found?", justify="left")
        for name, exists in tools_exist.items():
            if exists:
                found = "[green] yes"
            else:
                found = "[red] no"
            table.add_row(name, found)
        console.print(table)
        console.print(
            "It's recommeneded to install pycashier within a conda environment."
        )
        console.print(
            "See README on github for details: [link]https://github.com/daylinmorgan/pycashier/[/link]"
        )
        sys.exit(1)


def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""

    return which(name) is not None
