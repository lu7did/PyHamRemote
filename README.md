# PyMeter

Python based experimental remote meter for ham radio stations

## Overview

PyMeter is a lightweight, Python-based remote metering system designed for ham radio stations. It provides real-time monitoring of various station parameters through a simple TCP client-server architecture.

## Features

- **Multiple Meter Types**:
  - Power Meter (RF output power in watts)
  - SWR Meter (Standing Wave Ratio for antenna efficiency)
  - Signal Strength Meter (S-meter readings in dB)
  - Voltage Meter (Power supply monitoring)

- **Remote Access**: TCP-based client-server architecture for monitoring from anywhere on the network
- **Simulated Data**: Built-in data simulation for testing and development
- **Hardware Integration Ready**: Easy-to-extend classes for connecting real hardware sensors
- **No External Dependencies**: Uses only Python standard library

## Installation

### From Source

```bash
git clone https://github.com/lu7did/PyMeter.git
cd PyMeter
pip install -e .
```

## Quick Start

### Running the Server

Start a meter server with default meters:

```bash
pymeter server
```

Or specify custom host and port:

```bash
pymeter server --host 0.0.0.0 --port 5555
```

### Using the Client

List available meters:

```bash
pymeter client --list
```

Get all meter readings:

```bash
pymeter client
```

Get reading from specific meter:

```bash
pymeter client --meter Power
```

Monitor all meters continuously:

```bash
pymeter client --monitor --interval 2.0
```

Connect to remote server:

```bash
pymeter client --host 192.168.1.100 --port 5555 --monitor
```

## Programming Interface

### Server Example

```python
from pymeter import MeterServer, PowerMeter, SWRMeter

# Create and configure server
server = MeterServer(host='0.0.0.0', port=5555)
server.add_meter(PowerMeter("TX Power", max_power=100.0))
server.add_meter(SWRMeter("Antenna SWR"))

# Start server (blocking)
server.start()
```

### Client Example

```python
from pymeter import MeterClient

# Connect to server
client = MeterClient(host='localhost', port=5555)
client.connect()

# List available meters
meters = client.list_meters()
for meter in meters:
    print(f"{meter['name']} ({meter['unit']})")

# Get all readings
readings = client.get_all_readings()
for name, reading in readings.items():
    print(f"{reading['name']}: {reading['value']:.2f} {reading['unit']}")

# Disconnect
client.disconnect()
```

### Using Context Manager

```python
from pymeter import MeterClient

with MeterClient(host='localhost', port=5555) as client:
    readings = client.get_all_readings()
    # Process readings...
```

### Hardware Integration

To integrate with real hardware, extend the meter classes:

```python
from pymeter.meters import BaseMeter

class CustomPowerMeter(BaseMeter):
    def __init__(self, name="Custom Power"):
        super().__init__(name, "W")
        # Initialize your hardware connection
        
    def read(self):
        # Read from your hardware
        self._value = read_from_hardware()
        return self._value
```

## Architecture

PyMeter uses a simple client-server architecture:

- **Server**: Manages meter instances and serves readings over TCP
- **Client**: Connects to server and retrieves meter data
- **Meters**: Individual measurement classes with simulated or real hardware backends

### Communication Protocol

Communication uses JSON over TCP sockets:

**Request:**
```json
{"command": "get_all"}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "Power": {
      "name": "Power",
      "value": 45.2,
      "unit": "W",
      "timestamp": "2025-12-08T12:00:00.000Z"
    }
  }
}
```

### Available Commands

- `get_all`: Get readings from all meters
- `get_meter`: Get reading from specific meter (requires "meter" parameter)
- `list_meters`: List all available meters

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

Or with unittest:

```bash
python -m unittest discover tests
```

## Examples

See the `examples/` directory for more usage examples:

- `server_example.py`: Running a custom server
- `client_example.py`: Various client usage patterns

## Development Status

PyMeter is currently in experimental/alpha stage. It is designed as a framework for remote metering and can be extended for production use with real hardware.

## License

MIT License - see LICENSE file for details

## Author

Dr. Pedro E. Colla (LU7DZ)

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Future Enhancements

- Web-based dashboard for visualization
- Data logging and historical analysis
- Support for additional meter types
- MQTT integration for IoT applications
- Configuration file support
- Authentication and security features
