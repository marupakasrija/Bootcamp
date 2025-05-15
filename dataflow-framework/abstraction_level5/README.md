# Level 5: DAG Routing and Conditional Flows

## Task Description 

In this level, you will build a general-purpose DAG-based processing engine where each line can take a different path through the system based on its content or tags. 

This is a major abstraction step — you’re no longer just transforming lines, you're building a flexible routing system.

### 📋 Motivating Example: Log Routing

Imagine you're building a log processing tool.

Each line might be:
- An error that needs to be logged separately
- A warning to be counted
- A regular message to just pass through

#### Different kinds of lines need different processors.

### Desired Flow
1. All lines go through a trim processor.
2. Each line is tagged by tag_error or tag_warn (adds routing info).
3. A generic splitter sends lines to different branches:
   - **`errors`** → _count_ and _archive_ 
   - **`warnings`** → _tally_
   - **`general`** → _format_ and _print_
   
Now you need a system where:
1. Processors can tag their output
2. The engine routes based on tags
3. You define all routing behavior in a config file

### 🧠 What You’re Building
A general DAG-based processing engine where:
- Each processor is a **node**
- Processors yield **tagged lines** (e.g., (`"errors", line`))
- The engine uses **routing rules** to send lines to the right downstream node(s)
- You can define **multiple paths** in one config


---
## 📂 Structure
```
abstraction-level-5/
├── cli.py
├── core/             # Core processing and routing logic
│   ├── __init__.py
│   ├── engine.py     # The DAG execution engine
│   └── utils.py      # Helpers (like get_stream_processor from L4)
├── main.py
├── pipeline.py       # Loads DAG config
├── types.py          # Updates types for tagged lines and DAG config
├── processors/       # Processor modules
│   ├── __init__.py
│   ├── upper.py
│   ├── snake.py
│   └── taggers.py    # New processor for tagging
├── dag_config.yaml   # New config file for DAG
└── requirements.txt
```

---

## ⚙️ Installation

```bash
uv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
uv pip install -r requirement.txt
```

---

## 🔧 Configuration (`pipeline.yaml`)
- In `pipeline.yaml`, list each processing step (node) by name, point to its processor function (e.g., `processors.trimming.trim`), and map output tags to the next node. 


- Use `end` to mark terminal stages. All routing behavior lives here—no code changes needed for new branches.


---

## 🚦Implementation

```plaintext
- The DAGExecutionEngine.run method is the most complex part. The simple processing_backlog list sketch is illustrative but not a robust queue management system. A real implementation would need:
  - A mechanism to feed lines into node-specific input queues.
  - A loop that processes nodes when they have input in their queue.
  - Handling of processor yielding multiple outputs ((tag, line)).
  - Careful management of the processing lifecycle and knowing when all lines are processed and queues are empty.
  - Using queue.Queue for thread safety if moving towards concurrency later.
- Adapting str -> str processors to Iterator[str] -> Iterator[TaggedLine] is crucial. The simplest way for this level is to wrap them in TaggedStreamProcessor classes that apply the old function and yield a fixed output tag.
- Error handling within the engine loop (what happens if a processor raises an exception?) is important.
```

---

## 🚀 Usage

1. To know the usage, use:
```bash
python main.py --help
```

2. Place your logs in `input.txt`, then:
```bash
python main.py --input input.txt --config pipeline.yaml --output output.txt
```
- Omit `--output` to print to stdout.


---

## 🧪 Example

**Input File**
```
This is a general message
ERROR: Something went wrong
Another general line
WARNING: Low disk space
Final line

```

**Run**
```bash
python -m abstraction_level5.main --input abstraction_level5/input.txt --config abstraction_level5/dag_config.yaml
```

**Output**

```text
Starting DAG processing...
Loading DAG engine from config file: abstraction_level5/dag_config.yaml
Loaded node 'start' with processor 'processors.taggers.StartTagger'
Loaded node 'content_router' with processor 'processors.taggers.ContentTagger'
Loaded node 'error_handler' with processor 'processors.taggers.ErrorOnlyProcessor'
DEBUG: Attempt 1: Dynamically importing module 'processors.upper' relative to package='abstraction_level5'
DEBUG: Attempt 2: Dynamically importing module using full path='abstraction_level5.processors.upper'
DEBUG: Attempt 2: Successfully imported module: abstraction_level5.processors.upper
Loaded node 'warn_formatter' with processor 'processors.upper.UppercaseProcessor'
DEBUG: Attempt 1: Dynamically importing module 'processors.snake' relative to package='abstraction_level5'
DEBUG: Attempt 2: Dynamically importing module using full path='abstraction_level5.processors.snake'
DEBUG: Attempt 2: Successfully imported module: abstraction_level5.processors.snake
Loaded node 'final_formatter' with processor 'processors.snake.SnakecaseProcessor'
DEBUG: Attempt 1: Dynamically importing module 'processors.taggers' relative to package='abstraction_level5'
DEBUG: Attempt 2: Dynamically importing module using full path='abstraction_level5.processors.taggers'
DEBUG: Attempt 2: Successfully imported module: abstraction_level5.processors.taggers
Loaded node 'output_collector' with processor 'processors.taggers.OutputCollector'
Streaming pipeline loaded successfully with 3 steps.
Reading from file: abstraction_level5/input.txt with utf-16 encoding
Running DAG execution engine...
DEBUG: Processing lines with node 'start' (5 lines)
DEBUG: Node 'start' emitted ('start', 'This is a general message')
DEBUG: Node 'start' emitted ('start', 'ERROR: Something went wrong')
DEBUG: Node 'start' emitted ('start', 'Another general line')
DEBUG: Node 'start' emitted ('start', 'WARNING: Low disk space')
DEBUG: Node 'start' emitted ('start', 'Final line')
DEBUG: Processing lines with node 'content_router' (5 lines)
DEBUG: Node 'content_router' matched rule for tag 'is_error', yielding ('is_error', 'ERROR: Something went wrong')
DEBUG: Node 'content_router' no rule matched, yielding ('general', 'This is a general message')
DEBUG: Node 'content_router' no rule matched, yielding ('general', 'Another general line')
DEBUG: Node 'content_router' matched rule for tag 'is_warn', yielding ('is_warn', 'WARNING: Low disk space')
DEBUG: Node 'content_router' no rule matched, yielding ('general', 'Final line')
DEBUG: Processing lines with node 'error_handler' (1 lines)
DEBUG: Node 'error_handler' found ERROR, yielding ('error_processed', 'ERROR: Something went wrong')
DEBUG: Processing lines with node 'warn_formatter' (1 lines)
DEBUG: Node 'warn_formatter' yielding ('warn_formatted', 'WARNING: LOW DISK SPACE')
DEBUG: Processing lines with node 'final_formatter' (4 lines)
DEBUG: Node 'final_formatter' yielding ('ready_for_output', 'this_is_a_general_message')
DEBUG: Node 'final_formatter' yielding ('ready_for_output', 'another_general_line')
DEBUG: Node 'final_formatter' yielding ('ready_for_output', 'warning:_low_disk_space')
DEBUG: Node 'final_formatter' yielding ('ready_for_output', 'final_line')
DEBUG: Processing lines with node 'output_collector' (5 lines)
DEBUG: Line reached final output: 'ERROR: Something went wrong'
DEBUG: Line reached final output: 'this_is_a_general_message'
DEBUG: Line reached final output: 'another_general_line'
DEBUG: Line reached final output: 'warning:_low_disk_space'
DEBUG: Line reached final output: 'final_line'
DAG execution finished, yielding final collected output.
ERROR: Something went wrong
this_is_a_general_message
another_general_line
warning:_low_disk_space
final_line
DAG processing finished.
```
(The exact order of the final output lines might vary slightly depending on the internal processing order of the engine's loop when multiple nodes have input, but all five lines should appear, transformed according to the paths they took through the DAG.)


---

## 🔑 Highlights

- Successful dynamic loading of processors using the fallback logic.
- Lines being routed based on tags emitted by the content_router.
- Different processors (error_handler, warn_formatter, final_formatter) being applied to different lines.
- Fan-in to the final_formatter and output_collector nodes.
- Lines reaching the output_collector being collected as the final output.


---
