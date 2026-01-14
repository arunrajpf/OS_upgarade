import json
import glob

# Find all files matching the pattern
file_paths = glob.glob("error-*.sys.comcast.net.json")

# Iterate over each file path
for file_path in file_paths:
    # Extract server name from the file path
    server_name = file_path.split("error-")[1].split(".")[0]

    # Open and process the JSON file
    with open(file_path, "r") as file:
        json_data = json.load(file)

    # Iterate over tasks
    for task in json_data["tasks"]:
        # Extract message information
        message_raw = task.get("words_after", "")

        # Splitting message string
        message_parts = message_raw.split(", ")

        # Creating the final dictionary with split parts
        for part in message_parts:
            output_dict = {
                "server_name": server_name,
                "message": part.strip('"')
            }
            # Printing the dictionary
            print(json.dumps(output_dict, indent=2))
