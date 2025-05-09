from typing import Callable, Iterator, Any, Dict, List, Optional

ProcessorFn = Callable[[str], str]

StreamProcessorFn = Callable[[Iterator[str]], Iterator[str]]

# Type for processor configuration
ProcessorConfig = Dict[str, Any]

# Type for a step in the pipeline config, including type and optional config
PipelineStepConfig = Dict[str, Any] 

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


