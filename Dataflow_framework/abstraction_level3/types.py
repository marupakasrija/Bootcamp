from typing import Callable, Iterator, Dict, Any

# Define a type alias for our line processor function.
ProcessorFn = Callable[[str], str]

# Used for further lines
ProcessorConfig = Dict[str, Any]

# Define a type alias for a pipeline step config (used in pipeline.py)
PipelineStepConfig = Dict[str, Any] 
