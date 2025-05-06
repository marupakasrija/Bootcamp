import typer
from rich.console import Console
from datetime import datetime
import random

app = typer.Typer()
console = Console()

quotes = [
    "Keep going, you're doing great!",
    "The best time to start was yesterday. The second best time is now.",
    "Success is the sum of small efforts, repeated day in and day out.",
    "Don’t stop when you’re tired. Stop when you’re done."
]

def get_time_of_day():
    hour = datetime.now().hour
    if hour < 12:
        return "morning"
    elif 12 <= hour < 18:
        return "afternoon"
    else:
        return "evening"

@app.command()
def greet(name: str = "World", color: str = "green"):
    """Greets the user with a personalized message and time of day."""
    time_of_day = get_time_of_day()
    quote = random.choice(quotes)
    console.print(f"Good {time_of_day}, {name}!", style=color)
    console.print(f"[italic yellow]Quote of the day:[/italic yellow] {quote}", style="bold magenta")

@app.command()
def exit_app():
    """Exit the application with a farewell message."""
    console.print("Thanks for using the app! Goodbye!", style="bold red")
    raise typer.Exit()

if __name__ == "__main__":
    app()
