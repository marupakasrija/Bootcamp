import sys 
from typing import Iterator, List
from .types import ProcessorFn

def apply_pipeline(lines: Iterator[str], pipeline: List[ProcessorFn]) -> Iterator[str]:
    """
    Applies a list of processor functions sequentially to each line from the input iterator.

    Each processor function in the pipeline is expected to take a string (the
    output of the previous processor, or the initial stripped line) and return
    a string (the processed line).

    Args:
        lines: An iterator yielding input lines (strings).
        pipeline: A list of ProcessorFn functions to apply in order.

    Yields:
        Processed lines after applying all pipeline steps.
        If an error occurs during processing a line, the line in its state
        before the failing processor is yielded, and subsequent processors
        for that line are skipped.
    """
    print("Applying pipeline...") 

    for line in lines:
        current_line_state = line.strip()
        for i, processor in enumerate(pipeline):
            # Get the processor's name for logging purposes.
            # Use __name__ if available, otherwise use its index.
            processor_name = getattr(processor, '__name__', f'processor_{i}')

            try:
                # Apply the current processor to the current state of the line.
                next_line_state = processor(current_line_state)
                # Update the line state for the next processor in the sequence.
                current_line_state = next_line_state

            except Exception as e:
                # If any exception occurs during processing by a specific processor:
                # 1. Log the error to standard error.
                print(
                    f"Error applying processor '{processor_name}' to line "
                    f"'{current_line_state}': {e}",
                    file=sys.stderr
                )
                # 2. Decide how to handle the error for this line.
                #    In this implementation, we yield the line as it was *before*
                #    this failing processor and stop processing this specific line
                #    through any remaining steps in the pipeline. This prevents
                #    subsequent processors from potentially failing on bad input.
                yield current_line_state
                # Break out of the inner loop (processing this line's pipeline)
                # and move to the next line from the input iterator.
                break
        else:
            # This 'else' block is executed only if the inner 'for' loop
            # (iterating through processors) completes without hitting a 'break'.
            # This means all processors in the pipeline were applied successfully
            # to the current line.
            yield current_line_state 

    print("Pipeline application finished.")
