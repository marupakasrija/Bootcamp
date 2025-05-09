# This is abstraction-level-3/main.py
# The main entry point for the application.
# Handles CLI arguments, loads configuration, and orchestrates processing.

import sys  # Needed for sys.stdin, sys.stderr, sys.exit
import typer
import os   # Needed for os.getenv (though less used in L3 with config file)
from typing import Optional, Iterator # Import Iterator

# Import components from our modules using RELATIVE imports.
# This tells Python to look for these modules within the current package directory.
# Ensure you have an empty file named __init__.py in this directory
# for these relative imports to work correctly when running as a package.
from .cli import app # Import the Typer app instance
from .core import apply_pipeline # Use the core processing logic
from .pipeline import get_pipeline_from_config # Use the dynamic config loader
# This import was causing the specific error you reported:
# from .types import ProcessorFn # <-- Removed this import as ProcessorFn is used by core and pipeline, not directly in main

# --- Helper functions for reading/writing ---
# These could be moved to a separate utils.py module in later levels,
# using a relative import like 'from .utils import ...'.

def read_lines(path: str) -> Iterator[str]:
    """
    Reads lines from a file or stdin.

    Args:
        path: The path to the input file, or "-" to read from standard input.

    Returns:
        An iterator yielding lines from the source.

    Raises:
        SystemExit: If the input file is not found or cannot be opened.
    """
    if path == "-":
        print("Reading from stdin...", file=sys.stderr)
        # sys.stdin is already an iterator of strings
        return sys.stdin
    else:
        try:
            # Open the file and return an iterator over its lines.
            # The caller is responsible for closing the file handle if needed.
            # In this simple case, the 'with open' in main will handle it if we read all lines.
            # However, apply_pipeline consumes the iterator lazily.
            # A more robust approach for iterators from files is needed if not reading all at once.
            # Let's return the file handle itself, which is an iterator.
            file_handle = open(path, 'r')
            print(f"Reading from file: {path}", file=sys.stderr)
            return file_handle # Return iterator (file handle)

        except FileNotFoundError:
            print(f"Error: Input file not found at {path}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error opening input file {path}: {e}", file=sys.stderr)
            sys.exit(1)


def write_output(lines: Iterator[str], output_path: Optional[str]):
    """
    Writes processed lines to a file or stdout.

    Args:
        lines: An iterator yielding processed lines (strings).
        output_path: The path to the output file, or None to write to standard output.

    Raises:
        SystemExit: If there is an error writing to the output file.
    """
    if output_path is None:
        print("Writing to stdout...", file=sys.stderr)
        # Iterate through the processed lines and print each one.
        # print() adds a newline by default. Ensure lines from processors
        # don't have trailing newlines if you don't want double newlines.
        for line in lines:
            print(line, end='\n') # Explicitly add newline
    else:
        try:
            # Open the output file in write mode.
            with open(output_path, 'w') as f:
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
    Processes text lines from an input source using a dynamic pipeline
    loaded from a configuration file and writes the results to an output destination.
    """
    typer.echo(f"Starting processing...") # Use typer.echo for CLI output

    # --- Load the pipeline dynamically from the config file ---
    pipeline = [] # Initialize pipeline list
    try:
        pipeline = get_pipeline_from_config(config)
        if not pipeline:
             typer.echo("Warning: Pipeline is empty. No processing will occur.", err=True)
             # Decide if this should be a hard error or just a warning.
             # For now, allow empty pipeline.
    except Exception as e:
        # If loading the config or any processor fails, the exception is re-raised
        # by get_pipeline_from_config. Catch it here and exit.
        typer.echo(f"Failed to load pipeline from '{config}': {e}", err=True)
        sys.exit(1)

    # --- Read input lines ---
    lines_iterator = None # Initialize to None
    try:
        lines_iterator = read_lines(input)
    except SystemExit: # read_lines already prints error and exits on FileNotFoundError/Error
        sys.exit(1) # Ensure main process exits

    # --- Apply the pipeline to the lines iterator ---
    # apply_pipeline is a generator, so processing is streamed line by line.
    processed_lines_iterator = apply_pipeline(lines_iterator, pipeline)

    # --- Write output ---
    try:
        write_output(processed_lines_iterator, output)
    except SystemExit: # write_output already prints error and exits on IOError/Error
        sys.exit(1) # Ensure main process exits

    # --- Cleanup ---
    # If reading from a file, close the file handle.
    # stdin doesn't need explicit closing in this context.
    if input != "-" and lines_iterator is not None:
         try:
             # Check if the iterator has a 'close' method (like file objects)
             if hasattr(lines_iterator, 'close'):
                 lines_iterator.close()
                 # print("DEBUG: Input file closed.") # Optional debug
         except Exception as e:
             print(f"Error closing input file {input}: {e}", file=sys.stderr)


    typer.echo("Processing finished.")

# --- Main execution block ---
# This is the standard Python entry point.
if __name__ == "__main__":
    # Run the Typer application. This parses CLI arguments and calls
    # the appropriate command function (process_file in this case).
    app()
