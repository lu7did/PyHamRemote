"""
Client implementation for accessing remote meters
"""

import socket
import json
import logging
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MeterClient:
    """TCP client for accessing remote meters"""
    
    def __init__(self, host: str = 'localhost', port: int = 5555):
        """
        Initialize the meter client
        
        Args:
            host: Server host address
            port: Server port number
        """
        self.host = host
        self.port = port
        self.socket = None
        
    def connect(self) -> bool:
        """
        Connect to the meter server
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            logger.info(f"Connected to meter server at {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to server: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the meter server"""
        if self.socket:
            try:
                self.socket.close()
                logger.info("Disconnected from meter server")
            except:
                pass
            finally:
                self.socket = None
    
    def _send_command(self, command: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Send a command to the server
        
        Args:
            command: Command dictionary
            
        Returns:
            Response dictionary or None on error
        """
        if not self.socket:
            logger.error("Not connected to server")
            return None
            
        try:
            # Send command
            self.socket.send(json.dumps(command).encode('utf-8'))
            
            # Receive response
            data = self.socket.recv(4096).decode('utf-8')
            return json.loads(data)
            
        except Exception as e:
            logger.error(f"Communication error: {e}")
            return None
    
    def get_all_readings(self) -> Optional[Dict[str, Any]]:
        """
        Get readings from all meters
        
        Returns:
            Dictionary of all meter readings or None on error
        """
        command = {'command': 'get_all'}
        response = self._send_command(command)
        
        if response and response.get('status') == 'success':
            return response.get('data')
        return None
    
    def get_meter_reading(self, meter_name: str) -> Optional[Dict[str, Any]]:
        """
        Get reading from a specific meter
        
        Args:
            meter_name: Name of the meter
            
        Returns:
            Dictionary containing the meter reading or None on error
        """
        command = {'command': 'get_meter', 'meter': meter_name}
        response = self._send_command(command)
        
        if response and response.get('status') == 'success':
            return response.get('data')
        return None
    
    def list_meters(self) -> Optional[list]:
        """
        Get list of available meters
        
        Returns:
            List of meter information dictionaries or None on error
        """
        command = {'command': 'list_meters'}
        response = self._send_command(command)
        
        if response and response.get('status') == 'success':
            return response.get('data', {}).get('meters', [])
        return None
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
