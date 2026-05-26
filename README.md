# FastBox Logistics Delivery Simulator

## Overview

This project simulates package delivery operations for FastBox logistics company.

The system:
- Reads multiple JSON test case files
- Assigns packages to nearest delivery agents
- Calculates travel distances
- Generates delivery reports
- Exports reports in JSON and CSV format

---

## Features

- Automatic processing of all test cases
- Nearest agent assignment
- Delivery simulation
- JSON report generation
- CSV export
- Flexible JSON structure handling

---

## Assumptions

- Agents start from their initial coordinates
- Nearest available agent is selected
- Efficiency = distance / packages
- Supports both:
  - warehouse
  - warehouse_id

---

## Project Structure

Python Assignment -2026/

data/
    TEST_CASES
output/
    REPORT
src/
    main.py
README.md
requirements.txt
.gitignore

---

## Run Project


python src/main.py




## Output

Reports are generated inside the output folder.