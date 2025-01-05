from rich.console import Console
from rich.prompt import Prompt

console = Console()

console.print("[bold blue]Welcome to the TUI![/bold blue]")
name = Prompt.ask("What is your name")
console.print(f"Hello, [bold green]{name}[/bold green]! Press [bold red]Ctrl+C[/bold red] to exit.")
