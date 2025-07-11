from dotenv import load_dotenv
from truebit_client import TruebitClient
import os
import time

load_dotenv()

TRUEBIT_API_KEY = os.getenv("TRUEBIT_API_KEY")  # Load API key from
TRUEBIT_NAMESPACE = os.getenv("TRUEBIT_NAMESPACE")  # Load Truebit Namespace
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")  # Load Etherscan API key

client = TruebitClient(
  base_url="https://run.truebit.network",
  api_key=TRUEBIT_API_KEY
)

data = {
  'namespace': TRUEBIT_NAMESPACE,
  'taskName': 'etherscan-accounts',
  'input': {
      'path': '/api?chainid={chainid}&module={module}&action={action}&address={address}&tag={tag}&apikey={apiKey}',
      'method': 'GET', 'params': {
        'chainid': 1,
        'module': 'account',
        'action': 'balance',
        'address': '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045',
        'tag': 'latest',
        'apiKey': ETHERSCAN_API_KEY
      }
  },
  'executionTimeout': 10000,
  'async': True
}

response = client.api_task_execute(data)
# Get Execution ID
execution_id = response['executionId']
# Wait the Task being Executed
time.sleep(2)
# Get API Task Status by execution
task_status = client.get_api_task_status_by_execution_id(execution_id)
