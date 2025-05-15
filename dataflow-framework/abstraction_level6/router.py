# router.py

import yaml
import importlib
import logging
from collections import deque
from typing import Dict, Any, Tuple, Iterator, List

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RoutingEngine:
    """
    The core state-based routing engine.
    Manages processors, the routing queue, and the state transitions.
    """
    def __init__(self, config_path: str):
        """
        Initializes the RoutingEngine by loading configuration and processors.

        Args:
            config_path: Path to the configuration file (e.g., 'config/config.yaml').
        """
        self.config = self._load_config(config_path)
        self.processors = self._load_processors(self.config)
        # Use a deque for efficient appending and popping from both ends.
        self.routing_queue = deque()
        self.active_lines = set() # Keep track of lines currently being processed to help detect cycles

        # Optional: Use networkx to represent the graph (for visualization/validation)
        # try:
        #     import networkx as nx
        #     self.graph = nx.DiGraph()
        #     self._build_graph()
        # except ImportError:
        #     logging.warning("networkx not installed. Graph visualization/validation disabled.")
        #     self.graph = None

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Loads the routing configuration from a YAML file."""
        logging.info(f"Loading configuration from {config_path}")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        logging.info("Configuration loaded successfully.")
        return config

    def _load_processors(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Loads and instantiates processor classes based on the configuration.
        Maps tag names to processor instances.
        """
        logging.info("Loading processors...")
        processors = {}
        for node in config.get('nodes', []):
            tag = node.get('tag')
            processor_type = node.get('type')
            if not tag or not processor_type:
                logging.error(f"Invalid node configuration: {node}")
                continue

            try:
                # Dynamically import the module and get the class
                module_name, class_name = processor_type.rsplit('.', 1)
                module = importlib.import_module(module_name)
                processor_class = getattr(module, class_name)
                # Instantiate the processor
                processors[tag] = processor_class()
                logging.info(f"Loaded processor for tag '{tag}': {processor_type}")
            except ImportError:
                logging.error(f"Could not import processor module: {module_name}")
                raise
            except AttributeError:
                logging.error(f"Could not find processor class '{class_name}' in module '{module_name}'")
                raise
            except Exception as e:
                logging.error(f"Error instantiating processor {processor_type}: {e}")
                raise

        logging.info(f"Finished loading {len(processors)} processors.")
        return processors

    # Optional networkx integration (uncomment if networkx is installed)
    # def _build_graph(self):
    #     """Builds the routing graph using networkx."""
    #     if not self.graph:
    #         return
    #     logging.info("Building routing graph...")
    #     for node in self.config.get('nodes', []):
    #         tag = node.get('tag')
    #         if tag:
    #             self.graph.add_node(tag)
    #     # Note: Edges are dynamic based on processor output.
    #     # A static graph representation would require knowing all possible
    #     # output tags for each processor, which isn't explicitly in this config.
    #     # For visualization, you could add edges as lines are processed,
    #     # or if processors declared their possible outputs.
    #     logging.info("Routing graph nodes added.")

    def add_line(self, tag: str, line: str):
        """Adds a line with an initial tag to the routing queue."""
        if tag not in self.processors and tag != 'end':
             logging.warning(f"Attempted to add line with unknown tag '{tag}'. Line: '{line}'. Discarding.")
             return

        logging.info(f"Adding line to queue with tag '{tag}': {line}")
        self.routing_queue.append((tag, line))
        self.active_lines.add(line) # Track the line

    def process_queue(self):
        """Processes items from the routing queue until it's empty."""
        logging.info("Starting queue processing.")
        processed_count = 0
        # A simple safeguard against infinite loops: limit the total number of processing steps.
        max_processing_steps = 1000
        current_steps = 0

        while self.routing_queue and current_steps < max_processing_steps:
            current_steps += 1

            # --- Added check here ---
            if not self.routing_queue:
                 logging.debug("Queue is empty, exiting loop.")
                 break # Should be caught by while condition, but added for safety

            try:
                # Pop the next item from the queue
                queue_item = self.routing_queue.popleft()
                # --- Added check here ---
                if queue_item is None:
                    logging.error(f"Queue returned None unexpectedly at step {current_steps}. Exiting.")
                    break # Exit if popleft returns None (should not happen with deque)

                current_tag, line_to_process = queue_item
                processed_count += 1
                logging.debug(f"Processing item {processed_count} (Step {current_steps}): Tag='{current_tag}', Line='{line_to_process}'")

            except IndexError:
                logging.debug("Queue became empty during popleft. Exiting loop.")
                break # Queue is empty, finish processing

            if current_tag == 'end':
                logging.info(f"Line reached 'end' state: {line_to_process}")
                if 'end' in self.processors:
                     # Wrap the single line in an iterator for the processor
                    try:
                        end_processor_output = self.processors['end'].process(iter([(current_tag, line_to_process)]))
                        # --- Added check here ---
                        if end_processor_output is not None:
                             # Consume the iterator even if it's empty to ensure process method runs
                             list(end_processor_output)
                        else:
                             logging.warning(f"End processor for tag 'end' returned None instead of an iterator.")
                    except Exception as e:
                         logging.error(f"Error running end processor for line '{line_to_process}': {e}")

                if line_to_process in self.active_lines:
                    self.active_lines.remove(line_to_process)
                continue # This line is done, move to the next in the queue

            if current_tag not in self.processors:
                logging.error(f"No processor found for tag '{current_tag}'. Discarding line: {line_to_process}")
                if line_to_process in self.active_lines:
                    self.active_lines.remove(line_to_process)
                continue

            processor = self.processors[current_tag]

            try:
                # Pass the line to the processor. Wrap the single line in an iterator.
                # The processor yields (next_tag, processed_line) tuples.
                processor_output_iterator = processor.process(iter([(current_tag, line_to_process)]))

                # --- Added check here ---
                if processor_output_iterator is None:
                    logging.warning(f"Processor for '{current_tag}' returned None instead of an iterator for line '{line_to_process}'. Discarding output.")
                    continue # Discard if processor returns None

                # Convert the iterator to a list to process all emitted items
                output_lines = list(processor_output_iterator)

                for next_tag, processed_line in output_lines:
                    if next_tag not in self.processors and next_tag != 'end':
                        logging.warning(f"Processor for '{current_tag}' emitted unknown tag '{next_tag}' for line: {processed_line}. Discarding.")
                        continue

                    logging.debug(f"Processor for '{current_tag}' emitted tag '{next_tag}' for line: {processed_line}")
                    self.routing_queue.append((next_tag, processed_line))

            except Exception as e:
                logging.error(f"Error processing line '{line_to_process}' with tag '{current_tag}' by processor {type(processor).__name__}: {e}")
                if line_to_process in self.active_lines:
                    self.active_lines.remove(line_line_to_process) # type: ignore # Corrected typo here
                    # Corrected typo above: should be line_to_process
                    if line_to_process in self.active_lines:
                        self.active_lines.remove(line_to_process)

        if current_steps >= max_processing_steps:
            logging.warning(f"Max processing steps ({max_processing_steps}) reached. Potential infinite loop or very long process.")
            logging.warning(f"Remaining items in queue: {len(self.routing_queue)}")

        logging.info("Queue processing finished.")
        if self.active_lines:
            logging.warning(f"Processing finished, but {len(self.active_lines)} lines did not reach the 'end' state.")

    # Optional networkx visualization (uncomment if networkx is installed)
    # def visualize_graph(self, filename="routing_graph.png"):
    #     """Visualizes the routing graph (requires networkx and matplotlib)."""
    #     if not self.graph:
    #         logging.warning("Graph visualization disabled (networkx not installed).")
    #         return
    #     try:
    #         import matplotlib.pyplot as plt
    #         logging.info(f"Attempting to visualize graph to {filename}")
    #         pos = nx.spring_layout(self.graph) # or other layout algorithms
    #         nx.draw(self.graph, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, arrows=True)
    #         plt.title("Routing Engine Graph")
    #         plt.savefig(filename)
    #         logging.info(f"Graph saved to {filename}")
    #     except ImportError:
    #         logging.warning("matplotlib not installed.")
    #     except Exception as e:
    #         logging.error(f"Error visualizing graph: {e}")
