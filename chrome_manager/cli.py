"""
chrome_manager/cli.py - Main Entry Point
🎮 Chrome Profile Sheet Manager CLI entry point
"""

import sys
import logging
from pathlib import Path

from rich.console import Console
from rich.logging import RichHandler

from chrome_manager.commands.profile_sync import sync_profiles
from chrome_manager.commands.viewer import view_profiles, view_tmp_files, view_sheets_history
from chrome_manager.commands.maintenance import clean_old_entries, configure_settings
from chrome_manager.core.sheets import SheetsManager

# Constants
SPREADSHEET_ID = "1xDJeKh11yj_E_eO7PCrAVGy7UJa-7d_5zBx94alVfa8"
CREDENTIALS_PATH = Path("chrome_manager/config/credentials/service_account.json")

# Initialize console and logging
console = Console()
logging.basicConfig(
    level="DEBUG",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
log = logging.getLogger("chrome_manager")

class ChromeSheetsCLI:
    """🎮 Main CLI application controller"""
    
    def __init__(self):
        """Initialize CLI application"""
        self._running = True
        
        # Initialize sheets manager
        self.sheets_manager = SheetsManager(
            credentials_path=CREDENTIALS_PATH,
            spreadsheet_id=SPREADSHEET_ID
        )
        
        self.menu_options = {
            '1': ('🔍 Scan Profiles to tmp', view_profiles),
            '2': ('📁 View tmp Files', view_tmp_files),
            '3': ('🔄 Sync Profiles to Sheets', self._sync_profiles),
            '4': ('📊 View Sheets History', self._view_sheets_history),
            '5': ('🧹 Clean Old Entries', clean_old_entries),
            '6': ('⚙️ Configure Settings', configure_settings),
            '7': ('❌ Exit', self.exit_cli)
        }

    def _sync_profiles(self) -> None:
        """Wrapper for sync_profiles command"""
        sync_profiles(self.sheets_manager)

    def _view_sheets_history(self) -> None:
        """Wrapper for view_sheets_history command"""
        view_sheets_history(self.sheets_manager)

    def display_menu(self) -> None:
        """Display main menu"""
        console.clear()
        console.print("\n🔄 Chrome Profile Sheet Manager", style="bold blue")
        
        for key, (description, _) in self.menu_options.items():
            console.print(f"{key}. {description}")

    def run(self) -> int:
        """Run the CLI application"""
        try:
            while self._running:
                try:
                    self.display_menu()
                    choice = input("\nSelect an option: ").strip()
                    
                    if choice in self.menu_options:
                        _, handler = self.menu_options[choice]
                        handler()
                    else:
                        console.print("❌ Invalid choice", style="bold red")
                        
                except KeyboardInterrupt:
                    self.exit_cli()
                except Exception as e:
                    log.error(f"Command error: {e}")
                    console.print(f"\n❌ Error: {e}", style="bold red")
                    input("\nPress Enter to continue...")

            return 0
            
        except Exception as e:
            log.error(f"Fatal error: {e}")
            console.print(f"\n❌ Fatal Error: {e}", style="bold red")
            return 1

    def exit_cli(self) -> None:
        """Clean exit from CLI"""
        console.print("\n👋 Goodbye!", style="bold blue")
        self._running = False

def main() -> int:
    """CLI entry point"""
    try:
        cli = ChromeSheetsCLI()
        return cli.run()
    except KeyboardInterrupt:
        console.print("\n\n👋 Goodbye!", style="bold blue")
        return 0

if __name__ == "__main__":
    sys.exit(main())