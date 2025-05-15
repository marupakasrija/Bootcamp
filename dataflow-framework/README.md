# Dataflow Framework

## 🚀 Purpose

This project is a **streaming dataflow engine** that processes text data through a flexible, configurable pipeline. It began as a simple line-processing script and evolved into a **modular, observable, and fault-tolerant system**. The goal is to demonstrate how complex systems can be incrementally built with a focus on:

- Modularity
- Testability
- Observability
- Extensibility
- Crash recovery

---

## 🛠 What It Does

- Processes input line-by-line or in batches
- Routes data through a configurable pipeline (defined via YAML)
- Supports **dynamic processor loading**
- Enables **tag-based conditional flows** (like a DAG)
- Provides **real-time metrics and a monitoring dashboard**
- Can **continuously monitor folders** and recover from crashes

---

## 🧱 Features

- **Configurable Pipelines**: Define flows in YAML
- **Stream Processing**: Iterator-based for memory efficiency
- **Dynamic Processor Loading**: Import logic at runtime
- **Stateful Processing**: Maintain context between lines
- **Tag-Based Routing**: Conditional path control
- **Fan-in/Fan-out Support**
- **Real-Time Observability**: Metrics, tracing, errors
- **FastAPI Dashboard**: At `http://localhost:8000`
- **Folder Monitoring**: Auto-process new files
- **Crash Recovery**: Resume interrupted work
- **Dockerized Deployment**

---