import json

def proof_of_fund(input_string):
    """Look for Uniswap trades """
    if input_string.get('status') != '1' or input_string.get('message') != 'OK' or 'result' not in input_string:
        return False
    
    # Iterate through transactions in the result
    min_amount = 1000
    decimals = 18
    token_balance = int(input_string.get('result')) / (10 ** decimals)
    return token_balance > min_amount

def run_task(input_string):
    """Count Uniswap transactions and return True if there's more than 10 Uniswap tx."""
    return proof_of_fund(input_string)

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
