"""
cli/config/settings.py
⚙️ Configuration settings and constants
"""

import os
from pathlib import Path

# Application Information
APP_NAME = "Chrome Profile Sheet Manager"
APP_VERSION = "0.1.0"
APP_AUTHOR = "Your Name"

# Logging Configuration
LOG_LEVEL = os.getenv('CHROME_MANAGER_LOG_LEVEL', 'INFO')
LOG_FORMAT = "%(message)s"
LOG_DATE_FORMAT = "[%X]"

# Paths Configuration
BASE_DIR = Path(__file__).parent.parent
CREDENTIALS_DIR = BASE_DIR / 'config' / 'credentials'
DEFAULT_CREDENTIALS_PATH = CREDENTIALS_DIR / 'service_account.json'

# Google Sheets Configuration
CREDENTIALS_PATH = Path(os.getenv(
    'CHROME_MANAGER_CREDENTIALS',
    str(DEFAULT_CREDENTIALS_PATH)
))
SPREADSHEET_ID = os.getenv('CHROME_MANAGER_SPREADSHEET_ID', '')

# Chrome Configuration
CHROME_CONFIG_PATH = Path.home() / '.config' / 'google-chrome'

# Sheet Management Configuration
DEFAULT_RETENTION_DAYS = int(os.getenv('CHROME_MANAGER_RETENTION_DAYS', '30'))
WORKSHEET_NAME = "Chrome Profiles"
MAX_ROWS = 1000

# Error Messages
ERROR_MESSAGES = {
    'no_chrome': "❌ Chrome configuration not found",
    'no_credentials': "❌ Service account credentials not found",
    'no_spreadsheet': "❌ Spreadsheet ID not configured",
    'invalid_days': "❌ Invalid number of days specified",
    'auth_failed': "❌ Google Sheets authentication failed",
    'sheet_update_failed': "❌ Failed to update sheet",
}

# Success Messages
SUCCESS_MESSAGES = {
    'profiles_updated': "✅ Successfully updated profiles",
    'entries_cleaned': "✅ Successfully cleaned old entries",
    'sheet_created': "✅ Created new tracking sheet",
}

# Ensure required directories exist
CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)

# Validation
def validate_config() -> bool:
    """Validate critical configuration"""
    if not SPREADSHEET_ID:
        print(ERROR_MESSAGES['no_spreadsheet'])
        return False
        
    if not CREDENTIALS_PATH.exists():
        print(ERROR_MESSAGES['no_credentials'])
        return False
        
    if not CHROME_CONFIG_PATH.exists():
        print(ERROR_MESSAGES['no_chrome'])
        return False
        
    return True

# Environment setup
def get_env_settings() -> dict:
    """Get all environment-specific settings"""
    return {
        'log_level': LOG_LEVEL,
        'credentials_path': str(CREDENTIALS_PATH),
        'spreadsheet_id': SPREADSHEET_ID,
        'retention_days': DEFAULT_RETENTION_DAYS
    }