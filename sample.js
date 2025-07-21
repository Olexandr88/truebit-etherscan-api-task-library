require('dotenv').config();
const { TruebitClient } = require('./TruebitClient');

const TRUEBIT_API_KEY = process.env.TRUEBIT_API_KEY;
const TRUEBIT_NAMESPACE = process.env.TRUEBIT_NAMESPACE;
const ETHERSCAN_API_KEY = process.env.ETHERSCAN_API_KEY;

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
    async: false,
  };

  try {
    // Execute task
    const response = await client.apiTaskExecute(data);

    // Get etherscan response
    const etherscanResponse = response.clearTextSolution.output;
    console.log('Etherscan response:', etherscanResponse);

    // Get Execution ID
    const executionId = response.executionId;
    // Get transcript
    const transcript = await client.getTranscriptByExecutionId(executionId);

    // Get transcript hash
    const transcriptHash = client.getTranscriptHash(transcript);

    // Find transcript by hash
    const transcriptVerified = await client.findTranscriptByHash(transcriptHash);

    // Get again transcript hash
    const transcriptHashVerified = client.getTranscriptHash(transcriptVerified);

    // Verify hashes
    if (transcriptHash !== transcriptHashVerified) {
      console.error('Transcript hash:', transcriptHash);
      console.error('Transcript hash (verified):', transcriptHashVerified);
      throw new Error('Transcript hash verification failed: hashes do not match');
    }

    // Get invoice
    const invoice = await client.findInvoiceByExecutionId(executionId);
    console.log('Invoice:', invoice);
  } catch (err) {
    console.error('Error:', err);
  }
})(); 