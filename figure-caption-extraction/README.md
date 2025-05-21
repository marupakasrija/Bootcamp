# Figure Caption Extraction System

A production-ready system that extracts, stores, and provides access to scientific publication data, focusing on figure captions and related metadata from PubMed Central (PMC) articles. The system leverages BioC-PMC and PubTator3 APIs for data extraction and entity recognition.

## Features

- Extract figures and captions from PubMed/PMC articles
- Entity recognition in figure captions
- Support for both PMC IDs and PubMed IDs
- Multiple interfaces (API, CLI, and Streamlit UI)
- Local database storage with CSV export
- Docker support

## Installation

### Prerequisites
- Python 3.8+
- pip
- SQLite3

### Setup
1. Clone the repository:
```bash
git clone https://github.com/marupakasrija/Bootcamp.git
cd figure-caption-extraction
```
2. Create and activate virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Streamlit UI
Run the Streamlit interface:
```bash
streamlit run src/streamlit_app.py
```
Features:
- Process individual papers or batch process from file
- View extracted figures and captions
- Export data to CSV

### CLI
Process papers using command line:
```bash
# Process single PMC paper
python -m src.cli.main process-papers PMC1234567
# Process multiple papers from file
python -m src.cli.main process-file pmcids.txt
```

### API
Start the FastAPI server:
```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```
API endpoints:
- POST /papers/process : Process multiple papers
- GET /papers/{paper_id} : Get processed paper data

## Docker Support

Build and run with Docker:
```bash
docker-compose up --build
```

## Data Structure

The system stores data in SQLite with the following structure:
- Papers: Basic paper information
- Figures: Figure data and captions
- Entities: Extracted entities from captions
Data can be exported to CSV format using the UI or CLI.


## Demo

1. Docker deployment
[![asciicast](https://asciinema.org/connect/1af33fce-f016-46dd-ae64-401112477c12.svg)](https://asciinema.org/connect/1af33fce-f016-46dd-ae64-401112477c12)
2. Working of application
[![loomvideo]](https://www.loom.com/share/9a79c6a50a9c41949baaedcf99e352e2?sid=d9e89e48-4d59-4d2b-87e2-19fff445c45b)
