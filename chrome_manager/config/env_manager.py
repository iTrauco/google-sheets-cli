"""
config/env_manager.py
🔐 Environment configuration management
"""

import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv, set_key, find_dotenv
from rich.console import Console
from rich.prompt import Prompt

console = Console()

class EnvManager:
    """Environment variable manager"""
    
    ENV_VARS = {
        'CHROME_MANAGER_SPREADSHEET_ID': {
            'default': '1xDJeKh11yj_E_eO7PCrAVGy7UJa-7d_5zBx94alVfa8',
            'description': 'Google Sheet ID for profile tracking'
        },
        'CHROME_MANAGER_LOG_LEVEL': {
            'default': 'INFO',
            'description': 'Logging level (DEBUG, INFO, WARNING, ERROR)'
        },
        'CHROME_MANAGER_CREDENTIALS': {
            'default': str(Path(__file__).parent / 'credentials' / 'service_account.json'),
            'description': 'Path to service account credentials'
        }
    }
    
    def __init__(self):
        """Initialize environment manager"""
        self.env_file = find_dotenv()
        if not self.env_file:
            self.env_file = str(Path(__file__).parent.parent.parent / '.env')
            Path(self.env_file).touch()
        
        load_dotenv(self.env_file)

    def setup_env(self) -> None:
        """Interactive environment setup"""
        console.print("\n🔧 Environment Configuration", style="bold blue")
        
        for var_name, config in self.ENV_VARS.items():
            current_value = os.getenv(var_name, config['default'])
            console.print(f"\n📝 {config['description']}")
            console.print(f"Current value: {current_value}", style="cyan")
            
            if Prompt.ask("Update this value?", choices=["y", "n"], default="n") == "y":
                new_value = Prompt.ask("Enter new value", default=current_value)
                set_key(self.env_file, var_name, new_value)
                os.environ[var_name] = new_value
        
        console.print("\n✅ Environment configuration updated!", style="bold green")

    def get_env_info(self) -> Dict[str, Any]:
        """Get current environment configuration"""
        return {
            name: os.getenv(name, config['default'])
            for name, config in self.ENV_VARS.items()
        }

    def display_config(self) -> None:
        """Display current configuration"""
        console.print("\n⚙️ Current Configuration", style="bold blue")
        
        for var_name, config in self.ENV_VARS.items():
            value = os.getenv(var_name, config['default'])
            console.print(f"\n{config['description']}:", style="cyan")
            console.print(f"  {value}")

def setup_environment():
    """Quick setup function"""
    manager = EnvManager()
    manager.setup_env()

if __name__ == "__main__":
    setup_environment()