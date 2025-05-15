# Persistence Drills

This repository contains a set of drills designed to help you learn and practice data persistence in Python, covering both file-based methods and database interactions with SQLite and later SQLAlchemy/PostgreSQL.

**Important:** These drills are for *your* learning and practice. Do not delegate the problem-solving to an LLM. Try each exercise yourself to understand the concepts and how you are implementing them. Use LLMs for clarifying doubts or understanding concepts *after* attempting the problems.

## Table of Contents

1.  [Getting Started](#getting-started)
2.  [File-Based Persistence](#file-based-persistence)
    * [Serialization & Deserialization](#serialization--deserialization)
    * [Custom Handling](#custom-handling)
3.  [SQLite Database Basics](#sqlite-database-basics)
    * [Concepts & Setup](#concepts--setup)
    * [Python `sqlite3` Practice](#python-sqlite3-practice)
4.  [SQLite Transactions](#sqlite-transactions)
5.  [Advanced Python Usage (ORM, SQLAlchemy, Pydantic, Async)](#advanced-python-usage-orm-sqlalchemy-pydantic-async)
    * [SQLAlchemy + Pydantic Practice](#sqlalchemy--pydantic-practice)
    * [Level-Up Drills: Real-World Design](#level-up-drills-real-world-design)

## Getting Started

* **Learn the Basics:** Before diving into the code, familiarize yourself with Python's built-in persistence capabilities, especially `pickle` and `json`.
    * Python Persistence Documentation: [https://docs.python.org/3/library/persistence.html](https://docs.python.org/3/library/persistence.html)
* **Prerequisites:**
    * Python 3
    * PyYAML (`pip install PyYAML`) for YAML exercises.
    * SQLite3 command-line tool (check your OS or download from [https://www.sqlite.org/download.html](https://www.sqlite.org/download.html)).
    * For Advanced sections: PostgreSQL, SQLAlchemy, Pydantic, asyncpg (`pip install sqlalchemy pydantic asyncpg psycopg2-binary`).
* **Repository Structure:** The drills are organized into directories (`file_based/`, `sqlite_basics/`, `sqlite_transactions/`, etc.). Navigate into the specific directory for each exercise set.

## File-Based Persistence

Located in the `file_based/` directory, these exercises cover various methods for saving and loading Python objects to files.

### Serialization & Deserialization

* **Pickle:** Serialize/deserialize Python objects.
* **JSON:** Work with JSON data format.
* **YAML:** Work with YAML data format (requires PyYAML).

### Custom Handling

* Serializing complex objects (like Graphs).
* Skipping attributes during serialization.
* Saving and restoring object state (like game state).
* Handling different versions of serialized data.
* Serializing custom collection classes.
* Handling objects with cyclic references.

Each subdirectory (`01_pickle_serialization/`, `02_pickle_deserialization/`, etc.) contains the specific exercise code and instructions on how to run them.

## SQLite Database Basics

Located in the `sqlite_basics/` directory, this section introduces interaction with SQLite databases using Python's built-in `sqlite3` module.

### Concepts & Setup

* Understand database basics, transactions, and ACID properties. (References to learning resources provided in the drill description).
* Install and test the SQLite3 command-line tool.
* Learn about SQLite's key characteristics (serverless, single file).

### Python `sqlite3` Practice

* Connecting to/creating a database (`store.db`).
* Creating tables (`products`, etc.).
* Basic CRUD operations (Create, Read, Update, Delete) using functions.
* Implementing CRUD operations within a Python class.
* Handling database exceptions.
* Searching data.
* Implementing data validation.
* Using basic transactions.
* Performing JOIN queries (introducing `categories` table).
* Performing aggregation queries (SUM, COUNT, AVG).
* Exporting data to CSV.
* Performing batch insertions.

Each subdirectory (`01_setup_and_test/`, `02_basic_crud/`, etc.) contains the specific exercise code. Refer to the detailed instructions for running each script from its respective directory.

## SQLite Transactions

Located in the `sqlite_transactions/` directory, these exercises focus specifically on using transactions to maintain data integrity in more complex scenarios.

* Basic transaction commit and rollback.
* Transactions involving updates across multiple tables.
* Using transactions for batch inserts.
* Simulating transactional banking operations.
* Handling complex business logic atomically within a transaction (e.g., inventory management).

Each subdirectory (`01_basic_transaction/`, `02_multi_table_transaction/`, etc.) contains the specific exercise code.

## Advanced Python Usage (ORM, SQLAlchemy, Pydantic, Async)

This section, covered in separate directories (not detailed in the provided text but implied by the exercise descriptions), delves into more advanced database interaction patterns.

* **ORM Concepts:** Learn what an Object-Relational Mapper (ORM) is and why it's used.
* **SQLAlchemy + Pydantic:** Practice using SQLAlchemy models with Pydantic for data validation and serialization layers.
    * Define Models and Schemas.
    * Perform CRUD operations via SQLAlchemy sessions.
    * Filter, Update, and Delete data.
    * Handle relationships between models.
    * Use transactions for bulk operations.
    * Convert operations to be asynchronous (requires AsyncIO and async database drivers like asyncpg for Postgres).
* **Level-Up Drills: Real-World Design:** Tackle more complex, practical scenarios:
    * Schema Evolution and Migrations.
    * Model Boundary Enforcement (ORM vs API models).
    * Idempotent Upserts.
    * Versioned Data Storage.
    * Concurrency and Race Condition Management.
    * Handling Large Binary Data.
    * Schema-First vs Code-First Modeling.
    * Data Lifecycle Management (Soft Deletes).
    * Boundary Testing with Large Datasets.

---
