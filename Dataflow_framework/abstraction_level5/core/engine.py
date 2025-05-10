# This is abstraction-level-5/core/engine.py
# Contains the DAG execution engine for Level 5.

import sys # Needed for sys.stderr
from typing import Iterator, List, Dict, Tuple, Any
from collections import defaultdict
import queue # Using queue for conceptual flow, though single-threaded here
# import networkx as nx # Optional: for graph validation/representation

# Import types and utilities using relative imports within the core package
from ..types import TaggedLine, TaggedStreamProcessor, TaggedStreamProcessorFn, DAGConfig, NodeConfig, EdgeConfig, ProcessorConfig
from .utils import get_tagged_stream_processor, load_processor_definition # Import helpers

# Define a special tag for lines that have completed processing and should be outputted
FINAL_OUTPUT_TAG = "final_output"

class DAGExecutionEngine:
    def __init__(self, dag_config: DAGConfig):
        # Map node names to processor functions/instances
        self.nodes: Dict[str, TaggedStreamProcessorFn] = {}
        # Map node name to its routing rules {node_name: {emitted_tag: next_node_name}}
        self.routes: EdgeConfig = {}
        # Map node name to its configuration (optional, for introspection)
        self._node_configs: Dict[str, NodeConfig] = {}

        self._load_config(dag_config)

        # Optional: Build and validate graph with networkx
        # self._graph = self._build_graph()
        # self._validate_graph()

    def _load_config(self, dag_config: DAGConfig):
        """Loads node processors and routing rules from config."""
        node_configs: List[NodeConfig] = dag_config.get('nodes', [])
        self.routes: EdgeConfig = dag_config.get('edges', {})

        # First, load and instantiate all nodes
        for node_config in node_configs:
            node_name = node_config.get('name')
            processor_path = node_config.get('type')
            processor_config = {k: v for k, v in node_config.items() if k not in ['name', 'type']}

            if not node_name or not processor_path:
                 print(f"Skipping invalid node config (missing name or type): {node_config}", file=sys.stderr)
                 continue

            if node_name in self.nodes:
                 print(f"Warning: Duplicate node name '{node_name}' found in config. Skipping.", file=sys.stderr)
                 continue

            self._node_configs[node_name] = node_config # Store original config

            try:
                # Dynamically load the processor definition (class or function)
                # Use the helper from utils.py
                processor_definition = load_processor_definition(processor_path)
                # Get the stream processor function (handle classes/functions, passes name and config)
                stream_processor_fn = get_tagged_stream_processor(processor_definition, name=node_name, config=processor_config)
                self.nodes[node_name] = stream_processor_fn
                print(f"Loaded node '{node_name}' with processor '{processor_path}'", file=sys.stderr)
            except Exception as e:
                print(f"Error loading or instantiating processor for node '{node_name}' ({processor_path}): {e}", file=sys.stderr)
                raise # Fail fast if a processor can't be loaded/instantiated

        # Second, validate routes reference existing nodes or the final output tag
        for from_node_name, tag_routes in self.routes.items():
            if from_node_name not in self.nodes:
                print(f"Warning: Route defined from unknown node '{from_node_name}'. Skipping routes from this node.", file=sys.stderr)
                continue
            if not isinstance(tag_routes, dict):
                 print(f"Warning: Routes for node '{from_node_name}' are not a dictionary. Skipping routes from this node.", file=sys.stderr)
                 continue

            invalid_routes = []
            for emitted_tag, to_node_name in tag_routes.items():
                if not isinstance(to_node_name, str):
                     print(f"Warning: Destination node name for tag '{emitted_tag}' from '{from_node_name}' is not a string ('{to_node_name}'). This route will be ignored.", file=sys.stderr)
                     invalid_routes.append(emitted_tag)
                     continue

                if to_node_name != FINAL_OUTPUT_TAG and to_node_name not in self.nodes:
                    print(f"Warning: Route from '{from_node_name}' with tag '{emitted_tag}' points to unknown destination node '{to_node_name}'. This route will be ignored.", file=sys.stderr)
                    invalid_routes.append(emitted_tag)

            # Remove invalid routes after iterating
            for tag in invalid_routes:
                del self.routes[from_node_name][tag]


    # Optional: networkx graph building and validation methods
    # def _build_graph(self) -> nx.DiGraph:
    #    G = nx.DiGraph()
    #    for node_name in self.nodes:
    #        G.add_node(node_name)
    #    for from_node, tag_routes in self.routes.items():
    #        for tag, to_node in tag_routes.items():
    #            if to_node in self.nodes or to_node == FINAL_OUTPUT_TAG:
    #                 G.add_edge(from_node, to_node, tag=tag)
    #    return G

    # def _validate_graph(self):
    #    # Check for cycles if the DAG is strictly required to be acyclic
    #    if not nx.is_directed_acyclic_graph(self._graph):
    #        print("Warning: The defined graph contains cycles. This engine supports cycles, but verify if this is intended.", file=sys.stderr)
    #    # Check for disconnected nodes, etc.


    def run(self, initial_lines: Iterator[str]) -> Iterator[str]:
        """
        Runs the DAG processing engine.

        Args:
            initial_lines: An iterator yielding the initial input lines.

        Yields:
            Processed lines that reach the 'final_output' tag.
        """
        print("Running DAG execution engine...", file=sys.stderr)

        # Initialize input lists for each node (using lists for simplicity in single-thread)
        node_input_lists: Dict[str, List[str]] = defaultdict(list)

        # Queue to collect final output lines
        final_output_lines: List[str] = []

        # --- Initial Injection ---
        # The first node to receive input is typically defined implicitly or by config.
        # Let's assume there's a node explicitly named 'start' in the config
        # that is designed to take the initial raw lines and tag them.
        start_node_name = 'start'
        if start_node_name not in self.nodes:
            raise ValueError(f"DAG config must include a node named '{start_node_name}' as the entry point.")

        # Feed initial lines into the 'start' node's input list
        # Ensure lines are stripped of trailing newlines here
        for line in initial_lines:
             node_input_lists[start_node_name].append(line.rstrip('\r\n'))

        # Keep track of nodes that currently have input and need processing
        nodes_with_input = {start_node_name} if node_input_lists[start_node_name] else set()

        # Safety break for potential loops
        processing_iterations = 0 # Count iterations of the main while loop
        max_iterations = 10000 * len(self.nodes) # Arbitrary limit based on number of nodes

        # The core processing loop
        # Continues as long as there are nodes with input to process
        while nodes_with_input and processing_iterations < max_iterations:
            processing_iterations += 1

            # Get a copy of the set of nodes that had input at the start of this iteration
            current_nodes_to_process = list(nodes_with_input)
            nodes_with_input.clear() # Clear the set for the next round

            # Process each node that had input
            for node_name in current_nodes_to_process:
                 if node_name not in self.nodes:
                     # Should not happen if validation is correct, but defensive
                     print(f"Error: Attempted to process unknown node '{node_name}'", file=sys.stderr)
                     continue

                 # Get all lines currently in this node's input list and clear it
                 lines_for_node = node_input_lists[node_name]
                 if not lines_for_node:
                     # This node's input list might have been cleared by another process
                     # if this were multi-threaded, but in single-thread, this is defensive.
                     continue

                 # Clear the input list *before* processing, so new lines arriving
                 # during processing go into the list for the *next* iteration.
                 node_input_lists[node_name] = []

                 processor_fn = self.nodes[node_name]
                 # print(f"DEBUG: Processing lines with node '{node_name}' ({len(lines_for_node)} lines)", file=sys.stderr) # Optional debug

                 try:
                     # Run the processor on the iterator of lines from its input list
                     processed_stream: Iterator[TaggedLine] = processor_fn(iter(lines_for_node))

                     # Route the output of the processor
                     for emitted_tag, processed_line in processed_stream:
                         # print(f"DEBUG: Node '{node_name}' emitted ('{emitted_tag}', '{processed_line}')", file=sys.stderr) # Optional debug
                         next_routes = self.routes.get(node_name, {})
                         next_node_name = next_routes.get(emitted_tag)

                         if emitted_tag == FINAL_OUTPUT_TAG:
                             # This line is done, collect it
                             final_output_lines.append(processed_line)
                             # print(f"DEBUG: Line reached final output: '{processed_line}'", file=sys.stderr) # Optional debug
                         elif next_node_name:
                             if next_node_name in self.nodes:
                                 # Route to the next node by adding to its input list
                                 node_input_lists[next_node_name].append(processed_line)
                                 # Add the next node to the set of nodes that need processing
                                 nodes_with_input.add(next_node_name)
                                 # print(f"DEBUG: Routed line from '{node_name}' (tag '{emitted_tag}') to '{next_node_name}'.", file=sys.stderr) # Optional debug
                             else:
                                 # This case should be caught by validation, but defensive check
                                 print(f"Error: Configured next node '{next_node_name}' for tag '{emitted_tag}' from '{node_name}' not found. Line dropped: '{processed_line}'", file=sys.stderr)
                         else:
                             # No route defined for this tag from this node
                             print(f"Warning: No route defined for tag '{emitted_tag}' from node '{node_name}'. Line dropped: '{processed_line}'", file=sys.stderr)


                 except Exception as e:
                     print(f"Error processing lines by node '{node_name}': {e}", file=sys.stderr)
                     # Handle error - depending on policy, could add lines back to queue,
                     # route to an error state, log, or drop lines.
                     # For now, just log and drop the lines that were being processed by this node.


        if processing_iterations >= max_iterations:
             print(f"Warning: Reached maximum processing iterations ({max_iterations}). Potential infinite loop detected or complex graph.", file=sys.stderr)

        # After the loop finishes, yield collected final outputs
        # print("DEBUG: DAG execution finished, yielding final collected output.", file=sys.stderr) # Optional debug
        yield from final_output_lines

        # print("DAG execution engine finished.", file=sys.stderr) # Informative print

