# Daily Learning Log

This document serves as a daily journal to track what I've learned and what confused me during my work on this project. The goal is to reflect on my progress, identify areas needing more attention, and foster a better understanding over time.

---

## [07-05-2025]

### What I Learned Today:

* **Core Python Concepts:** Practiced fundamental Python skills through Language Drills, including working with basic data structures, comprehensions, functions, scope, error handling, iterators, and generators.
* **Documentation Fundamentals:** Engaged with the Doctools material, reinforcing knowledge of Markdown essentials like formatting, lists, tables, and links.
* **Mermaid.js Diagrams:** Learned how to create simple diagrams like sequence diagrams directly within Markdown using Mermaid.js syntax.

### What Confused Me Today:

* **Advanced Documentation Tools:** Started exploring tools like Draw.io and MkDocs for more complex documentation needs, feeling a bit unsure about the best practices for embedding external diagrams or structuring documentation for larger projects.
* **README Structure:** Grappled with minor decisions around structuring and linking within the main project README to effectively summarize progress and link to specific drills or project levels.

---

## [08-05-2025]

### What I Learned Today:

* **Consolidated Python Skills:** Further solidified understanding of Pythonic idioms and standard library usage through continued work on Language Drills.
* **Deepened Documentation Practice:** Gained more hands-on experience with the Doctools, likely practicing creating READMEs and potentially working with MkDocs setup or basic diagramming.

### What Confused Me Today:

* **Applying Doctools to Project:** Continued to find it slightly challenging to consistently apply all recommended documentation practices (like specific diagram types or detailed READMEs) to the ongoing project structure effectively.
* **Balancing Detail in Docs:** Unsure about the right level of detail required for documentation across different project parts – how much should go in a README vs. separate design docs or daily logs.

---

## [09-05-2025]

### What I Learned Today:

* **Dataflow Framework Basics (L0-L4):** Rapidly progressed through the initial levels of the Dataflow Framework project. Learned to build a basic script (L0), add CLI arguments and config (L1), modularize code (L2), implement dynamic loading from config (L3), and introduce stream processing and stateful processors (L4).
* **Debugging Circular Dependencies:** Successfully identified and resolved a circular dependency issue encountered during the development of the Dataflow Framework, reinforcing debugging skills and modular design principles (potentially by moving type definitions).

### What Confused Me Today:

* **Stream Processor Design:** Designing processors that operate on iterators (L4) and handle internal state introduced complexity compared to simple line-by-line functions. Figuring out how to handle initialization and state within these processors was challenging.
* **Preparing for DAGs (L5):** Began thinking about the requirements for Level 5 (DAG Routing), finding it conceptually challenging to move from a linear pipeline to a dynamic, tag-based routing system.

---

## [10-05-2025]

### What I Learned Today:

* **Advanced Dataflow Concepts (L5-L7):** Completed significant portions of the Dataflow Framework (L0-L7). Mastered DAG routing and conditional flows based on tags (L5), built a state-based routing engine resembling a state machine (L6), and implemented observability features including metrics, tracing, and a FastAPI web dashboard (L7).
* **Concurrent Programming Basics:** Gained experience running components like the FastAPI dashboard on a separate thread while the main processing continued, introducing concepts of concurrency and shared state (with potential use of locks).

### What Confused Me Today:

* **Designing State-Based Routing (L6):** Building the state transition engine and correctly handling tagged inputs/outputs and potential cycles was a significant design challenge.
* **Integrating Observability (L7):** Integrating metrics collection and tracing into the existing processing flow and exposing them correctly via the FastAPI application required careful thought about where to add hooks and manage shared data structures.
* **Preparing for Operationalization (L8/Final):** Started looking ahead to Level 8 (Folder Monitoring) and the Final Project, anticipating confusion related to implementing robust file monitoring, crash recovery, and packaging the entire system for deployment (Docker, Makefiles).

---

## [11-05-2025]

### What I Learned Today:

* **Completed Dataflow Framework (L8 & Final):** Successfully implemented the Automated Folder Monitor and Recovery (L8) and completed the Final Project requirements. This involved setting up the folder-based processing queue, implementing crash recovery logic, and adding deployment artifacts like a Makefile and Dockerfile.
* **System Integration and Operationalization:** Gained practical experience in integrating different system components (monitor, processor, dashboard) and preparing the application for real-world use, including defining execution modes and writing deployment notes.
* **Project Reflection and Documentation:** Completed the final project write-up, prompting reflection on architectural choices, tradeoffs, scalability, and security, and solidifying the importance of comprehensive documentation.

### What Confused Me Today:

* **Robust Folder Monitoring:** Ensuring the folder monitoring was truly robust, handling edge cases like partial file writes or race conditions if multiple instances were running, required careful consideration.
* **Integration Complexity:** While resolved, the process of seamlessly integrating the continuous monitoring loop with the existing processing engine and the live dashboard presented potential points of confusion and required diligent testing.

---

## [12-05-2025]

### What I Learned Today:

* **Introduction to Persistence:** Began the Persistence Drills, learning about different methods for serializing and deserializing Python objects using built-in libraries like Pickle and JSON, and external ones like PyYAML.
* **SQLite Fundamentals:** Started working with `sqlite3` in Python, learning how to connect to databases, create tables, and perform basic Create, Read, Update, and Delete (CRUD) operations.

### What Confused Me Today:

* **Choosing Serialization Format:** Figuring out when to use Pickle vs. JSON vs. YAML, considering factors like readability, security, and object type support, was initially confusing.
* **Basic SQL Syntax:** While seemingly straightforward, remembering specific SQL syntax for table creation and basic queries within the `sqlite3` context required referencing documentation.

---

## [13-05-2025]

### What I Learned Today:

* **Advanced SQLite with Python:** Completed the SQLite portion of the persistence drills, gaining experience with more advanced `sqlite3` usage including transactions, exception handling, searching, data validation, joins, aggregation, and batch insertion.
* **Introduction to ORM (SQLAlchemy):** Began the SQLAlchemy + Pydantic drills, learning the basic concepts of Object-Relational Mappers (ORM) and setting up simple SQLAlchemy models and connections.
* **Slideshow Preparation:** Started organizing thoughts and content for the project slideshow, which helped in summarizing the work done so far and identifying key learning points.

### What Confused Me Today:

* **ORM Paradigm Shift:** Transitioning from writing raw SQL with `sqlite3` to using an ORM like SQLAlchemy felt like a significant shift in thinking and required understanding new concepts like sessions and declarative mapping.
* **SQLAlchemy and Pydantic Integration:** Integrating Pydantic for data validation with SQLAlchemy models introduced an additional layer of complexity and required understanding how they interact.
* **Structuring the Slideshow:** Deciding on the most effective structure and key takeaways for the project slideshow to clearly present the complex Dataflow Framework and persistence work was challenging.

---

## [14-05-2025]

### What I Learned Today:

* **Intermediate SQLAlchemy:** Focused on the intermediate level Persistence Drills, practicing more complex SQLAlchemy operations such as filtering data, updating existing records, and deleting data using the ORM.
* **SQLAlchemy Session Management:** Gained a better understanding of how SQLAlchemy sessions work and their importance in managing database interactions.

### What Confused Me Today:

* **Handling Updates and Deletes with ORM:** Ensuring updates and deletions were performed correctly and efficiently using SQLAlchemy's methods, especially in different session states, required careful attention.
* **Querying Relationships (Upcoming):** Anticipating the next steps in the persistence drills involving relationships between tables using SQLAlchemy, expecting potential confusion in defining and querying these connections effectively.

---

## [15-05-2025]

### What I Learned Today:

* **Advanced Persistence Patterns:** Completed the Persistence Drills, covering advanced topics like schema evolution, model boundary enforcement (SQLA vs Pydantic), idempotent upserts, versioned data storage, concurrency/race conditions, handling large binary data, and comparing schema-first vs code-first modeling.
* **Figure Caption Extraction Requirements:** Began exploring the requirements for the new Figure Caption Extraction project, understanding the high-level goals, user/admin/ops expectations, and potential tools/APIs (BioC-PMC, PubTator3).
* **Project Initiation and Structure:** Started the initial steps for the Figure Caption Extraction project, likely involving setting up the basic folder structure and beginning the design phase.

### What Confused Me Today:

* **Understanding External APIs:** Grasping the details and usage of the external APIs (BioC-PMC, PubTator3) for extracting paper structure and entities from scientific publications presents a new learning curve.
* **Designing the Extraction Pipeline:** Figuring out how to design a robust and extensible pipeline to extract, store (potentially in DuckDB), and query the required information (title, abstract, captions, entities) from diverse sources is a significant design challenge.
* **Structuring a New Project:** Deciding on the initial architecture and folder structure for a brand new project like Figure Caption Extraction requires careful consideration to ensure it is modular and scalable from the start.