# main.py

import logging
from router import RoutingEngine

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Main function to set up and run the routing engine.
    """
    config_path = 'config/config.yaml'

    try:
        # Initialize the routing engine with the configuration
        engine = RoutingEngine(config_path)

        # Add some initial lines to the engine, all tagged with 'start'.
        # The 'start' processor will then assign them their first routing tag.
        initial_lines = [
            "This is a general message.",
            "ERROR: Something went wrong.",
            "A warning occurred WARN.",
            "Another general line.",
            "ERROR in processing data.",
            "WARN: Low disk space.",
            "CamelCaseExampleLine", # Will be processed by snakecase
            "AnotherLineToProcess"
        ]

        logging.info(f"Adding {len(initial_lines)} initial lines to the engine.")
        for line in initial_lines:
            engine.add_line('start', line) # All initial lines enter with the 'start' tag

        # Start processing the queue
        engine.process_queue()

        logging.info("Routing engine finished processing.")

        # Optional: Visualize the graph (if networkx and matplotlib are installed)
        # engine.visualize_graph()

    except FileNotFoundError:
        logging.error(f"Configuration file not found at {config_path}")
    except Exception as e:
        logging.error(f"An error occurred during engine execution: {e}")

if __name__ == "__main__":
    main()
