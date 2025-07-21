const axios = require('axios');
const { URL } = require('url');

class TruebitAPIError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.name = 'TruebitAPIError';
    this.statusCode = statusCode;
  }
}

class TruebitClient {
  constructor({ baseUrl = 'https://run.truebit.network', apiKey = null } = {}) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
    this.apiKey = apiKey;
    this.axiosInstance = axios.create({
      baseURL: this.baseUrl,
      headers: apiKey ? { 'x-api-key': apiKey } : {},
    });
  }

  async _request(method, endpoint, options = {}) {
    const url = new URL(endpoint, this.baseUrl).toString();
    try {
      const response = await this.axiosInstance.request({
        method,
        url,
        ...options,
      });
      return response.data;
    } catch (error) {
      if (error.response) {
        throw new TruebitAPIError(
          `${error.response.status} - ${error.response.data ? JSON.stringify(error.response.data) : error.response.statusText}`,
          error.response.status
        );
      } else {
        throw new TruebitAPIError(`Network error: ${error.message}`);
      }
    }
  }

  getTranscriptHash(data) {
    if (!data.transcript) return null;
    for (const item of data.transcript) {
      if (item.type === 'execution_completed') {
        return item.transcriptHash;
      }
    }
    return null;
  }

  async getFunctionTaskStatusByExecutionId(executionId) {
    return this._request('GET', `/task/function/execution-status/${executionId}`);
  }

  async getApiTaskStatusByExecutionId(executionId) {
    return this._request('GET', `/task/api/execution-status/${executionId}`);
  }

  async apiTaskExecute(data) {
    return this._request('POST', '/task/api/execute-by-name', { data });
  }

  async functionTaskExecute(data) {
    return this._request('POST', '/task/function/execute-by-name', { data });
  }

  async getTranscriptByExecutionId(executionId) {
    return this._request('GET', `/task/${executionId}/transcript`);
  }

  async findTranscriptByHash(transcriptHash) {
    return this._request('GET', `/task/hash/${transcriptHash}/transcript`);
  }

  async findInvoiceByExecutionId(executionId) {
    return this._request('GET', `/task/${executionId}/transcriptInvoice`);
  }
}

module.exports = { TruebitClient, TruebitAPIError }; 