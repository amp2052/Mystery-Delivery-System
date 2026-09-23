import json
import math
import os
import sys
import csv

def calculate_distance(point_a, point_b):
    return math.sqrt((point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1])**2)

def normalize_input_data(raw_data):
    canonical_data = {
        "warehouses": {},
        "agents": {},
        "packages": []
    }
    
    warehouses_raw = raw_data.get("warehouses", {})
    if isinstance(warehouses_raw, list):
        for wh in warehouses_raw:
            canonical_data["warehouses"][wh["id"]] = wh["location"]
    else:
        canonical_data["warehouses"] = warehouses_raw

    agents_raw = raw_data.get("agents", {})
    if isinstance(agents_raw, list):
        for ag in agents_raw:
            canonical_data["agents"][ag["id"]] = ag["location"]
    else:
        canonical_data["agents"] = agents_raw

    packages_raw = raw_data.get("packages", [])
    for pkg in packages_raw:
        canonical_data["packages"].append({
            "id": pkg["id"],
            "warehouse": pkg.get("warehouse") or pkg.get("warehouse_id"),
            "destination": pkg["destination"]
        })
        
    return canonical_data

def run_simulation(input_file_path, output_json_path, output_csv_path):
    with open(input_file_path, 'r') as file:
        raw_json_data = json.load(file)
        
    data = normalize_input_data(raw_json_data)
    
    active_agent_positions = {agent_id: list(coords) for agent_id, coords in data["agents"].items()}
    metrics_tracker = {
        agent_id: {"packages_delivered": 0, "total_distance": 0.0}
        for agent_id in data["agents"]
    }
    agent_work_queues = {agent_id: [] for agent_id in data["agents"]}
    
    for package in data["packages"]:
        target_wh_id = package["warehouse"]
        wh_location = data["warehouses"].get(target_wh_id)
        
        if not wh_location:
            continue
            
        assigned_agent = None
        shortest_vector = float('inf')
        
        for agent_id in sorted(data["agents"].keys()):
            initial_agent_loc = data["agents"][agent_id]
            vector_dist = calculate_distance(initial_agent_loc, wh_location)
            
            if vector_dist < shortest_vector:
                shortest_vector = vector_dist
                assigned_agent = agent_id
                
        if assigned_agent:
            agent_work_queues[assigned_agent].append(package)

    for agent_id, job_queue in agent_work_queues.items():
        for package in job_queue:
            wh_loc = data["warehouses"][package["warehouse"]]
            dropoff_loc = package["destination"]
            
            departure_point = active_agent_positions[agent_id]
            pickup_overhead = calculate_distance(departure_point, wh_loc)
            delivery_overhead = calculate_distance(wh_loc, dropoff_loc)
            
            combined_leg_distance = pickup_overhead + delivery_overhead
            metrics_tracker[agent_id]["total_distance"] += combined_leg_distance
            metrics_tracker[agent_id]["packages_delivered"] += 1
            
            active_agent_positions[agent_id] = dropoff_loc

    compiled_report = {}
    optimal_agent_id = None
    best_efficiency_score = float('inf')
    
    for agent_id in sorted(metrics_tracker.keys()):
        summary = metrics_tracker[agent_id]
        total_delivered = summary["packages_delivered"]
        cumulative_dist = round(summary["total_distance"], 2)
        efficiency_ratio = round(cumulative_dist / total_delivered, 2) if total_delivered > 0 else 0.0
        
        compiled_report[agent_id] = {
            "packages_delivered": total_delivered,
            "total_distance": cumulative_dist,
            "efficiency": efficiency_ratio
        }
        
        if total_delivered > 0 and efficiency_ratio < best_efficiency_score:
            best_efficiency_score = efficiency_ratio
            optimal_agent_id = agent_id

    compiled_report["best_agent"] = optimal_agent_id
    
    with open(output_json_path, 'w') as out_file:
        json.dump(compiled_report, out_file, indent=4)

    if optimal_agent_id:
        with open(output_csv_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Agent ID", "Packages Delivered", "Total Distance", "Efficiency"])
            stats = compiled_report[optimal_agent_id]
            writer.writerow([
                optimal_agent_id,
                stats["packages_delivered"],
                stats["total_distance"],
                stats["efficiency"]
            ])

def batch_process_pipeline():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    output_dir = os.path.join(base_dir, "output")
    
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(data_dir) or not os.listdir(data_dir):
        print(f"Error: Directory '{data_dir}' is empty or missing.")
        sys.exit(1)
        
    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            input_path = os.path.join(data_dir, filename)
            output_json_path = os.path.join(output_dir, f"report_{filename}")
            output_csv_path = os.path.join(output_dir, f"top_performer_{filename.replace('.json', '.csv')}")
            
            try:
                run_simulation(input_path, output_json_path, output_csv_path)
                print(f"Processed: {filename}")
            except Exception as e:
                print(f"Failed {filename}: {str(e)}")

if __name__ == "__main__":
    batch_process_pipeline()
