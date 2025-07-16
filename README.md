
# Etherscan Truebit API task
This library makes it possible to utilise some of Etherscan's API v2 functionality:
- Accounts: https://docs.etherscan.io/etherscan-v2/api-endpoints/accounts
- Tokens: https://docs.etherscan.io/etherscan-v2/api-endpoints/tokens

via truebit API Task:
https://devs.truebit.io/developing-truebit-tasks/writing-api-tasks

## Setup
- Register into Truebit and create an account: https://devs.truebit.io/getting-started/get-started
- Create a `TRUEBIT_NAMESPACE`:
	```bash
	truebit namespace register <your-namespace>
	```
- Create a `TRUEBIT_API_KEY`:
	```bash
	truebit auth new-apikey
	```
- Register your `TRUEBIT_API_KEY`:
	```bash
	truebit auth register <truebit-api-key>
	```
## Truebit-Etherscan API Tasks
- Clone the repository
	```bash
	git clone git@github.com:DAC-CHAIN/truebit-etherscan-api-task-library.git
	```
- Create "accounts" the API task:
	```bash
	cd truebit-etherscan-api-task-library
	truebit create-api api-tasks/etherscan.accounts.manifest.json
	```
- Deploy "accounts" the API task:
	```bash
	truebit deploy <your-namespace> etherscan-accounts --taskId <your-task-id>
	```
- Create "tokens" the API task:
	```bash
	cd truebit-etherscan-api-task-library
	truebit create-api api-tasks/etherscan.tokens.manifest.json
	```
- Deploy "tokens" the API task:
	```bash
	truebit deploy <your-namespace> etherscan-tokens --taskId <your-task-id>
	```

### Python Setup Instructions
1. **Create virtual environment**:
	Install dependencies:
     ```bash
     python -m venv venv
     source venv/bin/activate  # or venv\Scripts\activate on Windows
     pip install -r requirements.txt
     ```
2. **Add to the .env file**:
	`TRUEBIT_API_KEY=<your-api-key>`
	`TRUEBIT_NAMESPACE=<your-namespace>`
	`ETHERSCAN_API_KEY=<etherscan-api-key>`
 
### Sample usage:
```python
from dotenv import load_dotenv
from truebit_client import TruebitClient
import os

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
  'async': False
}
response = client.api_task_execute(data)
 ```

### Get Etherscan Response
```python
etherscan_response = response['clearTextSolution']['output']
```
### Get Transcript
```python
# Get Execution ID
execution_id = response['executionId']
# Get transcript
transcript = client.get_transcript_by_execution_id(execution_id)
```
### Find Transcript by Hash
```python
# Get transcript hash
transcript_hash = client.get_transcript_hash(transcript)
# Find transcript by hash
transcript = client.find_transcript_by_hash(transcript_hash)
```
