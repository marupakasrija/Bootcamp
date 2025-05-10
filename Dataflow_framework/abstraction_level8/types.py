# This is abstraction-level-8/types.py
# Defines type aliases and data models for Level 8 Observability and Folder Monitoring.

from collections import defaultdict
from typing import Callable, Iterator, Any, Dict, List, Optional, Tuple
import time # For timing metrics
import threading # For thread-safe data structures
import uuid # For unique line IDs

# --- Core Processing Types (Adapted for Tracing) ---

# Type: A line tagged with a routing key/state, now includes a unique ID and history
# (line_id, tag, line_content, trace_history)
# Note: line_id should uniquely identify the *original* line content across files and runs.
# For simplicity in L8, we'll generate a UUID per line per run, which is sufficient
# for tracing within a single run but not for tracking a line across crashes/restarts.
# A more robust system would hash the content or use a file_id + line_number.
TracedLine = Tuple[str, str, str, List[str]]

# New stream processor type: takes an iterator of TracedLine, yields an iterator of TracedLine
# Processors now receive lines *with* their current tag/history and emit lines with the *next* tag/updated history.
StateProcessorFn = Callable[[Iterator[TracedLine]], Iterator[TracedLine]]

# Define a base class for stateful, tag-emitting stream processors (States).
# Processors inheriting from this can maintain state and control the next state via tags.
# Adapted to receive and yield TracedLine.
class StateProcessor:
    """Base class for stateful stream processors acting as States."""
    def __init__(self, tag: str, config: Optional[Dict[str, Any]] = None):
        # Each processor instance is associated with a specific tag/state
        self.tag = tag
        self.config = config or {}

    def process(self, lines: Iterator[TracedLine]) -> Iterator[TracedLine]:
        """
        Processes an iterator of (id, tag, line, history) tuples and yields
        (id, next_tag, line, updated_history) tuples.
        The incoming tag is the current state; the yielded tag is the next state.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement process()")

    # Optional: Add setup/teardown methods if needed for resource management
    # def setup(self): pass
    # def teardown(self): pass

# Config types for State Transition System
ProcessorDefinitionConfig = Dict[str, Any] # Should include 'type' and optional config
StateConfig = Dict[str, ProcessorDefinitionConfig] # Maps tag (state) to processor definition {tag: {type: ..., config: ...}}
StateSystemConfig = Dict[str, Any] # Top level config including 'states'

# Define special tags
START_TAG = "start"
END_TAG = "end"

# --- Observability and Monitoring Types ---

# Data structure for capturing metrics per state/processor
class ProcessorMetrics:
    def __init__(self):
        self.lines_received: int = 0
        self.lines_emitted: int = 0
        self.processing_time_seconds: float = 0.0
        self.errors_count: int = 0
        self.last_activity_time: float = time.time() # Timestamp of last line processed

    def to_dict(self):
        return {
            "lines_received": self.lines_received,
            "lines_emitted": self.lines_emitted,
            "processing_time_seconds": round(self.processing_time_seconds, 4),
            "errors_count": self.errors_count,
            "last_activity_timestamp": self.last_activity_time # raw timestamp
        }

# Data structure for capturing recent errors
class ErrorData:
    def __init__(self, timestamp: float, state: str, message: str, line_id: str, line_content: str, file_name: Optional[str] = None):
        self.timestamp = timestamp
        self.state = state
        self.message = message
        self.line_id = line_id
        self.line_content = line_content # Capture the line content at the time of error
        self.file_name = file_name # File associated with the error

    def to_dict(self):
        return {
            "timestamp": self.timestamp, # raw timestamp
            "state": self.state,
            "message": self.message,
            "line_id": self.line_id,
            "line_content": self.line_content,
            "file_name": self.file_name
        }

# Data structure for capturing line traces
class LineTrace:
    def __init__(self, line_id: str, final_content: str, history: List[str], status: str = "completed", file_name: Optional[str] = None):
        self.line_id = line_id
        self.final_content = final_content
        self.history = history # List of states visited
        self.status = status # e.g., "completed", "dropped_loop", "dropped_error", "dropped_invalid_route", "dropped_max_iterations"
        self.file_name = file_name # File associated with the trace

    def to_dict(self):
        return {
            "line_id": self.line_id,
            "final_content": self.final_content,
            "history": self.history,
            "status": self.status,
            "file_name": self.file_name
        }

# Data structure for tracking file status
class FileStatus:
    UNPROCESSED = "unprocessed"
    UNDERPROCESS = "underprocess"
    PROCESSED = "processed"
    ERROR = "error" # New state for files that caused processing errors

    def __init__(self, file_name: str, status: str, timestamp: float):
        self.file_name = file_name
        self.status = status
        self.timestamp = timestamp # Timestamp of last status change

    def to_dict(self):
        return {
            "file_name": self.file_name,
            "status": self.status,
            "timestamp": self.timestamp
        }

# Shared data structure for observability data
class ObservabilityData:
    def __init__(self, max_traces: int = 1000, max_errors: int = 100, max_recent_files: int = 50):
        # Metrics: {state_tag: ProcessorMetrics instance}
        self.metrics: Dict[str, ProcessorMetrics] = defaultdict(ProcessorMetrics)
        # Traces: List of LineTrace instances (recent traces)
        self.traces: List[LineTrace] = []
        self.max_traces = max_traces
        # Errors: List of ErrorData instances (recent errors)
        self.errors: List[ErrorData] = []
        self.max_errors = max_errors

        # File Monitoring Data
        self.file_counts: Dict[str, int] = {
            FileStatus.UNPROCESSED: 0,
            FileStatus.UNDERPROCESS: 0,
            FileStatus.PROCESSED: 0,
            FileStatus.ERROR: 0 # New count for error state
        }
        self.current_file_processing: Optional[str] = None
        self.recent_files: List[FileStatus] = [] # List of recent file status changes
        self.max_recent_files = max_recent_files

        # Locks for thread-safe access
        self._metrics_lock = threading.Lock()
        self._traces_lock = threading.Lock()
        self._errors_lock = threading.Lock()
        self._file_status_lock = threading.Lock() # Lock for file monitoring data

    def update_metrics(self, state: str, received: int = 0, emitted: int = 0, processing_time: float = 0.0, errors: int = 0):
        with self._metrics_lock:
            metrics = self.metrics[state] # Accesses or creates the metrics for the state
            metrics.lines_received += received
            metrics.lines_emitted += emitted
            metrics.processing_time_seconds += processing_time
            metrics.errors_count += errors
            metrics.last_activity_time = time.time()

    def add_trace(self, line_trace: LineTrace):
        with self._traces_lock:
            self.traces.append(line_trace)
            # Keep only the most recent traces
            if len(self.traces) > self.max_traces:
                self.traces = self.traces[-self.max_traces:] # Keep the last N

    def add_error(self, error_data: ErrorData):
        with self._errors_lock:
            self.errors.append(error_data)
            # Keep only the most recent errors
            if len(self.errors) > self.max_errors:
                self.errors = self.errors[-self.max_errors:] # Keep the last N

    def update_file_status_counts(self, unprocessed: int, underprocess: int, processed: int, error: int):
         with self._file_status_lock:
             self.file_counts[FileStatus.UNPROCESSED] = unprocessed
             self.file_counts[FileStatus.UNDERPROCESS] = underprocess
             self.file_counts[FileStatus.PROCESSED] = processed
             self.file_counts[FileStatus.ERROR] = error # Update error count

    def set_current_file(self, file_name: Optional[str]):
         with self._file_status_lock:
             self.current_file_processing = file_name

    def add_recent_file(self, file_status: FileStatus):
         with self._file_status_lock:
             # Remove existing entry for the same file if it exists
             self.recent_files = [f for f in self.recent_files if f.file_name != file_status.file_name]
             self.recent_files.append(file_status)
             # Keep only the most recent file status changes
             if len(self.recent_files) > self.max_recent_files:
                 # Sort by timestamp and keep the last N
                 self.recent_files.sort(key=lambda f: f.timestamp)
                 self.recent_files = self.recent_files[-self.max_recent_files:]


    def get_metrics(self) -> Dict[str, Dict[str, Any]]:
        with self._metrics_lock:
            # Return a dictionary of dictionaries for easy JSON serialization
            return {tag: metrics.to_dict() for tag, metrics in self.metrics.items()}

    def get_traces(self, n: int = 100) -> List[Dict[str, Any]]:
        with self._traces_lock:
            # Return a list of dictionaries for easy JSON serialization
            return [trace.to_dict() for trace in self.traces[-n:]] # Get the last N traces

    def get_errors(self, n: int = 100) -> List[Dict[str, Any]]:
        with self._errors_lock:
            # Return a list of dictionaries for easy JSON serialization
            return [error.to_dict() for error in self.errors[-n:]] # Get the last N errors

    def get_file_status(self) -> Dict[str, Any]:
         with self._file_status_lock:
             return {
                 "file_counts": self.file_counts,
                 "current_file_processing": self.current_file_processing,
                 "recent_files": [f.to_dict() for f in self.recent_files]
             }

