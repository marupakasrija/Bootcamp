# main.py
import argparse
import os
import sys
import uvicorn
import threading
import asyncio

# Import your core modules
from api import app as fastapi_app, set_watch_base_dir # Import the FastAPI app instance and config function
from watcher import start_watching # Import the watcher function
from processor import process_file, update_stats # Import processing logic and stats update

# Define the base directory for watch_dir relative to main.py script location
# This ensures it works correctly regardless of the current working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_WATCH_BASE_DIR = os.path.join(BASE_DIR, 'watch_dir')
DEFAULT_UNPROCESSED_DIR = os.path.join(DEFAULT_WATCH_BASE_DIR, 'unprocessed')
DEFAULT_PROCESSED_DIR = os.path.join(DEFAULT_WATCH_BASE_DIR, 'processed')
DEFAULT_ERROR_DIR = os.path.join(DEFAULT_WATCH_BASE_DIR, 'error')


def run_single_file_mode(filepath: str):
    """Processes a single file and exits."""
    print(f"Running in Single File Mode for: {filepath}")
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}", file=sys.stderr)
        sys.exit(1)

    # Define target directories for single file mode processing results
    # You might want dedicated dirs or use the standard ones
    # For simplicity, we'll use the default watch_dir structure
    processed_dir = DEFAULT_PROCESSED_DIR
    error_dir = DEFAULT_ERROR_DIR

    # Ensure target directories exist
    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(error_dir, exist_ok=True)

    success = process_file(filepath, processed_dir, error_dir)
    update_stats(success) # Update stats even in single file mode

    print("Processing complete.")
    # Exit is handled by argparse logic implicitly after this function returns

async def run_watch_mode(watch_directory: str, processed_dir: str, error_dir: str):
    """Starts the watcher and the API concurrently."""
    print(f"Running in Watch Mode. Monitoring: {watch_directory}")

    # Ensure directories exist
    os.makedirs(watch_directory, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(error_dir, exist_ok=True)

    # --- Start the Watcher in a separate thread or using asyncio ---
    # Using a separate thread for the blocking watcher function
    watcher_thread = threading.Thread(target=start_watching, args=(watch_directory, processed_dir, error_dir), daemon=True)
    watcher_thread.start()
    # -------------------------------------------------------------

    # --- Start the FastAPI API using uvicorn ---
    print("Starting FastAPI server...")
    # Configure the API with the correct watch_dir base path
    set_watch_base_dir(DEFAULT_WATCH_BASE_DIR) # Use the default for API directory listing

    # Run uvicorn using the async method run()
    # uvicorn.run() is blocking, we need to run it within an asyncio event loop
    # and manage it alongside the watcher thread (or integrate watcher with asyncio)

    # A simpler approach for demonstration is to just start the API and let it run
    # alongside the watcher thread which is marked as daemon.
    # The main thread will technically exit the asyncio.run block once the uvicorn server stops,
    # but the daemon watcher thread will keep the process alive until interrupted (e.g., Ctrl+C).
    # For robust production, consider better process/thread management or full asyncio integration.

    config = uvicorn.Config(
        app=fastapi_app,
        host="0.0.0.0", # Listen on all interfaces in Docker, or localhost locally
        port=8000,
        log_level="info" # Configure based on args if needed
        # reload=True # Useful for development
    )
    server = uvicorn.Server(config)
    await server.serve() # This is an async method

    # -------------------------------------------

    print("Watch mode stopping.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Real-Time File Processing System. Processes files from a watched directory or a single specified file."
    )

    # Mutually exclusive group for --input or --watch
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--input",
        help="Process a single file and exit. Specify the file path."
    )
    mode_group.add_argument(
        "--watch",
        action="store_true", # This makes it a boolean flag
        help="Continuously monitor the watch directory for new files and run the API."
    )

    # Optional arguments
    parser.add_argument(
        "--watch-dir",
        default=DEFAULT_UNPROCESSED_DIR, # Default to the 'unprocessed' subdir
        help=f"Directory to monitor for watch mode (default: {DEFAULT_UNPROCESSED_DIR})."
    )
    # Add more args like --debug, --log-level, --config-file etc.

    args = parser.parse_args()

    # --- Argument Validation and Execution ---

    if args.input:
        # Single File Mode
        # Ensure the input path is absolute for clarity in processor logs
        input_filepath = os.path.abspath(args.input)
        run_single_file_mode(input_filepath)

    elif args.watch:
        # Watch Mode
        # The watcher needs the unprocessed dir to watch and processed/error dirs to move files to
        watch_dir_to_monitor = os.path.abspath(args.watch_dir) # Make absolute
        # Assume processed/error are siblings of the watch_dir being monitored
        # If monitoring ./watch_dir/unprocessed, then processed is ../processed, error is ../error
        # Adjust paths based on your desired structure
        watch_base = os.path.dirname(watch_dir_to_monitor) # e.g., ./watch_dir
        processed_dir = os.path.join(watch_base, 'processed')
        error_dir = os.path.join(watch_base, 'error')

        print(f"Watcher will monitor: {watch_dir_to_monitor}")
        print(f"Processed files go to: {processed_dir}")
        print(f"Error files go to: {error_dir}")
        print("-" * 20)

        # Run the async watch mode function
        # This will start the watcher thread and the uvicorn server
        asyncio.run(run_watch_mode(watch_dir_to_monitor, processed_dir, error_dir))

    print("Application finished.")