from dotenv import load_dotenv
from truebit_client import TruebitClient
import os
import json

# Load environment variables from .env file
load_dotenv()

# Configuration
BASE_URL = "https://run.truebit.network"
TRUEBIT_API_KEY = os.getenv("TRUEBIT_API_KEY")      # Load API key from
TRUEBIT_NAMESPACE = os.getenv("TRUEBIT_NAMESPACE")  # Load Truebit Namespace
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")  # Load Etherscan API key
INPUT_FOLDER = os.getenv("INPUT_FOLDER")
MODULE_LIST = ['accounts', 'tokens']

def main():
    # Initialize the client
    client = TruebitClient(base_url=BASE_URL, api_key=TRUEBIT_API_KEY)

    for module in MODULE_LIST:
        input_folder = os.path.join(INPUT_FOLDER, module)
        # Iterate through all files in the folder
        for filename in os.listdir(input_folder):
            # Check if file has .json extension
            if filename.lower().endswith('.json'):
                file_path = os.path.join(input_folder, filename)
                # Open JSON file
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                    data['input']['params']['apiKey'] = ETHERSCAN_API_KEY
                    data['namespace'] = TRUEBIT_NAMESPACE
                    data['taskName'] = f"etherscan-{module}"
                    task_data = client.api_task_execute(data)

if __name__ == "__main__":
    main()
