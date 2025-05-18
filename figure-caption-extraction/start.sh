#!/bin/bash

# Start FastAPI server in background
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit
streamlit run src/streamlit_app.py