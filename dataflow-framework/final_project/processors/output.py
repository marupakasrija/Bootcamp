# processors/output.py

import logging
import time
from typing import Iterator, Tuple, List, Dict, Any

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Note: Processor methods now accept a trace list and file_path
# The process method signature is now: Iterator[Tuple[str, str, List[str], str]] -> Iterator[Tuple[str, str, List[str], str]]
# The end processor does not yield, effectively returning an empty iterator.

class TerminalOutputProcessor:
    """
    Processor that prints the final processed lines to the terminal.
    This processor is typically used for lines tagged 'end'.
    It does not emit any further tags, effectively terminating the line's journey.
    Includes basic timing and error handling.
    """
    def process(self, lines: Iterator[Tuple[str, str, List[str], str]]) -> Iterator[Tuple[str, str, List[str], str]]:
        """
        Processes an iterator of (tag, line, trace, file_path) tuples by printing the lines.
        Does not yield any output, as this is an end state.

        Args:
            lines: An iterator yielding (tag, line, trace, file_path) tuples.

        Yields:
            Nothing.
        """
        logging.debug("TerminalOutputProcessor received lines tagged 'end'.")
        start_time = time.time()
        processed_count = 0
        error_count = 0

        try:
            for current_tag, line, trace, file_path in lines:
                processed_count += 1
                # Append current tag to trace, even for the end state
                updated_trace = trace + [current_tag]

                # Print the final processed line.
                print(f"FINAL OUTPUT [Tag: {current_tag}] (File: {file_path}): {line}")
                logging.debug(f"TerminalOutputProcessor: Printed line '{line}' from '{file_path}'. Trace: {updated_trace}")
                # This processor is an end state. It does not yield any further tags.

        except Exception as e:
            error_count += 1
            logging.error(f"Error in TerminalOutputProcessor processing line from '{file_path}': {e}", exc_info=True)
            # Handle error logging/reporting

        end_time = time.time()
        processing_time = end_time - start_time

        # Metrics update is handled in the router.

        # Explicitly yield nothing to ensure this is treated as a generator
        # and returns an empty iterator.
        if False:
            yield
