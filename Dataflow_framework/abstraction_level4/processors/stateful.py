# This is abstraction-level-4/processors/stateful.py
# Contains stateful stream processor examples for Level 4.

import sys # Needed for sys.stderr
from typing import Iterator, Optional, Any, Dict, Tuple
# Import the base class and types using relative imports from the parent package
from ..types import StreamProcessor, ProcessorConfig

class LineCounterProcessor(StreamProcessor):
    """
    A stateful stream processor that adds a count to each line.
    Inherits from StreamProcessor to manage state (self.line_count).
    """
    def __init__(self, config: Optional[ProcessorConfig] = None):
        # Call the parent class constructor to handle config
        super().__init__(config)
        # Initialize state
        self.line_count = 0
        # Get configuration options with defaults
        self.prefix = self.config.get("prefix", "Line ")
        # print(f"DEBUG: Initialized LineCounterProcessor with prefix='{self.prefix}'", file=sys.stderr) # Optional debug

    def process(self, lines: Iterator[str]) -> Iterator[str]:
        """
        Processes an iterator of lines, adding a count and prefix to each.
        Maintains state (line_count) across calls within the same instance.
        """
        # print("DEBUG: LineCounterProcessor processing stream...", file=sys.stderr) # Optional debug
        for line in lines:
            self.line_count += 1
            processed_line = f"{self.prefix}{self.line_count}: {line}"
            # print(f"DEBUG: LineCounterProcessor yielding: {processed_line}", file=sys.stderr) # Optional debug
            yield processed_line
        # print("DEBUG: LineCounterProcessor finished stream.", file=sys.stderr) # Optional debug


class LineSplitterProcessor(StreamProcessor):
    """
    A stateful stream processor that splits lines on a delimiter (fan-out).
    Inherits from StreamProcessor.
    """
    def __init__(self, config: Optional[ProcessorConfig] = None):
        super().__init__(config)
        self.delimiter = self.config.get("delimiter", ",")
        # print(f"DEBUG: Initialized LineSplitterProcessor with delimiter='{self.delimiter}'", file=sys.stderr) # Optional debug

    def process(self, lines: Iterator[str]) -> Iterator[str]:
        """
        Processes an iterator of lines, splitting each incoming line
        and yielding multiple outgoing lines (fan-out).
        """
        # print("DEBUG: LineSplitterProcessor processing stream...", file=sys.stderr) # Optional debug
        for line in lines:
            # Split the line based on the configured delimiter
            parts = line.split(self.delimiter)
            # Yield each part after stripping whitespace
            for part in parts:
                processed_part = part.strip()
                # print(f"DEBUG: LineSplitterProcessor yielding part: {processed_part}", file=sys.stderr) # Optional debug
                yield processed_part
        # print("DEBUG: LineSplitterProcessor finished stream.", file=sys.stderr) # Optional debug


# Example of a function-based stream processor (without state or config)
# This function matches the StreamProcessorFn signature: Iterator[str] -> Iterator[str]
def add_prefix_stream(lines: Iterator[str]) -> Iterator[str]:
    """
    Stream processor function: Adds a simple prefix to each line in the stream.
    Matches StreamProcessorFn signature.
    """
    # print("DEBUG: add_prefix_stream processing stream...", file=sys.stderr) # Optional debug
    for line in lines:
        processed_line = f"[PROCESSED] {line}"
        # print(f"DEBUG: add_prefix_stream yielding: {processed_line}", file=sys.stderr) # Optional debug
        yield processed_line
    # print("DEBUG: add_prefix_stream finished stream.", file=sys.stderr) # Optional debug

