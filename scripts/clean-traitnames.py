import json
import sys
import os

def clean_name(name):
    name = name.replace("'", "")
    name = name.replace("&", "And")
    name = name.replace(" ", "_")
    return name

def main():
    if len(sys.argv) < 2:
        print("Usage: python clean_traits.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]

    if not os.path.isfile(json_path):
        print(f"File not found: {json_path}")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cleaned_dict = {}
    for category, obj in data.items():
        cleaned_dict[category] = {}
        for val in obj['values']:
            cleaned = clean_name(val)
            cleaned_dict[category][val] = cleaned

    print(json.dumps(cleaned_dict, indent=2))

if __name__ == "__main__":
    main()
