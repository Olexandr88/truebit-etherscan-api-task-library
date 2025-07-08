import requests
from urllib.parse import urljoin

class TruebitClient:
    """A Python client for interacting with the Task Execution API."""

    def __init__(self, base_url="https://run.truebit.network", api_key=None):
        """
        Initialize the Truebit Dispatcher client.

        Args:
            base_url (str): Base URL of the Truebit Dispatcher API.
            api_key (str, optional): API key for authentication, if required.
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"x-api-key": f"{api_key}"})

    def _request(self, method, endpoint, **kwargs):
        """
        Make an HTTP request to the API.

        Args:
            method (str): HTTP method (e.g., 'GET', 'POST').
            endpoint (str): API endpoint
            **kwargs: Additional arguments for the request (e.g., json, params).

        Returns:
            dict: JSON response from the API.

        Raises:
            TruebitAPIError: If the request fails.
        """
        url = urljoin(self.base_url, endpoint)
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise TruebitAPIError(
                f"{response.status_code} - {response.text}",
                response.status_code
            )
        except requests.exceptions.RequestException as e:
            raise TruebitAPIError(f"Network error: {str(e)}")

    def get_function_task_status_by_execution_id(self, execution_id):
        """
        Retrieve the status of a task.

        Args:
            execution_id (str): ID of the task to check.

        Returns:
            dict: Task status information.

        Raises:
            TaskStatusError: If task status retrieval fails.
        """
        return self._request("GET", f"/task/function/execution-status/{execution_id}")


    def get_api_task_status_by_execution_id(self, execution_id):
        """
        Retrieve the status of an API task.

        Args:
            execution_id (str): ID of the task to check.

        Returns:
            dict: Task status information.

        Raises:
            TaskStatusError: If task status retrieval fails.
        """
        return self._request("GET", f"/task/api/execution-status/{execution_id}")

    def api_task_execute(self, data):
        """
        Execute an API Task by name.

        Args:
          dict: input data

        Returns:
            dict: Response indicating solver stop status.
        """
        return self._request("POST", "/task/api/execute-by-name", json=data)

    def function_task_execute(self, verifier_config):
        """
        Execute a Function Task by name.

        Args:
            dict: input data

        Returns:
            dict: Response indicating verifier start status.
        """
        return self._request("POST", "/task/function/execute-by-name", json=data)

    def close(self):
        """Close the HTTP session."""
        self.session.close()

class TruebitAPIError(Exception):
    """Base exception for Truebit API errors."""
    def __init__(self, message, status_code=None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
