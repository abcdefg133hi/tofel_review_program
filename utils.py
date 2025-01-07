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
    table.add_row("clear_record", "Clear all the records")
    table.add_row("print_record", "Print your practice record")
    table.add_row("print", "Print all the words in the word pools")
    table.add_row("speaking", "Practice Speaking")
    table.add_row("speaking_add", "Add speaking problem into the corpus")
    table.add_row("speaking_clear", "Clear all the speaking problems into the corpus")
    table.add_row("speaking_print", "Print all the speaking problems from the corpus")
    table.add_row("speaking_remove", "Remove one specific speaking problem from the corpus")

    # Display the table
    console.print(table)

