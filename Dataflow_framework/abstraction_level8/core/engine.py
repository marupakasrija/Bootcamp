# This is abstraction-level-8/core/engine.py
# Contains the State Transition execution engine for Level 8 (with Observability).

import sys # Needed for sys.stderr
import time # For timing
from typing import Iterator, List, Dict, Tuple, Any, Set, Optional
from collections import defaultdict
import queue # Using queue for conceptual flow, though single-threaded here
import networkx as nx # For graph representation, validation, and cycle detection
import uuid # For generating unique line IDs
import os # For path manipulation

# Import types and utilities using relative imports within the core package
from ..types import TracedLine, StateProcessor, StateProcessorFn, StateSystemConfig, StateConfig, ProcessorDefinitionConfig, START_TAG, END_TAG, ObservabilityData, ProcessorMetrics, ErrorData, LineTrace
from .utils import get_state_processor_fn, load_processor_definition # Import helpers

# Define a maximum number of times a single line can visit states to guard against infinite loops
MAX_STATE_VISITS_PER_LINE = 100

class StateTransitionEngine:
    def __init__(self, state_config: StateSystemConfig, observability_data: ObservabilityData, enable_tracing: bool = False):
        # Map tag (state) to processor function/instance
        self.states: Dict[str, StateProcessorFn] = {}
        # Store original state configurations
        self._state_configs: StateConfig = {}

        # Observability data shared with the dashboard
        self.observability_data = observability_data
        self.enable_tracing = enable_tracing

        self._load_config(state_config)

        # Build and validate the state graph (using networkx)
        self._graph = self._build_graph()
        self._validate_graph()


    def _load_config(self, state_config: StateSystemConfig):
        """Loads state processors from config."""
        state_definitions: StateConfig = state_config.get('states', {})
        self._state_configs = state_definitions

        # Load and instantiate processors for each defined state
        for tag, processor_def_config in state_definitions.items():
            if not isinstance(processor_def_config, dict):
                 print(f"Skipping invalid state config for tag '{tag}': {processor_def_config} (must be a dictionary)", file=sys.stderr)
                 continue

            processor_path = processor_def_config.get('type')
            processor_config = {k: v for k, v in processor_def_config.items() if k != 'type'}

            if not processor_path:
                 print(f"Skipping state '{tag}' (missing processor 'type'): {processor_def_config}", file=sys.stderr)
                 continue

            if tag in self.states:
                 print(f"Warning: Duplicate state tag '{tag}' found in config. Skipping.", file=sys.stderr)
                 continue

            try:
                # Dynamically load the processor definition (class or function)
                # Use the helper from utils.py
                processor_definition = load_processor_definition(processor_path)
                # Get the state processor function (handle classes/functions, passes the tag and config)
                state_processor_fn = get_state_processor_fn(processor_definition, tag=tag, config=processor_config)
                self.states[tag] = state_processor_fn
                print(f"Loaded state '{tag}' with processor '{processor_path}'", file=sys.stderr)

                # Initialize metrics for this state if not already present (defaultdict handles this, but explicit is clear)
                if tag not in self.observability_data.metrics:
                     self.observability_data.metrics[tag] = ProcessorMetrics()

            except Exception as e:
                print(f"Error loading or instantiating processor for state '{tag}' ({processor_path}): {e}", file=sys.stderr)
                # Add error to observability data (no line_id/content at this stage)
                self.observability_data.add_error(ErrorData(time.time(), tag, f"Initialization Error: {e}", "N/A", "N/A", file_name="Configuration Loading"))
                raise # Fail fast if a processor can't be loaded/instantiated

        # Ensure START and END states are defined
        if START_TAG not in self.states:
             raise ValueError(f"Config must include a state defined for the '{START_TAG}' tag.")
        if END_TAG not in self.states:
             # The END state processor is crucial for collecting output.
             # If not explicitly defined, we could potentially use a default one.
             # For now, let's make it required.
             raise ValueError(f"Config must include a state defined for the '{END_TAG}' tag.")

        # Initialize metrics for the special END_TAG if not explicitly in config
        if END_TAG not in self.observability_data.metrics:
             self.observability_data.metrics[END_TAG] = ProcessorMetrics()


    def _build_graph(self) -> nx.DiGraph:
       """Builds a networkx graph representing state transitions (based on defined states)."""
       G = nx.DiGraph()

       # Add nodes for all defined states
       for tag in self.states:
           G.add_node(tag)

       # Note: Edges are not statically defined in this state-based system,
       # they are determined dynamically by the tags emitted by processors.
       # A static graph here only shows the *possible* states/nodes.
       # For visualization or static analysis of potential paths/cycles,
       # you would need to infer edges based on declared output tags from processors
       # or by analyzing the config rules if the 'taggers' explicitly list outputs.

       # For L8, we don't strictly *need* the graph for execution, but it's good
       # practice to build it for potential future validation/visualization.
       # Let's build a simple graph with nodes as states.

       return G # Return graph with just nodes (states)


    def _validate_graph(self):
       """Performs basic validation on the state graph."""
       # Check if START_TAG exists (already done in _load_config)
       # Check if END_TAG exists (already done in _load_config)

       # For L8, we won't do complex static cycle detection.
       # Execution-time loop guarding is implemented in `run`.

       print("Basic state graph validation complete (nodes checked).", file=sys.stderr)


    def run(self, initial_lines: Iterator[str], file_name: Optional[str] = None) -> Iterator[str]:
        """
        Runs the State Transition engine for a single set of initial lines (e.g., from one file).

        Args:
            initial_lines: An iterator yielding the initial input lines (will be tagged 'start' and given IDs).
            file_name: Optional name of the file being processed, for logging/observability.

        Yields:
            Processed lines that reach the 'end' state.
        """
        print(f"Running State Transition engine for file: {file_name or 'stdin'}", file=sys.stderr)

        # Use queues for inter-state communication within this single file's processing.
        # Each state (tag) gets an input queue.
        state_input_queues: Dict[str, queue.Queue[TracedLine]] = {}
        for tag in self.states:
             state_input_queues[tag] = queue.Queue()

        # Queue to collect final output lines for this file
        final_output_queue: queue.Queue[str] = queue.Queue()

        # --- Initial Injection ---
        # All initial lines enter the system tagged with START_TAG and a unique ID.
        start_tag = START_TAG
        if start_tag not in self.states:
             # This should be caught by _load_config, but defensive
             raise ValueError(f"Engine requires a state defined for the '{START_TAG}' tag.")

        # Feed initial lines into the 'start' state's input queue
        # print(f"DEBUG: Injecting initial lines into '{START_TAG}' state for file {file_name or 'stdin'}...", file=sys.stderr) # Optional debug)
        for line in initial_lines:
             # Generate a unique ID for each line.
             # In a real system, this ID should be persistent across runs (e.g., hash + file info).
             line_id = str(uuid.uuid4()) # Use UUID for robustness in this run
             # Create the initial TracedLine tuple
             traced_line: TracedLine = (line_id, START_TAG, line.rstrip('\r\n'), []) # Start with empty history
             state_input_queues[START_TAG].put(traced_line)


        # Keep track of states that currently have input
        states_with_input: Set[str] = {START_TAG} if not state_input_queues[START_TAG].empty() else set()

        # Safety break for potential infinite loops or very large inputs
        total_lines_processed_count = 0 # Count total (id, tag, line, history) tuples processed
        max_total_processed = 1000000 # Arbitrary high limit per file

        # print("Starting state transition loop for file...", file=sys.stderr) # Informative print)

        # The core processing loop
        # Continues as long as there are states with input
        while states_with_input and total_lines_processed_count < max_total_processed:

            # Get a copy of the set of states that had input at the start of this iteration
            current_states_to_process = list(states_with_input)
            states_with_input.clear() # Clear the set for the next round

            # Process each state that had input
            for current_tag in current_states_to_process:
                 if current_tag not in self.states:
                     # Should not happen if validation is correct, but defensive
                     print(f"Error: Attempted to process unknown state '{current_tag}' for file {file_name or 'stdin'}", file=sys.stderr)
                     # Add error to observability data
                     self.observability_data.add_error(ErrorData(time.time(), current_tag, f"Attempted to process unknown state", "N/A", "N/A", file_name=file_name))
                     continue

                 # Get all lines currently in this state's input queue
                 lines_for_state: List[TracedLine] = []
                 while not state_input_queues[current_tag].empty():
                     lines_for_state.append(state_input_queues[current_tag].get())

                 if not lines_for_state:
                     # This state's input queue might have been emptied by another process
                     # if this were multi-threaded, but in single-thread, this is defensive.
                     continue

                 processor_fn = self.states[current_tag]
                 # print(f"DEBUG: Processing lines in state '{current_tag}' ({len(lines_for_state)} lines) for file {file_name or 'stdin'}", file=sys.stderr) # Optional debug)

                 # --- Metrics: Start timing ---
                 start_time = time.time()
                 lines_received_count = len(lines_for_state)
                 lines_emitted_count = 0
                 errors_during_processing = 0

                 try:
                     # Run the processor on the iterator of lines for this state
                     processed_stream: Iterator[TracedLine] = processor_fn(iter(lines_for_state))

                     # Route the output of the processor
                     for next_line_tuple in processed_stream:
                         # Ensure the processor yielded a valid TracedLine tuple
                         if not isinstance(next_line_tuple, tuple) or len(next_line_tuple) != 4:
                             print(f"Warning: State '{current_tag}' processor for file {file_name or 'stdin'} yielded invalid output: {next_line_tuple}. Expected (id, tag, line, history). Dropping output.", file=sys.stderr)
                             errors_during_processing += 1 # Count as an error related to processor output format
                             # Add error to observability data
                             # Note: Cannot get line_id or content reliably from malformed output.
                             self.observability_data.add_error(ErrorData(time.time(), current_tag, f"Processor yielded invalid output format", "N/A", "N/A", file_name=file_name))
                             continue

                         line_id, next_tag, processed_line_content, history = next_line_tuple # Use 'history' from the tuple as the base

                         # --- Update history and check for loops ---
                         # Add the current state *before* checking for loops in the updated history
                         updated_history = history + [current_tag]

                         # Check the length of the history to detect potential loops
                         if len(updated_history) > MAX_STATE_VISITS_PER_LINE:
                             print(f"Warning: Line ID '{line_id}' from file {file_name or 'stdin'} exceeded max state visits ({MAX_STATE_VISITS_PER_LINE}). Possible infinite loop. Dropping line. History: {updated_history}", file=sys.stderr)
                             # Add trace with 'dropped_loop' status if tracing is enabled
                             if self.enable_tracing:
                                 self.observability_data.add_trace(LineTrace(line_id, processed_line_content, updated_history, status="dropped_loop", file_name=file_name))
                             errors_during_processing += 1 # Count loop as an error
                             # Add error to observability data
                             self.observability_data.add_error(ErrorData(time.time(), current_tag, f"Exceeded max state visits ({MAX_STATE_VISITS_PER_LINE})", line_id, processed_line_content, file_name=file_name))
                             continue # Skip routing this line

                         # Now that history is updated and loop checked, increment emitted count
                         lines_emitted_count += 1 # Count lines successfully emitted by this processor

                         # --- Routing ---
                         if next_tag == END_TAG:
                             # This line is done, put it in the final output queue
                             final_output_queue.put(processed_line_content)
                             # print(f"DEBUG: Line ID '{line_id}' from file {file_name or 'stdin'} reached END state: '{processed_line_content}'", file=sys.stderr) # Optional debug)
                             # Add trace with 'completed' status if tracing is enabled
                             if self.enable_tracing:
                                 # Add the final END state to the history for the trace
                                 final_history_for_trace = updated_history + [END_TAG]
                                 self.observability_data.add_trace(LineTrace(line_id, processed_line_content, final_history_for_trace, status="completed", file_name=file_name))

                         elif next_tag in self.states:
                             # Route to the next state by adding to its input queue
                             # Pass the *updated* history with the line
                             state_input_queues[next_tag].put((line_id, next_tag, processed_line_content, updated_history))
                             # Add the next state to the set of states that need processing
                             states_with_input.add(next_tag)
                             # print(f"DEBUG: Routed line ID '{line_id}' from '{current_tag}' to '{next_tag}' for file {file_name or 'stdin'}.", file=sys.stderr) # Optional debug)
                         else:
                             # Emitted tag does not correspond to a defined state (and is not END_TAG)
                             print(f"Warning: Emitted tag '{next_tag}' from state '{current_tag}' for line ID '{line_id}' from file {file_name or 'stdin'} does not match any defined state or '{END_TAG}'. Line dropped: '{processed_line_content}'", file=sys.stderr)
                             errors_during_processing += 1 # Count as a routing error
                             # Add trace with 'dropped_invalid_route' status if tracing is enabled
                             if self.enable_tracing:
                                 self.observability_data.add_trace(LineTrace(line_id, processed_line_content, updated_history + [f"DROPPED_INVALID_ROUTE:{next_tag}"], status="dropped_invalid_route", file_name=file_name))
                             # Add error to observability data
                             self.observability_data.add_error(ErrorData(time.time(), current_tag, f"Invalid emitted tag '{next_tag}'", line_id, processed_line_content, file_name=file_name))


                 except Exception as e:
                     print(f"Error processing lines by state '{current_tag}' for file {file_name or 'stdin'}: {e}", file=sys.stderr)
                     # Count all lines that were intended for this batch as potentially affected/errored
                     errors_during_processing += len(lines_for_state)
                     # Add error details to observability data
                     # Note: Capturing the exact line that caused the error in a batch is hard.
                     # Here we log the state, error message, file, and potentially the first line in the batch.
                     first_line_in_batch_id = lines_for_state[0][0] if lines_for_state else "N/A"
                     first_line_in_batch_content = lines_for_state[0][2] if lines_for_state else "N/A"
                     self.observability_data.add_error(ErrorData(time.time(), current_tag, str(e), first_line_in_batch_id, first_line_in_batch_content, file_name=file_name))

                     # Handle error policy - log and drop the lines that were being processed by this state.
                     # If tracing is enabled, add traces for these dropped lines.
                     if self.enable_tracing:
                         for line_id, incoming_tag, line_content, history in lines_for_state:
                             # Add the state where the error occurred to the history for the trace
                             self.observability_data.add_trace(LineTrace(line_id, line_content, history + [f"ERROR_IN_STATE:{current_tag}"], status="dropped_error", file_name=file_name))


                 finally:
                     # --- Metrics: End timing and update ---
                     end_time = time.time()
                     processing_duration = end_time - start_time
                     self.observability_data.update_metrics(
                         state=current_tag,
                         received=lines_received_count,
                         emitted=lines_emitted_count,
                         processing_time=processing_duration,
                         errors=errors_during_processing
                     )


        if total_lines_processed_count >= max_total_processed:
             print(f"Warning: Reached maximum total processed lines ({max_total_processed}) for file {file_name or 'stdin'}. Potential infinite loop detected or very large input. Some lines may not have reached END.", file=sys.stderr)
             # If tracing is enabled, add traces for lines still in queues with 'dropped_max_iterations' status
             if self.enable_tracing:
                 for tag, q in state_input_queues.items():
                     while not q.empty():
                         line_id, current_tag, line_content, history = q.get()
                         self.observability_data.add_trace(LineTrace(line_id, line_content, history + [f"STILL_IN_QUEUE_AT_MAX_ITERATIONS:{tag}"], status="dropped_max_iterations", file_name=file_name))
             # Add error to observability data
             self.observability_data.add_error(ErrorData(time.time(), "Engine", f"Max total lines processed exceeded ({max_total_processed})", "N/A", "N/A", file_name=file_name))


        # After the loop finishes (all queues are empty and max iterations not reached),
        # yield collected final outputs from the END_TAG state.
        # print("State transition loop finished for file.", file=sys.stderr) # Informative print)
        # print("Collecting final output for file...", file=sys.stderr) # Informative print)

        # Yield all items from the final output queue for this file
        while not final_output_queue.empty():
            yield final_output_queue.get()

        print(f"State Transition engine finished for file: {file_name or 'stdin'}", file=sys.stderr) # Informative print

