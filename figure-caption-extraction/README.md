# Figure Caption Extraction System

## Purpose
A production-ready system that extracts, stores, and provides access to scientific publication data, focusing on figure captions and related metadata from PubMed Central (PMC) articles. The system leverages BioC-PMC and PubTator3 APIs for data extraction and entity recognition.

## Demo
1. Docker deployment
[![asciicast](https://asciinema.org/connect/1af33fce-f016-46dd-ae64-401112477c12.svg)](https://asciinema.org/connect/1af33fce-f016-46dd-ae64-401112477c12)
2. Working of application
[![loomvideo]](https://www.loom.com/share/9a79c6a50a9c41949baaedcf99e352e2?sid=d9e89e48-4d59-4d2b-87e2-19fff445c45b)

## Features
- Extract paper metadata (title, abstract)
- Extract and process figure captions
- Identify figure URLs
- Entity recognition in captions (genes, etc.)
- Batch processing capabilities
- API and CLI interfaces
- Configurable storage and authentication

## Tech Stack
- Python 3.11
- Streamlit for web interface
- SQLite for data storage
- Docker for containerization
- RESTful API with authentication
## Prerequisites
- Python 3.11
- Docker and Docker Compose
- Internet connection for accessing PMC articles

## Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd figure-caption-extraction
```
2.Configure environment variables:
```bash
cp template.env .env
```
3. Build and run with Docker:
```bash
docker-compose up -d --build
```

## Usage
1. Access the web interface at http://localhost:8501
2. Enter a PMC ID or upload a file containing multiple PMC IDs
3. View the extracted figures and captions

## Environment Variables
- API_PORT : Port for the web interface (default: 8001)
- DB_PATH : Path to SQLite database
- PUBTATOR_API_URL : URL for PubTator API

## Testing
```bash
python -m pytest tests/
```