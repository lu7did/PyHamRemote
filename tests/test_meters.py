"""
Unit tests for meter classes
"""

import unittest
import time
from pymeter.meters import PowerMeter, SWRMeter, SignalStrengthMeter, VoltageMeter


class TestPowerMeter(unittest.TestCase):
    """Tests for PowerMeter class"""
    
    def test_initialization(self):
        """Test meter initialization"""
        meter = PowerMeter("Test Power", max_power=50.0)
        self.assertEqual(meter.name, "Test Power")
        self.assertEqual(meter.unit, "W")
        self.assertEqual(meter.max_power, 50.0)
    
    def test_read_simulated(self):
        """Test simulated reading"""
        meter = PowerMeter(max_power=100.0)
        value = meter.read()
        self.assertGreaterEqual(value, 0)
        self.assertLessEqual(value, 100.0)
    
    def test_set_value(self):
        """Test manual value setting"""
        meter = PowerMeter()
        meter.set_value(45.5)
        self.assertEqual(meter.value, 45.5)
    
    def test_set_value_bounds(self):
        """Test value bounds checking"""
        meter = PowerMeter(max_power=100.0)
        meter.set_value(150.0)
        self.assertEqual(meter.value, 100.0)
        meter.set_value(-10.0)
        self.assertEqual(meter.value, 0.0)
    
    def test_get_reading(self):
        """Test get_reading returns complete data"""
        meter = PowerMeter()
        reading = meter.get_reading()
        self.assertIn('name', reading)
        self.assertIn('value', reading)
        self.assertIn('unit', reading)
        self.assertIn('timestamp', reading)
        self.assertEqual(reading['unit'], 'W')


class TestSWRMeter(unittest.TestCase):
    """Tests for SWRMeter class"""
    
    def test_initialization(self):
        """Test meter initialization"""
        meter = SWRMeter("Test SWR")
        self.assertEqual(meter.name, "Test SWR")
        self.assertEqual(meter.unit, ":1")
    
    def test_read_simulated(self):
        """Test simulated reading"""
        meter = SWRMeter()
        value = meter.read()
        self.assertGreaterEqual(value, 1.0)
        self.assertLessEqual(value, 2.0)
    
    def test_set_value(self):
        """Test manual value setting"""
        meter = SWRMeter()
        meter.set_value(1.5)
        self.assertEqual(meter.value, 1.5)
    
    def test_minimum_value(self):
        """Test minimum SWR value is 1.0"""
        meter = SWRMeter()
        meter.set_value(0.5)
        self.assertEqual(meter.value, 1.0)


class TestSignalStrengthMeter(unittest.TestCase):
    """Tests for SignalStrengthMeter class"""
    
    def test_initialization(self):
        """Test meter initialization"""
        meter = SignalStrengthMeter("Test Signal")
        self.assertEqual(meter.name, "Test Signal")
        self.assertEqual(meter.unit, "dB")
    
    def test_read_simulated(self):
        """Test simulated reading"""
        meter = SignalStrengthMeter()
        value = meter.read()
        self.assertGreaterEqual(value, -120)
        self.assertLessEqual(value, -20)
    
    def test_set_value(self):
        """Test manual value setting"""
        meter = SignalStrengthMeter()
        meter.set_value(-60.0)
        self.assertEqual(meter.value, -60.0)


class TestVoltageMeter(unittest.TestCase):
    """Tests for VoltageMeter class"""
    
    def test_initialization(self):
        """Test meter initialization"""
        meter = VoltageMeter("Test Voltage", max_voltage=15.0)
        self.assertEqual(meter.name, "Test Voltage")
        self.assertEqual(meter.unit, "V")
        self.assertEqual(meter.max_voltage, 15.0)
    
    def test_read_simulated(self):
        """Test simulated reading"""
        meter = VoltageMeter()
        value = meter.read()
        self.assertGreaterEqual(value, 12.5)
        self.assertLessEqual(value, 14.2)
    
    def test_set_value(self):
        """Test manual value setting"""
        meter = VoltageMeter()
        meter.set_value(13.8)
        self.assertEqual(meter.value, 13.8)
    
    def test_set_value_bounds(self):
        """Test value bounds checking"""
        meter = VoltageMeter(max_voltage=15.0)
        meter.set_value(20.0)
        self.assertEqual(meter.value, 15.0)
        meter.set_value(-5.0)
        self.assertEqual(meter.value, 0.0)


if __name__ == '__main__':
    unittest.main()
