# router.py

import yaml
import importlib
import logging
import time
import threading
from collections import deque, Counter
from typing import Dict, Any, Tuple, Iterator, List, Deque

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define a type alias for the data tuple flowing through the engine
ProcessingItem = Tuple[str, str, List[str]] # (tag, line, trace)

class RoutingEngine:
    """
    The core state-based routing engine.
    Manages processors, the routing queue, state transitions, metrics, and tracing.
    """
    def __init__(self, config_path: str, enable_tracing: bool = False):
        """
        Initializes the RoutingEngine by loading configuration and processors,
        setting up metrics and tracing.

        Args:
            config_path: Path to the configuration file (e.g., 'config/config.yaml').
            enable_tracing: Boolean flag to enable/disable line tracing.
        """
        self.config = self._load_config(config_path)
        self.processors = self._load_processors(self.config)
        self.routing_queue: Deque[ProcessingItem] = deque()
        self.active_lines = set() # Keep track of lines currently being processed

        self.enable_tracing = enable_tracing
        self.trace_history: Deque[Tuple[str, List[str]]] = deque(maxlen=1000) # Store last 1000 traces
        self.error_history: Deque[Tuple[str, str, str]] = deque(maxlen=100) # Store last 100 errors (processor, message, line)

        # Metrics storage - thread-safe
        self.metrics = {
            tag: {
                'received_count': 0,
                'emitted_count': 0,
                'processing_time_total': 0.0,
                'error_count': 0
            } for tag in self.processors
        }
        # Add 'end' tag to metrics for received count and processing time
        if 'end' not in self.metrics:
             self.metrics['end'] = {
                'received_count': 0,
                'emitted_count': 0, # End state doesn't emit
                'processing_time_total': 0.0,
                'error_count': 0
            }

        self._metrics_lock = threading.Lock()
        self._trace_lock = threading.Lock()
        self._error_lock = threading.Lock()
        self._active_lines_lock = threading.Lock()


    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Loads the routing configuration from a YAML file."""
        logging.info(f"Loading configuration from {config_path}")
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logging.info("Configuration loaded successfully.")
            return config
        except FileNotFoundError:
            logging.error(f"Configuration file not found: {config_path}")
            raise
        except yaml.YAMLError as e:
            logging.error(f"Error parsing configuration file {config_path}: {e}")
            raise

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

    def add_line(self, tag: str, line: str):
        """Adds a line with an initial tag and an empty trace to the routing queue."""
        if tag not in self.processors and tag != 'end':
             logging.warning(f"Attempted to add line with unknown initial tag '{tag}'. Line: '{line}'. Discarding.")
             return

        logging.debug(f"Adding line to queue with tag '{tag}': {line}")
        initial_trace: List[str] = [] if self.enable_tracing else [] # Initialize trace if tracing is enabled
        self.routing_queue.append((tag, line, initial_trace))
        with self._active_lines_lock:
             self.active_lines.add(line) # Track the line

        # Increment received count for the initial tag
        if tag in self.metrics:
             with self._metrics_lock:
                  self.metrics[tag]['received_count'] += 1


    def process_queue(self):
        """Processes items from the routing queue until it's empty."""
        logging.info("Starting queue processing.")
        processed_count = 0
        # A simple safeguard against infinite loops: limit the total number of processing steps.
        max_processing_steps = 10000 # Increased limit for more complex flows
        current_steps = 0

        while self.routing_queue and current_steps < max_processing_steps:
            current_steps += 1

            try:
                # Pop the next item from the queue
                queue_item: ProcessingItem = self.routing_queue.popleft()

                # --- Added check here ---
                if queue_item is None or not isinstance(queue_item, tuple) or len(queue_item) != 3:
                    logging.error(f"Queue returned invalid item unexpectedly at step {current_steps}: {queue_item}. Exiting.")
                    break # Exit if popleft returns None or invalid format

                current_tag, line_to_process, trace = queue_item
                processed_count += 1
                logging.debug(f"Processing item {processed_count} (Step {current_steps}): Tag='{current_tag}', Line='{line_to_process}'")

            except IndexError:
                logging.debug("Queue became empty during popleft. Exiting loop.")
                break # Queue is empty, finish processing
            except Exception as e:
                 logging.error(f"Unexpected error popping from queue at step {current_steps}: {e}", exc_info=True)
                 break # Exit on unexpected queue error


            if current_tag == 'end':
                logging.debug(f"Line reached 'end' state: {line_to_process}")
                # Increment received count for 'end' tag
                if 'end' in self.metrics:
                     with self._metrics_lock:
                          self.metrics['end']['received_count'] += 1

                start_time = time.time()
                try:
                    if 'end' in self.processors:
                         # Pass the line to the end processor. Wrap in an iterator.
                         # The end processor is expected to yield nothing.
                         end_processor_output = self.processors['end'].process(iter([(current_tag, line_to_process, trace)]))
                         # Consume the iterator to ensure the process method runs
                         list(end_processor_output)
                    else:
                         # If no 'end' processor is defined, just log and remove.
                         print(f"FINAL OUTPUT [Tag: {current_tag}]: {line_to_process}")
                         logging.debug(f"No 'end' processor defined, printed line. Trace: {trace}")

                    # Record trace if tracing is enabled
                    if self.enable_tracing:
                         with self._trace_lock:
                              self.trace_history.append((line_to_process, trace + [current_tag])) # Append final tag to trace

                except Exception as e:
                     logging.error(f"Error running end processor for line '{line_to_process}': {e}", exc_info=True)
                     with self._error_lock:
                          self.error_history.append(('end', str(e), line_to_process))
                     with self._metrics_lock:
                          self.metrics['end']['error_count'] += 1
                finally:
                     end_time = time.time()
                     with self._metrics_lock:
                          self.metrics['end']['processing_time_total'] += (end_time - start_time)

                # Remove the line from active tracking as it has finished its journey
                with self._active_lines_lock:
                    if line_to_process in self.active_lines:
                        self.active_lines.remove(line_to_process)
                continue # This line is done, move to the next in the queue


            if current_tag not in self.processors:
                logging.error(f"No processor found for tag '{current_tag}'. Discarding line: {line_to_process}. Trace: {trace}")
                with self._error_lock:
                     self.error_history.append(('router', f"No processor for tag '{current_tag}'", line_to_process))
                # If a tag doesn't have a corresponding processor, the line is dropped.
                with self._active_lines_lock:
                    if line_to_process in self.active_lines:
                        self.active_lines.remove(line_to_process)
                continue

            processor = self.processors[current_tag]

            # Increment received count for the current tag
            if current_tag in self.metrics:
                 with self._metrics_lock:
                      self.metrics[current_tag]['received_count'] += 1

            start_time = time.time()
            try:
                # Pass the line to the processor. Wrap the single item in an iterator.
                # The processor yields (next_tag, processed_line, updated_trace) tuples.
                processor_output_iterator = processor.process(iter([(current_tag, line_to_process, trace)]))

                # --- Added check here ---
                if processor_output_iterator is None:
                    logging.warning(f"Processor for '{current_tag}' returned None instead of an iterator for line '{line_to_process}'. Discarding output. Trace: {trace}")
                    with self._error_lock:
                         self.error_history.append((current_tag, "Processor returned None", line_to_process))
                    with self._metrics_lock:
                         self.metrics[current_tag]['error_count'] += 1
                    continue # Discard if processor returns None

                emitted_count_for_this_line = 0
                # Convert the iterator to a list to process all emitted items
                output_items: List[ProcessingItem] = list(processor_output_iterator)

                for next_tag, processed_line, updated_trace in output_items:
                    emitted_count_for_this_line += 1
                    if next_tag not in self.processors and next_tag != 'end':
                        logging.warning(f"Processor for '{current_tag}' emitted unknown tag '{next_tag}' for line: {processed_line}. Discarding. Trace: {updated_trace}")
                        with self._error_lock:
                             self.error_history.append((current_tag, f"Emitted unknown tag '{next_tag}'", processed_line))
                        with self._metrics_lock:
                            self.metrics[current_tag]['error_count'] += 1 # Count as an error related to emission
                        continue # Discard lines with unknown next tags

                    logging.debug(f"Processor for '{current_tag}' emitted tag '{next_tag}' for line: {processed_line}. Trace: {updated_trace}")
                    # Add the processed line with its new tag and updated trace back to the queue
                    self.routing_queue.append((next_tag, processed_line, updated_trace))

                # Increment emitted count for the current tag
                if current_tag in self.metrics:
                     with self._metrics_lock:
                          self.metrics[current_tag]['emitted_count'] += emitted_count_for_this_line


            except Exception as e:
                logging.error(f"Error processing line '{line_to_process}' with tag '{current_tag}' by processor {type(processor).__name__}: {e}", exc_info=True)
                # Handle processor errors - maybe add to an error queue or discard.
                with self._error_lock:
                     self.error_history.append((current_tag, str(e), line_to_process))
                with self._metrics_lock:
                     self.metrics[current_tag]['error_count'] += 1
                # For now, we just log and discard the line.
                with self._active_lines_lock:
                    if line_to_process in self.active_lines:
                        self.active_lines.remove(line_to_process)
            finally:
                 end_time = time.time()
                 # Update processing time for the current tag
                 if current_tag in self.metrics:
                      with self._metrics_lock:
                           self.metrics[current_tag]['processing_time_total'] += (end_time - start_time)


        if current_steps >= max_processing_steps:
            logging.warning(f"Max processing steps ({max_processing_steps}) reached. Potential infinite loop or very long process.")
            logging.warning(f"Remaining items in queue: {len(self.routing_queue)}")
            # You might want to log the remaining items or handle them differently here.

        logging.info("Queue processing finished.")
        with self._active_lines_lock:
            if self.active_lines:
                logging.warning(f"Processing finished, but {len(self.active_lines)} lines did not reach the 'end' state.")
                # You might want to inspect or report on these lines.

    def get_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Returns a snapshot of the current metrics."""
        with self._metrics_lock:
            # Return a copy to avoid external modification of internal state
            return dict(self.metrics)

    def get_traces(self) -> List[Dict[str, Any]]:
        """Returns a list of recent traces."""
        if not self.enable_tracing:
             return [{"message": "Tracing is not enabled."}]

        with self._trace_lock:
            # Return a list of dictionaries for easier JSON serialization
            return [{"line": line, "trace": trace} for line, trace in list(self.trace_history)]

    def get_errors(self) -> List[Dict[str, Any]]:
        """Returns a list of recent errors."""
        with self._error_lock:
            # Return a list of dictionaries for easier JSON serialization
            return [{"processor": proc, "message": msg, "line": line} for proc, msg, line in list(self.error_history)]


    # Optional networkx visualization (uncomment if networkx is installed)
    # This visualization is static based on the config, not the dynamic flow.
    # def visualize_graph(self, filename="routing_graph.png"):
    #     """Visualizes the routing graph (requires networkx and matplotlib)."""
    #     try:
    #         import networkx as nx
    #         import matplotlib.pyplot as plt
    #         logging.info(f"Attempting to visualize graph to {filename}")

    #         graph = nx.DiGraph()
    #         nodes = {node['tag']: node.get('type', 'Unknown') for node in self.config.get('nodes', [])}

    #         for tag, type_str in nodes.items():
    #             graph.add_node(tag, type=type_str)

    #         # To draw edges, we would need processors to declare their possible output tags.
    #         # Since they don't in this version, we can only draw nodes.
    #         # A more advanced version could dynamically add edges as lines flow.

    #         pos = nx.spring_layout(graph) # or other layout algorithms
    #         node_labels = {tag: tag for tag in graph.nodes()}
    #         # Edge labels would require knowing the conditions for transitions

    #         nx.draw(graph, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, arrows=True)
    #         plt.title("Routing Engine Graph (Configured Nodes)")
    #         plt.savefig(filename)
    #         logging.info(f"Graph saved to {filename}")
    #     except ImportError:
    #         logging.warning("networkx or matplotlib not installed. Graph visualization disabled.")
    #     except Exception as e:
    #         logging.error(f"Error visualizing graph: {e}", exc_info=True)

