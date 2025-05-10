# 🔢 Level 1 – Parameters and CLI Interface

This project introduces:
- CLI (Command Line Interface) arguments
- Basic processing functions
- Configurable behavior using a `.env` file

---

## 🏗 Structure

```bash
abstraction-level-1/
├── .env
├── process.py
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