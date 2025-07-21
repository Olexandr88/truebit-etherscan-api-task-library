import fs from 'fs';

// Function to count Uniswap transactions
function countUniswapTransaction(input) {
    // Validate input object
    if (input.status !== '1' || input.message !== 'OK' || !input.result) {
        return false;
    }

    // Iterate through transactions in the result
    const UNISWAP_TRANSACTION = 'ethUnoswap';
    let count = 0;
    for (const tx of input.result) {
        if (tx.functionName.includes(UNISWAP_TRANSACTION)) {
            count += 1;
        }
    }
    return count > 10;
}

// Function to process input and return result
function runTask(input) {
    return countUniswapTransaction(input);
}

let data = fs.readFileSync('input.txt', 'utf8')
const output = runTask(JSON.parse(data.trim()));
fs.writeFileSync('output.txt', output)
