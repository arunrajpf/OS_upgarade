import json
import glob
 
# Find all files matching the pattern
file_paths = glob.glob("error-*.sys.comcast.net.json")
 
# Iterate over each file path
for file_path in file_paths:
    # Extract server name from the file path
    server_name = file_path.split("error-")[1].split(".")[0]
 
    # Create a new JSON file for the server
    output_file_path = f"error-{server_name}.json"
    with open(output_file_path, "w") as output_file:
        # Open and process the JSON file
        with open(file_path, "r") as file:
            json_data = json.load(file)
 
        # Initialize a list to store server tasks
        server_tasks = []
 
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
                # Add the dictionary to the server tasks list
                server_tasks.append(output_dict)
 
        # Read contents from controllernode.txt
        with open("controllernode.txt", "r") as controller_file:
            controller_contents = controller_file.read()
 
        # Append the specified lines and controller contents to the generated JSON file
        output_file.write('\n{"tasks":\n\n')
        json.dump(server_tasks, output_file, indent=2)
        output_file.write(',\n\n"The Controller Node is": ' + json.dumps(controller_contents, indent=2) + '\n}')
