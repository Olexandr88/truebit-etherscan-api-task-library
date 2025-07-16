from dotenv import load_dotenv
from truebit_client import TruebitClient
import os
import json

# Load environment variables from .env file
load_dotenv()

# Configuration
BASE_URL = "https://run.truebit.network"
TRUEBIT_API_KEY = os.getenv("TRUEBIT_API_KEY")  # Load API key from
TRUEBIT_NAMESPACE = os.getenv("TRUEBIT_NAMESPACE")  # Load Truebit Namespace
TASK_NAME = os.getenv("TASK_NAME")  # Load API Task name
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")  # Load Etherscan API key
INPUT_FOLDER = os.getenv("INPUT_FOLDER")

def main():
    # Initialize the client
    client = TruebitClient(base_url=BASE_URL, api_key=TRUEBIT_API_KEY)

    # Iterate through all files in the folder
    for filename in os.listdir(INPUT_FOLDER):
        # Check if file has .json extension
        if filename.lower().endswith('.json'):
            file_path = os.path.join(INPUT_FOLDER, filename)
            # Open JSON file
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                data['input']['params']['apiKey'] = ETHERSCAN_API_KEY
                data['namespace'] = TRUEBIT_NAMESPACE
                data['taskName'] = TASK_NAME
                task_data = client.api_task_execute(data)

if __name__ == "__main__":
    main()
