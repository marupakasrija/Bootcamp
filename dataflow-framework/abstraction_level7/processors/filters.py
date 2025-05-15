# processors/filters.py

import logging
import time
from typing import Iterator, Tuple, List, Dict, Any

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Note: Processor methods now accept and yield a trace list as the third element in the tuple.
# The process method signature is now: Iterator[Tuple[str, str, List[str]]] -> Iterator[Tuple[str, str, List[str]]]

class OnlyErrorProcessor:
    """
    Processor that only passes through lines containing the word 'ERROR'.
    Emits lines tagged 'general' if they pass the filter, otherwise discards them.
    Includes basic timing and error handling.
    """
    def process(self, lines: Iterator[Tuple[str, str, List[str]]]) -> Iterator[Tuple[str, str, List[str]]]:
        """
        Processes an iterator of (tag, line, trace) tuples.

        Args:
            lines: An iterator yielding (tag, line, trace) tuples.

        Yields:
            (next_tag, processed_line, updated_trace) tuples for lines that pass the filter.
        """
        logging.debug("OnlyErrorProcessor received lines.")
        start_time = time.time()
        processed_count = 0
        error_count = 0

        try:
            for current_tag, line, trace in lines:
                processed_count += 1
                updated_trace = trace + [current_tag] # Append current tag to trace

                if "ERROR" in line.upper():
                    logging.debug(f"OnlyErrorProcessor: Found ERROR in '{line}'. Emitting 'general'.")
                    # If the line contains 'ERROR', send it to the 'general' state.
                    yield 'general', line, updated_trace
                else:
                    logging.debug(f"OnlyErrorProcessor: No ERROR in '{line}'. Discarding.")
                    # Discard lines that don't contain 'ERROR'.
                    # These lines do not yield, effectively ending their journey here.
                    pass # Explicitly do nothing

        except Exception as e:
            error_count += 1
            logging.error(f"Error in OnlyErrorProcessor: {e}", exc_info=True)
            # In a real system, you might yield an error tag or log more details.
            # For this example, we just count the error and let the line be potentially lost.

        end_time = time.time()
        processing_time = end_time - start_time

        # Return metrics for this processing batch
        # Note: This is a simple way to return metrics for a batch.
        # In a real system, metrics would be updated in a shared, thread-safe store.
        # We will handle metric updates in the router based on processor execution.
        # The processor's primary job is to yield output lines.
        # Metrics are a side effect managed by the engine calling the processor.


class OnlyWarnProcessor:
    """
    Processor that only passes through lines containing the word 'WARN'.
    Emits lines tagged 'general' if they pass the filter, otherwise discards them.
    Includes basic timing and error handling.
    """
    def process(self, lines: Iterator[Tuple[str, str, List[str]]]) -> Iterator[Tuple[str, str, List[str]]]:
        """
        Processes an iterator of (tag, line, trace) tuples.

        Args:
            lines: An iterator yielding (tag, line, trace) tuples.

        Yields:
            (next_tag, processed_line, updated_trace) tuples for lines that pass the filter.
        """
        logging.debug("OnlyWarnProcessor received lines.")
        start_time = time.time()
        processed_count = 0
        error_count = 0

        try:
            for current_tag, line, trace in lines:
                processed_count += 1
                updated_trace = trace + [current_tag] # Append current tag to trace

                if "WARN" in line.upper():
                    logging.debug(f"OnlyWarnProcessor: Found WARN in '{line}'. Emitting 'general'.")
                    # If the line contains 'WARN', send it to the 'general' state.
                    yield 'general', line, updated_trace
                else:
                    logging.debug(f"OnlyWarnProcessor: No WARN in '{line}'. Discarding.")
                    # Discard lines that don't contain 'WARN'.
                    pass # Explicitly do nothing

        except Exception as e:
            error_count += 1
            logging.error(f"Error in OnlyWarnProcessor: {e}", exc_info=True)
            # Handle error logging/reporting

        end_time = time.time()
        processing_time = end_time - start_time

        # Metrics handling is done in the router.

# You can add more filter processors here as needed.
