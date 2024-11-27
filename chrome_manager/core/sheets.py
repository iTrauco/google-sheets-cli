"""
chrome_manager/core/sheets.py
📊 Google Sheets integration with connection logging
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials
from rich.console import Console

console = Console()
log = logging.getLogger("sheets")

class SheetsManager:
    """📝 Google Sheets management for Chrome profile tracking"""
    
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    SHEET_CONFIG = {
        'name': 'Chrome Profiles',
        'headers': [
            'Timestamp',
            'Hostname',
            'OS Info',
            'IP Address',
            'Memory Total',
            'Memory Available',
            'Profile Name',
            'Profile Email',
            'Profile Type',
            'Custom Name',
            'Last Used',
            'Username'
        ]
    }
    
    def __init__(self, credentials_path: Path, spreadsheet_id: str):
        """Initialize sheets manager"""
        self.credentials_path = credentials_path
        self.spreadsheet_id = spreadsheet_id
        
        # Add debug logging
        log.debug(f"Initializing SheetsManager with:")
        log.debug(f"Credentials path: {self.credentials_path}")
        log.debug(f"Spreadsheet ID: {self.spreadsheet_id}")
        
        self.client = self._initialize_client()
        self.spreadsheet = self._get_spreadsheet()
        self._ensure_sheet_exists()

    def _initialize_client(self) -> gspread.Client:
        """Initialize Google Sheets client"""
        try:
            log.debug("Attempting to initialize Google Sheets client...")
            credentials = Credentials.from_service_account_file(
                self.credentials_path,
                scopes=self.SCOPES
            )
            client = gspread.authorize(credentials)
            log.debug("Successfully initialized Google Sheets client")
            return client
        except Exception as e:
            log.error(f"Failed to initialize sheets client: {e}")
            raise

    def _get_spreadsheet(self) -> gspread.Spreadsheet:
        """Get the target spreadsheet"""
        try:
            log.debug(f"Attempting to open spreadsheet with ID: {self.spreadsheet_id}")
            spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            log.debug("Successfully opened spreadsheet")
            return spreadsheet
        except Exception as e:
            log.error(f"Error accessing spreadsheet: {e}")
            raise

    def _ensure_sheet_exists(self) -> None:
        """Ensure the worksheet exists with correct headers"""
        try:
            try:
                worksheet = self.spreadsheet.worksheet(self.SHEET_CONFIG['name'])
                headers = worksheet.row_values(1)
                if headers != self.SHEET_CONFIG['headers']:
                    log.debug("Updating sheet headers...")
                    worksheet.clear()
                    worksheet.append_row(self.SHEET_CONFIG['headers'])
                    log.debug("Updated sheet headers")
            except gspread.WorksheetNotFound:
                log.debug("Creating new worksheet...")
                worksheet = self.spreadsheet.add_worksheet(
                    self.SHEET_CONFIG['name'],
                    1000,
                    len(self.SHEET_CONFIG['headers'])
                )
                worksheet.append_row(self.SHEET_CONFIG['headers'])
                log.debug("Created new worksheet")
                
        except Exception as e:
            log.error(f"Error setting up worksheet: {e}")
            raise

    def update_profiles(self, profiles: List[Dict], system_info: Dict) -> bool:
        """Update sheet with profile and system information"""
        try:
            worksheet = self.spreadsheet.worksheet(self.SHEET_CONFIG['name'])
            timestamp = datetime.now().isoformat()
            
            log.debug("Preparing profile data for sheet update...")
            # Prepare rows with combined information
            rows = []
            for profile in profiles:
                row = [
                    timestamp,
                    system_info.get('hostname', ''),
                    system_info.get('os_info', ''),
                    system_info.get('ip_address', ''),
                    system_info.get('memory_total', ''),
                    system_info.get('memory_available', ''),
                    profile.get('name', ''),
                    profile.get('email', ''),
                    'Local' if profile.get('is_local', True) else 'Signed-in',
                    profile.get('custom_name', ''),
                    profile.get('last_used', ''),
                    system_info.get('username', '')
                ]
                rows.append(row)
            
            if rows:
                log.debug(f"Attempting to update sheet with {len(rows)} rows...")
                worksheet.append_rows(
                    rows,
                    value_input_option='USER_ENTERED',
                    insert_data_option='INSERT_ROWS'
                )
                log.info(f"Successfully updated {len(rows)} profile entries")
                return True
            
            log.warning("No rows to update")
            return False
            
        except Exception as e:
            log.error(f"Error updating sheet: {e}")
            return False

    def get_last_sync_time(self) -> Optional[str]:
        """Get the timestamp of last sync"""
        try:
            worksheet = self.spreadsheet.worksheet(self.SHEET_CONFIG['name'])
            values = worksheet.get_all_values()
            
            if len(values) > 1:
                return values[-1][0]
            return None
            
        except Exception as e:
            log.error(f"Error getting last sync time: {e}")
            return None