# State-Based Routing Engine with Observability

This project implements a state-based routing engine in Python, enhanced with real-time observability features including metrics collection, execution tracing, and a simple web dashboard built with FastAPI.

## Purpose

Building upon the core state-based routing logic, this level adds the capability to monitor and understand the system's behavior in real-time. This is crucial for operating the system effectively, debugging issues, identifying bottlenecks, and gaining insights into how data flows through the defined states.

Key capabilities added in this level:

* **Metrics:** Track counts (received, emitted, errors) and processing time per processor.
* **Tracing:** Optionally record the path (sequence of tags/states) each line takes through the engine.
* **Dashboard:** Expose live metrics, recent traces, and errors via a simple web API using FastAPI.
* **Concurrency:** Run the processing engine and the dashboard concurrently using threading.

## Core Concepts

* **Lines:** Units of data flowing through the system (strings), now also carrying an optional **Trace** history.
* **Tags:** Labels attached to lines determining their current state and next processor.
* **Processors:** Python classes registered under tags, processing lines and emitting them with new tags. Processors now contribute to **Metrics** and **Error** tracking.
* **States:** Represented by tags.
* **Routing:** Dynamic, tag-based transitions between processors.
* **'start' Tag:** Entry point.
* **'end' Tag:** Exit point.
* **Metrics Store:** A shared, thread-safe structure (`dict` with `threading.Lock`) holding live counts and timing data for each processor.
* **Trace History:** A shared, thread-safe structure (`collections.deque` with `threading.Lock`) storing the recent journey of lines if tracing is enabled.
* **Error History:** A shared, thread-safe structure (`collections.deque` with `threading.Lock`) storing details of recent exceptions or processing errors.
* **Dashboard:** A FastAPI application running in a separate thread, providing API endpoints to access the metrics, traces, and errors.

## Project Structure

```
routing_engine/
├── config/
│   └── config.yaml         # Defines tag-to-processor mapping
├── dashboard/
│   └── server.py           # FastAPI web server and endpoints
├── processors/
│   ├── __init__.py         # Makes processors a Python package
│   ├── filters.py          # Filtering processors (updated for tracing/metrics)
│   ├── formatters.py       # Formatting processors (updated for tracing/metrics)
│   ├── output.py           # Final output processor (updated for tracing/metrics)
│   └── start.py            # Initial tagging processor (updated for tracing/metrics)
├── router.py               # Core routing engine logic, metrics, tracing, and error handling
└── main.py                 # Entry point with CLI args, threading, and engine execution
```

## Setup and Installation

1.  **Clone or download the project files.** Ensure you have the directory structure as shown above.
2.  **Make sure you have Python installed.** This project was developed with Python 3.
3.  **Install required libraries.** Open your terminal or command prompt, navigate to the `routing_engine` directory, and run:
    ```bash
    pip install PyYAML fastapi uvicorn
    ```
4.  **Optional Libraries:** If you want to enable the (currently commented out) static graph visualization feature in `router.py`, install `networkx` and `matplotlib`:
    ```bash
    pip install networkx matplotlib
    ```

## How to Run

1.  **Navigate to the project directory** in your terminal:
    ```bash
    cd path/to/routing_engine
    ```
2.  **Run the main script:**
    ```bash
    python main.py
    ```
    This will start the routing engine and the dashboard server on `http://127.0.0.1:8000` by default.

    To **enable tracing**, add the `--trace` flag:
    ```bash
    python main.py --trace
    ```

    You can also specify the dashboard port and host:
    ```bash
    python main.py --dashboard-port 8001 --dashboard-host 0.0.0.0
    ```

3.  **Access the Dashboard:** Open your web browser and go to `http://127.0.0.1:8000/docs` (or the host/port you specified). This will show the FastAPI interactive documentation (Swagger UI).

## Dashboard Endpoints

Access these endpoints via your web browser or tools like `curl` after running `main.py`:

* **`/stats`**: Returns a JSON object containing live metrics for each processor (received count, emitted count, total processing time, error count).
    * Example: `http://127.0.0.1:8000/stats`
* **`/traces`**: Returns a JSON list of recent line traces. Each entry shows the line content and the sequence of tags (states) it passed through. Only available if `--trace` is enabled.
    * Example: `http://127.0.0.1:8000/traces`
* **`/errors`**: Returns a JSON list of recent errors logged by the engine or processors. Each entry includes the processor/source, the error message, and the line being processed when the error occurred.
    * Example: `http://127.0.0.1:8000/errors`


## Output

The console output will show logging messages from the routing engine's processing loop, including lines reaching the `FINAL OUTPUT` state.
Accessing the dashboard endpoints in your browser or via API calls will provide the live metrics, traces, and error information as JSON responses.

```bash
PS D:\Bootcamp\Dataflow_framework\abstraction_level7> python main.py
2025-05-11 20:39:35,570 - INFO - Loading configuration from config/config.yaml
2025-05-11 20:39:35,572 - INFO - Configuration loaded successfully.
2025-05-11 20:39:35,572 - INFO - Loading processors...
2025-05-11 20:39:35,575 - INFO - Loaded processor for tag 'start': processors.start.TagLinesProcessor
2025-05-11 20:39:35,576 - INFO - Loaded processor for tag 'error': processors.filters.OnlyErrorProcessor
2025-05-11 20:39:35,577 - INFO - Loaded processor for tag 'warn': processors.filters.OnlyWarnProcessor
2025-05-11 20:39:35,577 - INFO - Loaded processor for tag 'general': processors.formatters.SnakecaseProcessor
2025-05-11 20:39:35,578 - INFO - Loaded processor for tag 'end': processors.output.TerminalOutputProcessor
2025-05-11 20:39:35,578 - INFO - Finished loading 5 processors.
2025-05-11 20:39:35,578 - INFO - Routing engine initialized. Tracing enabled: False
2025-05-11 20:39:35,580 - INFO - Starting dashboard server on http://127.0.0.1:8000
INFO:     Started server process [20512]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
2025-05-11 20:39:36,582 - INFO - Adding 8 initial lines to the engine.
2025-05-11 20:39:36,582 - INFO - Starting queue processing.
FINAL OUTPUT [Tag: end]: another general line.
FINAL OUTPUT [Tag: end]: camel_case_example_line
FINAL OUTPUT [Tag: end]: error: _something went wrong.
2025-05-11 20:39:36,584 - INFO - Queue processing finished.
2025-05-11 20:39:36,584 - WARNING - Processing finished, but 8 lines did not reach the 'end' state.
2025-05-11 20:39:36,585 - INFO - Routing engine finished processing.

Routing engine processing finished. Dashboard server is still running.
Access dashboard at http://127.0.0.1:8000/docs
Press Ctrl+C to exit.
2025-05-11 20:39:38,800 - INFO - Shutdown signal received. Exiting.
PS D:\Bootcamp\Dataflow_framework\abstraction_level7> python main.py --trace
2025-05-11 20:39:43,590 - INFO - Loading configuration from config/config.yaml
2025-05-11 20:39:43,593 - INFO - Configuration loaded successfully.
2025-05-11 20:39:43,593 - INFO - Loading processors...
2025-05-11 20:39:43,596 - INFO - Loaded processor for tag 'start': processors.start.TagLinesProcessor
2025-05-11 20:39:43,598 - INFO - Loaded processor for tag 'error': processors.filters.OnlyErrorProcessor
2025-05-11 20:39:43,599 - INFO - Loaded processor for tag 'warn': processors.filters.OnlyWarnProcessor
2025-05-11 20:39:43,600 - INFO - Loaded processor for tag 'general': processors.formatters.SnakecaseProcessor
2025-05-11 20:39:43,601 - INFO - Loaded processor for tag 'end': processors.output.TerminalOutputProcessor
2025-05-11 20:39:43,602 - INFO - Finished loading 5 processors.
2025-05-11 20:39:43,602 - INFO - Routing engine initialized. Tracing enabled: True
2025-05-11 20:39:43,604 - INFO - Starting dashboard server on http://127.0.0.1:8000
INFO:     Started server process [2152]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
2025-05-11 20:39:44,606 - INFO - Adding 8 initial lines to the engine.
2025-05-11 20:39:44,608 - INFO - Starting queue processing.
FINAL OUTPUT [Tag: end]: error: _something went wrong.
FINAL OUTPUT [Tag: end]: another general line.
2025-05-11 20:39:44,609 - INFO - Queue processing finished.
2025-05-11 20:39:44,610 - WARNING - Processing finished, but 8 lines did not reach the 'end' state.
2025-05-11 20:39:44,610 - INFO - Routing engine finished processing.

Routing engine processing finished. Dashboard server is still running.
Access dashboard at http://127.0.0.1:8000/docs
Press Ctrl+C to exit.
2025-05-11 20:39:47,672 - INFO - Shutdown signal received. Exiting.
PS D:\Bootcamp\Dataflow_framework\abstraction_level7> python main.py --trace --dashboard-port 8001 --dashboard-host 0.0.0.0
2025-05-11 20:39:52,201 - INFO - Loading configuration from config/config.yaml
2025-05-11 20:39:52,204 - INFO - Configuration loaded successfully.
2025-05-11 20:39:52,204 - INFO - Loading processors...
2025-05-11 20:39:52,207 - INFO - Loaded processor for tag 'start': processors.start.TagLinesProcessor
2025-05-11 20:39:52,208 - INFO - Loaded processor for tag 'error': processors.filters.OnlyErrorProcessor
2025-05-11 20:39:52,208 - INFO - Loaded processor for tag 'warn': processors.filters.OnlyWarnProcessor
2025-05-11 20:39:52,210 - INFO - Loaded processor for tag 'general': processors.formatters.SnakecaseProcessor
2025-05-11 20:39:52,211 - INFO - Loaded processor for tag 'end': processors.output.TerminalOutputProcessor
2025-05-11 20:39:52,211 - INFO - Finished loading 5 processors.
2025-05-11 20:39:52,212 - INFO - Routing engine initialized. Tracing enabled: True
2025-05-11 20:39:52,213 - INFO - Starting dashboard server on http://0.0.0.0:8001
INFO:     Started server process [3000]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
2025-05-11 20:39:53,214 - INFO - Adding 8 initial lines to the engine.
2025-05-11 20:39:53,215 - INFO - Starting queue processing.
FINAL OUTPUT [Tag: end]: this is a general message.
FINAL OUTPUT [Tag: end]: error in processing data.
FINAL OUTPUT [Tag: end]: warn: _low disk space.
2025-05-11 20:39:53,217 - INFO - Queue processing finished.
2025-05-11 20:39:53,217 - WARNING - Processing finished, but 8 lines did not reach the 'end' state.
2025-05-11 20:39:53,218 - INFO - Routing engine finished processing.

Routing engine processing finished. Dashboard server is still running.
Access dashboard at http://0.0.0.0:8001/docs
Press Ctrl+C to exit.
2025-05-11 20:40:40,044 - INFO - Shutdown signal received. Exiting.
```
## Extending the Engine and Observability

* **Add New Processors:** Create new processor classes and update `config.yaml`. Ensure new processors also append to the trace list if tracing is enabled and contribute to metrics/error reporting via the `RoutingEngine`.
* **More Detailed Metrics:** Add specific counters or timers within processors for fine-grained metrics (e.g., count of lines matching a specific pattern). Update the `RoutingEngine` and dashboard to expose these.
* **Advanced Tracing:** Store more context in the trace (e.g., timestamps for each state transition).
* **Improved Error Handling:** Implement retry logic, dead-letter queues, or more structured error reporting.
* **Frontend Dashboard:** Build a simple HTML/JavaScript frontend to visualize the JSON data from the FastAPI endpoints in a more user-friendly way.
* **Persistent Storage:** Store metrics, traces, and errors in a database instead of in-memory deques for longer history and more complex querying.
* **Distributed System:** Consider how metrics, tracing, and error reporting would change in a multi-machine environment (e.g., using a centralized logging system, distributed tracing tools, and a time-series database for metrics).

This level transforms the routing engine from a simple processing loop into a system that can be monitored and understood while it's running, a critical step towards building production-ready applications.
