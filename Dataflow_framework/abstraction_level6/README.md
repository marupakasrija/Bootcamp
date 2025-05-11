## Routing Engine Details: Structure, Input/Output, and Flow

This document provides a deeper dive into the architecture and operation of the state-based routing engine.

### Project Structure Explained

The project is organized into a logical directory structure to separate configuration, processing logic, and the core engine mechanics:

```
routing_engine/
├── config/
│   └── config.yaml         # Configuration file defining the mapping between state tags and processor classes. This is where you configure the routing graph.
├── processors/
│   ├── __init__.py         # An empty file that tells Python the 'processors' directory is a package. This allows importing modules from within it (e.g., `processors.filters`).
│   ├── filters.py          # Contains processor classes whose primary role is to conditionally pass or discard lines based on their content or characteristics.
│   ├── formatters.py       # Contains processor classes that transform or modify the content of lines.
│   ├── output.py           # Contains the processor responsible for handling lines that have reached the 'end' state, typically performing a final action like printing or saving.
│   └── start.py            # Contains the initial processor that takes raw input lines and assigns them their first routing tag, directing them into the system's flow.
├── router.py               # This is the heart of the engine. It contains the `RoutingEngine` class which loads the config, manages processor instances, handles the routing queue, and executes the main processing loop.
└── main.py                 # The main script to run the application. It initializes the engine, provides the initial data input, and starts the processing.
```

This structure promotes modularity. You can add new types of processors or modify existing ones without changing the core `router.py` logic, as long as they adhere to the expected processor interface (`process` method).

### Input and Output

**Input:**

* **Initial Input:** Data enters the system as raw lines of text. These lines are explicitly added to the engine's internal queue using the `engine.add_line(tag, line)` method.
* **Entry Point ('start'):** All initial lines *must* be added with the tag `'start'`. This designates them as new data entering the routing process.
* **Processor Input:** Internally, processors receive data as an iterator of `(tag, line)` tuples. The `RoutingEngine` feeds lines to the appropriate processor one by one (or potentially in batches in a more advanced version). The `tag` received by the processor is the tag under which that processor is registered in the configuration.

**Output:**

* **Processor Output:** Processors produce output by *yielding* `(next_tag, processed_line)` tuples from their `process` method.
    * `next_tag`: The tag assigned to the line for the next routing step. This determines which processor will receive the line next.
    * `processed_line`: The line after the processor has potentially modified or filtered it.
* **Exit Point ('end'):** A line's journey through the routing engine is considered complete when a processor emits it with the tag `'end'`.
* **Final Output:** Lines tagged `'end'` are sent to the processor registered under the `'end'` tag (e.g., `TerminalOutputProcessor`). This final processor performs the designated output action (like printing) and does *not* yield any further `(tag, line)` tuples, effectively removing the line from the routing queue.

```text
PS D:\Bootcamp\Dataflow_framework\abstraction_level6> python main.py
2025-05-11 20:02:58,959 - INFO - Loading configuration from config/config.yaml
2025-05-11 20:02:58,962 - INFO - Configuration loaded successfully.
2025-05-11 20:02:58,962 - INFO - Loading processors...
2025-05-11 20:02:58,966 - INFO - Loaded processor for tag 'start': processors.start.TagLinesProcessor
2025-05-11 20:02:58,967 - INFO - Loaded processor for tag 'error': processors.filters.OnlyErrorProcessor
2025-05-11 20:02:58,967 - INFO - Loaded processor for tag 'warn': processors.filters.OnlyWarnProcessor
2025-05-11 20:02:58,968 - INFO - Loaded processor for tag 'general': processors.formatters.SnakecaseProcessor
2025-05-11 20:02:58,970 - INFO - Loaded processor for tag 'end': processors.output.TerminalOutputProcessor
2025-05-11 20:02:58,970 - INFO - Finished loading 5 processors.
2025-05-11 20:02:58,970 - INFO - Adding 8 initial lines to the engine.
2025-05-11 20:02:58,971 - INFO - Adding line to queue with tag 'start': This is a general message.
2025-05-11 20:02:58,971 - INFO - Adding line to queue with tag 'start': ERROR: Something went wrong.
2025-05-11 20:02:58,971 - INFO - Adding line to queue with tag 'start': A warning occurred WARN.
2025-05-11 20:02:58,972 - INFO - Adding line to queue with tag 'start': Another general line.
2025-05-11 20:02:58,972 - INFO - Adding line to queue with tag 'start': ERROR in processing data.
2025-05-11 20:02:58,972 - INFO - Adding line to queue with tag 'start': WARN: Low disk space.
2025-05-11 20:02:58,973 - INFO - Adding line to queue with tag 'start': CamelCaseExampleLine
2025-05-11 20:02:58,973 - INFO - Adding line to queue with tag 'start': AnotherLineToProcess
2025-05-11 20:02:58,973 - INFO - Starting queue processing.
2025-05-11 20:02:58,974 - INFO - TagLinesProcessor received lines tagged 'start'.
2025-05-11 20:02:58,974 - INFO - TagLinesProcessor: Tagging line 'This is a general message.' with 'warn'.
2025-05-11 20:02:58,974 - INFO - TagLinesProcessor received lines tagged 'start'.
2025-05-11 20:02:58,974 - INFO - TagLinesProcessor: Tagging line 'ERROR: Something went wrong.' with 'general'.
2025-05-11 20:02:58,974 - INFO - TagLinesProcessor received lines tagged 'start'.
2025-05-11 20:02:58,974 - INFO - TagLinesProcessor: Tagging line 'A warning occurred WARN.' with 'warn'.
2025-05-11 20:02:58,975 - INFO - TagLinesProcessor received lines tagged 'start'.
2025-05-11 20:02:58,975 - INFO - TagLinesProcessor: Tagging line 'Another general line.' with 'error'.
2025-05-11 20:02:58,975 - INFO - TagLinesProcessor received lines tagged 'start'.
2025-05-11 20:02:58,975 - INFO - TagLinesProcessor: Tagging line 'ERROR in processing data.' with 'warn'.
2025-05-11 20:02:58,976 - INFO - TagLinesProcessor received lines tagged 'start'.
2025-05-11 20:02:58,977 - INFO - TagLinesProcessor: Tagging line 'WARN: Low disk space.' with 'warn'.
2025-05-11 20:02:58,978 - INFO - TagLinesProcessor received lines tagged 'start'.
2025-05-11 20:02:58,978 - INFO - TagLinesProcessor: Tagging line 'CamelCaseExampleLine' with 'warn'.
2025-05-11 20:02:58,978 - INFO - TagLinesProcessor received lines tagged 'start'.
2025-05-11 20:02:58,978 - INFO - TagLinesProcessor: Tagging line 'AnotherLineToProcess' with 'error'.
2025-05-11 20:02:58,978 - INFO - OnlyWarnProcessor received lines.
2025-05-11 20:02:58,979 - INFO - OnlyWarnProcessor: No WARN in 'This is a general message.'. Discarding.
2025-05-11 20:02:58,979 - INFO - SnakecaseProcessor received lines.
2025-05-11 20:02:58,980 - INFO - SnakecaseProcessor: Converted 'ERROR: Something went wrong.' to 'error: _something went wrong.'. Emitting 'end'.
2025-05-11 20:02:58,981 - INFO - OnlyWarnProcessor received lines.
2025-05-11 20:02:58,981 - INFO - OnlyWarnProcessor: Found WARN in 'A warning occurred WARN.'. Emitting 'general'.
2025-05-11 20:02:58,981 - INFO - OnlyErrorProcessor received lines.
2025-05-11 20:02:58,982 - INFO - OnlyErrorProcessor: No ERROR in 'Another general line.'. Discarding.
2025-05-11 20:02:58,982 - INFO - OnlyWarnProcessor received lines.
2025-05-11 20:02:58,982 - INFO - OnlyWarnProcessor: No WARN in 'ERROR in processing data.'. Discarding.
2025-05-11 20:02:58,982 - INFO - OnlyWarnProcessor received lines.
2025-05-11 20:02:58,982 - INFO - OnlyWarnProcessor: Found WARN in 'WARN: Low disk space.'. Emitting 'general'.
2025-05-11 20:02:58,982 - INFO - OnlyWarnProcessor received lines.
2025-05-11 20:02:58,983 - INFO - OnlyWarnProcessor: No WARN in 'CamelCaseExampleLine'. Discarding.
2025-05-11 20:02:58,983 - INFO - OnlyErrorProcessor received lines.
2025-05-11 20:02:58,983 - INFO - OnlyErrorProcessor: No ERROR in 'AnotherLineToProcess'. Discarding.
2025-05-11 20:02:58,983 - INFO - Line reached 'end' state: error: _something went wrong.
2025-05-11 20:02:58,983 - INFO - TerminalOutputProcessor received lines tagged 'end'.
FINAL OUTPUT [Tag: end]: error: _something went wrong.
2025-05-11 20:02:58,983 - INFO - TerminalOutputProcessor: Printed line 'error: _something went wrong.'.
2025-05-11 20:02:58,984 - INFO - SnakecaseProcessor received lines.
2025-05-11 20:02:58,984 - INFO - SnakecaseProcessor: Converted 'A warning occurred WARN.' to 'a warning occurred warn.'. Emitting 'end'.
2025-05-11 20:02:58,984 - INFO - SnakecaseProcessor received lines.
2025-05-11 20:02:58,984 - INFO - SnakecaseProcessor: Converted 'WARN: Low disk space.' to 'warn: _low disk space.'. Emitting 'end'.
2025-05-11 20:02:58,984 - INFO - Line reached 'end' state: a warning occurred warn.
2025-05-11 20:02:58,985 - INFO - TerminalOutputProcessor received lines tagged 'end'.
FINAL OUTPUT [Tag: end]: a warning occurred warn.
2025-05-11 20:02:58,985 - INFO - TerminalOutputProcessor: Printed line 'a warning occurred warn.'.
2025-05-11 20:02:58,985 - INFO - Line reached 'end' state: warn: _low disk space.
2025-05-11 20:02:58,985 - INFO - TerminalOutputProcessor received lines tagged 'end'.
FINAL OUTPUT [Tag: end]: warn: _low disk space.
2025-05-11 20:02:58,985 - INFO - TerminalOutputProcessor: Printed line 'warn: _low disk space.'.
2025-05-11 20:02:58,985 - INFO - Queue processing finished.
2025-05-11 20:02:58,986 - WARNING - Processing finished, but 8 lines did not reach the 'end' state.
2025-05-11 20:02:58,986 - INFO - Routing engine finished processing.
```

### Core Functionality and Flow

The core functionality resides within the `RoutingEngine` class in `router.py`. Its main responsibilities and the data flow are as follows:

1.  **Initialization:**
    * The `RoutingEngine` is created with a path to the configuration file (`config/config.yaml`).
    * It loads the configuration, which maps state tags (like 'start', 'error', 'warn', 'general', 'end') to specific Python processor classes.
    * It dynamically imports and instantiates all the required processor classes, storing them in a dictionary where keys are the tags and values are the processor instances.
    * An internal queue (`collections.deque`) is initialized to hold `(tag, line)` tuples waiting to be processed.

2.  **Adding Initial Data:**
    * The `main.py` script (or any external system) calls `engine.add_line('start', line)` for each initial piece of data.
    * Each `(start, line)` tuple is added to the `routing_queue`.

3.  **Processing Loop (`process_queue`):**
    * The `process_queue` method starts the main loop.
    * As long as the `routing_queue` is not empty and a safety limit (`max_processing_steps`) hasn't been reached, it continues:
        * It takes the oldest `(current_tag, line_to_process)` tuple from the *left* side of the `routing_queue` using `popleft()`.
        * **Check for 'end' state:** If `current_tag` is `'end'`, the line has reached its destination. The line is passed to the processor registered under the 'end' tag. This processor performs the final action (e.g., printing) and yields no further output. The line is then removed from the engine's active tracking.
        * **Find Processor:** If `current_tag` is *not* 'end', the engine looks up the processor instance associated with `current_tag` in its `self.processors` dictionary.
        * **Process Line:** The `process` method of the found processor is called, passing an iterator containing the single `(current_tag, line_to_process)` tuple.
        * **Handle Processor Output:** The engine iterates over the `(next_tag, processed_line)` tuples yielded by the processor's `process` method.
        * **Queue for Next Step:** For each yielded tuple, the `(next_tag, processed_line)` is added to the *right* side of the `routing_queue` using `append()`. These lines will be picked up for processing in a subsequent iteration of the loop.
        * **Filtering/Discarding:** If a processor does not yield any output for a given input line, that line is effectively discarded from the system and will not be processed further. This is how filtering works (e.g., in `OnlyErrorProcessor`).
    * The loop continues until the queue is empty (all lines have reached 'end' or been filtered out) or the maximum processing steps are reached (potentially indicating a cycle).

4.  **Completion:**
    * When `process_queue` finishes, the engine logs that processing is complete.
    * It also reports how many lines did *not* reach the 'end' state, which corresponds to the lines that were filtered out.

This dynamic, tag-based routing allows lines to follow different paths through the network of processors based on the logic within each processor, creating a powerful and flexible data processing system.
