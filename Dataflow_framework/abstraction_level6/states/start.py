# This is abstraction-level-6/states/start.py
# The initial state processor.

import sys # Needed for sys.stderr
from typing import Iterator, Optional, Tuple
# Import base class and types using relative imports from the parent package (states)
# Need to go up one level to abstraction-level-6, then down into types
from ..types import StateProcessor, ProcessorConfig, TaggedLine, START_TAG

class InitialTagger(StateProcessor):
     """
     The processor for the 'start' state. Takes raw lines (implicitly tagged 'start')
     and emits them with a configurable initial tag, or routes them based on content.
     """
     def __init__(self, tag: str, config: Optional[ProcessorConfig] = None):
         # This processor is associated with the START_TAG
         super().__init__(tag, config)
         # Configurable initial tag for routing after start
         self.next_tag = self.config.get("next_tag", "process") # Default tag after 'start'

         # Optional: Add content-based rules here if 'start' should route directly
         # self.rules = self.config.get("rules", [])
         # self.default_next_tag = self.config.get("default_next_tag", self.next_tag)

         # print(f"DEBUG: Initialized InitialTagger for state '{self.tag}' with next_tag='{self.next_tag}'", file=sys.stderr) # Optional debug


     def process(self, lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
         """
         Processes lines received in the 'start' state.
         Yields (next_tag, line) for routing.
         """
         # print(f"DEBUG: InitialTagger for state '{self.tag}' processing stream...", file=sys.stderr) # Optional debug
         for incoming_tag, line in lines:
             # In the 'start' state, the incoming_tag should always be START_TAG.
             # We yield the line with the configured next_tag.
             # print(f"DEBUG: InitialTagger '{self.tag}' yielding ('{self.next_tag}', '{line}')", file=sys.stderr) # Optional debug
             yield (self.next_tag, line)

             # Optional: Implement content-based routing here instead of a separate tagger state
             # emitted = False
             # for rule in self.rules:
             #     tag = rule.get("tag", self.default_next_tag)
             #     contains_text = rule.get("contains")
             #     if contains_text is not None and contains_text in line:
             #         yield (tag, line)
             #         emitted = True
             #         break
             # if not emitted:
             #     yield (self.default_next_tag, line)

         # print(f"DEBUG: InitialTagger for state '{self.tag}' finished stream.", file=sys.stderr) # Optional debug

