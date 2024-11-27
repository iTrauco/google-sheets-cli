"""
chrome_manager/commands/profile_sync.py
🔄 Profile scanning and syncing command implementation
"""

import json
import logging
from pathlib import Path
from typing import Optional, List, Dict
from rich.console import Console
from rich.prompt import Confirm

from chrome_manager.utils.chrome_scanner import ChromeProfileScanner
from chrome_manager.utils.system_info import SystemInfoCollector
from chrome_manager.core.sheets import SheetsManager

console = Console()
log = logging.getLogger("profile_sync")

def scan_to_tmp() -> Optional[Path]:
    """Scan Chrome profiles to tmp file"""
    try:
        scanner = ChromeProfileScanner()
        profiles = scanner.get_profiles()  # This now writes to tmp and returns data
        return next(Path("tmp").glob("chrome_profiles_*.json"), None)
    except Exception as e:
        log.error(f"Error scanning profiles: {e}")
        console.print(f"\n❌ Error scanning profiles: {e}", style="bold red")
        return None

def review_tmp_data(tmp_file: Path) -> bool:
    """Review the temporary data before syncing"""
    try:
        with open(tmp_file, 'r') as f:
            data = json.load(f)
        
        console.print("\n📊 Scanned Profile Data:", style="bold blue")
        console.print(f"Total Profiles: {data['total_profiles']}")
        console.print("\nProfiles:")
        for profile in data['profiles']:
            console.print(f"\n• {profile['name']}")
            console.print(f"  Email: {profile['email']}")
            console.print(f"  Type: {'Local' if profile['is_local'] else 'Signed-in'}")
            console.print(f"  Last Used: {profile['last_used']}")
        
        return Confirm.ask("\nSync this data to Google Sheets?")
    except Exception as e:
        log.error(f"Error reviewing tmp data: {e}")
        console.print(f"\n❌ Error reviewing data: {e}", style="bold red")
        return False

def sync_to_sheets(tmp_file: Path, sheets_manager: SheetsManager) -> bool:
    """Sync data from tmp file to Google Sheets"""
    try:
        # Read tmp file
        with open(tmp_file, 'r') as f:
            data = json.load(f)
        
        # Get system info
        system_info = SystemInfoCollector().get_sheet_data()
        
        # Sync to sheets
        success = sheets_manager.update_profiles(data['profiles'], system_info)
        
        if success:
            console.print("\n✅ Successfully synced to Google Sheets!", style="bold green")
            return True
        else:
            console.print("\n❌ Failed to sync to Google Sheets", style="bold red")
            return False
            
    except Exception as e:
        log.error(f"Error syncing to sheets: {e}")
        console.print(f"\n❌ Error syncing to sheets: {e}", style="bold red")
        return False

def sync_profiles(sheets_manager: SheetsManager) -> None:
    """Main profile sync command"""
    try:
        # First scan to tmp
        console.print("\n🔍 Scanning Chrome profiles...", style="bold blue")
        tmp_file = scan_to_tmp()
        
        if not tmp_file:
            console.print("\n❌ No profile data found", style="bold red")
            return
            
        # Review the data
        if review_tmp_data(tmp_file):
            # Sync to sheets if approved
            sync_to_sheets(tmp_file, sheets_manager)
        else:
            console.print("\nSync cancelled", style="yellow")
            
    except Exception as e:
        log.error(f"Error in profile sync: {e}")
        console.print(f"\n❌ Error: {e}", style="bold red")
    
    input("\nPress Enter to continue...")