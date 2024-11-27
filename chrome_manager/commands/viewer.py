"""
chrome_manager/commands/viewer.py
👀 Profile and file viewing command implementations
"""

import json
import logging
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

from chrome_manager.utils.chrome_scanner import ChromeProfileScanner
from chrome_manager.core.sheets import SheetsManager

console = Console()
log = logging.getLogger("viewer")

def view_profiles() -> None:
    """Scan and display current Chrome profiles"""
    try:
        scanner = ChromeProfileScanner()
        profiles = scanner.get_profiles()  # This now writes to tmp
        
        table = Table(title="Current Chrome Profiles")
        table.add_column("Name", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Email/Identity", style="blue")
        table.add_column("Last Used", style="magenta")
        
        for profile in profiles:
            table.add_row(
                profile['name'],
                "🔒 Local" if profile['is_local'] else "🌐 Signed-in",
                profile['email'] or "N/A",
                profile['last_used'] or "Unknown"
            )
        
        console.print("\n")
        console.print(table)
        
    except Exception as e:
        log.error(f"Error viewing profiles: {e}")
        console.print(f"\n❌ Error: {e}", style="bold red")
    
    input("\nPress Enter to continue...")

def view_tmp_files() -> None:
    """View and inspect temporary profile scan files"""
    try:
        tmp_dir = Path("tmp")
        if not tmp_dir.exists():
            console.print("\n❌ No tmp directory found", style="bold red")
            return
            
        files = list(tmp_dir.glob("chrome_profiles_*.json"))
        if not files:
            console.print("\n📂 No profile scans found", style="yellow")
            return
            
        # Show available files
        console.print("\n📁 Available Profile Scans:", style="bold blue")
        for i, file in enumerate(files, 1):
            console.print(f"{i}. {file.name}")
            
        # Let user choose a file to view
        choice = Prompt.ask(
            "\nSelect a file to view (number)", 
            choices=[str(i) for i in range(1, len(files) + 1)]
        )
        
        # Display chosen file contents
        file = files[int(choice) - 1]
        with open(file, 'r') as f:
            data = json.load(f)
            
        console.print(f"\n📄 File: {file.name}", style="bold blue")
        console.print(f"Timestamp: {data['timestamp']}")
        console.print(f"Total Profiles: {data['total_profiles']}")
        
        for profile in data['profiles']:
            console.print(f"\n• {profile['name']}")
            console.print(f"  Email: {profile['email']}")
            console.print(f"  Type: {'Local' if profile['is_local'] else 'Signed-in'}")
            console.print(f"  Last Used: {profile['last_used']}")
            
    except Exception as e:
        log.error(f"Error viewing tmp files: {e}")
        console.print(f"\n❌ Error: {e}", style="bold red")
    
    input("\nPress Enter to continue...")

def view_sheets_history(sheets_manager: SheetsManager) -> None:
    """View Google Sheets sync history"""
    try:
        last_sync = sheets_manager.get_last_sync_time()
        if last_sync:
            console.print(f"\n📅 Last sync: {last_sync}", style="bold blue")
        else:
            console.print("\n⚠️ No sync history found", style="yellow")
    except Exception as e:
        log.error(f"Error viewing sheets history: {e}")
        console.print(f"\n❌ Error: {e}", style="bold red")
    
    input("\nPress Enter to continue...")