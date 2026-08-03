import typer

from termboard.app import TermBoardApp

app = typer.Typer(help="TermBoard: The TUI Dashboard for Python projects")


@app.command()
def start():
    """Start the TermBoard dashboard."""
    ui = TermBoardApp()
    ui.run()


def main():
    app()


if __name__ == "__main__":
    main()
