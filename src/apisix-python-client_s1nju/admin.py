from typing import Dict, List, Optional
import requests

class Admin :
    def __init__(self, base_url: str, api_key: str):
        """
        Initialize the APISIX client.

        Args:
            base_url: The base URL of the APISIX Admin API (e.g., 'http://localhost:9080/apisix/admin')
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
        Make an HTTP request to the APISIX Admin API.
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Request data (for POST/PUT)

        Returns:
            API response as a dictionary
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=self.headers, json=data)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=self.headers)
            elif method.upper() == 'PATCH':
                response = requests.patch(url, headers=self.headers,json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Error connecting to APISIX: {str(e)}")
    #
    # Routes API
    #
    def list_routes(self) -> List[Dict]:
        """List all routes."""
        response = self._make_request('GET', '/routes')
        return response.get('node', {}).get('nodes', [])

    def get_route(self, route_id: str) -> Dict:
        """Get a route by ID"""
        return self._make_request('GET', f'/routes/{route_id}')

    def create_route(self, route_config: Dict, ttl: Optional[int] = None) -> Dict:
        """Create a new route with random id"""
        if ttl != None:
            return self._make_request('POST', f'/routes?ttl={ttl}', data=route_config)
        return self._make_request('POST', '/routes', data=route_config)

    def update_route(self, route_id: str, route_config: Dict, ttl: Optional[int] = None) -> Dict:
        """Updates an existing route."""
        if ttl is not None:
            return self._make_request('PATCH', f'/routes/{route_id}?ttl={ttl}', data=route_config)
        return self._make_request('PATCH', f'/routes/{route_id}', data=route_config)

    def update_route_with_path(self,route_id: str,route_path: str, route_config: Dict, ttl: Optional[int] = None) -> Dict:
        """	Updates the attribute specified in the path. The values of other attributes remain unchanged."""
        if ttl != None:
            return self._make_request('PATCH', f'/routes/{route_id}/{route_path}?ttl={ttl}', data=route_config)
        return self._make_request('PATCH', f'/routes/{route_id}/{route_path}', data=route_config)

    def create_route_with_id(self, route_id: str, route_config: Dict, ttl: Optional[int] = None) -> Dict:
        """Creates a new route with the specified id."""
        if ttl is not None:
            return self._make_request('PUT', f'/routes/{route_id}?ttl={ttl}', data=route_config)
        return self._make_request('PUT', f'/routes/{route_id}', data=route_config)

    def delete_route(self, route_id: str) -> Dict:
        """Delete a route"""
        return self._make_request('DELETE', f'/routes/{route_id}')




    #
    # service API
    #
    def list_services(self) -> List[Dict]:
        """Fetches a list of available Services."""
        response = self._make_request('GET', '/services')
        return response.get('node', {}).get('nodes', [])

    def get_service(self, service_id: str) -> Dict:
        """Fetches specified Service by id."""
        return self._make_request('GET', f'/services/{service_id}')

    def create_service(self, service_config: Dict) -> Dict:
        """Creates a Service and assigns a random id."""
        return self._make_request('POST', '/services', data=service_config)

    def update_service(self,service_id: str, service_config: Dict) -> Dict:
        """Updates the selected attributes of the specified, existing Service. To delete an attribute, set value of attribute set to null."""
        return self._make_request('PATCH', f'/services/{service_id}', data=service_config)

    def update_service_with_path(self,service_id: str,service_path: str, service_config: Dict) -> Dict:
        """	Updates the attribute specified in the path. The values of other attributes remain unchanged."""
        return self._make_request('PATCH', f'/services/{service_id}/{service_path}', data=service_config)

    def create_service_with_id(self, service_id: str, service_config: Dict ) -> Dict:
        """	Creates a Service with the specified id."""
        return self._make_request('PUT', f'/services/{service_id}', data=service_config)

    def delete_service(self, service_id: str) -> Dict:
        """Delete a service"""
        return self._make_request('DELETE', f'/services/{service_id}')


    #
    # Consumer API
    #

    def list_consumers(self) -> List[Dict]:
        """List all consumers"""
        response = self._make_request('GET', '/consumers')
        return response.get('node', {}).get('nodes', [])

    def get_consumer(self, username: str) -> Dict:
        """Get a consumer by username"""
        return self._make_request('GET', f'/consumers/{username}')

    def create_consumer(self, consumer_config: Dict) -> Dict:
        """Create a new consumer"""
        return self._make_request('POST', '/consumers', data=consumer_config)

    def update_consumer(self, username: str, consumer_config: Dict) -> Dict:
        """Update an existing consumer"""
        return self._make_request('PUT', f'/consumers/{username}', data=consumer_config)

    def delete_consumer(self, username: str) -> Dict:
        """Delete a consumer"""
        return self._make_request('DELETE', f'/consumers/{username}')
    #
    # Credential API
    #

    def list_consumer_credentials(self, username: str) -> List[Dict]:
        """Fetches list of all credentials of the Consumer"""
        return self._make_request('GET', f'/consumers/{username}/credentials')

    def get_consumer_credential(self, username: str, credential_id: str) -> Dict:
        """Fetches the Credential by credential_id"""
        return self._make_request('GET', f'/consumers/{username}/credentials/{credential_id}')

    def create_or_update_consumer_credential(self, username: str, credential_id: str, credential_config: Dict) -> Dict:
        """Create or update a Credential"""
        return self._make_request('PUT', f'/consumers/{username}/credentials/{credential_id}', data=credential_config)

    def delete_consumer_credential(self, username: str, credential_id: str) -> Dict:
        """Delete the Credential"""
        return self._make_request('DELETE', f'/consumers/{username}/credentials/{credential_id}')


    #
    # Upstream API
    #

    def list_upstreams(self) -> List[Dict]:
        """Fetch a list of all configured Upstreams."""
        response = self._make_request('GET', '/upstreams')
        return response.get('node', {}).get('nodes', [])

    def get_upstream(self, upstream_id: str) -> Dict:
        """Fetches specified Upstream by id."""
        return self._make_request('GET', f'/upstreams/{upstream_id}')

    def create_upstream_with_id(self, upstream_id: str, upstream_config: Dict) -> Dict:
        """Creates an Upstream with the specified id."""
        return self._make_request('PUT', f'/upstreams/{upstream_id}', data=upstream_config)

    def create_upstream(self, upstream_config: Dict) -> Dict:
        """Creates an Upstream and assigns a random id."""
        return self._make_request('POST', '/upstreams', data=upstream_config)

    def update_upstream(self, upstream_id: str, upstream_config: Dict) -> Dict:
        """Updates the selected attributes of the specified, existing Upstream. To delete an attribute, set value of attribute set to null."""
        return self._make_request('PATCH', f'/upstreams/{upstream_id}', data=upstream_config)

    def update_upstream_with_path(self, upstream_id: str, path: str, upstream_config: Dict) -> Dict:
        """Updates the attribute specified in the path. The values of other attributes remain unchanged."""
        return self._make_request('PATCH', f'/upstreams/{upstream_id}/{path}', data=upstream_config)

    def delete_upstream(self, upstream_id: str) -> Dict:
        """Removes the Upstream with the specified id."""
        return self._make_request('DELETE', f'/upstreams/{upstream_id}')

    #
    # SSL API
    #

    def list_ssl(self) -> List[Dict]:
        """List all SSL certificates"""
        response = self._make_request('GET', '/ssl')
        return response.get('node', {}).get('nodes', [])

    def get_ssl(self, ssl_id: str) -> Dict:
        """Get an SSL certificate by ID"""
        return self._make_request('GET', f'/ssl/{ssl_id}')

    def create_ssl(self, ssl_config: Dict) -> Dict:
        """Create a new SSL certificate"""
        return self._make_request('POST', '/ssl', data=ssl_config)

    def update_ssl(self, ssl_id: str, ssl_config: Dict) -> Dict:
        """Update an existing SSL certificate"""
        return self._make_request('PUT', f'/ssl/{ssl_id}', data=ssl_config)

    def delete_ssl(self, ssl_id: str) -> Dict:
        """Delete an SSL certificate"""
        return self._make_request('DELETE', f'/ssl/{ssl_id}')

    #
    # Global Rules API
    #

    def list_global_rules(self) -> List[Dict]:
        """Fetches a list of all Global Rules."""
        response = self._make_request('GET', '/global_rules')
        return response.get('node', {}).get('nodes', [])

    def get_global_rule(self, rule_id: str) -> Dict:
        """Fetches specified Global Rule by id."""
        return self._make_request('GET', f'/global_rules/{rule_id}')

    def create_global_rule_with_id(self, rule_id: str, rule_config: Dict) -> Dict:
        """Creates a Global Rule with the specified id."""
        return self._make_request('PUT', f'/global_rules/{rule_id}', data=rule_config)

    def delete_global_rule(self, rule_id: str) -> Dict:
        """Removes the Global Rule with the specified id."""
        return self._make_request('DELETE', f'/global_rules/{rule_id}')

    def update_global_rule(self, rule_id: str, rule_config: Dict) -> Dict:
        """Updates the selected attributes of the specified, existing Global Rule. To delete an attribute, set value of attribute set to null."""
        return self._make_request('PATCH', f'/global_rules/{rule_id}', data=rule_config)

    def update_global_rule_with_path(self, rule_id: str, path: str, rule_config: Dict) -> Dict:
        """Updates the attribute specified in the path. The values of other attributes remain unchanged."""
        return self._make_request('PATCH', f'/global_rules/{rule_id}/{path}', data=rule_config)

    #
    # Consumer Groups API
    #

    def list_consumer_groups(self) -> List[Dict]:
        """Fetches a list of all Consumer groups."""
        response = self._make_request('GET', '/consumer_groups')
        return response.get('node', {}).get('nodes', [])

    def get_consumer_group(self, group_id: str) -> Dict:
        """Fetches specified Consumer group by id."""
        return self._make_request('GET', f'/consumer_groups/{group_id}')

    def create_consumer_group_with_id(self, group_id: str, group_config: Dict) -> Dict:
        """Creates a new Consumer group with the specified id."""
        return self._make_request('PUT', f'/consumer_groups/{group_id}', data=group_config)

    def delete_consumer_group(self, group_id: str) -> Dict:
        """Removes the Consumer group with the specified id."""
        return self._make_request('DELETE', f'/consumer_groups/{group_id}')

    def update_consumer_group(self, group_id: str, group_config: Dict) -> Dict:
        """Updates the selected attributes of the specified, existing Consumer group. To delete an attribute, set value of attribute set to null."""
        return self._make_request('PATCH', f'/consumer_groups/{group_id}', data=group_config)

    def update_consumer_group_with_path(self, group_id: str, path: str, group_config: Dict) -> Dict:
        """Updates the attribute specified in the path. The values of other attributes remain unchanged."""
        return self._make_request('PATCH', f'/consumer_groups/{group_id}/{path}', data=group_config)

    #
    # Plugin Configs API
    #

    def list_plugin_configs(self) -> List[Dict]:
        """Fetches a list of all Plugin configs."""
        response = self._make_request('GET', '/plugin_configs')
        return response.get('node', {}).get('nodes', [])

    def get_plugin_config(self, config_id: str) -> Dict:
        """Fetches specified Plugin config by id."""
        return self._make_request('GET', f'/plugin_configs/{config_id}')

    def create_plugin_config_with_id(self, config_id: str, config: Dict) -> Dict:
        """Creates a new Plugin config with the specified id."""
        return self._make_request('PUT', f'/plugin_configs/{config_id}', data=config)

    def delete_plugin_config(self, config_id: str) -> Dict:
        """Removes the Plugin config with the specified id."""
        return self._make_request('DELETE', f'/plugin_configs/{config_id}')

    def update_plugin_config(self, config_id: str, config: Dict) -> Dict:
        """Updates the selected attributes of the specified, existing Plugin config. To delete an attribute, set value of attribute set to null."""
        return self._make_request('PATCH', f'/plugin_configs/{config_id}', data=config)

    def update_plugin_config_with_path(self, config_id: str, path: str, config: Dict) -> Dict:
        """Updates the attribute specified in the path. The values of other attributes remain unchanged."""
        return self._make_request('PATCH', f'/plugin_configs/{config_id}/{path}', data=config)

    #
    # Plugin Metadata API
    #

    def get_plugin_metadata(self, plugin_name: str) -> Dict:
        """Fetches the metadata of the specified Plugin by plugin_name."""
        return self._make_request('GET', f'/plugin_metadata/{plugin_name}')

    def create_plugin_metadata(self, plugin_name: str, metadata: Dict) -> Dict:
        """Creates metadata for the Plugin specified by the plugin_name."""
        return self._make_request('PUT', f'/plugin_metadata/{plugin_name}', data=metadata)

    def delete_plugin_metadata(self, plugin_name: str) -> Dict:
        """Removes metadata for the Plugin specified by the plugin_name."""
        return self._make_request('DELETE', f'/plugin_metadata/{plugin_name}')

    #
    # Plugins API
    #

    def list_plugins(self) -> List[Dict]:
        """Fetches a list of all Plugins."""
        response = self._make_request('GET', '/plugins/list')
        return response.get('node', {}).get('nodes', [])

    def get_plugin(self, plugin_name: str) -> Dict:
        """Fetches the specified Plugin by plugin_name."""
        return self._make_request('GET', f'/plugins/{plugin_name}')

    def get_all_plugins_properties(self) -> Dict:
        """Get all properties of all plugins."""
        return self._make_request('GET', '/plugins?all=true')

    def get_all_stream_plugins_properties(self) -> Dict:
        """Gets properties of all Stream plugins."""
        return self._make_request('GET', '/plugins?all=true&subsystem=stream')

    def get_all_http_plugins_properties(self) -> Dict:
        """Gets properties of all HTTP plugins."""
        return self._make_request('GET', '/plugins?all=true&subsystem=http')

    def reload_plugins(self) -> Dict:
        """Reloads the plugin according to the changes made in code."""
        return self._make_request('PUT', '/plugins/reload')

    def get_plugin_properties(self, plugin_name: str, subsystem: str = None) -> Dict:
        """Gets properties of a specified plugin if it is supported in the specified subsystem."""
        if subsystem:
            return self._make_request('GET', f'/plugins/{plugin_name}?subsystem={subsystem}')
        return self._make_request('GET', f'/plugins/{plugin_name}')

    #
    # Stream Routes API
    #

    def list_stream_routes(self) -> List[Dict]:
        """Fetches a list of all configured Stream Routes."""
        response = self._make_request('GET', '/stream_routes')
        return response.get('node', {}).get('nodes', [])

    def get_stream_route(self, route_id: str) -> Dict:
        """Fetches specified Stream Route by id."""
        return self._make_request('GET', f'/stream_routes/{route_id}')

    def create_stream_route_with_id(self, route_id: str, route_config: Dict) -> Dict:
        """Creates a Stream Route with the specified id."""
        return self._make_request('PUT', f'/stream_routes/{route_id}', data=route_config)

    def create_stream_route(self, route_config: Dict) -> Dict:
        """Creates a Stream Route and assigns a random id."""
        return self._make_request('POST', '/stream_routes', data=route_config)

    def delete_stream_route(self, route_id: str) -> Dict:
        """Removes the Stream Route with the specified id."""
        return self._make_request('DELETE', f'/stream_routes/{route_id}')

    #
    # Secrets API
    #

    def list_secrets(self) -> List[Dict]:
        """Fetches a list of all secrets."""
        response = self._make_request('GET', '/secrets')
        return response.get('node', {}).get('nodes', [])

    def get_secret(self, manager: str, secret_id: str) -> Dict:
        """Fetches specified secrets by id."""
        return self._make_request('GET', f'/secrets/{manager}/{secret_id}')

    def create_secret(self, manager: str, secret_config: Dict) -> Dict:
        """Create new secrets configuration."""
        return self._make_request('PUT', f'/secrets/{manager}', data=secret_config)

    def delete_secret(self, manager: str, secret_id: str) -> Dict:
        """Removes the secrets with the specified id."""
        return self._make_request('DELETE', f'/secrets/{manager}/{secret_id}')

    def update_secret(self, manager: str, secret_id: str, secret_config: Dict) -> Dict:
        """Updates the selected attributes of the specified, existing secrets. To delete an attribute, set value of attribute set to null."""
        return self._make_request('PATCH', f'/secrets/{manager}/{secret_id}', data=secret_config)

    def update_secret_with_path(self, manager: str, secret_id: str, path: str, secret_config: Dict) -> Dict:
        """Updates the attribute specified in the path. The values of other attributes remain unchanged."""
        return self._make_request('PATCH', f'/secrets/{manager}/{secret_id}/{path}', data=secret_config)

    #
    # Protos API
    #

    def list_protos(self) -> List[Dict]:
        """List all Protos."""
        response = self._make_request('GET', '/protos')
        return response.get('node', {}).get('nodes', [])

    def get_proto(self, proto_id: str) -> Dict:
        """Get a Proto by id."""
        return self._make_request('GET', f'/protos/{proto_id}')

    def create_proto_with_id(self, proto_id: str, proto_config: Dict) -> Dict:
        """Create or update a Proto with the given id."""
        return self._make_request('PUT', f'/protos/{proto_id}', data=proto_config)

    def create_proto(self, proto_config: Dict) -> Dict:
        """Create a Proto with a random id."""
        return self._make_request('POST', '/protos', data=proto_config)

    def delete_proto(self, proto_id: str) -> Dict:
        """Delete Proto by id."""
        return self._make_request('DELETE', f'/protos/{proto_id}')

    #
    # Schema Validation API
    #

    def validate_resource_schema(self, resource: str, config: Dict) -> Dict:
        """Validate the resource configuration against corresponding schema."""
        return self._make_request('POST', f'/schema/validate/{resource}', data=config)
