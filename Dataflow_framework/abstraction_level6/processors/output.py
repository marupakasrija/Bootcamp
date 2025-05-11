# processors/output.py

import logging
from typing import Iterator, Tuple

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TerminalOutputProcessor:
    """
    Processor that prints the final processed lines to the terminal.
    This processor is typically used for lines tagged 'end'.
    It does not emit any further tags, effectively terminating the line's journey.
    """
    def process(self, lines: Iterator[Tuple[str, str]]) -> Iterator[Tuple[str, str]]:
        """
        Processes an iterator of (tag, line) tuples by printing the lines.
        Does not yield any output, as this is an end state.

        Args:
            lines: An iterator yielding (tag, line) tuples.

        Yields:
            Nothing.
        """
        logging.info("TerminalOutputProcessor received lines tagged 'end'.")
        for current_tag, line in lines:
            # Print the final processed line.
            print(f"FINAL OUTPUT [Tag: {current_tag}]: {line}")
            logging.info(f"TerminalOutputProcessor: Printed line '{line}'.")

        # This is the crucial part: explicitly yield nothing to ensure
        # the method always returns an empty iterator, fulfilling the
        # requirement of a generator function.
        if False: # This condition is always false, so the yield never executes
            yield # But its presence makes the method a generator

# The method finishes here. Because it contains a 'yield' keyword, it is
# treated as a generator function and will always return an iterator.
# If the loop runs, the iterator is consumed. If the loop doesn't run,
# the 'yield' statement is never reached, but the function still returns
# an empty generator iterator, which is the desired behavior.
