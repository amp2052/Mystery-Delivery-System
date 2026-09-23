# FastBox Logistics Delivery Simulator

A robust, pure Python logistics simulation system designed to parse variable warehouse datasets, map optimal courier package workloads, simulate real-time sequential routing parameters, and evaluate agent operational performance metrics.

## 🚀 How to Run the Project

This project uses standard native libraries and requires no extra dependencies.

1. Open your terminal at the root of the project folder and run:
   ```bash
   python src/main.py
   ```
2. Your generated outputs will appear cleanly structured inside the `output/` directory as `report_<name>.json` and `top_performer_<name>.csv`.

## 🛠️ Architecture & Core Assumptions

* **Structural Normalization Layer**: Dynamic conversion mechanisms natively accept heterogeneous JSON architectures (handles both dictionary maps and structured item lists for warehouses/agents, alongside variable parameters like `warehouse` vs `warehouse_id`).
* **Continuous State Routing**: Multi-package operations follow a strict First-In, First-Out (FIFO) queue order. The agent's physical coordinate grid tracking shifts seamlessly to each delivery location, making successive distance vectors calculate dynamically rather than resetting back to home bases.
* **Deterministic Tie-Breaking**: Equidistant vector mappings are handled using alphabetical key sorting rules (`A1` handles tasks before `A2`).
* **Operational Performance Evaluation**: The efficiency rating reflects the structural distance traveled divided by individual units delivered. The top performer is accurately defined by locating the lowest positive efficiency ratio index across active working courier entities.
