"""
Unit tests for server and client communication
"""

import unittest
import threading
import time
from pymeter.server import MeterServer
from pymeter.client import MeterClient
from pymeter.meters import PowerMeter, SWRMeter


class TestServerClient(unittest.TestCase):
    """Tests for server-client communication"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test server"""
        cls.server = MeterServer(host='127.0.0.1', port=5556)
        cls.server.add_meter(PowerMeter("Power", max_power=100.0))
        cls.server.add_meter(SWRMeter("SWR"))
        
        # Start server in a separate thread
        cls.server_thread = threading.Thread(target=cls.server.start)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        
        # Give server time to start
        time.sleep(0.5)
    
    @classmethod
    def tearDownClass(cls):
        """Tear down test server"""
        cls.server.stop()
        time.sleep(0.5)
    
    def test_client_connect(self):
        """Test client connection"""
        client = MeterClient(host='127.0.0.1', port=5556)
        self.assertTrue(client.connect())
        client.disconnect()
    
    def test_list_meters(self):
        """Test listing available meters"""
        client = MeterClient(host='127.0.0.1', port=5556)
        client.connect()
        
        meters = client.list_meters()
        self.assertIsNotNone(meters)
        self.assertEqual(len(meters), 2)
        
        meter_names = [m['name'] for m in meters]
        self.assertIn('Power', meter_names)
        self.assertIn('SWR', meter_names)
        
        client.disconnect()
    
    def test_get_all_readings(self):
        """Test getting all meter readings"""
        client = MeterClient(host='127.0.0.1', port=5556)
        client.connect()
        
        readings = client.get_all_readings()
        self.assertIsNotNone(readings)
        self.assertIn('Power', readings)
        self.assertIn('SWR', readings)
        
        # Check structure of readings
        power_reading = readings['Power']
        self.assertIn('name', power_reading)
        self.assertIn('value', power_reading)
        self.assertIn('unit', power_reading)
        self.assertIn('timestamp', power_reading)
        
        client.disconnect()
    
    def test_get_specific_meter_reading(self):
        """Test getting specific meter reading"""
        client = MeterClient(host='127.0.0.1', port=5556)
        client.connect()
        
        reading = client.get_meter_reading('Power')
        self.assertIsNotNone(reading)
        self.assertEqual(reading['name'], 'Power')
        self.assertEqual(reading['unit'], 'W')
        self.assertGreaterEqual(reading['value'], 0)
        
        client.disconnect()
    
    def test_context_manager(self):
        """Test client context manager"""
        with MeterClient(host='127.0.0.1', port=5556) as client:
            readings = client.get_all_readings()
            self.assertIsNotNone(readings)


if __name__ == '__main__':
    unittest.main()
