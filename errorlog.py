import json
from datetime import datetime
 
with open("rocky_error_build_log.txt", "r") as file:
    lines = file.readlines()
 
output_data = []
 
for i, line in enumerate(lines):
    if "fatal" in line.lower():
        start_index = max(0, i - 1)
        end_index = min(len(lines), i + 2)
 
        words_before = " ".join(lines[start_index].split()[-15:])
        words_after = " ".join(lines[i].split()[:15])
 
        output_data.append({
            "words_before": words_before,
            "words_after": words_after
        })
 
# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")
 
# Construct the output file name with the current date
output_file_name = f"error-{current_date}.json"
 
# Write output to the JSON file with the constructed name
with open(output_file_name, "w") as json_file:
    json.dump(output_data, json_file, indent=2)
 
print(f"Output saved to {output_file_name}")
