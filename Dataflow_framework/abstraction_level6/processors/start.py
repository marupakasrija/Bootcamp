# processors/start.py

import logging
from typing import Iterator, Tuple
import random

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TagLinesProcessor:
    """
    The initial processor for lines tagged 'start'.
    It takes raw lines and assigns them an initial tag ('error', 'warn', or 'general')
    based on some simple logic (randomly in this example).
    """
    def process(self, lines: Iterator[Tuple[str, str]]) -> Iterator[Tuple[str, str]]:
        """
        Processes an iterator of (tag, line) tuples (expected tag is 'start').
        Assigns an initial tag to each line and yields it for the next step.

        Args:
            lines: An iterator yielding (tag, line) tuples.

        Yields:
            (next_tag, processed_line) tuples with assigned initial tags.
        """
        logging.info("TagLinesProcessor received lines tagged 'start'.")
        possible_tags = ['error', 'warn', 'general']
        for current_tag, line in lines:
            # Simple logic to assign a tag: randomly pick one.
            # In a real system, this logic would inspect the line content, metadata, etc.
            next_tag = random.choice(possible_tags)
            logging.info(f"TagLinesProcessor: Tagging line '{line}' with '{next_tag}'.")
            yield next_tag, line

# You can add other initial processors here if you have different ways
# of starting the routing process.
