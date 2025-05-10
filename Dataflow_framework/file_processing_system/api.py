# api.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
from typing import List
from .processor import get_stats # Assuming processor has stats

# Define base directory for watch_dir relative to where main.py runs
# This will be set dynamically in main.py, but needed for directory listing here
WATCH_BASE_DIR = os.path.join(os.path.dirname(__file__), 'watch_dir')
UNPROCESSED_DIR = os.path.join(WATCH_BASE_DIR, 'unprocessed')
PROCESSED_DIR = os.path.join(WATCH_BASE_DIR, 'processed')
ERROR_DIR = os.path.join(WATCH_BASE_DIR, 'error')


app = FastAPI(
    title="File Processing System API",
    description="API to interact with the real-time file processing system",
    version="1.0.0",
)

@app.get("/health", summary="Check system health")
async def health_check():
    """Returns a simple status to indicate if the API is running."""
    return {"status": "ok"}

@app.get("/stats", summary="Get processing statistics")
async def get_processing_stats():
    """Returns current processing counts (processed and error)."""
    # Use the stats from the processor module
    return get_stats()

@app.get("/files", summary="List files in processing directories")
async def list_files():
    """Lists files currently in the unprocessed, processed, and error directories."""
    try:
        unprocessed_files = os.listdir(UNPROCESSED_DIR)
        processed_files = os.listdir(PROCESSED_DIR)
        error_files = os.listdir(ERROR_DIR)

        return {
            "unprocessed": unprocessed_files,
            "processed": processed_files,
            "error": error_files,
        }
    except FileNotFoundError:
         raise HTTPException(status_code=404, detail="Watch directories not found. Ensure the application is run correctly.")
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"An error occurred listing files: {e}")


@app.post("/upload", summary="Upload a file for processing")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file via HTTP POST to be placed in the unprocessed directory."""
    if not file.filename:
         raise HTTPException(status_code=400, detail="No file name provided.")

    file_path = os.path.join(UNPROCESSED_DIR, file.filename)

    # Check if the watch directory exists
    if not os.path.exists(UNPROCESSED_DIR):
         raise HTTPException(status_code=500, detail=f"Unprocessed directory not found: {UNPROCESSED_DIR}. Ensure application is running in watch mode.")

    try:
        # Save the uploaded file to the unprocessed directory
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Note: The watcher (if running) will pick this up automatically.
        # If running in single-file mode, this upload wouldn't trigger processing.
        # For simplicity, we just save the file here. A real system might queue this.

        return {"message": f"File '{file.filename}' uploaded successfully to unprocessed directory."}
    except Exception as e:
        # Clean up potentially partially written file
        if os.path.exists(file_path):
             os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"An error occurred during file upload: {e}")

# You might need to dynamically update WATCH_BASE_DIR when the app starts
# This is handled in main.py when uvicorn is run.
def set_watch_base_dir(base_path: str):
     global WATCH_BASE_DIR, UNPROCESSED_DIR, PROCESSED_DIR, ERROR_DIR
     WATCH_BASE_DIR = base_path
     UNPROCESSED_DIR = os.path.join(WATCH_BASE_DIR, 'unprocessed')
     PROCESSED_DIR = os.path.join(WATCH_BASE_DIR, 'processed')
     ERROR_DIR = os.path.join(WATCH_BASE_DIR, 'error')