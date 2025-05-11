# processors/formatters.py

import logging
import time
from typing import Iterator, Tuple, List, Dict, Any
import re

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Note: Processor methods now accept and yield a trace list as the third element in the tuple.
# The process method signature is now: Iterator[Tuple[str, str, List[str]]] -> Iterator[Tuple[str, str, List[str]]]

class SnakecaseProcessor:
    """
    Processor that converts the line text to snake_case.
    Emits lines tagged 'end' after formatting.
    Includes basic timing and error handling.
    """
    def process(self, lines: Iterator[Tuple[str, str, List[str]]]) -> Iterator[Tuple[str, str, List[str]]]:
        """
        Processes an iterator of (tag, line, trace) tuples, converts lines to snake_case,
        and yields them tagged 'end'.

        Args:
            lines: An iterator yielding (tag, line, trace) tuples.

        Yields:
            (next_tag, processed_line, updated_trace) tuples, where next_tag is 'end'.
        """
        logging.debug("SnakecaseProcessor received lines.")
        start_time = time.time()
        processed_count = 0
        error_count = 0

        try:
            for current_tag, line, trace in lines:
                processed_count += 1
                updated_trace = trace + [current_tag] # Append current tag to trace

                # Convert line to snake_case
                s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', line)
                snake_case_line = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

                logging.debug(f"SnakecaseProcessor: Converted '{line}' to '{snake_case_line}'. Emitting 'end'.")
                # After formatting, send the line to the 'end' state.
                yield 'end', snake_case_line, updated_trace

        except Exception as e:
            error_count += 1
            logging.error(f"Error in SnakecaseProcessor: {e}", exc_info=True)
            # Handle error logging/reporting

        end_time = time.time()
        processing_time = end_time - start_time

        # Metrics handling is done in the router.

# You can add more formatter processors here as needed.
