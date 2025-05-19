# Figure Caption Extraction System

## Overview
This project is a web-based system that extracts and analyzes figure captions from scientific papers, specifically focusing on PubMed Central (PMC) articles. It uses Streamlit for the frontend interface and provides capabilities for extracting, storing, and analyzing figure captions along with their associated metadata.

## Demo
1. Docker deployment
[![asciicast](https://asciinema.org/connect/1af33fce-f016-46dd-ae64-401112477c12.svg)](https://asciinema.org/connect/1af33fce-f016-46dd-ae64-401112477c12)
2. Working of application
[![loomvideo]](https://www.loom.com/share/9a79c6a50a9c41949baaedcf99e352e2?sid=d9e89e48-4d59-4d2b-87e2-19fff445c45b)

## Features
- Extract figures and captions from PMC articles
- Entity recognition in figure captions
- Local database storage for extracted data
- Web interface for data visualization
- Batch processing capabilities

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
2. Build and run with Docker:
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