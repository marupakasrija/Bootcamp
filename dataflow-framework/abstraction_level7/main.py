# main.py

import logging
import argparse
import threading
import time
import sys

from router import RoutingEngine
# Import the run_dashboard function from the dashboard server file
from dashboard.server import run_dashboard

# Configure basic logging (set to DEBUG to see processor-level logs)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Main function to set up and run the routing engine and the dashboard.
    """
    parser = argparse.ArgumentParser(description="Run the state-based routing engine with optional tracing.")
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

    args = parser.parse_args()

    config_path = 'config/config.yaml'

    try:
        # Initialize the routing engine with the configuration and tracing flag
        engine = RoutingEngine(config_path, enable_tracing=args.trace)
        logging.info(f"Routing engine initialized. Tracing enabled: {args.trace}")

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


        # Add some initial lines to the engine, all tagged with 'start'.
        # The 'start' processor will then assign them their first routing tag.
        initial_lines = [
            "This is a general message.",
            "ERROR: Something went wrong.",
            "A warning occurred WARN.",
            "Another general line.",
            "ERROR in processing data.",
            "WARN: Low disk space.",
            "CamelCaseExampleLine", # Will be processed by snakecase if it reaches 'general'
            "AnotherLineToProcess"
        ]

        logging.info(f"Adding {len(initial_lines)} initial lines to the engine.")
        for line in initial_lines:
            engine.add_line('start', line) # All initial lines enter with the 'start' tag

        # Start processing the queue in the main thread
        engine.process_queue()

        logging.info("Routing engine finished processing.")

        # Keep the main thread alive while the dashboard thread is running
        # In a real application, you might have a more sophisticated way
        # to manage the main thread and signal shutdown.
        # For this example, we'll just wait a bit or wait for user input.
        print("\nRouting engine processing finished. Dashboard server is still running.")
        print(f"Access dashboard at http://{args.dashboard_host}:{args.dashboard_port}/docs")
        print("Press Ctrl+C to exit.")

        try:
            # Keep the main thread alive to allow the dashboard to be accessed
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            logging.info("Shutdown signal received. Exiting.")
            # Daemon thread will exit automatically

    except FileNotFoundError:
        logging.error(f"Configuration file not found at {config_path}")
    except Exception as e:
        logging.error(f"An error occurred during engine execution: {e}", exc_info=True)
        sys.exit(1) # Exit with a non-zero code on error


if __name__ == "__main__":
    main()
