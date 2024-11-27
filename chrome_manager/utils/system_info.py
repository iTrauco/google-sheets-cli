"""
cli/utils/system_info.py - System Information Collector
"""

import platform
import socket
import logging
from typing import Dict, Any
from datetime import datetime
import distro
import psutil
from pathlib import Path

from rich.console import Console

console = Console()
log = logging.getLogger("system_info")

class SystemInfoCollector:
    """💻 System information collection and management"""
    
    def __init__(self):
        """Initialize system info collector"""
        self._cache: Dict[str, Any] = {}
        self._last_update: datetime = None
        self._cache_duration = 300  # 5 minutes
    
    def get_system_info(self) -> Dict[str, Any]:
        """Collect comprehensive system information"""
        try:
            hostname = socket.gethostname()
            mem = psutil.virtual_memory()
            
            return {
                'hostname': hostname,
                'ip_address': socket.gethostbyname(hostname),
                'os_info': f"{platform.system()} {distro.name(pretty=True)}",
                'memory': {
                    'total': f"{mem.total / (1024**3):.2f}GB",
                    'available': f"{mem.available / (1024**3):.2f}GB",
                    'used': f"{mem.used / (1024**3):.2f}GB",
                    'percent': f"{mem.percent}%"
                },
                'username': Path.home().name,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            log.error(f"Error collecting system info: {e}")
            return {}

    def get_sheet_data(self) -> Dict[str, str]:
        """Get system info formatted for sheet"""
        try:
            info = self.get_system_info()
            return {
                'hostname': info.get('hostname', ''),
                'ip_address': info.get('ip_address', ''),
                'os_info': info.get('os_info', ''),
                'memory_total': info.get('memory', {}).get('total', ''),
                'memory_available': info.get('memory', {}).get('available', ''),
                'username': info.get('username', ''),
                'timestamp': info.get('timestamp', datetime.now().isoformat())
            }
        except Exception as e:
            log.error(f"Error formatting sheet data: {e}")
            return {
                'hostname': '',
                'ip_address': '',
                'os_info': '',
                'memory_total': '',
                'memory_available': '',
                'username': '',
                'timestamp': datetime.now().isoformat()
            }