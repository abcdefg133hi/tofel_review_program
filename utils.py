from rich.table import Table
from rich.console import Console


def initial_messages():
    console = Console()
    table = Table(title="[bold blue]Commands Usage[/bold blue]")

    table.add_column("Command", justify="right", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")

    # Add rows
    table.add_row("q", "Quit the program.")
    table.add_row("a", "Add word to the word pools.")
    table.add_row("p", "Practice words")
    table.add_row("r", "Remove word from the word pools")
    table.add_row("c", "Clear all the words in the word pools")
    table.add_row("print", "Print all the words in the word pools")

    # Display the table
    console.print(table)

