import fs from 'fs';

// Function to check for Uniswap trades
function proofOfFund(input) {
    // Validate input object
    if (input.status !== '1' || input.message !== 'OK' || !input.result) {
        return false;
    }

    // Calculate token balance
    const minAmount = 1000;
    const decimals = 18;
    const tokenBalance = parseInt(input.result) / Math.pow(10, decimals);
    return tokenBalance > minAmount;
}

// Function to process input and return result
function runTask(input) {
    return proofOfFund(input);
}

let data = fs.readFileSync('input.txt', 'utf8')
const output = runTask(JSON.parse(data.trim()));
fs.writeFileSync('output.txt', output)
