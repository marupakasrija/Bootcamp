# main.py

import logging
import argparse
import threading
import time
import sys
import os
import shutil
import glob # For finding files

from router import RoutingEngine
# Import the run_dashboard function from the dashboard server file
from dashboard.server import run_dashboard

# Configure basic logging (set to DEBUG to see processor-level logs)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_directories(watch_dir: str):
    """Creates the necessary watch directories if they don't exist."""
    unprocessed_dir = os.path.join(watch_dir, 'unprocessed')
    underprocess_dir = os.path.join(watch_dir, 'underprocess')
    processed_dir = os.path.join(watch_dir, 'processed')

    for directory in [unprocessed_dir, underprocess_dir, processed_dir]:
        os.makedirs(directory, exist_ok=True)
        logging.info(f"Ensured directory exists: {directory}")

    return unprocessed_dir, underprocess_dir, processed_dir

def perform_recovery(unprocessed_dir: str, underprocess_dir: str):
    """Moves files from underprocess back to unprocessed on startup."""
    logging.info("Performing recovery: Checking for files in underprocess...")
    files_to_recover = glob.glob(os.path.join(underprocess_dir, '*'))

    if files_to_recover:
        logging.warning(f"Found {len(files_to_recover)} files in underprocess/. Moving back to unprocessed/ for retry.")
        for file_path in files_to_recover:
            try:
                dest_path = os.path.join(unprocessed_dir, os.path.basename(file_path))
                shutil.move(file_path, dest_path)
                logging.info(f"Moved '{file_path}' to '{dest_path}'.")
            except Exception as e:
                logging.error(f"Error during recovery, failed to move '{file_path}': {e}", exc_info=True)
    else:
        logging.info("No files found in underprocess/. Recovery complete.")

def file_monitor_loop(engine: RoutingEngine, unprocessed_dir: str, underprocess_dir: str, poll_interval_seconds: int = 5):
    """Continuously monitors the unprocessed directory for new files."""
    logging.info(f"Starting file monitor loop for '{unprocessed_dir}'. Polling every {poll_interval_seconds} seconds.")
    while True:
        try:
            # Get list of files in unprocessed directory
            files_to_process = glob.glob(os.path.join(unprocessed_dir, '*'))

            for file_path in files_to_process:
                file_name = os.path.basename(file_path)
                logging.info(f"Found new file: {file_name}")

                # Move file to underprocess directory atomically
                underprocess_file_path = os.path.join(underprocess_dir, file_name)
                try:
                    shutil.move(file_path, underprocess_file_path)
                    logging.info(f"Moved '{file_name}' to underprocess/.")

                    # Update file counts for dashboard
                    with engine._file_state_lock:
                         engine._file_counts['unprocessed'] -= 1
                         engine._file_counts['underprocess'] += 1

                except Exception as e:
                    logging.error(f"Error moving file '{file_name}' to underprocess/: {e}", exc_info=True)
                    # If move fails, skip this file for now, it will be picked up in the next poll
                    continue # Skip to the next file

                # Read the file line by line and add to the engine's queue
                line_count = 0
                try:
                    with open(underprocess_file_path, 'r') as f:
                        for line in f:
                            line_count += 1
                            # Add line to the engine's queue with the file path
                            engine.add_line('start', line.strip(), underprocess_file_path) # Use underprocess path
                    logging.info(f"Added {line_count} lines from '{file_name}' to the processing queue.")

                    # The engine's process_queue will handle decrementing the line count
                    # and moving the file to 'processed' when all lines are done.

                except Exception as e:
                    logging.error(f"Error reading or adding lines from '{file_name}': {e}", exc_info=True)
                    # Handle file reading errors - maybe move to an error directory?
                    # For now, we just log and leave it in underprocess for manual inspection/cleanup.
                    with engine._error_lock:
                         engine.error_history.append(('file_monitor', f"Error reading file: {e}", "N/A", underprocess_file_path))


            # Sleep for the poll interval before checking again
            time.sleep(poll_interval_seconds)

        except Exception as e:
            logging.error(f"Unexpected error in file monitor loop: {e}", exc_info=True)
            time.sleep(poll_interval_seconds) # Wait before retrying loop


def process_single_file(engine: RoutingEngine, file_path: str):
    """Processes a single file line by line and adds to the queue."""
    logging.info(f"Processing single file: {file_path}")
    file_name = os.path.basename(file_path)
    try:
        line_count = 0
        with open(file_path, 'r') as f:
            for line in f:
                line_count += 1
                # Add line to the engine's queue with the file path
                engine.add_line('start', line.strip(), file_path) # Use original file path
        logging.info(f"Added {line_count} lines from '{file_name}' to the processing queue.")

        # For single file mode, we process the queue until it's empty
        engine.process_queue()
        logging.info(f"Finished processing single file: {file_name}")

        # Note: File state management (moving to processed) is not handled
        # in single-file mode as it's designed for ephemeral processing.
        # If persistent state for single files was needed, this logic would change.

    except FileNotFoundError:
        logging.error(f"Input file not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error processing single file '{file_name}': {e}", exc_info=True)
        sys.exit(1)


def main():
    """
    Main function to set up and run the routing engine, dashboard, and file monitor (if in watch mode).
    Supports single file or watch mode execution.
    """
    parser = argparse.ArgumentParser(description="Run the state-based routing engine.")
    parser.add_argument(
        '--trace',
        action='store_true',
        help='Enable tracing for lines flowing through the engine.'
    )
    parser.add_argument(
        '--dashboard-port',
        type=int,
        default=8000,
        help='Port for the FastAPI dashboard server (default: 8000).'
    )
    parser.add_argument(
        '--dashboard-host',
        type=str,
        default="127.0.0.1",
        help='Host for the FastAPI dashboard server (default: 127.0.0.1).'
    )

    # Add mutually exclusive group for --input or --watch
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        '--input',
        type=str,
        help='Path to a single file to process.'
    )
    mode_group.add_argument(
        '--watch',
        action='store_true',
        help='Enable watch mode to continuously monitor the watch directory.'
    )

    parser.add_argument(
        '--watch-dir',
        type=str,
        default="watch_dir",
        help='Base directory to monitor for new files in watch mode (default: watch_dir).'
    )
    parser.add_argument(
        '--poll-interval',
        type=int,
        default=5,
        help='Interval in seconds to poll the unprocessed directory in watch mode (default: 5).'
    )


    args = parser.parse_args()

    config_path = 'config/config.yaml'

    try:
        # Initialize the routing engine
        # Pass watch_dir only if in watch mode, as it's needed for file state tracking
        engine = RoutingEngine(
            config_path,
            watch_dir=args.watch_dir if args.watch else None,
            enable_tracing=args.trace
        )
        logging.info(f"Routing engine initialized. Tracing enabled: {args.trace}")

        # --- Start the FastAPI dashboard in a separate thread ---
        # Dashboard runs in both modes for observability
        dashboard_thread = threading.Thread(
            target=run_dashboard,
            args=(engine, args.dashboard_host, args.dashboard_port),
            daemon=True # Set as daemon so it exits when the main thread exits
        )
        dashboard_thread.start()
        # Give the server a moment to start
        time.sleep(1)
        logging.info(f"Dashboard running at http://{args.dashboard_host}:{args.dashboard_port}/docs")


        if args.watch:
            # --- Watch Mode ---
            logging.info("Running in Watch Mode.")
            # Setup and recover directories only in watch mode
            unprocessed_dir, underprocess_dir, processed_dir = setup_directories(args.watch_dir)
            perform_recovery(unprocessed_dir, underprocess_dir)

            # Update initial file counts for dashboard after recovery
            with engine._file_state_lock:
                engine._file_counts['unprocessed'] = len(glob.glob(os.path.join(unprocessed_dir, '*')))
                engine._file_counts['underprocess'] = len(glob.glob(os.path.join(underprocess_dir, '*')))
                engine._file_counts['processed'] = len(glob.glob(os.path.join(processed_dir, '*')))
            logging.info(f"Initial file counts: {engine.get_file_state()['file_counts']}")

            # Start the File Monitor in a separate thread
            monitor_thread = threading.Thread(
                target=file_monitor_loop,
                args=(engine, unprocessed_dir, underprocess_dir, args.poll_interval),
                daemon=True
            )
            monitor_thread.start()
            logging.info("File monitor thread started.")

            # Run the Routing Engine's continuous processing loop in the main thread
            logging.info("Starting main routing engine continuous processing loop.")
            engine.process_queue_continuously() # This runs indefinitely

        elif args.input:
            # --- Single File Mode ---
            logging.info(f"Running in Single File Mode for: {args.input}")
            # Process the single input file
            process_single_file(engine, args.input)
            logging.info("Single file processing finished. Exiting.")
            # In single file mode, the main thread exits after processing is done.
            # Daemon dashboard thread will also exit.


    except FileNotFoundError as e:
        logging.error(f"File not found: {e}", exc_info=True)
        sys.exit(1)
    except Exception as e:
        logging.error(f"An error occurred during engine setup or execution: {e}", exc_info=True)
        sys.exit(1) # Exit with a non-zero code on error


if __name__ == "__main__":
    main()
