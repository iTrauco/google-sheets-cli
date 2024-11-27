"""
chrome_manager/commands/maintenance.py
🧹 Maintenance and configuration commands
"""

import logging
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm

console = Console()
log = logging.getLogger("maintenance")

def clean_old_entries() -> None:
    """Clean old tmp files and sheet entries"""
    try:
        # Clean tmp files
        if Confirm.ask("\nClean old tmp files?"):
            tmp_dir = Path("tmp")
            if tmp_dir.exists():
                files = list(tmp_dir.glob("chrome_profiles_*.json"))
                if files:
                    for file in files[:-5]:  # Keep last 5 files
                        file.unlink()
                    console.print(f"\n✅ Cleaned {len(files) - 5} old tmp files", style="bold green")
                else:
                    console.print("\n📂 No tmp files to clean", style="yellow")
            
    except Exception as e:
        log.error(f"Error cleaning entries: {e}")
        console.print(f"\n❌ Error: {e}", style="bold red")
    
    input("\nPress Enter to continue...")

def configure_settings() -> None:
    """Configure application settings"""
    try:
        console.print("\n⚙️ Current Configuration:", style="bold blue")
        # Add configuration options here
        console.print("\n⚠️ Configuration options coming soon!", style="yellow")
    except Exception as e:
        log.error(f"Error in configuration: {e}")
        console.print(f"\n❌ Error: {e}", style="bold red")
    
    input("\nPress Enter to continue...")