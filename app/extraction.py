import json

# Load JSON file
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

# Load legal data
file_path = "/content/ma_parking_master_part1.json"  # Change path if needed
legal_data = load_json(file_path)

# Extract key sections
legal_framework = legal_data["ma_parking_system_part1"]["legal_framework"]
appeal_process = legal_data["ma_parking_system_part1"]["appeal_process"]

# Print example keys
print("Legal Framework Keys:", legal_framework.keys())
print("Appeal Process Keys:", appeal_process.keys())