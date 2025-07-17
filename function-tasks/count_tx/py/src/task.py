import json

def count_uniswap_transaction(input_string):
    """Look for Uniswap trades """
    if input_string.get('status') != '1' or input_string.get('message') != 'OK' or 'result' not in input_string:
        return False
    
    # Iterate through transactions in the result
    UNISWAP_TRANSACTION = 'ethUnoswap'
    count = 0
    for tx in input_string['result']:
        if UNISWAP_TRANSACTION in tx['functionName']:
            count+=1
    return count > 10

def run_task(transactions):
    """Count Uniswap transactions and return True if there's more than 10 Uniswap tx."""
    return count_uniswap_transaction(transactions)

def main():
    """ Main function to read, process, and count Uniswap transactions """
    try:
        with open("input.txt", "r") as file:
            input_string = file.read().strip()
    except FileNotFoundError:
        print("Error: The file 'input.txt' does not exist.")
        return
    except Exception as e:
        print(f"An error occurred while reading 'input.txt': {e}")
        return

    try:
        output_string = str(run_task(json.loads(input_string)))
    except Exception as e:
        print(f"An error occurred while processing the input: {e}")
        return

    try:
        with open("output.txt", "w") as file:
            file.write(output_string)
    except Exception as e:
        print(f"An error occurred while writing to 'output.txt': {e}")

if __name__ == "__main__":
    main()
