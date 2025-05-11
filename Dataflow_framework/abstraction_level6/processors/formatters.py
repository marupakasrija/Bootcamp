# processors/formatters.py

import logging
from typing import Iterator, Tuple
import re

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SnakecaseProcessor:
    """
    Processor that converts the line text to snake_case.
    Emits lines tagged 'end' after formatting.
    """
    def process(self, lines: Iterator[Tuple[str, str]]) -> Iterator[Tuple[str, str]]:
        """
        Processes an iterator of (tag, line) tuples, converts lines to snake_case,
        and yields them tagged 'end'.

        Args:
            lines: An iterator yielding (tag, line) tuples.

        Yields:
            (next_tag, processed_line) tuples, where next_tag is 'end'.
        """
        logging.info("SnakecaseProcessor received lines.")
        for current_tag, line in lines:
            # Convert line to snake_case
            # This is a simple conversion; more robust logic might be needed for complex cases.
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', line)
            snake_case_line = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

            logging.info(f"SnakecaseProcessor: Converted '{line}' to '{snake_case_line}'. Emitting 'end'.")
            # After formatting, send the line to the 'end' state.
            yield 'end', snake_case_line

# You can add more formatter processors here as needed.
