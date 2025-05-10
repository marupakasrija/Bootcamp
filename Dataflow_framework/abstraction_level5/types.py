# This is abstraction-level-5/types.py
# Defines type aliases and base classes for Level 5 DAG processing.

from typing import Callable, Iterator, Any, Dict, List, Optional, Tuple

# Existing types (kept for context, though less used directly by engine in L5)
ProcessorFn = Callable[[str], str]
StreamProcessorFn = Callable[[Iterator[str]], Iterator[str]]
ProcessorConfig = Dict[str, Any]
PipelineStepConfig = Dict[str, Any] # Used in L4, config format changes slightly for L5 nodes

# New type: A line tagged with a routing key
TaggedLine = Tuple[str, str] # (tag, line_content)

# New stream processor type: takes an iterator of lines, yields an iterator of TaggedLine
TaggedStreamProcessorFn = Callable[[Iterator[str]], Iterator[TaggedLine]]

# Define a base class for stateful, tag-emitting stream processors.
# Processors inheriting from this can maintain state and control routing.
class TaggedStreamProcessor:
    """Base class for stateful, tag-emitting stream processors."""
    def __init__(self, name: str, config: Optional[ProcessorConfig] = None):
        # Each processor node in the DAG needs a unique name
        self.name = name
        self.config = config or {}

    def process(self, lines: Iterator[str]) -> Iterator[TaggedLine]:
        """
        Processes an iterator of lines and yields (tag, line) tuples.
        The 'tag' determines the next node(s) in the DAG processing path.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement process()")

    # Optional: Add setup/teardown methods if needed for resource management
    # def setup(self): pass
    # def teardown(self): pass

# Config types for DAG
NodeConfig = Dict[str, Any] # Should include 'name', 'type', 'config'
RouteConfig = Dict[str, str] # Maps emitted tag to destination node name {emitted_tag: destination_node_name}
EdgeConfig = Dict[str, RouteConfig] # Node name -> {emitted_tag: destination_node_name}
DAGConfig = Dict[str, Any] # Top level config including 'nodes' and 'edges'
