# 🔢 Level 2 – Modular Structure and Standardized Processing

This project refactors the code into a modular structure and introduces a standardized processor signature for better scalability and maintainability.

---

## 🏗 Structure

```bash
abstraction-level-2/
├── cli.py
├── core.py
├── main.py
├── pipeline.py
├── types.py
└── requirements.txt
```

---

## 🛠 Setup

✅ **Requirements**
- Python 3
- Install dependencies:

```bash
pip install -r requirements.txt
```

---

 **.env Configuration**

The .env file controls the default mode:

Available modes:

- uppercase → Converts lines to UPPERCASE

- snakecase → Converts lines to snake_case

---

## Input File 

```bash
Hello World  
Another Line
  TEST this
```

---

## Run and Save Output to File

```bash
python process.py --input input.txt --mode snakecase --output out.txt
```
```bash
python process.py --input input.txt --mode uppercase --output out.txt
```

## Output 
- (Uppercase Mode)
```bash
Processing with mode: uppercase
HELLO WORLD
ANOTHER LINE
TEST THIS
```

- (Snakecase Mode)
```bash
Processing with mode: snakecase
hello_world
another_line
test_this
```