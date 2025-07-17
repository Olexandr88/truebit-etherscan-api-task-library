from dotenv import load_dotenv
from truebit_client import TruebitClient
from datetime import datetime
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
FUNCTION_TASKS = ['count-uniswap-tx', 'proof-of-fund-1000']

def test_function_tasks():
    # Initialize the client
    client = TruebitClient(base_url=BASE_URL, api_key=TRUEBIT_API_KEY)

    # Test Function tasks trough Truebit API endpoint
    for task_name in FUNCTION_TASKS:
        with open(f"downloads/{task_name}.txt", "r") as file:
            input_string = file.read().strip()

        data = {
          "namespace": TRUEBIT_NAMESPACE,
          "taskName": task_name,
          "input": input_string,
          "executionTimeout": 6000,
          "totalSolutions": 1,
          "requiredSolutions": 1,
          "taskRequesterTimestamp": int(datetime.now().timestamp()),
          "async": False
        }
        task_data = client.function_task_execute(data)
        print(task_data)

def test_api_tasks():
    # Initialize the client
    client = TruebitClient(base_url=BASE_URL, api_key=TRUEBIT_API_KEY)

    # Test API TASKs through Truebit API endpoint
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
def main():
    test_function_tasks()

if __name__ == "__main__":
    main()
