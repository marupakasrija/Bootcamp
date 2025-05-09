# This is abstraction-level-4/main.py
# The main entry point for the application in Level 4.
# Handles CLI arguments, loads configuration, and orchestrates streaming processing.

import sys  # Needed for sys.stdin, sys.stderr, sys.exit
import typer
import os   # Needed for os.getenv (though less used in L4 with config file)
from typing import Optional, Iterator # Import Iterator
import codecs # Needed for handling BOM

# Import components from our modules using RELATIVE imports.
# This tells Python to look for these modules within the current package directory.
# Ensure you have an empty file named __init__.py in this directory
# for these relative imports to work correctly when running as a package
# using 'python -m abstraction_level4.main'.
from .cli import app # Import the Typer app instance
from .core import apply_stream_pipeline # Use the new stream pipeline application logic from core
from .pipeline import get_streaming_pipeline_from_config # Use the dynamic stream config loader from pipeline

# --- Helper functions for reading/writing ---
# These could be moved to a separate utils.py module in later levels,
# using a relative import like 'from .utils import ...'.

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
        # sys.stdin is already an iterator of strings.
        # We can't easily re-open stdin with a specific encoding or handle BOM here.
        # Assume stdin is correctly encoded (e.g., UTF-8).
        # We will strip trailing newlines below.
        lines_source = sys.stdin
    else:
        try:
            # Open the file explicitly with UTF-16 encoding.
            # The 'utf-16' codec handles both big and little endian variants
            # and the UTF-16 BOM if present.
            # --- FIX: Changed encoding from 'utf-8-sig' to 'utf-16' ---
            file_handle = codecs.open(path, 'r', encoding='utf-16')
            print(f"Reading from file: {path} with utf-16 encoding", file=sys.stderr)
            lines_source = file_handle # Return iterator (file handle)

        except FileNotFoundError:
            print(f"Error: Input file not found at {path}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error opening input file {path}: {e}", file=sys.stderr)
            sys.exit(1)

    # Yield lines, stripping trailing newlines consistently.
    # This handles both \n and \r\n.
    for line in lines_source:
        yield line.rstrip('\r\n')

    # If reading from a file, close the file handle after iterating.
    # This is important for resource management.
    if path != "-" and hasattr(lines_source, 'close'):
         try:
             lines_source.close()
             # print("DEBUG: Input file closed.") # Optional debug
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
        # Iterate through the processed lines and print each one.
        # Since lines yielded by apply_stream_pipeline should not have trailing newlines,
        # print() will add the necessary newline.
        for line in lines:
            print(line) # print() adds a newline by default
    else:
        try:
            # Open the output file in write mode with UTF-8 encoding.
            with open(output_path, 'w', encoding='utf-8') as f:
                # Iterate through the processed lines and write each one to the file.
                for line in lines:
                    f.write(line + '\n') # Write line followed by a newline
            print(f"Output written to {output_path}", file=sys.stderr)
        except IOError as e:
            print(f"Error writing output to {output_path}: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred while writing output to {output_path}: {e}", file=sys.stderr)
            sys.exit(1)


# --- Typer Command Definition ---

# Define the main command using the imported 'app' instance from cli.py.
# This command is the entry point when the script is run.
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
    pipeline = [] # Initialize pipeline list
    try:
        pipeline = get_streaming_pipeline_from_config(config)
        if not pipeline:
             typer.echo("Warning: Streaming pipeline is empty. No processing will occur.", err=True)
             # Decide if this should be a hard error or just a warning.
             # For now, allow empty pipeline.
    except Exception as e:
        # If loading the config or any processor fails, the exception is re-raised
        # by get_streaming_pipeline_from_config. Catch it here and exit.
        typer.echo(f"Failed to load streaming pipeline from '{config}': {e}", err=True)
        sys.exit(1)

    # --- Read input lines ---
    lines_iterator = None # Initialize to None
    try:
        # read_lines now handles closing the file internally
        lines_iterator = read_lines(input)
    except SystemExit: # read_lines already prints error and exits on FileNotFoundError/Error
        sys.exit(1) # Ensure main process exits

    # --- Apply the streaming pipeline to the lines iterator ---
    # apply_stream_pipeline is a generator, so processing is streamed.
    # lines_iterator is now guaranteed to yield lines without trailing newlines.
    processed_lines_iterator = apply_stream_pipeline(lines_iterator, pipeline)

    # --- Write output ---
    try:
        write_output(processed_lines_iterator, output)
    except SystemExit: # write_output already prints error and exits on IOError/Error
        sys.exit(1) # Ensure main process exits

    # --- Cleanup ---
    # read_lines now handles closing the file, so no explicit close needed here.
    # If stdin was used, it doesn't need closing.

    typer.echo("Streaming processing finished.")

# --- Main execution block ---
# This is the standard Python entry point.
if __name__ == "__main__":
    # Run the Typer application. This parses CLI arguments and calls
    # the appropriate command function (process_file in this case).
    app()
