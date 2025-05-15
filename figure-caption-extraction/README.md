# Figure Captions Extraction System

## Purpose

This module builds a production-ready system to extract, store, and provide access to figure captions and related metadata from scientific publications—especially PubMed Central (PMC). The system is designed to be extensible, secure, and operable via API, CLI, or batch jobs.

## What This System Does

- Extracts **title**, **abstract**, and **figure captions** from PMC articles.
- Extracts **figure URLs** and **key biological entities** (e.g., genes) from captions.
- Makes the data accessible via API (JSON/CSV) and CLI.

> 🔗 Uses [BioC-PMC](https://www.ncbi.nlm.nih.gov/research/bionlp/APIs/BioC-PMC/) for structural data and [PubTator API](https://www.ncbi.nlm.nih.gov/research/pubtator3/api) for entity extraction.

---

## User Capabilities

- Submit PMC or PMID paper IDs for processing.
- Query results via a password/API-key protected REST API.
- Download extracted data in JSON or CSV.
- Upload IDs via API, CLI, or file.

## Admin Capabilities

- Configure data storage (default: DuckDB).
- Set API key/password, logging levels, and data sources.
- Add new sources without major system changes.

## Ops Capabilities

- Deploy with Docker.
- Run ingestion in batch mode (file, API, watched folder).
- Monitor logs and job summaries.
- Ensure clean exit statuses for jobs.

---

## Developer Checklist

### 1. Design Document
- Define architecture and components.
- Include system and deployment diagrams.
- Justify technology choices.

### 2. Implementation & Testing Plan
- Describe phases of build and test.
- Outline functional, security, and performance testing (mock + real data).

### 3. Implementation Deliverables
- CLI tools for ingestion.
- REST API for access.
- Config management system.
- Dockerfile, Makefile, and logs.

### 4. Operationalization
- Runbook for deployment and usage.
- Docker-based deployment steps.
- Sample config and usage scenarios.


