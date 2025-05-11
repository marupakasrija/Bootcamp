# processors/start.py

import logging
import time
import random
from typing import Iterator, Tuple, List, Dict, Any

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Note: Processor methods now accept and yield a trace list as the third element in the tuple.
# The process method signature is now: Iterator[Tuple[str, str, List[str]]] -> Iterator[Tuple[str, str, List[str]]]

class TagLinesProcessor:
    """
    The initial processor for lines tagged 'start'.
    It takes raw lines and assigns them an initial tag ('error', 'warn', or 'general')
    based on some simple logic (randomly in this example).
    Initializes the trace list.
    Includes basic timing and error handling.
    """
    def process(self, lines: Iterator[Tuple[str, str, List[str]]]) -> Iterator[Tuple[str, str, List[str]]]:
        """
        Processes an iterator of (tag, line, trace) tuples (expected tag is 'start').
        Assigns an initial tag to each line and yields it for the next step.
        Initializes the trace list for each line.

        Args:
            lines: An iterator yielding (tag, line, trace) tuples.

        Yields:
            (next_tag, processed_line, updated_trace) tuples with assigned initial tags.
        """
        logging.debug("TagLinesProcessor received lines tagged 'start'.")
        start_time = time.time()
        processed_count = 0
        error_count = 0

        possible_tags = ['error', 'warn', 'general']

        try:
            for current_tag, line, trace in lines:
                processed_count += 1
                # The trace list is expected to be empty for 'start' lines, but we append the current tag anyway.
                updated_trace = trace + [current_tag]

                # Simple logic to assign a tag: randomly pick one.
                next_tag = random.choice(possible_tags)
                logging.debug(f"TagLinesProcessor: Tagging line '{line}' with '{next_tag}'.")
                yield next_tag, line, updated_trace

        except Exception as e:
            error_count += 1
            logging.error(f"Error in TagLinesProcessor: {e}", exc_info=True)
            # Handle error logging/reporting

        end_time = time.time()
        processing_time = end_time - start_time

        # Metrics handling is done in the router.

# You can add other initial processors here if you have different ways
# of starting the routing process.
