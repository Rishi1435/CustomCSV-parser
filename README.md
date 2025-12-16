# Custom CSV Parser Implementation

## Overview
This project implements a robust CSV (Comma-Separated Values) Reader and Writer from scratch in Python, without relying on the built-in `csv` module. It demonstrates low-level file I/O, string manipulation, state management, and performance benchmarking.

The implementation correctly handles:
- Standard comma-delimited fields.
- Fields enclosed in double quotes.
- Escaped double quotes (`""`) within fields.
- Embedded newlines within quoted fields.

## Setup Instructions

### Prerequisites
- Python 3.6 or higher.
- No external dependencies are required (standard library only).

### Installation
1. Clone this repository.
2. Navigate to the project folder.

## Usage Examples

### Using the CustomCsvWriter

```python
from custom_csv import CustomCsvWriter

data = [
    ["Name", "Age", "Bio"],
    ["Alice", 30, "Loves coding"],
    ["Bob", 25, 'He said, "Hello World!"'],  # Contains quotes and comma
    ["Charlie", 35, "First Line\nSecond Line"] # Contains newline
]

with open('output.csv', 'w', encoding='utf-8') as f:
    writer = CustomCsvWriter(f)
    writer.writerows(data)

```

### Using the CustomCsvReader
```python
from custom_csv import CustomCsvReader

with open('output.csv', 'r', encoding='utf-8') as f:
    reader = CustomCsvReader(f)
    for row in reader:
        print(row)

```

## Performance Results
Tested on My OS/Processor with 10,000 rows.

| Operation | Standard Lib | Custom Lib | Slowdown Factor |
|-----------|--------------|------------|-----------------|
| Write     | 0.033s       | 0.066s     | 2.0x (Excellent)|
| Read      | 0.018s       | 0.218s     | 11.9x           |

**Analysis:**
The custom writer is highly efficient because it leverages Python's optimized string methods. The reader is slower because it requires a Python-level `while` loop to manage the state machine for character-by-character parsing, whereas the standard library handles this in C.
