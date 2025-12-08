#!/usr/bin/env python3
"""
Example of running a PyMeter server with custom meters
"""

import sys
import time
import signal
from pymeter import MeterServer, PowerMeter, SWRMeter, SignalStrengthMeter, VoltageMeter


def main():
    # Create server
    server = MeterServer(host='0.0.0.0', port=5555)
    
    # Add meters with custom configurations
    server.add_meter(PowerMeter("TX Power", max_power=100.0))
    server.add_meter(SWRMeter("Antenna SWR"))
    server.add_meter(SignalStrengthMeter("RX Signal"))
    server.add_meter(VoltageMeter("PSU Voltage", max_voltage=15.0))
    
    # Setup graceful shutdown
    def signal_handler(sig, frame):
        print("\nShutting down server...")
        server.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("PyMeter Server Example")
    print("=" * 50)
    print(f"Server listening on 0.0.0.0:5555")
    print("\nAvailable meters:")
    print("  - TX Power (W)")
    print("  - Antenna SWR (:1)")
    print("  - RX Signal (dB)")
    print("  - PSU Voltage (V)")
    print("\nPress Ctrl+C to stop")
    print("=" * 50)
    
    # Start server
    server.start()


if __name__ == '__main__':
    main()
