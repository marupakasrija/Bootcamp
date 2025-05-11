# State-Based Routing Engine with Automated Folder Monitor and Recovery

This project extends the state-based routing engine with the capability to continuously monitor a designated folder for new files, process them automatically, and recover from interruptions, making it a self-running and fault-tolerant system. Real-time observability via a web dashboard is maintained.

## Purpose

This level transforms the routing engine into a durable, autonomous daemon capable of handling continuous data ingestion. It mimics real-world scenarios where systems must process incoming files reliably, even in the face of crashes or restarts.

Key capabilities added in this level:

* **Folder Monitoring:** Continuously scans a directory for new input files.
* **File Lifecycle Management:** Moves files through `unprocessed`, `underprocess`, and `processed` states using atomic operations.
* **Recovery:** On startup, automatically moves files from `underprocess` back to `unprocessed` for retry.
* **Continuous Processing:** The engine runs indefinitely, processing lines from files as they are added to the queue by the monitor.
* **Dashboard Updates:** The web dashboard is updated to reflect the status of file processing.

## Core Concepts

* **Folder Queue:** A structured directory (`watch_dir`) with subdirectories (`unprocessed`, `underprocess`, `processed`) representing the state of files.
* **File Lifecycle:** The defined steps a file takes from arrival (`unprocessed`) to completion (`processed`).
* **Recovery:** The process of resetting files in `underprocess` to `unprocessed` on startup to ensure they are re-attempted.
* **File Monitor:** A background thread that polls the `unprocessed` directory for new files.
* **Line Tracking per File:** The engine tracks how many lines from each file are still active in the processing queue to determine when a file is fully processed.
* **Observability:** Metrics, tracing, and error reporting (from Level 7) are maintained and updated with file-specific context.
* **Dashboard:** The FastAPI dashboard now includes endpoints to show the state of files in the watched directories.

## Project Structure

```
routing_engine/
├── config/
│   └── config.yaml         # Defines tag-to-processor mapping
├── dashboard/
│   └── server.py           # FastAPI web server and endpoints (updated for file state)
├── processors/
│   ├── __init__.py         # Makes processors a Python package
│   ├── filters.py          # Filtering processors (updated for file_path)
│   ├── formatters.py       # Formatting processors (updated for file_path)
│   ├── output.py           # Final output processor (updated for file_path)
│   └── start.py            # Initial tagging processor (updated for file_path)
├── watch_dir/              # New directory to be monitored (created by main.py)
│   ├── unprocessed/     # Incoming files land here
│   ├── underprocess/    # Files currently being processed
│   └── processed/       # Successfully processed files
├── router.py               # Core routing engine logic, metrics, tracing, error handling, and file completion
└── main.py                 # Entry point with CLI args, threading, directory setup, recovery, and monitor startup
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
    This will set up the `watch_dir` structure (if it doesn't exist), perform recovery, start the routing engine, the dashboard server on `http://127.0.0.1:8000`, and the file monitor.

    To **enable tracing**, add the `--trace` flag:
    ```bash
    python main.py --trace
    ```

    You can also customize the dashboard port, host, watch directory, and monitor polling interval:
    ```bash
    python main.py --watch-dir /path/to/my/files --poll-interval 10 --dashboard-port 8080
    ```

3.  **Place Text Files:** While the system is running, place plain text files into the `watch_dir/unprocessed` directory. The monitor will automatically detect and process them.

4.  **Access the Dashboard:** Open your web browser and go to `http://127.0.0.1:8000/docs` (or the host/port you specified) to see the FastAPI interactive documentation (Swagger UI).

## Dashboard Endpoints

Access these endpoints via your web browser or tools like `curl` after running `main.py`:

* **`/stats`**: Returns live processor metrics (received count, emitted count, total processing time, error count).
* **`/traces`**: Returns recent line traces, including the file path (only if `--trace` is enabled).
* **`/errors`**: Returns recent errors, including the processor/source, message, line, and file path.
* **`/file_state`**: Returns the current state of file processing, including counts in each directory (`unprocessed`, `underprocess`, `processed`), the name of the file currently being processed, and a history of recently processed files.

## Output

The console output will show logging messages detailing the system's activity: directory setup, recovery, monitor polling, files being found and moved, lines being added to the queue, processor actions, and lines reaching the `FINAL OUTPUT` state (including the source file path).

Here is a sample of the console output when files are placed in the `unprocessed` directory:

```
PS D:\Bootcamp\Dataflow_framework\abstraction_level8> python main.py --trace --dashboard-port 8001 --dashboard-host 0.0.0.0
2025-05-11 21:26:44,820 - INFO - Ensured directory exists: watch_dir\unprocessed
2025-05-11 21:26:44,821 - INFO - Ensured directory exists: watch_dir\underprocess
2025-05-11 21:26:44,821 - INFO - Ensured directory exists: watch_dir\processed
2025-05-11 21:26:44,822 - INFO - Performing recovery: Checking for files in underprocess...
2025-05-11 21:26:44,822 - INFO - No files found in underprocess/. Recovery complete.
2025-05-11 21:26:44,822 - INFO - Loading configuration from config/config.yaml
2025-05-11 21:26:44,841 - INFO - Configuration loaded successfully.
2025-05-11 21:26:44,842 - INFO - Loading processors...
2025-05-11 21:26:44,844 - INFO - Loaded processor for tag 'start': processors.start.TagLinesProcessor
2025-05-11 21:26:44,846 - INFO - Loaded processor for tag 'error': processors.filters.OnlyErrorProcessor
2025-05-11 21:26:44,846 - INFO - Loaded processor for tag 'warn': processors.filters.OnlyWarnProcessor
2025-05-11 21:26:44,848 - INFO - Loaded processor for tag 'general': processors.formatters.SnakecaseProcessor
2025-05-11 21:26:44,849 - INFO - Loaded processor for tag 'end': processors.output.TerminalOutputProcessor
2025-05-11 21:26:44,849 - INFO - Finished loading 5 processors.
2025-05-11 21:26:44,849 - INFO - Routing engine initialized. Tracing enabled: True
2025-05-11 21:26:44,850 - INFO - Initial file counts: {'unprocessed': 3, 'underprocess': 0, 'processed': 0}
2025-05-11 21:26:44,851 - INFO - Starting dashboard server on [http://0.0.0.0:8001](http://0.0.0.0:8001)
INFO:       Started server process [24364]
INFO:       Waiting for application startup.
INFO:       Application startup complete.
INFO:       Uvicorn running on [http://0.0.0.0:8001](http://0.0.0.0:8001) (Press CTRL+C to quit)
2025-05-11 21:26:45,853 - INFO - Dashboard running at [http://0.0.0.0:8001/docs](http://0.0.0.0:8001/docs)
2025-05-11 21:26:45,854 - INFO - Starting file monitor loop for 'watch_dir\unprocessed'. Polling every 5 seconds.
2025-05-11 21:26:45,854 - INFO - File monitor thread started.
2025-05-11 21:26:45,855 - INFO - Found new file: sample_errors.txt
2025-05-11 21:26:45,855 - INFO - Starting main routing engine processing loop.
2025-05-11 21:26:45,856 - INFO - Starting continuous queue processing.
2025-05-11 21:26:45,857 - INFO - Moved 'sample_errors.txt' to underprocess/.
2025-05-11 21:26:45,858 - INFO - Added 5 lines from 'sample_errors.txt' to the processing queue.
2025-05-11 21:26:45,859 - INFO - Found new file: sample_general.txt
2025-05-11 21:26:45,860 - INFO - Moved 'sample_general.txt' to underprocess/.
2025-05-11 21:26:45,860 - INFO - Added 5 lines from 'sample_general.txt' to the processing queue.
2025-05-11 21:26:45,861 - INFO - Found new file: sample_warnings.txt
2025-05-11 21:26:45,862 - INFO - Moved 'sample_warnings.txt' to underprocess/.
2025-05-11 21:26:45,863 - INFO - Added 5 lines from 'sample_warnings.txt' to the processing queue.
FINAL OUTPUT [Tag: end] (File: watch_dir\underprocess\sample_general.txt): user_logged_in
FINAL OUTPUT [Tag: end] (File: watch_dir\underprocess\sample_warnings.txt): user login attempt from unknown ip.
FINAL OUTPUT [Tag: end] (File: watch_dir\underprocess\sample_warnings.txt): warn: _database connection slow.
FINAL OUTPUT [Tag: end] (File: watch_dir\underprocess\sample_errors.txt): error: _disk full. _cannot write data.
FINAL OUTPUT [Tag: end] (File: watch_dir\underprocess\sample_warnings.txt): warn: _low memory detected.
2025-05-11 21:26:46,863 - INFO - All lines from file 'watch_dir\underprocess\sample_errors.txt' processed. Moving to 'processed'.
2025-05-11 21:26:46,864 - INFO - Moved 'watch_dir\underprocess\sample_errors.txt' to 'watch_dir\processed\sample_errors.txt'.
2025-05-11 21:26:46,865 - INFO - All lines from file 'watch_dir\underprocess\sample_warnings.txt' processed. Moving to 'processed'.
2025-05-11 21:26:46,866 - INFO - Moved 'watch_dir\underprocess\sample_warnings.txt' to 'watch_dir\processed\sample_warnings.txt'.
2025-05-11 21:26:46,867 - INFO - All lines from file 'watch_dir\underprocess\sample_general.txt' processed. Moving to 'processed'.
2025-05-11 21:26:46,867 - INFO - Moved 'watch_dir\underprocess\sample_general.txt' to 'watch_dir\processed\sample_general.txt'.
2025-05-11 21:26:46,867 - INFO - Queue processing finished.
2025-05-11 21:26:46,868 - WARNING - Processing finished, but 8 lines did not reach the 'end' state.
2025-05-11 21:26:46,868 - INFO - Routing engine finished processing.
```

Accessing the dashboard endpoints will provide live JSON data reflecting the processing state.

## Extending the Engine and Observability

* **Handling Partial Files:** Implement a mechanism (e.g., checking file size stability over a few poll intervals, using a dedicated "landing" zone) to ensure files are fully written before moving them to `underprocess`.
* **Parallel File Processing:** Modify the `file_monitor_loop` to add files to a separate queue or use a thread pool to process multiple files concurrently.
* **Error Handling:** Implement strategies for handling files that consistently cause processing errors (e.g., move to an "error" directory after N retries).
* **Persistent State:** Store metrics, traces, and file state in a database for longer retention and analysis beyond the application's runtime.
* **Distributed System:** Adapt the monitoring and processing logic for a multi-node environment (e.g., using a distributed queue, shared storage, and a coordination service).
* **Advanced Dashboard:** Build a richer frontend visualization using JavaScript frameworks to display the data from the API endpoints in charts, tables, and interactive graphs.

This level provides a robust foundation for building production-grade file ingestion and processing systems that are autonomous, resilient, and observable.
