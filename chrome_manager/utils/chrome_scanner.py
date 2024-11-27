"""
chrome_manager/utils/chrome_scanner.py
🔍 Scans and extracts Chrome profile information
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

from rich.console import Console

console = Console()
log = logging.getLogger("chrome_scanner")

class ChromeProfileScanner:
    """🔍 Chrome profile scanner implementation"""
    
    def __init__(self, chrome_path: Optional[Path] = None, tmp_dir: Optional[Path] = None):
        self.chrome_path = chrome_path or Path.home() / ".config" / "google-chrome"
        self.tmp_dir = tmp_dir or Path("tmp")
        self._validate_paths()
    
    def _validate_paths(self) -> None:
        """✅ Validate required paths exist"""
        if not self.chrome_path.exists():
            raise FileNotFoundError(f"Chrome config not found at: {self.chrome_path}")
        
        # Create tmp directory if it doesn't exist
        self.tmp_dir.mkdir(parents=True, exist_ok=True)
        log.debug(f"Found Chrome config at: {self.chrome_path}")
        log.debug(f"Using tmp directory: {self.tmp_dir}")
    
    def get_profiles(self) -> List[Dict]:
        """📂 Get all Chrome profiles with account information"""
        profiles = []
        try:
            # Check Default profile
            default_path = self.chrome_path / "Default"
            if default_path.is_dir():
                if profile_info := self._read_profile_info(default_path):
                    profiles.append(profile_info)
            
            # Check all numbered profiles
            for profile_dir in sorted(self.chrome_path.glob("Profile *")):
                if profile_dir.is_dir():
                    if profile_info := self._read_profile_info(profile_dir):
                        profiles.append(profile_info)
            
            # Write to tmp file
            self._write_to_tmp(profiles)
            
            log.debug(f"Found {len(profiles)} Chrome profiles")
            return profiles
            
        except Exception as e:
            log.error(f"Error scanning profiles: {e}")
            return []
    def _read_profile_info(self, profile_path: Path) -> Optional[Dict]:
        """📋 Read Chrome profile information"""
        try:
            prefs_file = profile_path / "Preferences"
            if not prefs_file.exists():
                log.debug(f"No preferences file found for {profile_path.name}")
                return None

            with open(prefs_file, 'r', encoding='utf-8') as f:
                prefs = json.load(f)

            # Extract account info
            account_info = prefs.get('account_info', [{}])[0]
            email = account_info.get('email')

            # Extract profile info
            profile_info = prefs.get('profile', {})
            
            # Get profile name with better fallbacks for local profiles
            custom_name = None
            
            # Try to get name from profile info first
            if 'name' in profile_info:
                custom_name = profile_info['name']
            
            # Then try sync info
            if not custom_name:
                sync_info = prefs.get('google', {}).get('chrome_sync', {})
                if sync_info:
                    custom_name = sync_info.get('profile_name')
            
            # Finally check info cache
            if not custom_name:
                info_cache = profile_info.get('info_cache', {})
                custom_name = info_cache.get('name')

            # Get last used time
            last_used = None
            info_cache = profile_info.get('info_cache', {})
            if 'last_used' in info_cache:
                try:
                    last_used = datetime.fromtimestamp(info_cache['last_used']).isoformat()
                except:
                    last_used = datetime.now().isoformat()

            # For local profiles, use custom name as the email/identity if present
            display_identity = email if email else (custom_name or 'Local Profile')

            return {
                'name': profile_path.name,
                'path': str(profile_path),
                'is_local': not bool(email),
                'email': display_identity,
                'custom_name': custom_name or 'Unknown',
                'last_used': last_used,
            }

        except Exception as e:
            log.error(f"Error reading profile {profile_path.name}: {e}")
            return None

    def _write_to_tmp(self, profiles: List[Dict]) -> None:
        """💾 Write profile data to tmp file"""
        try:
            timestamp = datetime.now().isoformat()
            output_data = {
                'timestamp': timestamp,
                'total_profiles': len(profiles),
                'profiles': profiles
            }
            
            output_file = self.tmp_dir / f"chrome_profiles_{timestamp.replace(':', '-')}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2)
                
            log.debug(f"Wrote profile data to: {output_file}")
            console.print(f"\n💾 Profile data written to: {output_file}", style="bold green")
            
        except Exception as e:
            log.error(f"Error writing to tmp file: {e}")
            console.print(f"\n❌ Failed to write tmp file: {e}", style="bold red")

if __name__ == "__main__":
    # Test the scanner
    scanner = ChromeProfileScanner()
    profiles = scanner.get_profiles()
    
    console.print("\n📊 Chrome Profiles:", style="bold blue")
    for i, profile in enumerate(profiles, 1):
        console.print(f"\n{i}. {profile['name']}")
        console.print(f"   Type: {'Local' if profile['is_local'] else 'Signed-in'}")
        console.print(f"   Email: {profile['email']}")
        console.print(f"   Custom Name: {profile['custom_name']}")
        if profile['last_used']:
            console.print(f"   Last Used: {profile['last_used']}")