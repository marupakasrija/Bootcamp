# This is abstraction-level-4/core.py
# Contains core logic for applying stream processors and helper functions.

import sys # Needed for sys.stderr
from typing import Iterator, List, Optional, Any, Dict
# Import types using relative imports within the package
from .types import ProcessorFn, StreamProcessorFn, StreamProcessor, ProcessorConfig, PipelineStepConfig

# --- Wrapper for old str -> str processors ---
def line_processor_to_stream_processor(processor_fn: ProcessorFn) -> StreamProcessorFn:
    """
    Wraps a line-by-line processor (str -> str) to work on a stream (Iterator[str] -> Iterator[str]).
    """
    def stream_wrapper(lines: Iterator[str]) -> Iterator[str]:
        # print(f"DEBUG: Applying wrapped line processor: {getattr(processor_fn, '__name__', 'anonymous')}", file=sys.stderr) # Optional debug
        for line in lines:
            try:
                # Apply the original line processor function to each line
                yield processor_fn(line)
            except Exception as e:
                # Basic error handling: print error and yield the original line
                print(f"Error processing line '{line}' with wrapped processor {getattr(processor_fn, '__name__', 'anonymous')}: {e}", file=sys.stderr)
                yield line # Yield the original line on error
    return stream_wrapper

# --- Helper to instantiate processor classes ---
def instantiate_processor(processor_class, config: Optional[ProcessorConfig] = None) -> StreamProcessor:
    """Instantiates a processor class, passing configuration."""
    try:
        # Check if it's a class and a subclass of StreamProcessor (good practice)
        if not isinstance(processor_class, type) or not issubclass(processor_class, StreamProcessor):
             raise TypeError(f"Expected a StreamProcessor class, but got {type(processor_class)}")

        # Instantiate the class, passing the config
        instance = processor_class(config=config)
        # print(f"DEBUG: Instantiated processor class: {processor_class.__name__}", file=sys.stderr) # Optional debug
        return instance
    except Exception as e:
        print(f"Error instantiating processor class {getattr(processor_class, '__name__', 'anonymous')}: {e}", file=sys.stderr)
        raise # Re-raise the exception


# --- Helper to get a StreamProcessorFn from various types ---
def get_stream_processor(processor_definition, config: Optional[ProcessorConfig] = None) -> StreamProcessorFn:
    """
    Takes a processor definition (a StreamProcessor class or a str->str function)
    and returns a StreamProcessorFn (Iterator[str] -> Iterator[str]).

    Args:
        processor_definition: The processor class or function.
        config: Optional configuration dictionary for class-based processors.

    Returns:
        A callable function that takes an iterator and returns an iterator.

    Raises:
        TypeError: If the definition is not a supported type.
    """
    # Check if it's a StreamProcessor class
    if isinstance(processor_definition, type) and issubclass(processor_definition, StreamProcessor):
        # Instantiate the class and return its process method
        instance = instantiate_processor(processor_definition, config)
        return instance.process
    # Check if it's a callable (assume it's a str->str function for now)
    elif callable(processor_definition):
         # Wrap the str->str function to work on a stream
         # TODO: Could add a check here to see if it already matches StreamProcessorFn signature
         # If it does, return it directly.
         # For simplicity in L4, we assume callable means str->str unless it's a StreamProcessor class.
         return line_processor_to_stream_processor(processor_definition)
    else:
        raise TypeError(f"Processor definition must be a callable function or a StreamProcessor class, got {type(processor_definition)}")


# --- Core pipeline application logic (now stream-based) ---
def apply_stream_pipeline(lines: Iterator[str], pipeline: List[StreamProcessorFn]) -> Iterator[str]:
    """
    Applies a list of stream processors sequentially to the entire stream of lines.

    Args:
        lines: An iterator yielding input lines.
        pipeline: A list of StreamProcessorFn functions to apply in order.

    Yields:
        Processed lines from the final processor in the pipeline.
        If an error occurs during processing by a processor, the pipeline
        application for the remaining processors might stop or yield partial results
        depending on the processor's error handling.
    """
    # print("Applying streaming pipeline...", file=sys.stderr) # Informative print

    current_stream = lines # The input stream for the first processor

    # Iterate through each stream processor in the pipeline
    for i, processor in enumerate(pipeline):
        # Get the processor's name for logging purposes.
        processor_name = getattr(processor, '__name__', f'processor_{i}')
        # print(f"DEBUG: Sending stream to processor: {processor_name}", file=sys.stderr) # Optional debug

        try:
            # Pass the output stream of the previous processor as the input
            # stream to the current processor.
            current_stream = processor(current_stream)

        except Exception as e:
             # If an error occurs in a processor, print an error message.
             print(f"Error applying processor '{processor_name}': {e}", file=sys.stderr)
             # Decide how to handle this critical error.
             # Option 1: Stop processing the rest of the stream.
             # Option 2: Attempt to pass the remaining 'current_stream' through subsequent processors (might fail).
             # Option 3: Yield any results obtained so far and then stop.
             # For simplicity in L4, we will stop processing the stream.
             # A more robust system might have error-handling branches or dead-letter queues.
             return iter([]) # Yield nothing more if a processor fails

    # After the last processor runs, yield all lines from its output stream.
    # print("DEBUG: Pipeline finished, yielding final stream.", file=sys.stderr) # Optional debug
    yield from current_stream # Yield all items from the final iterator

    # print("Streaming pipeline application finished.", file=sys.stderr) # Informative print

