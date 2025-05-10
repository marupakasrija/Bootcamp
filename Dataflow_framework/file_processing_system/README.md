# Real-Time File Processing System

This project implements a simple, observable, file processing system that can operate on single files or continuously monitor a directory. It includes a web API for health checks, statistics, and file uploads.

## Project Structure
file_processing_system/
├── watch_dir/           # Directory for file monitoring
│   ├── unprocessed/   # Files dropped here for processing
│   ├── processed/     # Successfully processed files are moved here
│   └── error/         # Files that caused errors are moved here
├── api.py               # FastAPI application endpoints
├── processor.py         # Core file processing logic
├── watcher.py           # Directory monitoring logic (using watchdog)
├── main.py              # Main entry point, CLI argument handling, orchestrator
├── Makefile             # Shortcuts for common commands (build, run, clean)
├── Dockerfile           # Defines the Docker image
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── FINAL.md             # Project reflection essay

## Getting Started

### Prerequisites

* Python 3.8+
* pip (Python package installer)
* Docker (for containerized deployment)
* `make` (optional, but recommended for using the Makefile)

### Setup

1.  Clone the repository or create the files/directories manually as shown above.
2.  Navigate into the project directory: `cd file_processing_system`
3.  Create the watch directories:
    ```bash
    make dirs
    # Or: mkdir -p watch_dir/unprocessed watch_dir/processed watch_dir/error
    ```
4.  Install Python dependencies:
    ```bash
    make install
    # Or: pip install -r requirements.txt
    ```

## Running the System

You can run the system locally using Python directly or using Docker.

### Running Locally

Use `main.py` with command-line arguments or use the `make run-local` target.

* **Run in Watch Mode (continuous processing & API):**
    Monitors `./watch_dir/unprocessed` by default. The FastAPI server runs on `http://127.0.0.1:8000`.
    ```bash
    python main.py --watch
    # Or using Makefile:
    make run-local
    ```
    Use `Ctrl+C` to stop the application.

* **Run for a Single File:**
    Processes the specified file and exits.
    ```bash
    python main.py --input path/to/your/file.txt
    # Or using Makefile (pass arguments via ARGS):
    make run-local ARGS='--input ../path/to/another_file.csv'
    ```
    *Note: The single file mode will move the file to `./watch_dir/processed` or `./watch_dir/error` relative to where `main.py` is located.*

* **Specify Watch Directory:**
    ```bash
    python main.py --watch --watch-dir /custom/input/folder
    # make run-local ARGS='--watch --watch-dir /custom/input/folder'
    ```

### Running with Docker

Use the `make` targets to build the image and run the container.

1.  **Build the Docker Image:**
    ```bash
    make build-docker
    # Or manually: docker build -t file-processing-system .
    ```

2.  **Run the Docker Container:**
    This runs in watch mode by default, monitoring `/app/watch_dir/unprocessed` *inside* the container. It maps port 8000 on your host to the container's port 8000 and mounts your local `./watch_dir` to `/app/watch_dir` inside the container. This allows the code inside the container to read/write files in your local directory.
    ```bash
    make run-docker
    # Or manually:
    # docker run --rm -it -p 8000:8000 -v ${PWD}/watch_dir:/app/watch_dir file-processing-system
    ```
    Use `Ctrl+C` in your terminal to stop the container gracefully (because of the `--rm` flag in the Makefile target, the container will be removed afterward).

* **Run Single File Mode with Docker:**
    You need to mount the directory containing the input file as a volume and specify the file path relative to the container's file system (i.e., relative to `/app` or the volume mount point).
    ```bash
    # Example: Assuming your file is at /path/to/local/data/my_file.txt
    # Mount /path/to/local/data to /app/data inside the container
    make run-docker ARGS='--input /app/data/my_file.txt' DOCKER_RUN_FLAGS='-v /path/to/local/data:/app/data'
    # Manual example:
    # docker run --rm -it -p 8000:8000 -v ${PWD}/watch_dir:/app/watch_dir -v /path/to/local/data:/app/data file-processing-system --input /app/data/my_file.txt
    ```
    *Note: The single file mode in Docker will move the file to `/app/watch_dir/processed` or `/app/watch_dir/error` inside the container, which corresponds to `./watch_dir/processed` or `./watch_dir/error` on your host due to the volume mount.*


## Interacting with the System (FastAPI)

When running in watch mode (either locally or in Docker), the FastAPI server is available.

* **API Documentation (Swagger UI):** Open your browser to `http://127.0.0.1:8000/docs`
* **Available Endpoints:**
    * `GET /health`: Check if the API is running (`http://127.0.0.1:8000/health`)
    * `GET /stats`: Get processing statistics (`http://127.0.0.1:8000/stats`)
    * `GET /files`: List files in the watch directories (`http://127.0.0.1:8000/files`)
    * `POST /upload`: Upload a file via HTTP (`http://127.0.0.1:8000/upload`) - use the Swagger UI or a tool like `curl`.

## How to Upload/Provide Files

* **File Drop (Watch Mode):** The easiest way when running in watch mode is to simply copy or move files into the `./watch_dir/unprocessed` directory. The watcher will automatically detect and process them. You can use standard commands like `cp`, `mv`, or `rsync`.
    ```bash
    cp /path/to/your/document.pdf ./watch_dir/unprocessed/
    rsync /path/to/batch/*.txt ./watch_dir/unprocessed/
    ```
* **FastAPI Upload (Watch Mode):** Use the `/upload` endpoint via the Swagger UI (`/docs`) or tools like `curl`.
    ```bash
    curl -X POST -H "Content-Type: multipart/form-data" -F "file=@path/to/your/local/file_to_upload.txt" http://127.0.0.1:8000/upload
    ```

## Monitoring Uptime

To monitor the availability of your system's API in a production-like scenario, you can use free uptime monitoring services.

1.  Sign up for a service like [Better Uptime](https://betteruptime.com/), [UptimeRobot](https://uptimerobot.com/), or [Healthchecks.io](https://healthchecks.io/).
2.  Add a monitor (usually called a "check" or "heartbeat").
3.  Point the monitor to your system's health endpoint, e.g., `http://your_server_ip_or_domain:8000/health`.
4.  Configure the check to run periodically (e.g., every 5 minutes).
5.  Set up alerts (email, Slack, etc.) to notify you if the `/health` endpoint becomes unreachable or returns an error status code.

## Makefile Commands

Refer to the `Makefile` for specific targets, but the main ones are:
* `make dirs`: Create watch directories.
* `make install`: Install Python dependencies.
* `make run-local`: Run locally (pass args with `ARGS='...'`).
* `make build-docker`: Build the Docker image.
* `make run-docker`: Build and run the Docker container (pass args with `ARGS='...'`, add docker flags with `DOCKER_RUN_FLAGS='...'`).
* `make clean`: Clean build artifacts.
* `make help`: Show all targets.

## Development

[Add notes on how to contribute, run tests (if any), code style, etc.]

---

**Checklist Verification:**

* [x] Makefile supports major commands.
* [x] One-shot (`--input`) and continuous (`--watch`) modes are implemented.
* [x] User interaction via CLI, file drop, and browser (FastAPI) is possible.
* [ ] All code is committed and structured (Verify in your Git repo).
* [x] Deployment and monitoring instructions are clear.