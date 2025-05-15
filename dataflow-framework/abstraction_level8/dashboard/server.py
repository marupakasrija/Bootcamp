# dashboard/server.py

import logging
import threading
from fastapi import FastAPI, HTTPException
from typing import Dict, Any, List, Optional, Tuple
import uvicorn
import time

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# This variable will hold the reference to the RoutingEngine instance
# It needs to be set by the main thread before starting the server thread.
routing_engine_instance = None

app = FastAPI(
    title="Routing Engine Dashboard",
    description="Live metrics, traces, errors, and file state for the state-based routing engine.",
    version="1.0.0",
)

@app.get("/stats", response_model=Dict[str, Dict[str, Any]])
async def get_stats():
    """
    Returns live processor metrics.
    """
    if routing_engine_instance is None:
        raise HTTPException(status_code=503, detail="Routing engine not initialized.")

    logging.debug("Received request for /stats")
    metrics = routing_engine_instance.get_metrics()
    return metrics

@app.get("/traces", response_model=List[Dict[str, Any]])
async def get_traces():
    """
    Returns recent line traces (up to the configured limit).
    Requires tracing to be enabled in the engine.
    """
    if routing_engine_instance is None:
        raise HTTPException(status_code=503, detail="Routing engine not initialized.")

    logging.debug("Received request for /traces")
    traces = routing_engine_instance.get_traces()
    return traces

@app.get("/errors", response_model=List[Dict[str, Any]])
async def get_errors():
    """
    Returns recent errors logged by the engine or processors.
    """
    if routing_engine_instance is None:
        raise HTTPException(status_code=503, detail="Routing engine not initialized.")

    logging.debug("Received request for /errors")
    errors = routing_engine_instance.get_errors()
    return errors

@app.get("/file_state", response_model=Dict[str, Any])
async def get_file_state():
    """
    Returns the current state of file processing.
    Includes counts in each directory, currently processed file, and recently processed files.
    """
    if routing_engine_instance is None:
        raise HTTPException(status_code=503, detail="Routing engine not initialized.")

    logging.debug("Received request for /file_state")
    file_state = routing_engine_instance.get_file_state()
    return file_state


# Helper function to run the FastAPI server in a separate thread
def run_dashboard(engine_instance, host: str = "127.0.0.1", port: int = 8000):
    """
    Starts the FastAPI server in a separate thread.

    Args:
        engine_instance: The initialized RoutingEngine instance.
        host: The host address for the server.
        port: The port for the server.
    """
    global routing_engine_instance
    routing_engine_instance = engine_instance

    logging.info(f"Starting dashboard server on http://{host}:{port}")
    # Use uvicorn.run to start the server programmatically
    uvicorn.run(app, host=host, port=port, log_level="info") # log_level controls uvicorn's logging

# Note: The main application thread will need to start this function
# in a new thread using `threading.Thread`.
