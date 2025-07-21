# Truebit Task library

- [Introduction](#Introduction)
- [Truebit Setup](#Truebit-Setup)
- [Truebit-Etherscan API Task](#Truebit-Etherscan-API-Task)
- [Python Setup Instructions](#Python-Setup-Instructions)
- [Python Sample usage](#Python-Sample-usage)
- [Truebit Function Tasks](#Truebit-Function-Tasks)
- [Proof of fund ERC-20](#Proof-of-fund-ERC-20)
- [Count Uniswap Transactions](#Count-Uniswap-Transactions)
- [JavaScript Setup Instructions](#JavaScript-Setup-Instructions)
- [Truebit powered Aidrop](Truebit-powered-Aidrop)

## Introduction

This library makes it possible to utilise some of Etherscan's API v2 functionality:
- Accounts: https://docs.etherscan.io/etherscan-v2/api-endpoints/accounts
- Tokens: https://docs.etherscan.io/etherscan-v2/api-endpoints/tokens

via truebit API Task:
- https://devs.truebit.io/developing-truebit-tasks/writing-api-tasks

## Truebit Setup
Register into Truebit and create an account: https://devs.truebit.io/getting-started/get-started
Create a `TRUEBIT_NAMESPACE`:
```bash
truebit namespace register <your-namespace>
```
Create a `TRUEBIT_API_KEY`:
```bash
truebit auth new-apikey
```
Register your `TRUEBIT_API_KEY`:
```bash
truebit auth register <truebit-api-key>
```
## Truebit-Etherscan API Task
Clone the repository
```bash
git clone git@github.com:DAC-CHAIN/truebit-etherscan-api-task-library.git
```
Create the API task:
```bash
cd truebit-etherscan-api-task-library
truebit create-api etherscan.accounts.manifest.json 
```
Deploy the API task:
```bash
truebit deploy <your-namespace> etherscan-accounts --taskId <your-task-id>
```
### Python Setup Instructions
**Create virtual environment**:
Install dependencies:
 ```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
 ```

**Add to the .env file**:
```bash
TRUEBIT_API_KEY=<your-api-key>
TRUEBIT_NAMESPACE=<your-namespace>
ETHERSCAN_API_KEY=<etherscan-api-key>
```
 
### Python Sample usage
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

**Get Etherscan Response**

```python
etherscan_response = response['clearTextSolution']['output']
```

**Get Transcript**

```python
# Get Execution ID
execution_id = response['executionId']

# Get transcript
transcript = client.get_transcript_by_execution_id(execution_id)
```

**Find Transcript by Hash**

```python
# Get transcript hash
transcript_hash = client.get_transcript_hash(transcript)

# Find transcript by hash
transcript = client.find_transcript_by_hash(transcript_hash)
```

## Truebit Function Tasks
Two examples of truebit tasks making use of the data obtained via the truebit-etherscan api tasks are provided. Two simple examples are provided:

- Proof of fund ERC-20: which verifies that the given address has at least 1000 tokens in its balance

- Count Uniswap transactions: which verifies that the provided address has at least 10 transactions on an Uniswap pool

### Proof of fund ERC-20
Build the task
```bash
truebit build function-tasks/proof_of_funds/py/src/ -l py
```
Deploy the task
```bash
truebit deploy <your-namespace> proof-of-fund-1000 --taskId <your-task-id>
```

### Count Uniswap Transactions
Build the task
```bash
truebit build function-tasks/count_uniswap_tx/py/src/ -l py
```
Deploy the task
```bash
truebit deploy <your-namespace> count-uniswap-tx-10 --taskId <your-task-id>
```

Sample Usage
```python
from dotenv import load_dotenv
from truebit_client import TruebitClient

load_dotenv()

TRUEBIT_API_KEY = os.getenv("TRUEBIT_API_KEY")  # Load API key from
TRUEBIT_NAMESPACE = os.getenv("TRUEBIT_NAMESPACE")  # Load Truebit Namespace

client = TruebitClient(
  base_url="https://run.truebit.network",
  api_key=TRUEBIT_API_KEY
)

data = {
  'namespace': TRUEBIT_NAMESPACE,
  'taskName': 'proof-of-fund-1000',
  # Input from Truebit-Etherscan task API
  'input': '{"status": "1","message": "OK","result": "10500000000000000000000000"}',
  'executionTimeout': 6000,
  'totalSolutions': 1,
  'requiredSolutions': 1,
  'taskRequesterTimestamp': 1752768656,
  'async': False
}
task_data = client.function_task_execute(data)
```

### JavaScript Setup Instructions

Install dependencies
```bash
npm install
```
This will install all required packages, including `dotenv` and `axios`.

Run the sample
```bash
npm run sample
```

Run the asynchronous sample:
```bash
npm run sample-async
```
## Truebit powered Aidrop

Python

```python
python airdrop.py --address-list 0xAddress1 0xAddress2 0xAddress3
```

Javascript
```javascript
node airdrop.js --address-list 0xAddress1 0xAddress2 0xAddress3
```
