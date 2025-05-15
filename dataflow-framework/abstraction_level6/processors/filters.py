# processors/filters.py

import logging
from typing import Iterator, Tuple

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OnlyErrorProcessor:
    """
    Processor that only passes through lines containing the word 'ERROR'.
    Emits lines tagged 'general' if they pass the filter, otherwise discards them.
    """
    def process(self, lines: Iterator[Tuple[str, str]]) -> Iterator[Tuple[str, str]]:
        """
        Processes an iterator of (tag, line) tuples.

        Args:
            lines: An iterator yielding (tag, line) tuples.

        Yields:
            (next_tag, processed_line) tuples for lines that pass the filter.
        """
        logging.info("OnlyErrorProcessor received lines.")
        for current_tag, line in lines:
            if "ERROR" in line.upper():
                logging.info(f"OnlyErrorProcessor: Found ERROR in '{line}'. Emitting 'general'.")
                # If the line contains 'ERROR', send it to the 'general' state.
                yield 'general', line
            else:
                logging.info(f"OnlyErrorProcessor: No ERROR in '{line}'. Discarding.")
                # Discard lines that don't contain 'ERROR'.
                pass # Explicitly do nothing

class OnlyWarnProcessor:
    """
    Processor that only passes through lines containing the word 'WARN'.
    Emits lines tagged 'general' if they pass the filter, otherwise discards them.
    """
    def process(self, lines: Iterator[Tuple[str, str]]) -> Iterator[Tuple[str, str]]:
        """
        Processes an iterator of (tag, line) tuples.

        Args:
            lines: An iterator yielding (tag, line) tuples.

        Yields:
            (next_tag, processed_line) tuples for lines that pass the filter.
        """
        logging.info("OnlyWarnProcessor received lines.")
        for current_tag, line in lines:
            if "WARN" in line.upper():
                logging.info(f"OnlyWarnProcessor: Found WARN in '{line}'. Emitting 'general'.")
                # If the line contains 'WARN', send it to the 'general' state.
                yield 'general', line
            else:
                logging.info(f"OnlyWarnProcessor: No WARN in '{line}'. Discarding.")
                # Discard lines that don't contain 'WARN'.
                pass # Explicitly do nothing

# You can add more filter processors here as needed.
