require('dotenv').config();
const { TruebitClient } = require('./TruebitClient');

const TRUEBIT_API_KEY = process.env.TRUEBIT_API_KEY;
const TRUEBIT_NAMESPACE = process.env.TRUEBIT_NAMESPACE;
const ETHERSCAN_API_KEY = process.env.ETHERSCAN_API_KEY;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

(async () => {
  const client = new TruebitClient({
    baseUrl: 'https://run.truebit.network',
    apiKey: TRUEBIT_API_KEY,
  });

  const data = {
    namespace: TRUEBIT_NAMESPACE,
    taskName: 'etherscan-accounts',
    input: {
      path: '/api?chainid={chainid}&module={module}&action={action}&address={address}&tag={tag}&apikey={apiKey}',
      method: 'GET',
      params: {
        chainid: 1,
        module: 'account',
        action: 'balance',
        address: '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045',
        tag: 'latest',
        apiKey: ETHERSCAN_API_KEY,
      },
    },
    executionTimeout: 10000,
    async: true,
  };

  try {
    // Execute task
    const response = await client.apiTaskExecute(data);
    // Get Execution ID
    const executionId = response.executionId;
    // Wait for the task to be executed
    await sleep(2000);
    // Get API Task Status by execution
    const taskStatus = await client.getApiTaskStatusByExecutionId(executionId);
    console.log('Task Status:', taskStatus);
  } catch (err) {
    console.error('Error:', err);
  }
})(); 