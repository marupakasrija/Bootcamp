# This is abstraction-level-5/processors/taggers.py
# Contains processors that primarily focus on tagging lines for routing.

import sys # Needed for sys.stderr
from typing import Iterator, Optional, Tuple, Any, Dict
# Import base class and types using relative imports from the parent package
from ..types import TaggedStreamProcessor, ProcessorConfig, TaggedLine

class StartTagger(TaggedStreamProcessor):
     """
     Initial processor that tags all incoming lines with a configurable 'start' tag.
     This acts as the entry point for the DAG.
     """
     def __init__(self, name: str, config: Optional[ProcessorConfig] = None):
         super().__init__(name, config)
         # Configurable initial tag, defaults to 'start'
         self.start_tag = self.config.get("start_tag", "start")
         # print(f"DEBUG: Initialized StartTagger '{self.name}' with start_tag='{self.start_tag}'", file=sys.stderr) # Optional debug


     def process(self, lines: Iterator[str]) -> Iterator[TaggedLine]:
         """Processes lines and yields (start_tag, line)."""
         # print(f"DEBUG: StartTagger '{self.name}' processing stream...", file=sys.stderr) # Optional debug
         for line in lines:
             # Yield each incoming line tagged with the configured start tag
             # print(f"DEBUG: StartTagger '{self.name}' yielding ('{self.start_tag}', '{line}')", file=sys.stderr) # Optional debug
             yield (self.start_tag, line)
         # print(f"DEBUG: StartTagger '{self.name}' finished stream.", file=sys.stderr) # Optional debug


class ContentTagger(TaggedStreamProcessor):
    """
    Tags lines based on content matching rules.
    Emits a tag based on the first matching rule, or a default tag.
    """
    def __init__(self, name: str, config: Optional[ProcessorConfig] = None):
        super().__init__(name, config)
        # Config format: [{"tag": "tag_name", "contains": "text_to_match"}, ...]
        self.rules = self.config.get("rules", [])
        self.default_tag = self.config.get("default_tag", "default")
        # print(f"DEBUG: Initialized ContentTagger '{self.name}' with default_tag='{self.default_tag}' and {len(self.rules)} rules", file=sys.stderr) # Optional debug


    def process(self, lines: Iterator[str]) -> Iterator[TaggedLine]:
        """Processes lines and yields (tag, line) based on rules."""
        # print(f"DEBUG: ContentTagger '{self.name}' processing stream...", file=sys.stderr) # Optional debug
        for line in lines:
            emitted = False
            # Check each rule in order
            for rule in self.rules:
                tag = rule.get("tag", self.default_tag)
                contains_text = rule.get("contains")
                if contains_text is not None and contains_text in line:
                    # Found a match, yield with the rule's tag
                    # print(f"DEBUG: ContentTagger '{self.name}' matched rule for tag '{tag}', yielding ('{tag}', '{line}')", file=sys.stderr) # Optional debug
                    yield (tag, line)
                    emitted = True
                    # Optional: break after first match, or continue for multiple tags
                    # For simple routing, break is typical.
                    break
            if not emitted:
                # No rules matched, yield with the default tag
                # print(f"DEBUG: ContentTagger '{self.name}' no rule matched, yielding ('{self.default_tag}', '{line}')", file=sys.stderr) # Optional debug
                yield (self.default_tag, line)
        # print(f"DEBUG: ContentTagger '{self.name}' finished stream.", file=sys.stderr) # Optional debug


# Example of a processor that might filter lines (fan-in potential)
class ErrorOnlyProcessor(TaggedStreamProcessor):
    """
    Processes lines, only yielding those containing "ERROR" with a fixed tag.
    Can receive lines from multiple upstream nodes/tags.
    """
    def __init__(self, name: str, config: Optional[ProcessorConfig] = None):
        super().__init__(name, config)
        self.output_tag = self.config.get("output_tag", "error_processed")
        # print(f"DEBUG: Initialized ErrorOnlyProcessor '{self.name}' with output_tag='{self.output_tag}'", file=sys.stderr) # Optional debug

    def process(self, lines: Iterator[str]) -> Iterator[TaggedLine]:
        """Processes lines, yielding only error lines with a specific tag."""
        # print(f"DEBUG: ErrorOnlyProcessor '{self.name}' processing stream...", file=sys.stderr) # Optional debug
        for line in lines:
            if "ERROR" in line:
                # print(f"DEBUG: ErrorOnlyProcessor '{self.name}' found ERROR, yielding ('{self.output_tag}', '{line}')", file=sys.stderr) # Optional debug
                yield (self.output_tag, line)
            # else: line is dropped (not yielded)
        # print(f"DEBUG: ErrorOnlyProcessor '{self.name}' finished stream.", file=sys.stderr) # Optional debug


# Example of a processor that might format lines (fan-in potential)
class FormatterProcessor(TaggedStreamProcessor):
    """
    Processes lines, applies formatting, and yields with a fixed tag.
    Can receive lines from multiple upstream nodes/tags.
    """
    def __init__(self, name: str, config: Optional[ProcessorConfig] = None):
        super().__init__(name, config)
        self.output_tag = self.config.get("output_tag", "formatted")
        self.format_type = self.config.get("format_type", "uppercase") # e.g., 'uppercase', 'snakecase'
        # print(f"DEBUG: Initialized FormatterProcessor '{self.name}' with output_tag='{self.output_tag}', format_type='{self.format_type}'", file=sys.stderr) # Optional debug


    def process(self, lines: Iterator[str]) -> Iterator[TaggedLine]:
        """Processes lines, applies formatting, and yields with a specific tag."""
        # print(f"DEBUG: FormatterProcessor '{self.name}' processing stream...", file=sys.stderr) # Optional debug
        for line in lines:
            processed_line = line # Start with the original line
            if self.format_type == "uppercase":
                processed_line = line.strip().upper()
            elif self.format_type == "snakecase":
                processed_line = line.strip().lower().replace(" ", "_")
            # Add more formatting types as needed

            # print(f"DEBUG: FormatterProcessor '{self.name}' yielding ('{self.output_tag}', '{processed_line}')", file=sys.stderr) # Optional debug
            yield (self.output_tag, processed_line)
        # print(f"DEBUG: FormatterProcessor '{self.name}' finished stream.", file=sys.stderr) # Optional debug


# Example of a processor that might collect final output
class OutputCollector(TaggedStreamProcessor):
    """
    Collects lines and yields them with the special 'final_output' tag.
    This is the typical end node in a DAG that produces output.
    Can receive lines from multiple upstream nodes/tags.
    """
    def __init__(self, name: str, config: Optional[ProcessorConfig] = None):
        super().__init__(name, config)
        # This processor always yields with the 'final_output' tag by convention
        self.final_output_tag = "final_output"
        # print(f"DEBUG: Initialized OutputCollector '{self.name}'", file=sys.stderr) # Optional debug


    def process(self, lines: Iterator[str]) -> Iterator[TaggedLine]:
        """Processes lines and yields them with the 'final_output' tag."""
        # print(f"DEBUG: OutputCollector '{self.name}' processing stream...", file=sys.stderr) # Optional debug
        for line in lines:
            # print(f"DEBUG: OutputCollector '{self.name}' yielding ('{self.final_output_tag}', '{line}')", file=sys.stderr) # Optional debug
            yield (self.final_output_tag, line)
        # print(f"DEBUG: OutputCollector '{self.name}' finished stream.", file=sys.stderr) # Optional debug

