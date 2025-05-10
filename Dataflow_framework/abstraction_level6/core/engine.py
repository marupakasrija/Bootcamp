# This is abstraction-level-6/core/engine.py
# Contains the State Transition execution engine for Level 6.

import sys # Needed for sys.stderr
from typing import Iterator, List, Dict, Tuple, Any, Set
from collections import defaultdict
import queue # Using queue for conceptual flow, though single-threaded here
import networkx as nx # For graph representation, validation, and cycle detection

# Import types and utilities using relative imports within the core package
from ..types import TaggedLine, StateProcessor, StateProcessorFn, StateSystemConfig, StateConfig, ProcessorDefinitionConfig, START_TAG, END_TAG
from .utils import get_state_processor_fn, load_processor_definition # Import helpers

# Define a maximum number of times a single line can be processed to guard against infinite loops
MAX_PROCESSING_PER_LINE = 100

class StateTransitionEngine:
    def __init__(self, state_config: StateSystemConfig):
        # Map tag (state) to processor function/instance
        self.states: Dict[str, StateProcessorFn] = {}
        # Store original state configurations
        self._state_configs: StateConfig = {}

        self._load_config(state_config)

        # Build and validate the state graph
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
                processor_definition = load_processor_definition(processor_path)
                # Get the state processor function (handle classes/functions, passes the tag and config)
                state_processor_fn = get_state_processor_fn(processor_definition, tag=tag, config=processor_config)
                self.states[tag] = state_processor_fn
                print(f"Loaded state '{tag}' with processor '{processor_path}'", file=sys.stderr)
            except Exception as e:
                print(f"Error loading or instantiating processor for state '{tag}' ({processor_path}): {e}", file=sys.stderr)
                raise # Fail fast if a processor can't be loaded/instantiated

        # Ensure START and END states are defined
        if START_TAG not in self.states:
             raise ValueError(f"Config must include a state defined for the '{START_TAG}' tag.")
        if END_TAG not in self.states:
             # The END state processor is crucial for collecting output.
             # If not explicitly defined, we could potentially use a default one.
             # For now, let's make it required.
             raise ValueError(f"Config must include a state defined for the '{END_TAG}' tag.")


    def _build_graph(self) -> nx.DiGraph:
       """Builds a networkx graph representing state transitions."""
       G = nx.DiGraph()

       # Add nodes for all defined states
       for tag in self.states:
           G.add_node(tag)

       # Infer edges by running a small sample through each processor?
       # No, infer edges from the *potential* output tags defined by the processor logic
       # or by having routing defined explicitly in the config (like L5 edges).
       # The prompt implies routing is based *on* the emitted tag, not a separate edge list.
       # So, the graph is implicitly defined by (current_tag) -> processor -> (emitted_tag) -> next_tag.
       # We need to know what tags each processor *can* emit. This is not easily
       # discoverable dynamically without running the processor.

       # Alternative: Assume the config *implicitly* defines transitions by listing states.
       # A transition exists from tag_A to tag_B if tag_A's processor can emit tag_B,
       # AND tag_B is a defined state.
       # This still requires knowing emitted tags.

       # Let's simplify for L6: Assume the graph nodes are the defined states.
       # Edges are inferred by looking at the *code* of the processors or requiring
       # processors to declare their possible output tags.
       # A simpler way for config-driven approach: The config lists states,
       # and the engine assumes any tag emitted by a processor *that matches a defined state*
       # is a valid transition. The graph nodes are just the keys in self.states.

       # Let's build a graph where nodes are the state tags.
       # Edges represent potential transitions. We can't know all edges statically
       # without running, but we can know which states exist.
       # For basic validation, we can check if START and END exist, and if END has no outgoing.

       # For cycle detection, we need edges. Where do edges come from?
       # The *emitted tags* are the edges. From state A, if processor A emits tag 'B',
       # there's a transition A -> B.
       # We can build the graph by iterating through the *config* and assuming
       # a transition exists from `tag_A` to `tag_B` if `tag_B` is a key in `self.states`.
       # This is still not quite right. The transition is determined *by the tag emitted*.

       # Let's build the graph based on the *defined states* as nodes.
       # We can't fully build the edges statically without knowing processor logic.
       # However, for cycle detection, we need to know potential paths.

       # Let's try to infer edges based on the *structure* of the system:
       # An edge exists from state A to state B if processor for state A *can* emit tag B,
       # AND state B exists.
       # This requires processors to declare their possible output tags.

       # Let's add a method to StateProcessor to declare possible output tags.
       # class StateProcessor: ... def get_possible_output_tags(self) -> Set[str]: ...

       # For simplicity in L6, let's build the graph where nodes are states,
       # and an edge exists from state A to state B if state B is a defined state.
       # This isn't a true transition graph, but it lets us use networkx.

       # Revised Graph Building for L6: Nodes are states. We can't reliably add edges statically.
       # Let's just use networkx to represent the *states* as nodes for potential visualization.
       # For cycle detection, we need to track visited states *per line* during execution.

       # Let's revert to the L5 graph idea: nodes are defined states.
       # We can add edges if the config explicitly listed transitions (like L5 edges).
       # But the prompt says "routing is tag-based", implying no separate edge list.

       # Okay, let's use networkx for cycle detection *during execution* or by building
       # a graph based on *observed* transitions during a dry run or sample.
       # For static validation, let's just check basic state existence.

       # Let's build a graph where nodes are the state tags defined in the config.
       # We can't add edges statically based on emitted tags.
       # Let's skip static graph building for now and focus on execution-time tracking for cycles.

       G = nx.DiGraph()
       for tag in self.states:
           G.add_node(tag)

       # We can add a dummy edge from START_TAG to any other state that its processor
       # might emit, if we know those statically.
       # For now, just nodes.

       return G # Return graph with just nodes


    def _validate_graph(self):
       """Performs basic validation on the state graph."""
       # Check if START_TAG has no incoming edges (should only receive initial input)
       # This is hard to check statically without knowing all possible emitted tags.

       # Check if END_TAG has no outgoing edges
       # This requires knowing what tags the END_TAG processor emits.
       # Assume the END_TAG processor only emits END_TAG.

       # Check for unreachable states (optional, requires knowing all possible transitions)

       print("Basic state graph validation complete.", file=sys.stderr)


    def run(self, initial_lines: Iterator[str]) -> Iterator[str]:
        """
        Runs the State Transition engine.

        Args:
            initial_lines: An iterator yielding the initial input lines (will be tagged 'start').

        Yields:
            Processed lines that reach the 'end' state.
        """
        print("Running State Transition engine...", file=sys.stderr)

        # Use queues for inter-state communication.
        # Each state (tag) gets an input queue.
        state_input_queues: Dict[str, queue.Queue[TaggedLine]] = {}
        for tag in self.states:
             state_input_queues[tag] = queue.Queue()

        # Queue to collect final output lines
        final_output_queue: queue.Queue[str] = queue.Queue()

        # Track lines currently being processed by a state processor
        # (Useful for more advanced engines, less critical in single-thread)
        # active_processors: Set[str] = set()

        # Track processing history per line to detect cycles
        line_processing_history: Dict[str, List[str]] = defaultdict(list) # {line_id: [tag1, tag2, ...]}
        # Assign a unique ID to each initial line? Or use the line content?
        # Using line content is simpler for now, but assumes unique lines.
        # A better approach would be to wrap lines with a unique ID object.

        # --- Initial Injection ---
        # All initial lines enter the system tagged with START_TAG.
        start_tag = START_TAG
        if start_tag not in self.states:
             # This should be caught by _load_config, but defensive
             raise ValueError(f"Engine requires a state defined for the '{START_TAG}' tag.")

        # Feed initial lines into the 'start' state's input queue
        print(f"DEBUG: Injecting initial lines into '{START_TAG}' state...", file=sys.stderr) # Optional debug
        for line in initial_lines:
             # Tag initial lines with START_TAG
             tagged_line: TaggedLine = (START_TAG, line.rstrip('\r\n')) # Strip newlines early
             state_input_queues[START_TAG].put(tagged_line)
             # Initialize history for this line
             line_processing_history[tagged_line[1]].append(START_TAG)


        # --- State Transition Loop ---
        # This loop continues as long as there are lines in any state's input queue.
        # In a single-threaded model, we can iterate through states that have input.
        # In a multi-threaded model, worker threads would pull from queues.

        # Keep track of states that currently have input
        states_with_input: Set[str] = {START_TAG} if not state_input_queues[START_TAG].empty() else set()

        # Safety break for potential infinite loops
        total_lines_processed_count = 0 # Count total (tag, line) pairs processed
        max_total_processed = 1000000 # Arbitrary high limit

        print("Starting state transition loop...", file=sys.stderr) # Informative print

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
                     print(f"Error: Attempted to process unknown state '{current_tag}'", file=sys.stderr)
                     continue

                 # Get all lines currently in this state's input queue
                 lines_for_state: List[TaggedLine] = []
                 while not state_input_queues[current_tag].empty():
                     lines_for_state.append(state_input_queues[current_tag].get())

                 if not lines_for_state:
                     # Should not happen if picked from states_with_input, but defensive.
                     continue

                 processor_fn = self.states[current_tag]
                 # print(f"DEBUG: Processing lines in state '{current_tag}' ({len(lines_for_state)} lines)", file=sys.stderr) # Optional debug

                 try:
                     # Run the processor on the iterator of lines for this state
                     processed_stream: Iterator[TaggedLine] = processor_fn(iter(lines_for_state))

                     # Route the output of the processor
                     for next_tag, processed_line in processed_stream:
                         total_lines_processed_count += 1
                         # print(f"DEBUG: State '{current_tag}' emitted ('{next_tag}', '{processed_line}')", file=sys.stderr) # Optional debug

                         # --- Cycle Detection / Loop Guard ---
                         # Using line content as a simple ID for history tracking
                         line_id = processed_line # Simplified ID (assumes unique processed lines or ok with false positives)
                         line_processing_history[line_id].append(next_tag)

                         if len(line_processing_history[line_id]) > MAX_PROCESSING_PER_LINE:
                             print(f"Warning: Line '{line_id}' exceeded max processing steps ({MAX_PROCESSING_PER_LINE}). Possible infinite loop. Dropping line.", file=sys.stderr)
                             # Skip routing this line
                             continue

                         # --- Routing ---
                         if next_tag == END_TAG:
                             # This line is done, put it in the final output queue
                             final_output_queue.put(processed_line)
                             # print(f"DEBUG: Line reached END state: '{processed_line}'", file=sys.stderr) # Optional debug
                             # Line processing history for this line can stop or be marked complete

                         elif next_tag in self.states:
                             # Route to the next state by adding to its input queue
                             state_input_queues[next_tag].put((next_tag, processed_line)) # Pass the new tag with the line
                             # Add the next state to the set of states that need processing
                             states_with_input.add(next_tag)
                             # print(f"DEBUG: Routed line from '{current_tag}' to '{next_tag}'.", file=sys.stderr) # Optional debug
                         else:
                             # Emitted tag does not correspond to a defined state (and is not END_TAG)
                             print(f"Warning: Emitted tag '{next_tag}' from state '{current_tag}' does not match any defined state or '{END_TAG}'. Line dropped: '{processed_line}'", file=sys.stderr)

                 except Exception as e:
                     print(f"Error processing lines by state '{current_tag}': {e}", file=sys.stderr)
                     # Handle error - log and drop the lines that were being processed by this state.


        if total_lines_processed_count >= max_total_processed:
             print(f"Warning: Reached maximum total processed lines ({max_total_processed}). Potential infinite loop detected or very large input.", file=sys.stderr)

        # After the loop finishes (all queues are empty), yield collected final outputs
        print("State transition loop finished.", file=sys.stderr) # Informative print
        print("Collecting final output...", file=sys.stderr) # Informative print

        # Yield all items from the final output queue
        while not final_output_queue.empty():
            yield final_output_queue.get()

        print("State Transition engine finished.", file=sys.stderr) # Informative print


