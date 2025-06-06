from typing import Dict, List, Optional
import requests


class Control:
    def __init__(self, base_url: str, api_key: str):
        """
        Initialize the APISIX control client.

        Args:
            base_url: The base URL of the APISIX Control API (e.g., 'http://localhost:9080/apisix/v1')
            api_key: The API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': api_key
        }

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """
        Make an HTTP request to the APISIX Control API.
        Args:
            method: HTTP method (GET, POST, PUT)
            endpoint: API endpoint
            data: Request data (for POST/PUT)

        Returns:
            API response as a dictionary
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"  # Using v1 prefix

        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=self.headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Error connecting to APISIX: {str(e)}")

    #
    # Schema API
    #

    def get_schema(self) -> Dict:
        """Get the APISIX schema."""
        return self._make_request('GET', '/schema')

    #
    # Healthcheck API
    #

    def healthcheck(self) -> Dict:
        """Get healthcheck information."""
        return self._make_request('GET', '/healthcheck')

    #
    # Garbage Collection API
    #

    def trigger_gc(self) -> Dict:
        """Trigger garbage collection."""
        return self._make_request('POST', '/gc')

    #
    # Routes API
    #

    def list_routes(self) -> List[Dict]:
        """List all routes."""
        response = self._make_request('GET', '/routes')
        return response.get('node', {}).get('nodes', [])

    def get_route(self, route_id: str) -> Dict:
        """Get a route by ID."""
        return self._make_request('GET', f'/route/{route_id}')

    #
    # Services API
    #

    def list_services(self) -> List[Dict]:
        """List all services."""
        response = self._make_request('GET', '/services')
        return response.get('node', {}).get('nodes', [])

    def get_service(self, service_id: str) -> Dict:
        """Get a service by ID."""
        return self._make_request('GET', f'/service/{service_id}')

    #
    # Upstreams API
    #

    def list_upstreams(self) -> List[Dict]:
        """List all upstreams."""
        response = self._make_request('GET', '/upstreams')
        return response.get('node', {}).get('nodes', [])

    def get_upstream(self, upstream_id: str) -> Dict:
        """Get an upstream by ID."""
        return self._make_request('GET', f'/upstream/{upstream_id}')

    #
    # Plugin Metadata API
    #

    def list_plugin_metadatas(self) -> List[Dict]:
        """List all plugin metadatas."""
        response = self._make_request('GET', '/plugin_metadatas')
        return response.get('node', {}).get('nodes', [])

    def get_plugin_metadata(self, plugin_name: str) -> Dict:
        """Get plugin metadata by name."""
        return self._make_request('GET', f'/plugin_metadata/{plugin_name}')

    #
    # Plugins API
    #

    def reload_plugins(self) -> Dict:
        """Reload plugins."""
        return self._make_request('PUT', '/plugins/reload')

    #
    # Discovery API
    #

    def get_discovery_dump(self, service: str) -> Dict:
        """Get discovery dump for a service."""
        return self._make_request('GET', f'/discovery/{service}/dump')

    def show_discovery_dump_file(self, service: str) -> Dict:
        """Show discovery dump file for a service."""
        return self._make_request('GET', f'/discovery/{service}/show_dump_file')