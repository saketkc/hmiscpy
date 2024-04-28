"""Console script for hmispy."""

import hmispy

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for hmispy."""
    console.print("Replace this message by putting your code into " "hmispy.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")


if __name__ == "__main__":
    app()
