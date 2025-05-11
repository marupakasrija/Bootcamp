# FINAL.md - Project Reflection

## 1. Design Decisions

The most important architectural choices throughout this project revolved around **modularity** and **state management**.

* **Modular Processors:** Defining processors as independent classes with a standard `process` method was fundamental. This abstraction allowed adding, removing, or modifying processing logic without altering the core routing engine. It directly supported the extension requirements across levels.
* **State-Based Routing (Tags):** Moving from linear pipelines to tag-based routing was a critical shift. Tags act as explicit state labels, decoupling the flow logic from the processing code. This enabled complex branching, fan-in/fan-out, and laid the groundwork for potential cycles and more sophisticated workflows.
* **Observability Layer:** Integrating metrics, tracing, and error reporting directly into the engine and exposing them via a dashboard was vital for understanding the system's behavior. It shifted the focus from just building functionality to being able to operate and debug it effectively.
* **Folder Queue for Resilience:** The `unprocessed`/`underprocess`/`processed` directory structure provided a simple yet effective mechanism for persistence and recovery. It ensures that files are not lost and are retried upon restart, addressing a core requirement of a robust daemon.
* **Concurrency with Threading:** Using separate threads for the file monitor, the processing loop, and the dashboard allowed the system to be responsive and handle multiple tasks concurrently (monitoring, processing, serving requests).

The abstraction that helped the most was the **standard processor interface** (`process(self, lines: Iterator[Tuple[...]) -> Iterator[Tuple[...]])`). By defining a clear contract for how processors receive and emit data (including tags, lines, traces, and file paths), the core `RoutingEngine` could remain relatively stable while the processing logic evolved significantly across levels.

## 2. Tradeoffs

Several simplifications and omissions were made, leading to current limitations:

* **In-Memory Queue:** The `collections.deque` is simple and fast but is limited by available memory. Processing extremely large files or a massive backlog could exhaust memory.
* **Simple File Monitoring:** Polling the directory is easy to implement but less efficient than event-based monitoring (like `watchdog`) for very high file arrival rates. It also doesn't handle partial file writes gracefully without additional checks.
* **Basic Error Handling:** Lines or files encountering errors are currently logged and often discarded. There's no built-in retry mechanism *per line* within the engine, nor is there an automated dead-letter queue for failed items.
* **Single-Threaded Queue Processing:** While monitoring and the dashboard run in separate threads, the core `process_queue_continuously` loop processes items from the queue sequentially. This limits the ability to parallelize processing *of lines* across multiple CPU cores within a single instance.
* **Simple Cycle Detection:** The step limit is a basic guard. A true cycle detection mechanism would require tracking the history of tags for each line and identifying repeated sequences.
* **Limited Persistence:** Metrics, traces, and errors are stored in memory and lost on restart. File state is persistent, but line-level state within a file is not if a crash occurs mid-file processing (the whole file is retried).

## 3. Scalability

To handle 100x larger input (either in file size, file count, or arrival rate), significant changes would be needed:

* **Distributed Queue:** Replace the in-memory `deque` with a distributed message queue like Kafka, RabbitMQ, or AWS SQS. This provides durability, allows multiple processing instances to consume messages in parallel, and decouples the file monitor from the processors.
* **Distributed Storage:** Store input files and processed output in a distributed, scalable storage system like Amazon S3 or Google Cloud Storage instead of a local file system. The file monitor would then watch for objects in a storage bucket.
* **Parallel Processing Workers:** Implement multiple instances of the `RoutingEngine`'s processing logic, running as separate processes or on different machines. These workers would consume from the distributed queue in parallel.
* **Database for Observability:** Store metrics, traces, and errors in a time-series database (Prometheus/InfluxDB) and a centralized logging system (ELK stack/Splunk) for scalable storage, querying, and visualization (e.g., using Grafana).
* **Parallelizing Processing within a File:** This is more complex. It would require splitting a single file into chunks and processing those chunks in parallel, potentially needing a way to maintain line order if required downstream.

Yes, parallelizing processing safely is possible, but requires careful design:

* **Parallel Files (Simple):** Have multiple worker processes/threads that each pick up a *whole file* from the `unprocessed` queue (or distributed queue) and process it independently. File state management needs to be atomic (e.g., using distributed locks or relying on queue semantics).
* **Parallel Lines (Complex):** Split a file into line batches and send batches to different workers. This requires a mechanism to reassemble or order the results if the final output needs to maintain the original file's line order.

## 4. Extensibility & Security

To run this system for real users, several aspects are needed:

* **Authentication and Authorization:** Secure the dashboard and any potential file upload endpoints. Users should need to authenticate, and different users/roles might have different levels of access (e.g., view metrics vs. upload files vs. configure routing).
* **Input Validation and Sanitization:** Strictly validate incoming file content and line data to prevent injection attacks or unexpected processing errors caused by malformed data.
* **Secure Storage:** Ensure input, under-process, and processed data are stored securely, potentially with encryption at rest. Access to the `watch_dir` should be restricted.
* **Secure File Uploads:** If a file upload endpoint is added, it must handle large files securely, validate file types/sizes, scan for malware, and prevent directory traversal attacks.
* **Secrets Management:** Configuration containing sensitive information (e.g., database credentials, API keys) should be managed securely using environment variables or a dedicated secrets management system, not hardcoded or stored in plain text config files.
* **Robust Logging and Monitoring:** Beyond the in-memory history, integrate with a centralized logging system for long-term storage and analysis. Set up comprehensive monitoring and alerting on key metrics (error rates, queue size, processing latency).
* **Graceful Shutdown:** Implement more sophisticated shutdown handling to allow in-progress processing to complete or be checkpointed before the application exits.

Securing file uploads or protecting output data involves:

* **Upload:** Use a secure protocol (HTTPS), authenticate the uploader, validate file metadata (size, type), scan content for threats, store temporarily in a secure location, and then move to `unprocessed` only after checks pass.
* **Output:** Store processed data in a location with strict access controls. If data is sensitive, encrypt it before storing. If exposing processed data via an API, implement authentication and authorization for access.

## 🎉 Congratulations!

This project has been a journey through the fundamental building blocks of data processing systems. From basic pipelines to stateful routing, observability, resilience, and deployability, you've touched upon key concepts used in real-world infrastructure. This experience provides a strong foundation for understanding and building more complex data-intensive applications.
