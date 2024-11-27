# test_connection.py
from chrome_manager.core.sheets import SheetsManager
from chrome_manager.utils.system_info import SystemInfoCollector
from pathlib import Path

# Initialize components
sheets = SheetsManager(
    credentials_path=Path("chrome_manager/config/credentials/service_account.json"),
    spreadsheet_id="1xDJeKh11yj_E_eO7PCrAVGy7UJa-7d_5zBx94alVfa8"
)

system_info = SystemInfoCollector()

# Get system info
sys_info = system_info.get_sheet_data()

# Write test data
test_data = [{
    'name': 'Test Profile',
    'email': 'test@example.com',
    'is_local': False,
    'custom_name': 'Test User'
}]

# Update sheet
success = sheets.update_profiles(test_data, sys_info)
print(f"Update successful: {success}")