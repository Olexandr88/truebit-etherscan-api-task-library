require('dotenv').config();
const { TruebitClient } = require('./TruebitClient');
const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');

const BASE_URL = 'https://run.truebit.network';
const TRUEBIT_API_KEY = process.env.TRUEBIT_API_KEY;
const TRUEBIT_NAMESPACE = process.env.TRUEBIT_NAMESPACE;
const ETHERSCAN_API_KEY = process.env.ETHERSCAN_API_KEY;
const QDT_ERC20_ADDRESS = '0xf65B5C5104c4faFD4b709d9D60a185eAE063276c';
const DEPLOY_BLOCK = 12218196;
const RATIO = 2;

function nowTimestamp() {
  return Math.floor(Date.now() / 1000);
}

async function runAirdrop(addressList) {
  for (const address of addressList) {
    const client = new TruebitClient({ baseUrl: BASE_URL, apiKey: TRUEBIT_API_KEY });
    let balance, newBalance;
    // Task 1: Get token balance
    const inputDataTask1 = {
      namespace: TRUEBIT_NAMESPACE,
      taskName: 'etherscan-tokens',
      input: {
        path: '/api?chainid={chainid}&module={module}&action={action}&contractaddress={contractaddress}&address={address}&apikey={apiKey}',
        method: 'GET',
        params: {
          chainid: 1,
          module: 'account',
          action: 'tokenbalance',
          address,
          contractaddress: QDT_ERC20_ADDRESS,
          apiKey: ETHERSCAN_API_KEY,
        },
      },
      executionTimeout: 10000,
      async: false,
    };
    const response1 = await client.apiTaskExecute(inputDataTask1);
    balance = response1.clearTextSolution.output.result;
    console.log(`Raw balance for ${address}:`, balance);
    if (!balance || isNaN(balance)) {
      console.error(`Invalid balance for address ${address}:`, balance);
      continue;
    }
    // Task 2: Proof of fund
    const inputDataTask2 = {
      namespace: TRUEBIT_NAMESPACE,
      taskName: 'proof-of-fund-1000',
      input: JSON.stringify(response1.clearTextSolution.output),
      executionTimeout: 6000,
      totalSolutions: 1,
      requiredSolutions: 1,
      taskRequesterTimestamp: nowTimestamp(),
      async: false,
    };
    const response2 = await client.functionTaskExecute(inputDataTask2);
    if (response2.clearTextSolution.output) {
      // Task 3: Get token transactions
      const inputDataTask3 = {
        namespace: TRUEBIT_NAMESPACE,
        taskName: 'etherscan-accounts',
        input: {
          path: '/api?chainid={chainid}&module={module}&action={action}&address={address}&contractaddress={contractAddress}&startblock={startBlock}&endblock={endBlock}&page={page}&offset={offset}&sort={sort}&apikey={apiKey}',
          method: 'GET',
          params: {
            chainid: 1,
            module: 'account',
            action: 'tokentx',
            address,
            contractAddress: QDT_ERC20_ADDRESS,
            startBlock: DEPLOY_BLOCK,
            endBlock: 99999999,
            page: 1,
            offset: 100,
            sort: 'desc',
            apiKey: ETHERSCAN_API_KEY,
          },
        },
        executionTimeout: 10000,
        async: false,
      };
      const response3 = await client.apiTaskExecute(inputDataTask3);
      if (response3.clearTextSolution.output) {
        newBalance = (parseInt(balance) / (10 ** 18)) * RATIO;
      } else {
        newBalance = parseInt(balance);
      }
    } else {
      newBalance = parseInt(balance);
    }
    console.log(`Airdrop Amount NEW TOKEN for ${address}: ${newBalance}`);
  }
}

// Argument parsing
const argv = yargs(hideBin(process.argv))
  .option('address-list', {
    type: 'string',
    array: true,
    description: 'List of addresses (space-separated)',
    demandOption: true,
  })
  .help()
  .argv;

runAirdrop(argv['address-list'].map(String)); 