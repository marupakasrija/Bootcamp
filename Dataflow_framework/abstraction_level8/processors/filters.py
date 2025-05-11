# processors/filters.py

import logging
import time
from typing import Iterator, Tuple, List, Dict, Any

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Note: Processor methods now accept and yield a trace list and file_path
# The process method signature is now: Iterator[Tuple[str, str, List[str], str]] -> Iterator[Tuple[str, str, List[str], str]]

class OnlyErrorProcessor:
    """
    Processor that only passes through lines containing the word 'ERROR'.
    Emits lines tagged 'general' if they pass the filter, otherwise discards them.
    Includes basic timing and error handling.
    """
    def process(self, lines: Iterator[Tuple[str, str, List[str], str]]) -> Iterator[Tuple[str, str, List[str], str]]:
        """
        Processes an iterator of (tag, line, trace, file_path) tuples.

        Args:
            lines: An iterator yielding (tag, line, trace, file_path) tuples.

        Yields:
            (next_tag, processed_line, updated_trace, file_path) tuples for lines that pass the filter.
        """
        logging.debug("OnlyErrorProcessor received lines.")
        start_time = time.time()
        processed_count = 0
        error_count = 0

        try:
            for current_tag, line, trace, file_path in lines:
                processed_count += 1
                updated_trace = trace + [current_tag] # Append current tag to trace

                if "ERROR" in line.upper():
                    logging.debug(f"OnlyErrorProcessor: Found ERROR in '{line}' from '{file_path}'. Emitting 'general'.")
                    # If the line contains 'ERROR', send it to the 'general' state.
                    yield 'general', line, updated_trace, file_path
                else:
                    logging.debug(f"OnlyErrorProcessor: No ERROR in '{line}' from '{file_path}'. Discarding.")
                    # Discard lines that don't contain 'ERROR'.
                    # These lines do not yield, effectively ending their journey here.
                    pass # Explicitly do nothing

        except Exception as e:
            error_count += 1
            logging.error(f"Error in OnlyErrorProcessor processing line from '{file_path}': {e}", exc_info=True)
            # In a real system, you might yield an error tag or log more details.
            # For this example, we just count the error and let the line be potentially lost.

        end_time = time.time()
        processing_time = end_time - start_time

        # Metrics update is handled in the router.


class OnlyWarnProcessor:
    """
    Processor that only passes through lines containing the word 'WARN'.
    Emits lines tagged 'general' if they pass the filter, otherwise discards them.
    Includes basic timing and error handling.
    """
    def process(self, lines: Iterator[Tuple[str, str, List[str], str]]) -> Iterator[Tuple[str, str, List[str], str]]:
        """
        Processes an iterator of (tag, line, trace, file_path) tuples.

        Args:
            lines: An iterator yielding (tag, line, trace, file_path) tuples.

        Yields:
            (next_tag, processed_line, updated_trace, file_path) tuples for lines that pass the filter.
        """
        logging.debug("OnlyWarnProcessor received lines.")
        start_time = time.time()
        processed_count = 0
        error_count = 0

        try:
            for current_tag, line, trace, file_path in lines:
                processed_count += 1
                updated_trace = trace + [current_tag] # Append current tag to trace

                if "WARN" in line.upper():
                    logging.debug(f"OnlyWarnProcessor: Found WARN in '{line}' from '{file_path}'. Emitting 'general'.")
                    # If the line contains 'WARN', send it to the 'general' state.
                    yield 'general', line, updated_trace, file_path
                else:
                    logging.debug(f"OnlyWarnProcessor: No WARN in '{line}' from '{file_path}'. Discarding.")
                    # Discard lines that don't contain 'WARN'.
                    pass # Explicitly do nothing

        except Exception as e:
            error_count += 1
            logging.error(f"Error in OnlyWarnProcessor processing line from '{file_path}': {e}", exc_info=True)
            # Handle error logging/reporting

        end_time = time.time()
        processing_time = end_time - start_time

        # Metrics update is handled in the router.

# You can add more filter processors here as needed.
