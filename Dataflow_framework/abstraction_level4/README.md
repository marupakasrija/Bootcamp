# Level 4: Stream Processing and Stateful Processors

## Task Description

In this level, you will move from simple `str -> str` functions to full stream-based processing. This opens the door to much more powerful behaviors, including:

- Returning multiple lines from one line (fan-out)
- Combining multiple lines into one output (fan-in)
- Stateful processing (e.g. counters, buffers, aggregators)
- More modular and lifecycle-aware processors

### Problem Context

The current `str -> str` processors are limited:

- They can’t drop lines easily.
- They can’t emit zero or multiple lines.
- They can’t maintain state across lines. 

To build a real-world pipeline, we need processors that operate on streams — meaning, they take an iterator of lines and yield processed output lines one by one.

You will:
- Redesign your processor interface to be `Iterator[str] -> Iterator[str]`
- Convert your simple processors using a decorator or wrapper so you can still reuse existing ones
- Build at least one processor that requires internal state (e.g., line counting)


## Project Structure
```
abstraction-level-4/
├── cli.py
├── core.py         # Adapts to stream processors
├── main.py
├── pipeline.py     # Loads stream processors
├── types.py        # Updates types
├── processors/
│   ├── __init__.py
│   ├── upper.py    # Uses wrapper
│   ├── snake.py    # Uses wrapper
│   └── stateful.py # New stateful processor
└── pipeline.yaml   # References stateful processors

```

## ⚙️ Requirements

* **Python 3.7+**
* Install dependencies:

  ```bash
  uv pip install typer
  ```

## 🚀 Quick Start

1. **Prepare an input file** (`input.txt`):

    ```text
    Hello World
    Another Line
    TEST this
    ```

2. **Run the CLI** from this folder:
   ```bash
   python -m abstraction_level4.main --input abstraction_level4/input.txt --config abstraction_level4/pipeline.yaml
   ```
3. **Output** :
   ```text
   Starting streaming processing...
    Loading streaming pipeline from config file: abstraction_level4/pipeline.yaml
    DEBUG: Attempt 1: Dynamically importing module 'processors.stateful' relative to package='abstraction_level4'
    DEBUG: Attempt 2: Dynamically importing module using full path='abstraction_level4.processors.stateful'
    DEBUG: Attempt 2: Successfully imported module: abstraction_level4.processors.stateful
    DEBUG: Attempt 1: Dynamically importing module 'processors.upper' relative to package='abstraction_level4'
    DEBUG: Attempt 2: Dynamically importing module using full path='abstraction_level4.processors.upper'
    DEBUG: Attempt 2: Successfully imported module: abstraction_level4.processors.upper
    DEBUG: Attempt 1: Dynamically importing module 'processors.snake' relative to package='abstraction_level4'
    DEBUG: Attempt 2: Dynamically importing module using full path='abstraction_level4.processors.snake'
    DEBUG: Attempt 2: Successfully imported module: abstraction_level4.processors.snake
    Streaming pipeline loaded successfully with 3 steps.
    Writing to stdout...
    Reading from file: abstraction_level4/input.txt with utf-16 encoding
    item_#1:_hello_world
    item_#2:_another_line
    item_#3:_test_this
    Streaming processing finished.
   ```

(This output order may vary depending on processor sequence.)
---

