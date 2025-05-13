# router.py

import yaml
import importlib
import logging
import time
import threading
import os
import shutil
from collections import deque, Counter
from typing import Dict, Any, Tuple, Iterator, List, Deque

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define a type alias for the data tuple flowing through the engine
# Added file_path to the tuple
ProcessingItem = Tuple[str, str, List[str], str] # (tag, line, trace, file_path)

class RoutingEngine:
    """
    The core state-based routing engine.
    Manages processors, the routing queue, state transitions, metrics, tracing,
    and file processing lifecycle.
    """
    def __init__(self, config_path: str, watch_dir: str, enable_tracing: bool = False):
        """
        Initializes the RoutingEngine by loading configuration and processors,
        setting up metrics, tracing, and file monitoring paths.

        Args:
            config_path: Path to the configuration file (e.g., 'config/config.yaml').
            watch_dir: The base directory to monitor for files.
            enable_tracing: Boolean flag to enable/disable line tracing.
        """
        self.config = self._load_config(config_path)
        self.processors = self._load_processors(self.config)

        # File monitoring directories
        self.watch_dir = watch_dir
        self.unprocessed_dir = os.path.join(watch_dir, 'unprocessed')
        self.underprocess_dir = os.path.join(watch_dir, 'underprocess')
        self.processed_dir = os.path.join(watch_dir, 'processed')

        self.routing_queue: Deque[ProcessingItem] = deque()
        # Track lines per file to know when a file is fully processed
        self._lines_per_file: Dict[str, int] = {}
        self._lines_per_file_lock = threading.Lock()

        # Track active lines (less critical with file tracking, but kept for consistency)
        self._active_lines = set()
        self._active_lines_lock = threading.Lock()

        self.enable_tracing = enable_tracing
        self.trace_history: Deque[Tuple[str, List[str], str]] = deque(maxlen=1000) # Store last 1000 traces (line, trace, file_path)
        self.error_history: Deque[Tuple[str, str, str, str]] = deque(maxlen=100) # Store last 100 errors (processor, message, line, file_path)

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

        # File state metrics
        self._file_counts: Dict[str, int] = {
            'unprocessed': 0,
            'underprocess': 0,
            'processed': 0
        }
        self._current_processing_file: Optional[str] = None
        self._recently_processed_files: Deque[Tuple[str, float]] = deque(maxlen=50) # Store (file_name, timestamp)
        self._file_state_lock = threading.Lock()

        self._metrics_lock = threading.Lock()
        self._trace_lock = threading.Lock()
        self._error_lock = threading.Lock()


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

    def add_line(self, tag: str, line: str, file_path: str):
        """Adds a line with an initial tag, empty trace, and file_path to the routing queue."""
        # Ensure the tag is valid for initial entry or subsequent routing
        if tag not in self.processors and tag != 'end':
             logging.warning(f"Attempted to add line with unknown tag '{tag}' from file '{file_path}'. Line: '{line}'. Discarding.")
             with self._error_lock:
                  self.error_history.append(('router', f"Attempted to add line with unknown tag '{tag}'", line, file_path))
             return

        logging.debug(f"Adding line to queue with tag '{tag}' from file '{file_path}': {line}")
        initial_trace: List[str] = [] if self.enable_tracing else [] # Initialize trace if tracing is enabled
        self.routing_queue.append((tag, line, initial_trace, file_path))

        # Increment received count for the initial tag
        if tag in self.metrics:
             with self._metrics_lock:
                  self.metrics[tag]['received_count'] += 1

        # Track the line count for this file
        with self._lines_per_file_lock:
             self._lines_per_file[file_path] = self._lines_per_file.get(file_path, 0) + 1

        with self._active_lines_lock:
             self._active_lines.add((line, file_path)) # Track the line and its file


    def process_queue_continuously(self):
        """Processes items from the routing queue in a continuous loop."""
        logging.info("Starting continuous queue processing.")
        processed_count = 0
        # A simple safeguard against infinite loops: limit the total number of processing steps per queue item.
        # A more sophisticated approach would track line history or use graph cycle detection.
        max_processing_steps_per_item = 100 # Limit steps a single line can take
        current_steps = 0 # Total steps across all lines

        while True: # Run continuously
            if not self.routing_queue:
                logging.debug("Queue is empty. Sleeping...")
                time.sleep(1) # Sleep when queue is empty to avoid busy-waiting
                continue # Check queue again after sleeping

            # Process items from the queue
            # Limit processing per loop iteration to prevent one file from starving others
            items_to_process = min(len(self.routing_queue), 100) # Process up to 100 items at once

            for _ in range(items_to_process):
                current_steps += 1

                try:
                    # Pop the next item from the queue
                    queue_item: ProcessingItem = self.routing_queue.popleft()

                    # --- Validation check ---
                    if queue_item is None or not isinstance(queue_item, tuple) or len(queue_item) != 4:
                        logging.error(f"Queue returned invalid item unexpectedly: {queue_item}. Skipping.")
                        with self._error_lock:
                             self.error_history.append(('router', f"Invalid item in queue: {queue_item}", "N/A", "N/A"))
                        continue

                    current_tag, line_to_process, trace, file_path = queue_item
                    processed_count += 1
                    logging.debug(f"Processing item {processed_count} (Total Step {current_steps}): Tag='{current_tag}', Line='{line_to_process}' from file '{file_path}'")

                except IndexError:
                    logging.debug("Queue became empty during iteration.")
                    break # Queue is empty, exit inner loop and check outer loop condition
                except Exception as e:
                     logging.error(f"Unexpected error popping from queue: {e}", exc_info=True)
                     with self._error_lock:
                          self.error_history.append(('router', f"Error popping from queue: {e}", "N/A", "N/A"))
                     continue # Skip to next iteration


                # Update current processing file state for dashboard
                with self._file_state_lock:
                     self._current_processing_file = file_path


                if current_tag == 'end':
                    logging.debug(f"Line reached 'end' state: {line_to_process} from file '{file_path}'")
                    # Increment received count for 'end' tag
                    if 'end' in self.metrics:
                         with self._metrics_lock:
                              self.metrics['end']['received_count'] += 1

                    start_time = time.time()
                    try:
                        if 'end' in self.processors:
                             # Pass the line to the end processor. Wrap in an iterator.
                             # The end processor is expected to yield nothing.
                             end_processor_output = self.processors['end'].process(iter([(current_tag, line_to_process, trace, file_path)]))
                             # Consume the iterator to ensure the process method runs
                             list(end_processor_output)
                        else:
                             # If no 'end' processor is defined, just log and remove.
                             print(f"FINAL OUTPUT [Tag: {current_tag}] (File: {file_path}): {line_to_process}")
                             logging.debug(f"No 'end' processor defined, printed line. Trace: {trace}. File: {file_path}")

                        # Record trace if tracing is enabled
                        if self.enable_tracing:
                             with self._trace_lock:
                                  self.trace_history.append((line_to_process, trace + [current_tag], file_path)) # Append final tag to trace

                    except Exception as e:
                         logging.error(f"Error running end processor for line '{line_to_process}' from file '{file_path}': {e}", exc_info=True)
                         with self._error_lock:
                              self.error_history.append(('end', str(e), line_to_process, file_path))
                         with self._metrics_lock:
                              self.metrics['end']['error_count'] += 1
                    finally:
                         end_time = time.time()
                         with self._metrics_lock:
                              self.metrics['end']['processing_time_total'] += (end_time - start_time)

                    # Decrement line count for the file and check if processing is complete
                    self._decrement_line_count(file_path, line_to_process)
                    continue # This line is done, move to the next in the queue


                if current_tag not in self.processors:
                    logging.error(f"No processor found for tag '{current_tag}'. Discarding line: {line_to_process} from file '{file_path}'. Trace: {trace}")
                    with self._error_lock:
                         self.error_history.append(('router', f"No processor for tag '{current_tag}'", line_to_process, file_path))
                    # If a tag doesn't have a corresponding processor, the line is dropped.
                    # Decrement line count for the file as this line is discarded
                    self._decrement_line_count(file_path, line_to_process)
                    continue

                processor = self.processors[current_tag]

                # Increment received count for the current tag
                if current_tag in self.metrics:
                     with self._metrics_lock:
                          self.metrics[current_tag]['received_count'] += 1

                start_time = time.time()
                try:
                    # Pass the line to the processor. Wrap the single item in an iterator.
                    # The processor yields (next_tag, processed_line, updated_trace, file_path) tuples.
                    processor_output_iterator = processor.process(iter([(current_tag, line_to_process, trace, file_path)]))
                    # --- Validation check ---
                    if processor_output_iterator is None:
                        logging.warning(f"Processor for '{current_tag}' returned None instead of an iterator for line '{line_to_process}' from file '{file_path}'. Discarding output. Trace: {trace}")
                        with self._error_lock:
                             self.error_history.append((current_tag, "Processor returned None", line_to_process, file_path))
                        with self._metrics_lock:
                             self.metrics[current_tag]['error_count'] += 1
                        # This line is effectively discarded, so decrement line count for the file
                        self._decrement_line_count(file_path, line_to_process)
                        continue # Discard if processor returns None

                    emitted_count_for_this_line = 0
                    output_items: List[ProcessingItem] = list(processor_output_iterator)

                    # If a processor yields *any* output for a line, we assume it's still active.
                    # If it yields *no* output, the line is considered discarded by that processor.
                    if not output_items:
                         logging.debug(f"Processor for '{current_tag}' discarded line: {line_to_process} from file '{file_path}'. Trace: {trace}")
                         # This line is discarded, so decrement line count for the file
                         self._decrement_line_count(file_path, line_to_process)

                    for next_tag, processed_line, updated_trace, emitted_file_path in output_items:
                        emitted_count_for_this_line += 1
                        # Ensure the file_path is consistent (processors shouldn't change it)
                        if emitted_file_path != file_path:
                             logging.warning(f"Processor for '{current_tag}' changed file_path from '{file_path}' to '{emitted_file_path}' for line '{processed_line}'. Using original file_path.")
                             emitted_file_path = file_path # Use original file path

                        if next_tag not in self.processors and next_tag != 'end':
                            logging.warning(f"Processor for '{current_tag}' emitted unknown tag '{next_tag}' for line: {processed_line} from file '{emitted_file_path}'. Discarding. Trace: {updated_trace}")
                            with self._error_lock:
                                 self.error_history.append((current_tag, f"Emitted unknown tag '{next_tag}'", processed_line, emitted_file_path))
                            with self._metrics_lock:
                                self.metrics[current_tag]['error_count'] += 1 # Count as an error related to emission
                            # This emitted line is discarded, so decrement line count for the file
                            self._decrement_line_count(emitted_file_path, processed_line) # Use processed_line for active tracking
                            continue # Discard lines with unknown next tags

                        logging.debug(f"Processor for '{current_tag}' emitted tag '{next_tag}' for line: {processed_line} from file '{emitted_file_path}'. Trace: {updated_trace}")
                        # Add the processed line with its new tag and updated trace back to the queue
                        self.routing_queue.append((next_tag, processed_line, updated_trace, emitted_file_path))

                        # If a line is emitted, it's still active, so we don't decrement the line count here.
                        # The decrement happens only when a line is *not* emitted or reaches 'end'.


                    # Increment emitted count for the current tag
                    if current_tag in self.metrics:
                         with self._metrics_lock:
                              self.metrics[current_tag]['emitted_count'] += emitted_count_for_this_line


                except Exception as e:
                    logging.error(f"Error processing line '{line_to_process}' with tag '{current_tag}' by processor {type(processor).__name__} from file '{file_path}': {e}", exc_info=True)
                    # Handle processor errors
                    with self._error_lock:
                         self.error_history.append((current_tag, str(e), line_to_process, file_path))
                    with self._metrics_lock:
                         self.metrics[current_tag]['error_count'] += 1
                    # This line caused an error and is effectively discarded, so decrement line count for the file
                    self._decrement_line_count(file_path, line_to_process)
                finally:
                     end_time = time.time()
                     # Update processing time for the current tag
                     if current_tag in self.metrics:
                          with self._metrics_lock:
                               self.metrics[current_tag]['processing_time_total'] += (end_time - start_time)

            # After processing a batch of items, update the current file state if the queue is now empty
            if not self.routing_queue:
                 with self._file_state_lock:
                      self._current_processing_file = None # No file is actively being processed right now


    def _decrement_line_count(self, file_path: str, line_content: str):
        """Decrements the active line count for a file and moves the file if count reaches zero."""
        with self._lines_per_file_lock:
            if file_path in self._lines_per_file:
                self._lines_per_file[file_path] -= 1
                logging.debug(f"Decremented line count for '{file_path}'. Remaining: {self._lines_per_file[file_path]}")

                if self._lines_per_file[file_path] <= 0:
                    # All lines from this file have been processed or discarded
                    logging.info(f"All lines from file '{file_path}' processed. Moving to 'processed'.")
                    del self._lines_per_file[file_path] # Remove file from tracking

                    # Move the file from underprocess to processed
                    src_path = os.path.join(self.underprocess_dir, os.path.basename(file_path))
                    dest_path = os.path.join(self.processed_dir, os.path.basename(file_path))
                    try:
                        shutil.move(src_path, dest_path)
                        logging.info(f"Moved '{src_path}' to '{dest_path}'.")
                        # Update file counts and recently processed files
                        with self._file_state_lock:
                             self._file_counts['underprocess'] -= 1
                             self._file_counts['processed'] += 1
                             self._recently_processed_files.append((os.path.basename(file_path), time.time()))
                    except FileNotFoundError:
                         logging.warning(f"File '{src_path}' not found during move to 'processed'. Already moved or deleted?")
                         with self._file_state_lock:
                              self._file_counts['underprocess'] -= 1 # Assume it was moved
                    except Exception as e:
                        logging.error(f"Error moving file '{src_path}' to '{dest_path}': {e}", exc_info=True)
                        with self._error_lock:
                             self.error_history.append(('router', f"Error moving file to processed: {e}", "N/A", file_path))

        # Remove the line from active tracking
        with self._active_lines_lock:
             # Need to find the specific line and file_path tuple
             item_to_remove = (line_content, file_path)
             if item_to_remove in self._active_lines:
                  self._active_lines.remove(item_to_remove)
             # Note: Tracking active lines this way is complex with duplicate lines.
             # Tracking lines per file is a more robust indicator of file completion.


    def get_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Returns a snapshot of the current processor metrics."""
        with self._metrics_lock:
            # Return a copy to avoid external modification of internal state
            return dict(self.metrics)

    def get_traces(self) -> List[Dict[str, Any]]:
        """Returns a list of recent traces."""
        if not self.enable_tracing:
             return [{"message": "Tracing is not enabled."}]

        with self._trace_lock:
            # Return a list of dictionaries for easier JSON serialization
            return [{"line": line, "trace": trace, "file": file_path} for line, trace, file_path in list(self.trace_history)]

    def get_errors(self) -> List[Dict[str, Any]]:
        """Returns a list of recent errors."""
        with self._error_lock:
            # Return a list of dictionaries for easier JSON serialization
            return [{"processor": proc, "message": msg, "line": line, "file": file_path} for proc, msg, line, file_path in list(self.error_history)]

    def get_file_state(self) -> Dict[str, Any]:
        """Returns a snapshot of the current file processing state."""
        with self._file_state_lock:
             with self._lines_per_file_lock: # Also lock lines_per_file for consistency
                  return {
                      'file_counts': dict(self._file_counts),
                      'under_process_lines': dict(self._lines_per_file), # Show lines remaining per file under process
                      'current_processing_file': self._current_processing_file,
                      'recently_processed_files': list(self._recently_processed_files)
                  }

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

