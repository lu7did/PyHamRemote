#!/usr/bin/env python3
"""
Example of using PyMeter client to access remote meters
"""

import time
from pymeter import MeterClient


def main():
    print("PyMeter Client Example")
    print("=" * 50)
    
    # Create client and connect
    client = MeterClient(host='localhost', port=5555)
    
    if not client.connect():
        print("Failed to connect to server. Make sure the server is running.")
        return 1
    
    try:
        # List available meters
        print("\nListing available meters:")
        meters = client.list_meters()
        if meters:
            for meter in meters:
                print(f"  - {meter['name']} ({meter['unit']})")
        
        # Get all readings
        print("\n" + "=" * 50)
        print("Getting all meter readings:")
        readings = client.get_all_readings()
        if readings:
            for name, reading in readings.items():
                print(f"  {reading['name']}: {reading['value']:.2f} {reading['unit']}")
        
        # Monitor specific meter
        print("\n" + "=" * 50)
        print("Monitoring Power meter (5 readings):")
        for i in range(5):
            reading = client.get_meter_reading("TX Power")
            if reading:
                print(f"  Reading {i+1}: {reading['value']:.2f} {reading['unit']}")
            time.sleep(1)
        
        print("\n" + "=" * 50)
        print("Example completed successfully!")
        
    finally:
        client.disconnect()
    
    return 0


if __name__ == '__main__':
    exit(main())
