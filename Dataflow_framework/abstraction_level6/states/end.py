# This is abstraction-level-6/states/end.py
# The final state processor (collects output).

import sys # Needed for sys.stderr
from typing import Iterator, Optional, Tuple
# Import base class and types using relative imports from the parent package (states)
# Need to go up one level to abstraction-level-6, then down into types
from ..types import StateProcessor, ProcessorConfig, TaggedLine, END_TAG

class OutputCollector(StateProcessor):
    """
    The processor for the 'end' state. It receives lines that have completed
    processing and are ready to be collected as final output.
    """
    def __init__(self, tag: str, config: Optional[ProcessorConfig] = None):
        # This processor is associated with the END_TAG
        super().__init__(tag, config)
        # print(f"DEBUG: Initialized OutputCollector for state '{self.tag}'", file=sys.stderr) # Optional debug

    def process(self, lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
        """
        Processes lines received in the 'end' state.
        Yields the lines again with the END_TAG. The engine recognizes
        this tag as the signal to collect final output.
        """
        # print(f"DEBUG: OutputCollector for state '{self.tag}' processing stream...", file=sys.stderr) # Optional debug
        for incoming_tag, line in lines:
            # In the 'end' state, the incoming_tag should be END_TAG.
            # We yield them again with the END_TAG for the engine to collect.
            # print(f"DEBUG: OutputCollector '{self.tag}' yielding ('{END_TAG}', '{line}')", file=sys.stderr) # Optional debug
            yield (END_TAG, line)
        # print(f"DEBUG: OutputCollector for state '{self.tag}' finished stream.", file=sys.stderr) # Optional debug

