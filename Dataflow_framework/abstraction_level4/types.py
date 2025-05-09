# This is abstraction-level-4/types.py
# Defines type aliases and base classes for Level 4 stream processing.

from typing import Callable, Iterator, Any, Dict, List, Optional

# Existing line processor type (kept for compatibility/wrapping)
ProcessorFn = Callable[[str], str]

# New stream processor type: takes an iterator, returns an iterator
StreamProcessorFn = Callable[[Iterator[str]], Iterator[str]]

# Type for processor configuration
ProcessorConfig = Dict[str, Any]

# Type for a step in the pipeline config, including type and optional config
PipelineStepConfig = Dict[str, Any] # Should contain 'type' and optionally other keys

# Define a base class for stateful stream processors.
# Processors inheriting from this can maintain state across lines.
class StreamProcessor:
    """Base class for stateful stream processors."""
    def __init__(self, config: Optional[ProcessorConfig] = None):
        self.config = config or {}

    def process(self, lines: Iterator[str]) -> Iterator[str]:
        """
        Processes an iterator of lines and yields processed lines.
        Must be implemented by subclasses. This is the core processing logic.
        """
        raise NotImplementedError("Subclasses must implement process()")

    # Optional: Add setup/teardown methods if needed for resource management
    # def setup(self): pass
    # def teardown(self): pass

