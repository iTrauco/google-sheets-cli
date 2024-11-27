# test_setup.py
from pathlib import Path
from rich.console import Console
import os
from dotenv import load_dotenv

console = Console()

def check_setup():
    # Load .env
    load_dotenv()
    
    # Critical paths and values to check
    checks = {
        '.env file': Path('.env').exists(),
        'Service Account': Path('chrome_manager/config/credentials/service_account.json').exists(),
        'Spreadsheet ID': bool(os.getenv('CHROME_MANAGER_SPREADSHEET_ID')),
        'Sheet ID matches': os.getenv('CHROME_MANAGER_SPREADSHEET_ID') == '1xDJeKh11yj_E_eO7PCrAVGy7UJa-7d_5zBx94alVfa8'
    }
    
    for item, status in checks.items():
        console.print(f"{item}: {'✅' if status else '❌'}", 
                     style="green" if status else "red")
    
    return all(checks.values())

if __name__ == "__main__":
    console.print("\n🔍 Checking setup...", style="bold blue")
    if check_setup():
        console.print("\n✅ All components verified!", style="bold green")
    else:
        console.print("\n❌ Some components are missing!", style="bold red")