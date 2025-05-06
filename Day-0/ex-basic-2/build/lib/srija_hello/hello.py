from rich.console import Console

def main():
    console = Console()
    
    # Get the name from the command-line argument or default to "world"
    import sys
    name = sys.argv[1] if len(sys.argv) > 1 else "world"
    
    # Print a rich message
    console.print(f"Hello, [bold magenta]{name}[/bold magenta]!", style="bold green")
