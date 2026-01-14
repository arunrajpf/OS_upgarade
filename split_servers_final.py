import json
import glob
import re
from datetime import datetime

# Code 1: Extract server-specific error tasks from the latest error file
error_files = glob.glob("error-*.json")
if not error_files:
    print("No error files found.")
    exit()

latest_error_file = max(error_files, key=lambda x: x.split('-')[1])

with open(latest_error_file) as f:
    data = json.load(f)

servers = {}

for task in data['tasks']:
    server_name = task['words_after'].split('.')[0].split(':')[-1]
    if server_name not in servers:
        servers[server_name] = []
    servers[server_name].append(task)

for server_name, tasks in servers.items():
    output_file_name = f'error-{server_name}.sys.comcast.net.json'
    output_file_name = ''.join(char if char.isalnum() or char in {'-', '_', '.'} else '' for char in output_file_name)
    with open(output_file_name, 'w') as output_file:
        json.dump({'tasks': tasks}, output_file, indent=2)

# Code 2: Construct and print the URL based on the current date's error file
current_date = datetime.now().strftime("error-%Y-%m-%d.json")

with open(current_date, "r") as infile:
    json_data = json.load(infile)

server_names = set()
for task in json_data["tasks"]:
    original_context = task["words_after"]
    matches = re.findall(r'\[.*?([a-zA-Z0-9-]+\.sys\.comcast\.net).*?\]', original_context)
    server_names.update(matches)

url_template = "http://rckyels-ho-a1d-519642.sys.comcast.net:9200/rocky-upgrade-errors/_doc/"
constructed_urls = []

for server_name in server_names:
    constructed_url = url_template + f'{server_name}.json'
    constructed_url = ''.join(char if char.isalnum() or char in {'-', '_', '.', ':', '/'} else '' for char in constructed_url)
    constructed_urls.append(constructed_url)

print("Files created successfully.")
print("Constructed URLs:")
for url in constructed_urls:
    print(url)
