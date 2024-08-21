import json
import glob

def merge_openapi_json(file_list):
    merged_data = {
        "openapi": "3.0.0",  # Assuming all files are using OpenAPI 3.0.0
        "info": {
            "title": "Merged API",
            "version": "1.0.0"
        },
        "paths": {},
        "components": {}
    }

    for file_name in file_list:
        with open(file_name, 'r') as f:
            data = json.load(f)
            
            # Merge paths
            for path, path_item in data.get('paths', {}).items():
                if path in merged_data['paths']:
                    merged_data['paths'][path].update(path_item)
                else:
                    merged_data['paths'][path] = path_item
            
            # Merge components
            components = data.get('components', {})
            for component_type, component in components.items():
                if component_type not in merged_data['components']:
                    merged_data['components'][component_type] = {}
                for name, details in component.items():
                    merged_data['components'][component_type][name] = details

    return merged_data

# List of OpenAPI JSON files to merge
file_list = glob.glob("openapi_files/*.json")  # Adjust the path as needed

merged_json = merge_openapi_json(file_list)

# Write the merged data to a new JSON file
with open("merged_openapi.json", "w") as outfile:
    json.dump(merged_json, outfile, indent=2)

print("OpenAPI files merged successfully into 'merged_openapi.json'")
