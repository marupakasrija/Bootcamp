# This is abstraction-level-8/main.py
# The main entry point for the application in Level 8.
# Handles CLI arguments, loads State Transition configuration, orchestrates processing,
# runs the observability dashboard, and monitors a folder for new files.

from Dataflow_framework.abstraction_level8.types import ErrorData
from Dataflow_framework.abstraction_level8.pipeline import StateTransitionEngine
import sys  # Needed for sys.stdin, sys.stderr, sys.exit
import typer
import os   # Needed for os.getenv, os.path, os.listdir, os.makedirs, os.rename
import shutil # Needed for shutil.move
import time # For polling interval and timestamps
from typing import Optional, Iterator, List # Import Iterator, List
import codecs # Needed for handling BOM
import threading # Needed for running the dashboard in a separate thread
import uvicorn # ASGI server for FastAPI
import glob # For finding files

# Import components from our modules using RELATIVE imports.
# This tells Python to look for these modules within the current package directory.
# Ensure you have empty __init__.py files in this directory and its subdirectories
# for these relative imports to work correctly when running as a package
# using 'python -m abstraction_level8.main'.
from .cli import app # Import the Typer app instance
from .pipeline import get_state_transition_engine_from_config # Use the dynamic State config loader
from .types import ObservabilityData, FileStatus # Import shared data structures and file status types
# Import the FastAPI app instance from the dashboard module
from .dashboard.app import app as dashboard_app, observability_data as shared_observability_data_ref # Import app and the shared data reference

# --- Shared Observability Data Instance ---
# Create the single instance of ObservabilityData that will be shared
# between the main processing thread and the dashboard thread.
observability_data_instance = ObservabilityData()

# Update the reference in the dashboard app module
shared_observability_data_ref.observability_data = observability_data_instance


# --- Helper functions for reading/writing ---
# Reusing functions from previous levels.

def read_lines(path: str) -> Iterator[str]:
    """
    Reads lines from a file, handling common encodings (including UTF-16 BOM)
    and stripping trailing newlines. Designed for reading files from the watch directory.

    Args:
        path: The path to the input file.

    Returns:
        An iterator yielding lines from the source, stripped of trailing newlines.

    Raises:
        IOError: If the input file cannot be opened or read.
    """
    # Note: This version is specifically for files, not stdin.
    # Stdin handling is removed as the monitor processes files.
    try:
        # Open the file explicitly with UTF-16 encoding.
        # The 'utf-16' codec handles both big and little endian variants
        # and the UTF-16 BOM if present.
        file_handle = codecs.open(path, 'r', encoding='utf-16')
        print(f"Reading from file: {path} with utf-16 encoding", file=sys.stderr)
        lines_source = file_handle # Return iterator (file handle)

    except Exception as e:
        # Catch any file reading error and re-raise as IOError
        raise IOError(f"Error opening or reading input file {path}: {e}") from e


    # Yield lines, stripping trailing newlines consistently.
    # This handles both \n and \r\n.
    try:
        for line in lines_source:
            yield line.rstrip('\r\n')
    finally:
        # Ensure the file handle is closed after iterating
        if hasattr(lines_source, 'close'):
             try:
                 lines_source.close()
                 # print(f"DEBUG: Input file {path} closed.", file=sys.stderr) # Optional debug)
             except Exception as e:
                 print(f"Error closing input file {path}: {e}", file=sys.stderr)


def write_output(lines: Iterator[str], output_path: Optional[str]):
    """
    Writes processed lines to a file or stdout, ensuring each line ends with a newline.
    Adapted to work within the file processing loop.

    Args:
        lines: An iterator yielding processed lines (strings).
        output_path: The base directory for output files, or None for stdout.
                     If output_path is a directory, output will be written to
                     <output_path>/<input_filename>.processed.txt
                     If output_path is None, writes to stdout.

    Raises:
        IOError: If there is an error writing to the output file.
    """
    # Note: This function is simplified for the file monitoring context.
    # It assumes output_path is either None (stdout) or a directory path.

    if output_path is None:
        # print("Writing to stdout...", file=sys.stderr) # Already printed by engine run
        # Iterate through the processed lines and print each one.
        for line in lines:
            print(line) # print() adds a newline by default
    else:
        # Assuming output_path is a directory
        # The engine.run method doesn't know the input file name directly.
        # This write_output function is called *after* engine.run finishes for a file.
        # A better design might pass the input file name down or have the END state write.
        # For simplicity, let's assume output_path is the *full path* to the desired output file.
        # This requires the caller (the monitor loop) to construct the output path.
        # Let's adjust the monitor loop to handle output file path construction.
        # This function will just write to the given path.

        # Reverting to the simpler L7 write_output logic, assuming output_path is
        # either None or a specific file path provided by the CLI (less useful for monitoring).
        # For monitoring, we'll likely write to a file per input file.
        # Let's assume output_path is a directory, and we write to a file based on input file name.

        # This write_output is now called *per file* processed by the monitor.
        # The monitor loop will provide the correct output_path.

        # print(f"Writing output to {output_path}...", file=sys.stderr) # Already printed by monitor

        try:
            # Open the output file in write mode with UTF-8 encoding.
            with open(output_path, 'w', encoding='utf-8') as f:
                # Iterate through the processed lines and write each one to the file.
                for line in lines:
                    f.write(line + '\n') # Write line followed by a newline
            # print(f"Output written to {output_path}", file=sys.stderr) # Printed by monitor
        except IOError as e:
            raise IOError(f"Error writing output to {output_path}: {e}") from e
        except Exception as e:
            raise IOError(f"An unexpected error occurred while writing output to {output_path}: {e}") from e


# --- Dashboard Thread Function ---
def run_dashboard():
    """Runs the FastAPI dashboard using Uvicorn."""
    # Use reload=False when running in a separate thread to avoid issues
    # log_level can be adjusted (e.g., "info", "warning", "error")
    # Access the imported dashboard_app instance
    uvicorn.run(dashboard_app, host="127.0.0.1", port=8000, log_level="warning")

# --- Folder Monitoring Logic ---

def monitor_folder(watch_dir: str, engine: StateTransitionEngine, config_path: str, output_dir: Optional[str]):
    """
    Monitors the watch directory for new files and orchestrates processing.

    Args:
        watch_dir: The base directory to monitor.
        engine: The initialized StateTransitionEngine instance.
        config_path: Path to the state configuration file (for error logging).
        output_dir: Optional directory to write processed output files.
    """
    unprocessed_dir = os.path.join(watch_dir, "unprocessed")
    underprocess_dir = os.path.join(watch_dir, "underprocess")
    processed_dir = os.path.join(watch_dir, "processed")
    error_dir = os.path.join(watch_dir, "error") # New directory for failed files

    # Ensure watch directories exist
    for directory in [unprocessed_dir, underprocess_dir, processed_dir, error_dir]:
        os.makedirs(directory, exist_ok=True)

    print(f"Monitoring folder: {watch_dir}", file=sys.stderr)
    print(f"  Unprocessed: {unprocessed_dir}", file=sys.stderr)
    print(f"  Underprocess: {underprocess_dir}", file=sys.stderr)
    print(f"  Processed: {processed_dir}", file=sys.stderr)
    print(f"  Error: {error_dir}", file=sys.stderr)


    # --- Recovery Logic: Move files from underprocess back to unprocessed on startup ---
    print("Checking for files under process from previous run...", file=sys.stderr)
    files_under_process = glob.glob(os.path.join(underprocess_dir, "*"))
    if files_under_process:
        print(f"Found {len(files_under_process)} files under process. Moving back to unprocessed...", file=sys.stderr)
        for file_path in files_under_process:
            file_name = os.path.basename(file_path)
            dest_path = os.path.join(unprocessed_dir, file_name)
            try:
                shutil.move(file_path, dest_path)
                print(f"Moved '{file_name}' from underprocess to unprocessed.", file=sys.stderr)
                # Update observability data for recovery
                observability_data_instance.add_recent_file(FileStatus(file_name, FileStatus.UNPROCESSED, time.time()))
            except Exception as e:
                print(f"Error moving '{file_name}' during recovery: {e}", file=sys.stderr)
                # Log error to observability data
                observability_data_instance.add_error(ErrorData(time.time(), "Recovery", f"Error moving file: {e}", "N/A", "N/A", file_name=file_name))


    # --- Monitoring Loop ---
    polling_interval_seconds = 5 # How often to check the unprocessed folder

    print(f"Starting folder monitoring loop (polling every {polling_interval_seconds} seconds)...", file=sys.stderr)

    while True: # Run indefinitely
        try:
            # Update file counts for dashboard
            unprocessed_files = os.listdir(unprocessed_dir)
            underprocess_files = os.listdir(underprocess_dir)
            processed_files = os.listdir(processed_dir)
            error_files = os.listdir(error_dir) # Get error files count

            observability_data_instance.update_file_status_counts(
                len(unprocessed_files),
                len(underprocess_files),
                len(processed_files),
                len(error_files) # Pass error count
            )

            # Process files in the unprocessed directory
            # Sort files to process them in a predictable order (e.g., by name)
            unprocessed_files.sort()

            for file_name in unprocessed_files:
                file_path = os.path.join(unprocessed_dir, file_name)
                # Ensure it's actually a file and not a directory
                if not os.path.isfile(file_path):
                    continue

                print(f"Found new file: {file_name}. Starting processing...", file=sys.stderr)

                # --- Move to Under Process ---
                underprocess_file_path = os.path.join(underprocess_dir, file_name)
                try:
                    shutil.move(file_path, underprocess_file_path)
                    print(f"Moved '{file_name}' to underprocess.", file=sys.stderr)
                    # Update observability data: set current file, add recent file status
                    observability_data_instance.set_current_file(file_name)
                    observability_data_instance.add_recent_file(FileStatus(file_name, FileStatus.UNDERPROCESS, time.time()))
                    # Update counts immediately after move
                    observability_data_instance.update_file_status_counts(
                         len(os.listdir(unprocessed_dir)),
                         len(os.listdir(underprocess_dir)),
                         len(processed_files), # Keep previous processed count for now
                         len(error_files) # Keep previous error count for now
                    )

                except Exception as e:
                    print(f"Error moving '{file_name}' to underprocess: {e}. Skipping processing.", file=sys.stderr)
                    # Log error to observability data
                    observability_data_instance.add_error(ErrorData(time.time(), "Folder Monitor", f"Error moving file to underprocess: {e}", "N/A", "N/A", file_name=file_name))
                    # Update file status to ERROR if move fails? Or leave in unprocessed?
                    # Leaving in unprocessed might lead to repeated move errors.
                    # Let's move to error_dir if the initial move to underprocess fails.
                    error_file_path = os.path.join(error_dir, file_name)
                    try:
                        shutil.move(file_path, error_file_path)
                        print(f"Moved '{file_name}' to error directory due to move failure.", file=sys.stderr)
                        observability_data_instance.add_recent_file(FileStatus(file_name, FileStatus.ERROR, time.time()))
                         # Update counts after moving to error
                        observability_data_instance.update_file_status_counts(
                             len(os.listdir(unprocessed_dir)),
                             len(os.listdir(underprocess_dir)),
                             len(processed_files),
                             len(os.listdir(error_dir))
                        )
                    except Exception as move_to_error_e:
                         print(f"Critical Error: Could not move '{file_name}' to error directory after move to underprocess failed: {move_to_error_e}", file=sys.stderr)
                         # Log this critical error
                         observability_data_instance.add_error(ErrorData(time.time(), "Folder Monitor", f"Critical: Could not move file to error after move to underprocess failed: {move_to_error_e}", "N/A", "N/A", file_name=file_name))
                    continue # Skip processing this file

                # --- Process the file ---
                processing_successful = False
                try:
                    # Read lines from the file in the underprocess directory
                    lines_iterator = read_lines(underprocess_file_path)

                    # Run the State Transition engine on the lines from this file
                    # Pass the file_name to the engine for better error/trace logging
                    processed_lines_iterator = engine.run(lines_iterator, file_name=file_name)

                    # Write the output. Assuming output_dir is provided, write to a file.
                    if output_dir:
                        # Create output directory if it doesn't exist
                        os.makedirs(output_dir, exist_ok=True)
                        # Construct output file name (e.g., original_filename.processed.txt)
                        output_file_name = f"{file_name}.processed.txt"
                        output_file_path = os.path.join(output_dir, output_file_name)
                        write_output(processed_lines_iterator, output_file_path)
                        print(f"Output for '{file_name}' written to {output_file_path}", file=sys.stderr)
                    else:
                        # If no output_dir, write to stdout (less practical for monitoring)
                        print(f"Processing output for '{file_name}':", file=sys.stderr)
                        write_output(processed_lines_iterator, None) # None means stdout


                    processing_successful = True
                    print(f"Finished processing file: {file_name}.", file=sys.stderr)

                except Exception as e:
                    print(f"Error processing file '{file_name}': {e}", file=sys.stderr)
                    # Log error to observability data (engine might have already logged specific state errors)
                    observability_data_instance.add_error(ErrorData(time.time(), "Engine Orchestration", f"Error processing file: {e}", "N/A", "N/A", file_name=file_name))
                    processing_successful = False # Ensure this is False on error

                # --- Move to Processed or Error ---
                if processing_successful:
                    processed_file_path = os.path.join(processed_dir, file_name)
                    try:
                        shutil.move(underprocess_file_path, processed_file_path)
                        print(f"Moved '{file_name}' to processed.", file=sys.stderr)
                        # Update observability data
                        observability_data_instance.add_recent_file(FileStatus(file_name, FileStatus.PROCESSED, time.time()))
                         # Update counts after moving to processed
                        observability_data_instance.update_file_status_counts(
                             len(os.listdir(unprocessed_dir)),
                             len(os.listdir(underprocess_dir)),
                             len(os.listdir(processed_dir)),
                             len(error_files)
                        )
                    except Exception as e:
                        print(f"Error moving '{file_name}' to processed: {e}. File remains in underprocess.", file=sys.stderr)
                        # Log error to observability data
                        observability_data_instance.add_error(ErrorData(time.time(), "Folder Monitor", f"Error moving file to processed: {e}", "N/A", "N/A", file_name=file_name))
                        # File remains in underprocess for retry on next restart.
                        # Update file status to indicate it's still underprocess but had an issue.
                        observability_data_instance.add_recent_file(FileStatus(file_name, FileStatus.UNDERPROCESS, time.time())) # Status didn't change, but timestamp updates
                else:
                    # Processing failed, move to error directory
                    error_file_path = os.path.join(error_dir, file_name)
                    try:
                        shutil.move(underprocess_file_path, error_file_path)
                        print(f"Moved '{file_name}' to error directory due to processing failure.", file=sys.stderr)
                        # Update observability data
                        observability_data_instance.add_recent_file(FileStatus(file_name, FileStatus.ERROR, time.time()))
                         # Update counts after moving to error
                        observability_data_instance.update_file_status_counts(
                             len(os.listdir(unprocessed_dir)),
                             len(os.listdir(underprocess_dir)),
                             len(processed_files),
                             len(os.listdir(error_dir))
                        )
                    except Exception as e:
                        print(f"Critical Error: Could not move '{file_name}' to error directory after processing failed: {e}. File remains in underprocess.", file=sys.stderr)
                        # Log error to observability data
                        observability_data_instance.add_error(ErrorData(time.time(), "Folder Monitor", f"Critical: Could not move file to error after processing failed: {e}", "N/A", "N/A", file_name=file_name))
                        # File remains in underprocess for retry on next restart.
                        observability_data_instance.add_recent_file(FileStatus(file_name, FileStatus.UNDERPROCESS, time.time())) # Status didn't change, but timestamp updates


                # Reset current file processing status in observability data
                observability_data_instance.set_current_file(None)


            # Sleep for the polling interval before checking again
            time.sleep(polling_interval_seconds)

        except Exception as e:
            print(f"An unexpected error occurred in the folder monitoring loop: {e}", file=sys.stderr)
            # Log error to observability data
            observability_data_instance.add_error(ErrorData(time.time(), "Folder Monitor", f"Unexpected loop error: {e}", "N/A", "N/A", file_name="N/A"))
            # Sleep briefly before continuing the loop to avoid tight loop on persistent error
            time.sleep(polling_interval_seconds)


# --- Typer Command Definition ---

# Define the main command using the imported 'app' instance from cli.py.
# This command is the entry point when the script is run.
@app.command()
def monitor(
    # Define command-line options using typer.Option.
    # --watch-dir: Required directory to monitor.
    watch_dir: str = typer.Option(..., "--watch-dir", help="Directory to monitor for new files."),
    # --output-dir: Optional directory to write processed output files.
    # If not provided, output goes to stdout (less useful for monitoring).
    output_dir: Optional[str] = typer.Option(None, "--output-dir", help="Directory to write processed output files."),
    # --config: Required, defaults to "state_config.yaml".
    # This is the path to the YAML file defining the state transitions.
    config: str = typer.Option("state_config.yaml", "--config", help="Path to the YAML state transition configuration file."),
    # --trace: Optional flag to enable tracing
    trace: bool = typer.Option(False, "--trace", help="Enable line tracing for observability dashboard."),
):
    """
    Monitors a directory for new files, processes them using the state transition system,
    and runs an observability dashboard.
    """
    typer.echo(f"Starting Automated Folder Monitoring and Processing...") # Use typer.echo for CLI output

    # --- Start the Dashboard Thread ---
    # The dashboard needs access to the shared_observability_data_ref
    dashboard_thread = threading.Thread(target=run_dashboard, daemon=True) # daemon=True allows main thread to exit
    dashboard_thread.start()
    typer.echo("Dashboard running in background thread at http://127.0.0.1:8000", err=True)
    time.sleep(0.1) # Give the server a moment to start

    # --- Load the State Transition engine dynamically from the config file ---
    engine = None # Initialize engine
    try:
        # Pass the shared observability data instance and tracing flag to the engine
        engine = get_state_transition_engine_from_config(config, observability_data_instance, enable_tracing=trace)
        # The engine itself contains the state transition logic
    except Exception as e:
        # If loading the config or initializing the engine fails, catch it here and exit.
        typer.echo(f"Failed to load State Transition engine from '{config}': {e}", err=True)
        sys.exit(1)

    # --- Start the Folder Monitoring Loop ---
    # This function contains the main processing loop and recovery logic.
    # It will run indefinitely.
    try:
        monitor_folder(watch_dir, engine, config, output_dir)
    except Exception as e:
        # Catch unexpected errors from the monitor loop itself (e.g., invalid watch_dir)
        typer.echo(f"Critical Error in folder monitor: {e}", err=True)
        # Log error to observability data
        observability_data_instance.add_error(ErrorData(time.time(), "Folder Monitor", f"Critical startup error: {e}", "N/A", "N/A", file_name="N/A"))
        sys.exit(1) # Exit if the monitor cannot start


    # The monitor_folder function runs in a while True loop, so this line is
    # theoretically unreachable unless the loop is broken or an unhandled exception occurs.
    typer.echo("Automated Folder Monitoring processing finished (unexpected exit).")
    # The dashboard thread is daemonized, so it will exit when the main thread exits.


# --- Main execution block ---
# This is the standard Python entry point.
if __name__ == "__main__":
    # Run the Typer application. This parses CLI arguments and calls
    # the appropriate command function (monitor in this case).
    # Typer will handle exiting the process when the command finishes (or if monitor exits).
    app()
