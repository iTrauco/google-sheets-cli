"""
core/scanner.py - Chrome Profile Scanner
🔍 Scans and extracts Chrome profile information with enhanced error handling
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, NamedTuple
from datetime import datetime

from rich.console import Console
from rich.logging import RichHandler

# Initialize logging with rich
console = Console()
logging.basicConfig(
    level="DEBUG",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
log = logging.getLogger("chrome_scanner")

class ChromeProfile(NamedTuple):
    """📋 Structure for Chrome profile information"""
    name: str                   # Directory name (e.g., "Profile 1")
    email: Optional[str]        # Email if signed in
    is_local: bool             # True if local profile
    custom_name: Optional[str]  # User-set profile name
    last_used: Optional[str]    # Last used timestamp
    path: Path                 # Full path to profile directory

class ChromeProfileScanner:
    """🔎 Handles scanning and extraction of Chrome profile information"""
    
    def __init__(self, chrome_config_path: Optional[Path] = None):
        """
        Initialize scanner with configuration path
        
        Args:
            chrome_config_path: Optional custom path to Chrome config directory
        """
        self.config_path = chrome_config_path or Path.home() / ".config" / "google-chrome"
        self._validate_config_path()

    def _validate_config_path(self) -> None:
        """✅ Validate Chrome configuration path exists"""
        if not self.config_path.exists():
            log.error(f"Chrome config path not found: {self.config_path}")
            raise FileNotFoundError(f"Chrome configuration not found at {self.config_path}")
        log.debug(f"Found Chrome config at: {self.config_path}")

    def get_profile_dirs(self) -> List[Path]:
        """
        📂 Get all Chrome profile directories
        
        Returns:
            List of profile directory paths
        """
        try:
            profiles = []
            # Check Default profile
            default_profile = self.config_path / "Default"
            if default_profile.is_dir():
                profiles.append(default_profile)
            
            # Get numbered profiles
            for profile in self.config_path.glob("Profile *"):
                if profile.is_dir():
                    profiles.append(profile)
            
            log.debug(f"Found {len(profiles)} Chrome profiles")
            return sorted(profiles, key=self._profile_sort_key)
            
        except Exception as e:
            log.error(f"Error scanning profile directories: {e}")
            raise

    def _profile_sort_key(self, profile_path: Path) -> tuple:
        """🔤 Sort key for profile directories"""
        if profile_path.name == "Default":
            return (0, 0)
        try:
            num = int(profile_path.name.split()[-1])
            return (1, num)
        except (IndexError, ValueError):
            return (2, profile_path.name)

    def read_profile_preferences(self, profile_path: Path) -> Dict:
        """
        📖 Read and parse profile preferences file
        
        Args:
            profile_path: Path to profile directory
            
        Returns:
            Dictionary of profile preferences
        """
        try:
            prefs_file = profile_path / "Preferences"
            if not prefs_file.exists():
                log.warning(f"No preferences file found for profile: {profile_path.name}")
                return {}
                
            with open(prefs_file, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except json.JSONDecodeError as e:
            log.error(f"Invalid JSON in preferences file: {profile_path.name} - {e}")
            return {}
        except Exception as e:
            log.error(f"Error reading preferences for {profile_path.name}: {e}")
            return {}

    def extract_profile_info(self, profile_path: Path, prefs: Dict) -> ChromeProfile:
        """
        📑 Extract profile information from preferences
        
        Args:
            profile_path: Path to profile directory
            prefs: Profile preferences dictionary
            
        Returns:
            ChromeProfile object with extracted information
        """
        try:
            # Get account info
            account_info = prefs.get("account_info", [{}])[0]
            email = account_info.get("email")
            
            # Get profile info
            profile_info = prefs.get("profile", {})
            custom_name = profile_info.get("name")
            
            # Get last used time
            last_used = None
            if info_cache := prefs.get("profile", {}).get("info_cache", {}):
                last_used_timestamp = info_cache.get("last_used")
                if last_used_timestamp:
                    last_used = datetime.fromtimestamp(last_used_timestamp).isoformat()
            
            return ChromeProfile(
                name=profile_path.name,
                email=email,
                is_local=not bool(email),
                custom_name=custom_name,
                last_used=last_used,
                path=profile_path
            )
            
        except Exception as e:
            log.error(f"Error extracting profile info for {profile_path.name}: {e}")
            # Return a basic profile if extraction fails
            return ChromeProfile(
                name=profile_path.name,
                email=None,
                is_local=True,
                custom_name=None,
                last_used=None,
                path=profile_path
            )

    def scan_profiles(self) -> List[ChromeProfile]:
        """
        🔍 Scan all Chrome profiles and extract information
        
        Returns:
            List of ChromeProfile objects
        """
        profiles = []
        for profile_dir in self.get_profile_dirs():
            try:
                prefs = self.read_profile_preferences(profile_dir)
                profile = self.extract_profile_info(profile_dir, prefs)
                profiles.append(profile)
                log.debug(f"Processed profile: {profile.name} ({profile.email or 'local'})")
            except Exception as e:
                log.error(f"Error processing profile {profile_dir.name}: {e}")
                continue
        
        return profiles

if __name__ == "__main__":
    # Simple test code
    try:
        scanner = ChromeProfileScanner()
        console.print("🔍 Scanning Chrome Profiles...", style="bold blue")
        
        profiles = scanner.scan_profiles()
        
        console.print("\n📊 Found Profiles:", style="bold green")
        for profile in profiles:
            profile_type = "🔒 Local" if profile.is_local else f"🌐 Signed-in ({profile.email})"
            console.print(f"  • {profile.name}: {profile_type}")
            if profile.custom_name:
                console.print(f"    └─ Custom Name: {profile.custom_name}")
            if profile.last_used:
                console.print(f"    └─ Last Used: {profile.last_used}")
                
    except Exception as e:
        console.print(f"❌ Error: {e}", style="bold red")