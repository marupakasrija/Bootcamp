import sys 
import typer
import os  
from typing import Optional, Iterator
import codecs 

from .cli import app 
from .core import apply_stream_pipeline
from .pipeline import get_streaming_pipeline_from_config 


def read_lines(path: str) -> Iterator[str]:
    """
    Reads lines from a file or stdin, handling common encodings (including UTF-16 BOM)
    and stripping trailing newlines.

    Args:
        path: The path to the input file, or "-" to read from standard input.

    Returns:
        An iterator yielding lines from the source, stripped of trailing newlines.

    Raises:
        SystemExit: If the input file is not found or cannot be opened.
    """
    if path == "-":
        print("Reading from stdin...", file=sys.stderr)
        lines_source = sys.stdin
    else:
        try:
            file_handle = codecs.open(path, 'r', encoding='utf-16')
            print(f"Reading from file: {path} with utf-16 encoding", file=sys.stderr)
            lines_source = file_handle 

        except FileNotFoundError:
            print(f"Error: Input file not found at {path}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error opening input file {path}: {e}", file=sys.stderr)
            sys.exit(1)

    for line in lines_source:
        yield line.rstrip('\r\n')

    if path != "-" and hasattr(lines_source, 'close'):
         try:
             lines_source.close()
             # print("DEBUG: Input file closed.")
         except Exception as e:
             print(f"Error closing input file {input}: {e}", file=sys.stderr)


def write_output(lines: Iterator[str], output_path: Optional[str]):
    """
    Writes processed lines to a file or stdout, ensuring each line ends with a newline.

    Args:
        lines: An iterator yielding processed lines (strings).
        output_path: The path to the output file, or None to write to standard output.

    Raises:
        SystemExit: If there is an error writing to the output file.
    """
    if output_path is None:
        print("Writing to stdout...", file=sys.stderr)
        for line in lines:
            print(line) 
    else:
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for line in lines:
                    f.write(line + '\n') 
            print(f"Output written to {output_path}", file=sys.stderr)
        except IOError as e:
            print(f"Error writing output to {output_path}: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred while writing output to {output_path}: {e}", file=sys.stderr)
            sys.exit(1)


# --- Typer Command Definition ---

@app.command()
def process_file(
    # Define command-line options using typer.Option.
    # --input: Required, defaults to "-" (stdin).
    input: str = typer.Option("-", "--input", help="Input file path or '-' for stdin."),
    # --output: Optional, defaults to None (stdout).
    output: Optional[str] = typer.Option(None, "--output", help="Output file path. If not provided, prints to stdout."),
    # --config: Required, defaults to "pipeline.yaml".
    # This is the path to the YAML file defining the pipeline.
    config: str = typer.Option("pipeline.yaml", "--config", help="Path to the YAML pipeline configuration file."),
):
    """
    Processes text lines from an input source using a dynamic streaming pipeline
    loaded from a configuration file and writes the results to an output destination.
    """
    typer.echo(f"Starting streaming processing...") # Use typer.echo for CLI output

    # --- Load the streaming pipeline dynamically from the config file ---
    pipeline = [] 
    try:
        pipeline = get_streaming_pipeline_from_config(config)
        if not pipeline:
             typer.echo("Warning: Streaming pipeline is empty. No processing will occur.", err=True)
             
    except Exception as e:
        typer.echo(f"Failed to load streaming pipeline from '{config}': {e}", err=True)
        sys.exit(1)

    # --- Read input lines ---
    lines_iterator = None
    try:
        lines_iterator = read_lines(input)
    except SystemExit: 
        sys.exit(1)

    processed_lines_iterator = apply_stream_pipeline(lines_iterator, pipeline)

    # --- Write output ---
    try:
        write_output(processed_lines_iterator, output)
    except SystemExit: 
        sys.exit(1)

    # --- Cleanup ---
    # read_lines now handles closing the file, so no explicit close needed here.
    # If stdin was used, it doesn't need closing.

    typer.echo("Streaming processing finished.")

# --- Main execution block ---
if __name__ == "__main__":
    app()
