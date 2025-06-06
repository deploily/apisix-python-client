# APISIX Python Client

A Python client library for interacting with Apache APISIX Admin and Control APIs.

## Features

- Complete Admin API implementation
- Control API endpoints
- Type-safe HTTP requests
- Error handling and response parsing
- Support for all major APISIX resources:
  - Routes
  - Services
  - Upstreams
  - Consumers
  - Plugins
  - SSL certificates
  - And more...

## Installation

You can install the package using pip:

```bash
pip install apisix-python-client
```

## Usage

### Admin API

```python
from apisix_python_client import Admin

# Initialize the client
admin = Admin(
    base_url="http://localhost:9080/apisix/admin",
    api_key="your_api_key"
)

# Example: Create a route
route_config = {
    "uri": "/test",
    "upstream": {
        "nodes": {
            "127.0.0.1:1980": 1
        },
        "type": "roundrobin"
    }
}
route = admin.create_route(route_config)

# Example: List all routes
routes = admin.list_routes()
```

### Control API

```python
from apisix_python_client import Control

# Initialize the control client
control = Control(
    base_url="http://localhost:9080/apisix/v1",
    api_key="your_api_key"
)

# Example: Get healthcheck
health = control.healthcheck()

# Example: List all services
services = control.list_services()
```

## API Reference

### Admin API

#### Routes
- `list_routes()`
- `get_route(route_id)`
- `create_route(route_config)`
- `update_route(route_id, route_config)`
- `update_route_with_path(route_id, path, config)`
- `delete_route(route_id)`

#### Services
- `list_services()`
- `get_service(service_id)`
- `create_service(service_config)`
- `update_service(service_id, config)`
- `delete_service(service_id)`

#### Consumers
- `list_consumers()`
- `get_consumer(username)`
- `create_consumer(config)`
- `update_consumer(username, config)`
- `delete_consumer(username)`

#### Plugins
- `list_plugins()`
- `get_plugin(plugin_name)`
- `reload_plugins()`

### Control API

#### Healthcheck
- `healthcheck()`

#### Schema
- `get_schema()`

#### Garbage Collection
- `trigger_gc()`

#### Discovery
- `get_discovery_dump(service)`
- `show_discovery_dump_file(service)`

## Error Handling

The client handles HTTP errors and raises appropriate exceptions:

```python
try:
    response = admin.create_route(invalid_config)
except ConnectionError as e:
    print(f"Error: {str(e)}")
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the Apache License - see the LICENSE file for details.