# State-Based Routing Engine with Automated Folder Monitor and Recovery

This project implements a state-based routing engine in Python, enhanced with real-time observability, automated file monitoring, recovery from interruptions, and simplified execution via a Makefile and dual operational modes.

## Purpose

This project simulates the foundations of production-grade data processing infrastructure. It demonstrates building a system that can:

* Process data streams through a modular, tag-based state machine.
* Provide real-time visibility into processing (metrics, tracing, errors).
* Autonomously monitor a file drop-off location.
* Handle system restarts gracefully by recovering in-progress files.
* Be easily run and managed using standard tools like Make and Docker.

## Core Concepts

* **Modular Processors:** Reusable components for data transformation and filtering.
* **State-Based Routing:** Dynamic flow control using tags attached to data lines.
* **Observability:** In-memory metrics, tracing, and error history exposed via a FastAPI dashboard.
* **Folder Queue:** A structured directory (`watch_dir`) with subdirectories (`unprocessed`, `underprocess`, `processed`) representing the state of files.
* **Recovery:** Startup logic to resume processing of interrupted files.
* **Execution Modes:** Support for processing a single file once (`--input`) or continuously monitoring a folder (`--watch`).
* **Concurrency:** Uses threading for concurrent processing and dashboard operation.

## Project Structure

```
routing_engine/
├── config/
│   └── config.yaml         # Defines tag-to-processor mapping
├── dashboard/
│   └── server.py           # FastAPI web server and endpoints (updated for file state)
├── processors/
│   ├── __init__.py         # Makes processors a Python package
│   ├── filters.py          # Filtering processors
│   ├── formatters.py       # Formatting processors
│   ├── output.py           # Final output processor
│   └── start.py            # Initial tagging processor
├── watch_dir/              # New directory to be monitored (created by main.py)
│   ├── unprocessed/     # Incoming files land here
│   ├── underprocess/    # Files currently being processed
│   └── processed/       # Successfully processed files
├── router.py               # Core routing engine logic, metrics, tracing, error handling, and file completion
├── main.py                 # Entry point with CLI args, threading, directory setup, recovery, and mode handling
├── Makefile                # Helps automate common tasks
├── requirements.txt        # Lists Python dependencies
└── FINAL.md                # Project reflection document
```

## Setup and Installation

1.  **Clone or download the project files.** Ensure you have the directory structure as shown above.
2.  **Make sure you have Python 3 installed.**
3.  **Install required libraries.** Navigate to the `routing_engine` directory in your terminal and run the Makefile target:
    ```bash
    make install
    ```
    This will install dependencies listed in `requirements.txt`.
4.  **Optional Libraries:** If you want to enable the (currently commented out) static graph visualization feature in `router.py`, manually install `networkx` and `matplotlib`:
    ```bash
    pip install networkx matplotlib
    ```

## How to Run

The project can be run in two main modes using `main.py` or the provided `Makefile`.

### Using the Makefile

Navigate to the project directory in your terminal and use the `make` command:

* **Run in Watch Mode (continuous monitoring):**
    ```bash
    make run-watch
    ```
    This will start the system, set up `watch_dir`, perform recovery, start the file monitor, and run the processing engine continuously. The dashboard will be available at `http://127.0.0.1:8000`.
* **Run in Single File Mode:**
    ```bash
    make run-single FILE=path/to/your/file.txt
    ```
    Replace `path/to/your/file.txt` with the actual path to a text file. This will process the specified file line by line and exit once the file's lines have been processed through the engine. The dashboard will be available during processing.
* **Clean up:**
    ```bash
    make clean
    ```
    Removes cache directories and files from `watch_dir/unprocessed` and `watch_dir/underprocess`. Processed files are kept by default.
* **Build Docker Image:**
    ```bash
    make docker-build
    ```
* **Run with Docker (Watch Mode):**
    ```bash
    make docker-run
    ```
    Builds and runs the Docker container in the background (`-d`). It maps port 8000 and mounts the local `watch_dir` into the container so you can drop files into your local `watch_dir/unprocessed`. Access the dashboard at `http://127.0.0.1:8000`.

### Direct Execution (without Makefile)

You can also run `main.py` directly:

* **Watch Mode:**
    ```bash
    python main.py --watch --dashboard-port 8000 --dashboard-host 127.0.0.1
    ```
* **Single File Mode:**
    ```bash
    python main.py --input path/to/your/file.txt --dashboard-port 8000 --dashboard-host 127.0.0.1
    ```
* **Enable Tracing (in either mode):** Add the `--trace` flag.

## Placing Input Files (Watch Mode)

When running in Watch Mode (`make run-watch` or `python main.py --watch`), place plain text files into the `watch_dir/unprocessed` directory. The file monitor thread will automatically detect them, move them to `underprocess`, process their lines through the engine, and finally move them to `processed` upon completion.

## Dashboard Endpoints

Access the interactive API documentation at `http://127.0.0.1:8000/docs` (or your specified host/port) to explore the following endpoints:

* **`/stats`**: Live processor metrics.
* **`/traces`**: Recent line traces (if tracing is enabled).
* **`/errors`**: Recent errors.
* **`/file_state`**: Current state of files in the watched directories (only in watch mode).

## Output

Here is a sample of the console output when files are placed in the `unprocessed` directory:

```bash
PS D:\Bootcamp\Dataflow_framework\final_project> python main.py --watch --dashboard-port 8000 --dashboard-host 127.0.0.1
2025-05-11 21:49:42,183 - INFO - Loading configuration from config/config.yaml
2025-05-11 21:49:42,187 - INFO - Configuration loaded successfully.
2025-05-11 21:49:42,187 - INFO - Loading processors...
2025-05-11 21:49:42,209 - INFO - Loaded processor for tag 'start': processors.start.TagLinesProcessor
2025-05-11 21:49:42,213 - INFO - Loaded processor for tag 'error': processors.filters.OnlyErrorProcessor
2025-05-11 21:49:42,214 - INFO - Loaded processor for tag 'warn': processors.filters.OnlyWarnProcessor
2025-05-11 21:49:42,216 - INFO - Loaded processor for tag 'general': processors.formatters.SnakecaseProcessor
2025-05-11 21:49:42,222 - INFO - Loaded processor for tag 'end': processors.output.TerminalOutputProcessor
2025-05-11 21:49:42,222 - INFO - Finished loading 5 processors.
2025-05-11 21:49:42,223 - INFO - Routing engine initialized. Tracing enabled: False
2025-05-11 21:49:42,224 - INFO - Starting dashboard server on http://127.0.0.1:8000
INFO:     Started server process [7476]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
2025-05-11 21:49:43,225 - INFO - Dashboard running at http://127.0.0.1:8000/docs
2025-05-11 21:49:43,225 - INFO - Running in Watch Mode.
2025-05-11 21:49:43,248 - INFO - Ensured directory exists: watch_dir\unprocessed
2025-05-11 21:49:43,248 - INFO - Ensured directory exists: watch_dir\underprocess
2025-05-11 21:49:43,249 - INFO - Ensured directory exists: watch_dir\processed
2025-05-11 21:49:43,250 - INFO - Performing recovery: Checking for files in underprocess...
2025-05-11 21:49:43,251 - INFO - No files found in underprocess/. Recovery complete.
2025-05-11 21:49:43,252 - INFO - Initial file counts: {'unprocessed': 0, 'underprocess': 0, 'processed': 0}
2025-05-11 21:49:43,252 - INFO - Starting file monitor loop for 'watch_dir\unprocessed'. Polling every 5 seconds.
2025-05-11 21:49:43,253 - INFO - File monitor thread started.
2025-05-11 21:49:43,253 - INFO - Starting main routing engine continuous processing loop.
2025-05-11 21:49:43,253 - INFO - Starting continuous queue processing. 
INFO:     127.0.0.1:51295 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:51295 - "GET /openapi.json HTTP/1.1" 200 OK
INFO:     127.0.0.1:51786 - "GET /file_state HTTP/1.1" 200 OK
2025-05-11 21:52:08,275 - INFO - Found new file: sample_error.txt
2025-05-11 21:52:08,277 - INFO - Moved 'sample_error.txt' to underprocess/.
2025-05-11 21:52:08,279 - INFO - Added 0 lines from 'sample_error.txt' to the processing queue.
2025-05-11 21:52:18,281 - INFO - Found new file: sample_error.txt
2025-05-11 21:52:18,293 - INFO - Moved 'sample_error.txt' to underprocess/.
2025-05-11 21:52:18,295 - INFO - Added 5 lines from 'sample_error.txt' to the processing queue.
FINAL OUTPUT [Tag: end] (File: watch_dir\underprocess\sample_error.txt): processing record 123 failed. error code 500.
2025-05-11 21:52:18,325 - INFO - All lines from file 'watch_dir\underprocess\sample_error.txt' processed. Moving to 'processed'.
2025-05-11 21:52:18,326 - INFO - Moved 'watch_dir\underprocess\sample_error.txt' to 'watch_dir\processed\sample_error.txt'.
2025-05-11 21:53:08,304 - INFO - Found new file: sample_general.txt
2025-05-11 21:53:08,305 - INFO - Moved 'sample_general.txt' to underprocess/.
2025-05-11 21:53:08,306 - INFO - Added 0 lines from 'sample_general.txt' to the processing queue.
2025-05-11 21:53:13,308 - INFO - Found new file: sample_general.txt
2025-05-11 21:53:13,312 - INFO - Moved 'sample_general.txt' to underprocess/.
2025-05-11 21:53:13,315 - INFO - Added 5 lines from 'sample_general.txt' to the processing queue.
FINAL OUTPUT [Tag: end] (File: watch_dir\underprocess\sample_general.txt): user_logged_in
FINAL OUTPUT [Tag: end] (File: watch_dir\underprocess\sample_general.txt): application shutdown complete.
2025-05-11 21:53:13,353 - INFO - All lines from file 'watch_dir\underprocess\sample_general.txt' processed. Moving to 'processed'.
2025-05-11 21:53:13,355 - INFO - Moved 'watch_dir\underprocess\sample_general.txt' to 'watch_dir\processed\sample_general.txt'.
```

## Deployment Notes

* **Local Execution:** Run directly using `python main.py` or `make run-watch`/`make run-single`. Requires Python and dependencies installed locally.
* **Docker Deployment:** Use the provided `Dockerfile` and `Makefile` targets (`make docker-build`, `make docker-run`). Docker provides a portable and isolated environment. The `docker-run` target maps the dashboard port and mounts the `watch_dir` as a volume, allowing file drop-off from the host machine.
* **File Uploads:**
    * **Manual/Scripted:** Use tools like `cp`, `mv`, or `rsync` to copy files into the `watch_dir/unprocessed` directory. This is the simplest method for automated drops.
    * **API Upload (Potential Future Feature):** A more sophisticated system could add a FastAPI endpoint (`/upload`) to receive files via HTTP POST requests, placing them directly into the `unprocessed` directory. This would require implementing file handling and security considerations (authentication, validation, scanning).
* **Monitoring:**
    * **Dashboard:** Use the built-in FastAPI dashboard (`/stats`, `/file_state`, `/errors`) for real-time status.
    * **Health Check:** The FastAPI application implicitly provides a basic health check by responding to requests. For a more explicit check, a dedicated `/health` endpoint could be added that reports the status of internal components (queue size, thread status).
    * **External Monitoring:** Services like Better Uptime, UptimeRobot, or Prometheus/Grafana could be configured to periodically check the `/stats` or a dedicated `/health` endpoint to monitor the application's availability and key metrics.

This system is now packaged for easier use and deployment, providing the core functionality of a self-managing file processing daemon.
