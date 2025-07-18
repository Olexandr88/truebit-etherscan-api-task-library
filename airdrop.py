from dotenv import load_dotenv
from truebit_client import TruebitClient
from datetime import datetime

import os
import json
import argparse

# Load environment variables from .env file
load_dotenv()

BASE_URL = "https://run.truebit.network"
TRUEBIT_API_KEY = os.getenv("TRUEBIT_API_KEY")  # Load API key from
TRUEBIT_NAMESPACE = os.getenv("TRUEBIT_NAMESPACE")  # Load Truebit Namespace
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")  # Load Etherscan API key
#INPUT_FOLDER = os.getenv("INPUT_FOLDER")
QDT_ERC20_ADDRESS = '0xf65B5C5104c4faFD4b709d9D60a185eAE063276c'
TRU_ERC20_ADDRESS = '0x9Adc7710E9d1b29d8a78c04d52D32532297C2Ef3'
DEPLOY_BLOCK = 12218196
RATIO = 2

def main():
    parser = argparse.ArgumentParser(description="Script that takes a list of addresses.")
    parser.add_argument(
        "--address-list",
        nargs="+",
        help="List of addresses (space-separated)",
        required=True
    )
    args = parser.parse_args()
    run_airdrop(args.address_list)

def run_airdrop(address_list):
    for address in address_list:
        # Initialize Truebit client
        client = TruebitClient(base_url=BASE_URL, api_key=TRUEBIT_API_KEY)
        # Set the target address
        input_data_task1 = {
          "namespace": TRUEBIT_NAMESPACE,
          "taskName": "etherscan-tokens",
          "input": {
            "path": "/api?chainid={chainid}&module={module}&action={action}&contractaddress={contractaddress}&address={address}&apikey={apiKey}",
            "method": "GET",
            "params": {
              "chainid": 1,
              "module": "account",
              "action": "tokenbalance",
              "address": address,
              "contractaddress": QDT_ERC20_ADDRESS,
              "apiKey": ETHERSCAN_API_KEY
            }
          },
          "executionTimeout": 10000,
          "async": False
        }
        # call Etherscan Truebit API task
        response1 = client.api_task_execute(input_data_task1)
        intput_data_task2 = {
          "namespace": TRUEBIT_NAMESPACE,
          "taskName": "proof-of-fund-1000",
          "input": json.dumps(response1['clearTextSolution']['output']),
          "executionTimeout": 6000,
          "totalSolutions": 1,
          "requiredSolutions": 1,
          "taskRequesterTimestamp": int(datetime.now().timestamp()),
          "async": False
        }
        response2 = client.function_task_execute(intput_data_task2)
        if response2['clearTextSolution']['output']:
            input_data_task3 = {
                "namespace": TRUEBIT_NAMESPACE,
                "taskName": "etherscan-accounts",
                "input": {
                  "path": "/api?chainid={chainid}&module={module}&action={action}&address={address}&contractaddress={contractAddress}&startblock={startBlock}&endblock={endBlock}&page={page}&offset={offset}&sort={sort}&apikey={apiKey}",
                  "method": "GET",
                  "params": {
                    "chainid": 1,
                    "module": "account",
                    "action": "tokentx",
                    "address": address,
                    "contractAddress": QDT_ERC20_ADDRESS,
                    "startBlock": DEPLOY_BLOCK,
                    "endBlock": 99999999,
                    "page": 1,
                    "offset": 100,
                    "sort": "desc",
                    "apiKey": ETHERSCAN_API_KEY
                  }
                },
                "executionTimeout": 10000,
                "async": False
            }
            response3 = client.api_task_execute(input_data_task3)
            if response3['clearTextSolution']['output']:
                balance = response1['clearTextSolution']['output']['result']
                new_balance = int(balance) / (10 ** 18)*RATIO
            else:
                new_balance = int(balance)
        else:
          new_balance = int(balance)

        print(f"Airdrop Amount NEW TOKEN {new_balance}")

if __name__ == "__main__":
    main()
