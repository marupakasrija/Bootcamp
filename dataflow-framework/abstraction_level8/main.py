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


def main():
    """
    Main function to set up and run the routing engine, dashboard, and file monitor.
    """
    parser = argparse.ArgumentParser(description="Run the state-based routing engine with folder monitoring and dashboard.")
    parser.add_argument(
        '--trace',
        action='store_true', # This makes the argument a boolean flag
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
    parser.add_argument(
        '--watch-dir',
        type=str,
        default="watch_dir",
        help='Base directory to monitor for new files (default: watch_dir).'
    )
    parser.add_argument(
        '--poll-interval',
        type=int,
        default=5,
        help='Interval in seconds to poll the unprocessed directory (default: 5).'
    )


    args = parser.parse_args()

    config_path = 'config/config.yaml'

    try:
        # --- Setup Watch Directories ---
        unprocessed_dir, underprocess_dir, processed_dir = setup_directories(args.watch_dir)

        # --- Perform Recovery ---
        perform_recovery(unprocessed_dir, underprocess_dir)

        # --- Initialize Routing Engine ---
        # Pass the base watch_dir to the engine so it knows the structure
        engine = RoutingEngine(config_path, args.watch_dir, enable_tracing=args.trace)
        logging.info(f"Routing engine initialized. Tracing enabled: {args.trace}")

        # --- Update initial file counts for dashboard after recovery ---
        with engine._file_state_lock:
             engine._file_counts['unprocessed'] = len(glob.glob(os.path.join(unprocessed_dir, '*')))
             engine._file_counts['underprocess'] = len(glob.glob(os.path.join(underprocess_dir, '*')))
             engine._file_counts['processed'] = len(glob.glob(os.path.join(processed_dir, '*')))
        logging.info(f"Initial file counts: {engine.get_file_state()['file_counts']}")


        # --- Start the FastAPI dashboard in a separate thread ---
        # We need to pass the engine instance to the dashboard server
        dashboard_thread = threading.Thread(
            target=run_dashboard,
            args=(engine, args.dashboard_host, args.dashboard_port),
            daemon=True # Set as daemon so it exits when the main thread exits
        )
        dashboard_thread.start()
        # Give the server a moment to start
        time.sleep(1)
        logging.info(f"Dashboard running at http://{args.dashboard_host}:{args.dashboard_port}/docs")


        # --- Start the File Monitor in a separate thread ---
        monitor_thread = threading.Thread(
            target=file_monitor_loop,
            args=(engine, unprocessed_dir, underprocess_dir, args.poll_interval),
            daemon=True # Set as daemon so it exits when the main thread exits
        )
        monitor_thread.start()
        logging.info("File monitor thread started.")

        # --- Run the Routing Engine's processing loop in the main thread ---
        # The engine's process_queue_continuously method will now run indefinitely,
        # processing items added by the file monitor thread.
        logging.info("Starting main routing engine processing loop.")
        engine.process_queue_continuously()


    except FileNotFoundError:
        logging.error(f"Configuration file not found at {config_path}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An error occurred during engine setup or main loop execution: {e}", exc_info=True)
        sys.exit(1) # Exit with a non-zero code on error


if __name__ == "__main__":
    main()
