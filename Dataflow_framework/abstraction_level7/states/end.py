# This is abstraction-level-7/states/end.py
# The final state processor (collects output). Adapted for TracedLine.

import sys # Needed for sys.stderr
from typing import Iterator, Optional, Tuple
# Import base class and types using relative imports from the parent package (states)
# Need to go up one level to abstraction-level-7, then down into types
from ..types import StateProcessor, ProcessorConfig, TracedLine, END_TAG

class OutputCollector(StateProcessor):
    """
    The processor for the 'end' state. It receives lines that have completed
    processing and are ready to be collected as final output. Handles TracedLine.
    """
    def __init__(self, tag: str, config: Optional[ProcessorConfig] = None):
        # This processor is associated with the END_TAG
        super().__init__(tag, config)
        # print(f"DEBUG: Initialized OutputCollector for state '{self.tag}'", file=sys.stderr) # Optional debug

    def process(self, lines: Iterator[TracedLine]) -> Iterator[TracedLine]:
        """
        Processes lines received in the 'end' state (as TracedLine).
        Yields the lines again with the END_TAG and updated history.
        The engine recognizes this tag as the signal to collect final output.
        """
        # print(f"DEBUG: OutputCollector for state '{self.tag}' processing stream...", file=sys.stderr) # Optional debug
        for line_id, incoming_tag, line_content, history in lines:
            # In the 'end' state, the incoming_tag should be END_TAG.
            # Update history and yield them again with the END_TAG for the engine to collect.
            updated_history = history + [self.tag] # Add current state to history
            # print(f"DEBUG: OutputCollector '{self.tag}' yielding ('{line_id}', '{END_TAG}', '{line_content}', {updated_history})", file=sys.stderr) # Optional debug
            yield (line_id, END_TAG, line_content, updated_history)
        # print(f"DEBUG: OutputCollector for state '{self.tag}' finished stream.", file=sys.stderr) # Optional debug

