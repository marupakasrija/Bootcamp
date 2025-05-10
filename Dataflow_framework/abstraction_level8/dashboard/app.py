# This is abstraction-level-8/dashboard/app.py
# FastAPI application for the observability dashboard.

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
import threading # Not directly used in app, but needed for shared data type
import time # For timestamps

# Import shared data structure and Pydantic models from types
# Need to go up two levels to abstraction-level-8, then into types
from ..types import ObservabilityData, ProcessorMetrics, ErrorData, LineTrace, FileStatus

# This variable will hold the shared ObservabilityData instance,
# set by the main application thread.
observability_data: Optional[ObservabilityData] = None

# Create the FastAPI application instance
app = FastAPI(
    title="Abstraction Level 8 Dashboard API",
    description="API for monitoring the State Transition Engine and Folder Monitor.",
    version="0.8.0",
)

# --- Pydantic Models for API Responses ---
# These mirror the to_dict methods in types.py

from pydantic import BaseModel

class ProcessorMetricsResponse(BaseModel):
    lines_received: int
    lines_emitted: int
    processing_time_seconds: float
    errors_count: int
    last_activity_timestamp: float

class MetricsResponse(BaseModel):
    # Dictionary where keys are state tags and values are ProcessorMetricsResponse
    __root__: Dict[str, ProcessorMetricsResponse]

    # Pydantic v2 requires a validator for Dict roots
    @classmethod
    def model_validate(cls, data):
        return cls(__root__=data)


class ErrorDataResponse(BaseModel):
    timestamp: float
    state: str
    message: str
    line_id: str
    line_content: str
    file_name: Optional[str]

class ErrorsResponse(BaseModel):
    __root__: List[ErrorDataResponse]

    @classmethod
    def model_validate(cls, data):
        return cls(__root__=data)


class LineTraceResponse(BaseModel):
    line_id: str
    final_content: str
    history: List[str]
    status: str
    file_name: Optional[str]

class TracesResponse(BaseModel):
    __root__: List[LineTraceResponse]

    @classmethod
    def model_validate(cls, data):
        return cls(__root__=data)

class FileStatusResponse(BaseModel):
    file_name: str
    status: str
    timestamp: float

class FileStatusDataResponse(BaseModel):
    file_counts: Dict[str, int]
    current_file_processing: Optional[str]
    recent_files: List[FileStatusResponse]


# --- API Endpoints ---

@app.get("/stats", response_model=MetricsResponse)
async def get_stats():
    """
    Get live processing metrics for each state.
    """
    if observability_data is None:
        raise HTTPException(status_code=503, detail="Observability data not initialized.")
    # Use the thread-safe getter
    metrics_dict = observability_data.get_metrics()
    # Return the dictionary directly, Pydantic will validate and serialize
    return metrics_dict


@app.get("/traces", response_model=TracesResponse)
async def get_traces(limit: int = 100):
    """
    Get the most recent line traces.
    """
    if observability_data is None:
        raise HTTPException(status_code=503, detail="Observability data not initialized.")
    if not observability_data.enable_tracing:
        raise HTTPException(status_code=400, detail="Tracing is not enabled. Run with --trace flag.")

    # Use the thread-safe getter
    traces_list = observability_data.get_traces(n=limit)
    # Return the list directly, Pydantic will validate and serialize
    return traces_list


@app.get("/errors", response_model=ErrorsResponse)
async def get_errors(limit: int = 100):
    """
    Get the most recent processing errors.
    """
    if observability_data is None:
        raise HTTPException(status_code=503, detail="Observability data not initialized.")
    # Use the thread-safe getter
    errors_list = observability_data.get_errors(n=limit)
    # Return the list directly, Pydantic will validate and serialize
    return errors_list

@app.get("/file-status", response_model=FileStatusDataResponse)
async def get_file_status():
     """
     Get live file processing status and counts.
     """
     if observability_data is None:
         raise HTTPException(status_code=503, detail="Observability data not initialized.")
     # Use the thread-safe getter
     file_status_data = observability_data.get_file_status()
     # Return the dictionary directly, Pydantic will validate and serialize
     return file_status_data


# Optional: Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Abstraction Level 8 Dashboard API is running. Visit /docs for API documentation."}

# Note: The Uvicorn server will be started in a separate thread from main.py.
# This app.py file only defines the FastAPI application and its endpoints.
