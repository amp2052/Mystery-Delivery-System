import json
import math
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_FOLDER = os.path.join(BASE_DIR, "data")

OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def calculate_distance(p1, p2):
    return math.sqrt(
        (p2[0] - p1[0]) ** 2 +
        (p2[1] - p1[1]) ** 2
    )


def process_file(file_path):

    with open(file_path, "r") as file:
        data = json.load(file)

    warehouses = {}

    if isinstance(data["warehouses"], list):

        for warehouse in data["warehouses"]:
            warehouses[warehouse["id"]] = warehouse["location"]

    elif isinstance(data["warehouses"], dict):

        warehouses = data["warehouses"]

    agents = {}

    if isinstance(data["agents"], list):

        for agent in data["agents"]:
            agents[agent["id"]] = agent["location"]

    elif isinstance(data["agents"], dict):

        agents = data["agents"]

    report = {}

    for agent_id in agents:
        report[agent_id] = {
            "packages_delivered": 0,
            "total_distance": 0,
            "efficiency": 0
        }

    for package in data["packages"]:

        if "warehouse_id" in package:
            warehouse_id = package["warehouse_id"]

        elif "warehouse" in package:
            warehouse_id = package["warehouse"]

        else:
            continue

        warehouse_location = warehouses[warehouse_id]

        destination = package["destination"]

        nearest_agent = None

        minimum_distance = float("inf")

        for agent_id, agent_location in agents.items():

            distance_to_warehouse = calculate_distance(
                agent_location,
                warehouse_location
            )

            if distance_to_warehouse < minimum_distance:
                minimum_distance = distance_to_warehouse
                nearest_agent = agent_id

        delivery_distance = calculate_distance(
            warehouse_location,
            destination
        )

        total_trip_distance = (
            minimum_distance +
            delivery_distance
        )

        report[nearest_agent]["packages_delivered"] += 1

        report[nearest_agent]["total_distance"] += round(
            total_trip_distance,
            2
        )

    for agent_id in report:

        packages = report[agent_id]["packages_delivered"]

        distance = report[agent_id]["total_distance"]

        if distance > 0:
            efficiency = distance / packages
        else:
            efficiency = 0

        report[agent_id]["efficiency"] = round(
            efficiency,
            4
        )

    best_agent = max(
        report,
        key=lambda agent: report[agent]["efficiency"]
    )

    final_output = {
        "agent_report": report,
        "best_agent": best_agent
    }

    return final_output


for filename in os.listdir(DATA_FOLDER):

    if filename.endswith(".json"):

        file_path = os.path.join(
            DATA_FOLDER,
            filename
        )

        print(f"\nProcessing: {filename}")

        result = process_file(file_path)

        print(json.dumps(result, indent=4))

        output_filename = filename.replace(
            ".json",
            "_report.json"
        )

        output_path = os.path.join(
            OUTPUT_FOLDER,
            output_filename
        )

        with open(output_path, "w") as outfile:
            json.dump(result, outfile, indent=4)

        print(f"{output_filename} generated successfully!")