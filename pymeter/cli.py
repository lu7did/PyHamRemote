"""
Command-line interface for PyMeter
"""

import argparse
import sys
import time
import signal
from .server import MeterServer
from .client import MeterClient
from .meters import PowerMeter, SWRMeter, SignalStrengthMeter, VoltageMeter


def run_server(args):
    """Run the meter server"""
    server = MeterServer(host=args.host, port=args.port)
    
    # Add default meters
    server.add_meter(PowerMeter("Power", max_power=100.0))
    server.add_meter(SWRMeter("SWR"))
    server.add_meter(SignalStrengthMeter("Signal"))
    server.add_meter(VoltageMeter("Voltage"))
    
    # Handle shutdown gracefully
    def signal_handler(sig, frame):
        print("\nShutting down server...")
        server.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print(f"Starting PyMeter server on {args.host}:{args.port}")
    print("Available meters: Power, SWR, Signal, Voltage")
    print("Press Ctrl+C to stop")
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.stop()


def run_client(args):
    """Run the meter client"""
    client = MeterClient(host=args.host, port=args.port)
    
    if not client.connect():
        print("Failed to connect to server")
        return 1
    
    try:
        if args.list:
            # List available meters
            meters = client.list_meters()
            if meters:
                print("Available meters:")
                for meter in meters:
                    print(f"  - {meter['name']} ({meter['unit']})")
            else:
                print("No meters available or error occurred")
                
        elif args.meter:
            # Get specific meter reading
            reading = client.get_meter_reading(args.meter)
            if reading:
                print(f"{reading['name']}: {reading['value']:.2f} {reading['unit']}")
                print(f"Timestamp: {reading['timestamp']}")
            else:
                print(f"Failed to get reading for meter: {args.meter}")
                
        elif args.monitor:
            # Monitor all meters continuously
            print("Monitoring all meters (Press Ctrl+C to stop)...")
            try:
                while True:
                    readings = client.get_all_readings()
                    if readings:
                        print("\n" + "=" * 50)
                        for name, reading in readings.items():
                            print(f"{reading['name']}: {reading['value']:.2f} {reading['unit']}")
                        print("=" * 50)
                    time.sleep(args.interval)
            except KeyboardInterrupt:
                print("\nMonitoring stopped")
        else:
            # Get all readings once
            readings = client.get_all_readings()
            if readings:
                for name, reading in readings.items():
                    print(f"{reading['name']}: {reading['value']:.2f} {reading['unit']}")
            else:
                print("Failed to get readings")
                
    finally:
        client.disconnect()
    
    return 0


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='PyMeter - Remote meter for ham radio stations',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Server command
    server_parser = subparsers.add_parser('server', help='Run meter server')
    server_parser.add_argument(
        '--host',
        default='0.0.0.0',
        help='Host address to bind to (default: 0.0.0.0)'
    )
    server_parser.add_argument(
        '--port',
        type=int,
        default=5555,
        help='Port to listen on (default: 5555)'
    )
    
    # Client command
    client_parser = subparsers.add_parser('client', help='Connect to meter server')
    client_parser.add_argument(
        '--host',
        default='localhost',
        help='Server host address (default: localhost)'
    )
    client_parser.add_argument(
        '--port',
        type=int,
        default=5555,
        help='Server port (default: 5555)'
    )
    client_parser.add_argument(
        '--list',
        action='store_true',
        help='List available meters'
    )
    client_parser.add_argument(
        '--meter',
        help='Get reading from specific meter'
    )
    client_parser.add_argument(
        '--monitor',
        action='store_true',
        help='Continuously monitor all meters'
    )
    client_parser.add_argument(
        '--interval',
        type=float,
        default=1.0,
        help='Monitoring interval in seconds (default: 1.0)'
    )
    
    args = parser.parse_args()
    
    if args.command == 'server':
        return run_server(args)
    elif args.command == 'client':
        return run_client(args)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
