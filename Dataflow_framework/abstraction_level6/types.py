# This is abstraction-level-6/types.py
# Defines type aliases and base classes for Level 6 State-Based Routing.

from typing import Callable, Iterator, Any, Dict, List, Optional, Tuple

# Type: A line tagged with a routing key/state
TaggedLine = Tuple[str, str] # (tag, line_content)

# New stream processor type: takes an iterator of TaggedLine, yields an iterator of TaggedLine
# Processors now receive lines *with* their current tag and emit lines with the *next* tag.
StateProcessorFn = Callable[[Iterator[TaggedLine]], Iterator[TaggedLine]]

# Define a base class for stateful, tag-emitting stream processors (States).
# Processors inheriting from this can maintain state and control the next state via tags.
class StateProcessor:
    """Base class for stateful stream processors acting as States."""
    def __init__(self, tag: str, config: Optional[Dict[str, Any]] = None):
        # Each processor instance is associated with a specific tag/state
        self.tag = tag
        self.config = config or {}

    def process(self, lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
        """
        Processes an iterator of (tag, line) tuples and yields (next_tag, line) tuples.
        The incoming tag is the current state; the yielded tag is the next state.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement process()")

    # Optional: Add setup/teardown methods if needed for resource management
    # def setup(self): pass
    # def teardown(self): pass

# Config types for State Transition System
ProcessorDefinitionConfig = Dict[str, Any] # Should include 'type' and optional config
StateConfig = Dict[str, ProcessorDefinitionConfig] # Maps tag (state) to processor definition {tag: {type: ..., config: ...}}
StateSystemConfig = Dict[str, Any] # Top level config including 'states'

# Define special tags
START_TAG = "start"
END_TAG = "end"

