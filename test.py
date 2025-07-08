from pathlib import Path
from dotenv import load_dotenv

import subprocess
import json
import os

# Load .env file
env_loaded = load_dotenv()

def main():
    ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
    API_MANIFEST = os.getenv("API_MANIFEST")
    INPUT_FOLDER = os.getenv("INPUT_FOLDER")

    if not env_loaded:
        print("Error: .env file not found")
        exit(1)

    if not ETHERSCAN_API_KEY:
        print("Error: ETHERSCAN_API_KEY not set")
        exit(1)

    if not INPUT_FOLDER:
        print("Error: INPUT_FOLDER not set")
        exit(1)

    if not API_MANIFEST:
        print("Error: API_MANIFEST not set")
        exit(1)

    # Input folder
    input_dir = Path(INPUT_FOLDER)

    # Process each JSON file
    for json_file in input_dir.glob("*.json"):
        with open(json_file, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON: {json_file.name}")
                continue

        # Inject API key if possible
        try:
            data["input"]["params"]["apiKey"] = ETHERSCAN_API_KEY
        except KeyError:
            print(f"Skipping file (missing .input.params): {json_file.name}")
            continue

        # Write to temp file
        temp_file = json_file.with_suffix(".temp.json")
        with open(temp_file, "w") as f:
            json.dump(data, f, indent=2)

        try:
            result = subprocess.run(
                ["truebit",  "start-api", f"{API_MANIFEST}", f"{temp_file}"],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"Output: {result.stdout.strip()}")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

        # Delete temp file
        temp_file.unlink()
        print(f"Deleted temp file: {temp_file.name}")

if __name__ == "__main__":
    main()
