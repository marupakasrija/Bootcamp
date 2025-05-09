import sys
import typer
from typing import Optional
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Define processing functions
def transform_line(line: str, mode: str) -> str:
    """Applies transformation based on mode."""
    stripped_line = line.strip()
    if mode == "uppercase":
        return stripped_line.upper()
    elif mode == "snakecase":
        return stripped_line.lower().replace(" ", "_")
    else:
        # Handle unknown mode
        print(f"Warning: Unknown mode '{mode}'. Skipping transformation.", file=sys.stderr)
        return stripped_line

def read_lines(path: str) -> iter:
    """Reads lines from a file or stdin."""
    if path == "-":
        print("Reading from stdin...", file=sys.stderr)
        return sys.stdin
    else:
        try:
            return open(path, 'r')
        except FileNotFoundError:
            print(f"Error: Input file not found at {path}", file=sys.stderr)
            sys.exit(1)

def write_output(lines: iter, output_path: Optional[str]):
    """Writes processed lines to a file or stdout."""
    if output_path is None:
        print("Writing to stdout...", file=sys.stderr)
        for line in lines:
            print(line)
    else:
        try:
            with open(output_path, 'w') as f:
                for line in lines:
                    f.write(line + '\n')
            print(f"Output written to {output_path}", file=sys.stderr)
        except IOError as e:
            print(f"Error writing output to {output_path}: {e}", file=sys.stderr)
            sys.exit(1)


# Main Typer application
app = typer.Typer()

@app.command()
def main(
    input: str = typer.Option("-", "--input", help="Input file path or '-' for stdin."),
    output: Optional[str] = typer.Option(None, "--output", help="Output file path. If not provided, prints to stdout."),
    mode: str = typer.Option(os.getenv("MODE", "uppercase"), "--mode", help="Processing mode (uppercase or snakecase)."),
):
    """
    Processes text lines from input, transforms them, and writes to output.
    """
    typer.echo(f"Processing with mode: {mode}")

    lines_iterator = read_lines(input)

    processed_lines_iterator = (transform_line(line, mode) for line in lines_iterator)

    write_output(processed_lines_iterator, output)

    if input != "-":
         lines_iterator.close()


if __name__ == "__main__":
    app()