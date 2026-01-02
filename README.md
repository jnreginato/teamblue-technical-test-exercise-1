# teamblue-technical-test-exercise-1

## Overview

This repository contains the solution for **Exercise 1 of the team.blue Technical Test**.

The goal of this exercise is to process HTTP request logs and generate a **daily traffic report per IP address**, following the specifications provided in the technical assignment.

The solution is implemented in **Python 3**, using only **standard libraries**, with a strong focus on:

- Code clarity
- Robustness
- Testability
- Ease of execution

---

## Problem Summary

Given a log file containing HTTP request records, the program must generate a report that includes, per IP address:

- IP Address  
- Number of requests  
- Percentage of total requests  
- Total bytes sent  
- Percentage of total bytes sent  

### Constraints

- Only records with `STATUS == "OK"` are considered
- Input records are semicolon-separated
- Output must be sorted by **number of requests (descending)**
- The report can be generated in **CSV** or **JSON** format

---

## Input Format

Each line in the input log file follows this structure:

`<TIMESTAMP>;<BYTES><STATUS>;<REMOTE_ADDR>`

Example:

`2026-01-01T08:00:00;512;OK;192.168.1.1`

Malformed lines or records with a status different from `OK` are safely ignored.

---

## Project Structure

```
.
├── report_generator.py       # Main application logic
├── test_report_generator.py  # Unit tests
├── logfiles/
│ └── requests.log            # Sample input log file
└── README.md
```

---

## Requirements

- Python **3.10+** (tested with Python 3.13)
- No external dependencies

---

## How to Run

The script exposes a **Command Line Interface (CLI)** using `argparse`.

### Generate a CSV report (default)

```bash
python3 report_generator.py \
  --input logfiles/requests.log \
  --output reports/ipaddr.csv
```

### Generate a JSON report

```bash
python3 report_generator.py \
  --input logfiles/requests.log \
  --output reports/ipaddr.json \
  --format json
```

### CLI Help

```bash
python3 report_generator.py --help
```

---

## Output

### CSV Output Example

```csv
IP Address,Number of Requests,Percentage of Total Requests,Total Bytes Sent,Percentage of Total Bytes Sent
192.168.1.1,1,50.0%,512,50.0%
192.168.1.2,1,50.0%,512,50.0%
```

### JSON Output Example

```json
[
  {
    "ip_address": "192.168.1.1",
    "requests_count": 1,
    "requests_percentage": "50.0%",
    "bytes_sent": 512,
    "bytes_percentage": "50.0%"
  },
  {
    "ip_address": "192.168.1.2",
    "requests_count": 1,
    "requests_percentage": "50.0%",
    "bytes_sent": 512,
    "bytes_percentage": "50.0%"
  }
]
```

---

## Error Handling & Robustness

The parser is intentionally defensive and handles:

- Malformed lines 
- Missing or extra fields 
- Non-numeric byte values 
- Empty lines 
- Invalid statuses 
- Invalid records are ignored without interrupting execution.

---

## Testing

Basic unit tests are provided using Python’s built-in unittest module.

To run the tests:

```bash
python3 -m unittest test_report_generator.py
```

---

## Design Notes

- Business logic is fully decoupled from CLI parsing
- The script is safe to import as a module 
- Paths are provided externally (no hardcoded absolute paths)
- The solution favors readability and correctness over premature optimization

---

## Author

Jonatan Reginato

---

## Notes

This implementation was developed specifically for the team.blue Technical Test and reflects production-oriented coding practices commonly used in backend and infrastructure-related tooling.
