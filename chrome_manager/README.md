# 🚀 Chrome Profile Sheet Manager

[![GitHub license](https://img.shields.io/github/license/iTrauco/google-sheets-cli)](https://github.com/iTrauco/chrome-sheets-manager/blob/main/LICENSE)
![GitHub stars](https://img.shields.io/github/stars/iTrauco/google-sheets-cli?style=social)
[![Generic badge](https://img.shields.io/badge/Zsh-Required-purple.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Debian-24.04-blue.svg)](https://shields.io/)

> 🔄 Seamlessly sync your Chrome profile configurations and Zsh magic across all your Linux systems using Google Sheets as your single source of truth!

## 🎯 Why This Exists?

Ever found yourself setting up a new Linux system and thinking "ugh, not all these Chrome profiles and Zsh aliases again"? Same! That's why I built this tool to:

- 🏃‍♂️ Speed up system setup with synchronized Chrome profiles
- 🔧 Auto-generate Zsh aliases for lighting-fast browser workflows
- 📋 Keep all your `.zshrc` hacks and shortcuts in sync
- 🎮 Stop clicking through Chrome's GUI like it's 1999
- 🌐 Launch specific sites with the right profile via CLI
- ⚡ Bind everything to keyboard shortcuts for maximum velocity

## ✨ Features

- **🔍 Smart Profile Scanning**: Auto-detects all Chrome profiles on your system
- **📊 Google Sheets Integration**: Your configuration sanctuary in the cloud
- **💾 Local Caching**: Review changes before they hit your system
- **🚄 Zsh Optimization**: Generate powerful aliases for rapid profile switching
- **🔄 Cross-System Sync**: Keep all your machines in perfect harmony

## 🏃‍♂️ Quick Start

```bash
# Only works reliably with Zsh! Other shells may have syntax issues
# Install using pip
pip install chrome-sheets-manager

# First-time setup (requires Google Sheets credentials)
chrome-manager setup

# Scan profiles and generate Zsh magic
chrome-manager sync
```

## ⚙️ Configuration 

```bash
# 1. Place your Google Sheets creds here:
chrome_manager/config/credentials/service_account.json

# 2. Set your spreadsheet ID in .env:
CHROME_MANAGER_SPREADSHEET_ID=your_spreadsheet_id

# 3. Source your new configs:
source ~/.zshrc
```

## 🎮 Example Zsh Magic Generated

```bash
# 🏢 Work Environment
alias work-mail='chrome --profile-directory="Profile 1" https://workspace.google.com'
alias work-cal='chrome --profile-directory="Profile 1" https://calendar.google.com'

# 👩‍💻 Development Flow
alias dev-github='chrome --profile-directory="Profile 2" https://github.com'
alias dev-local='chrome --profile-directory="Profile 2" http://localhost:3000'

# 🏭 Client Projects
alias client1-admin='chrome --profile-directory="Profile 3" https://client1.admin.com'
alias client1-staging='chrome --profile-directory="Profile 3" https://staging.client1.com'
```

## ⚠️ Important Notes

- **🐚 Shell Support**: Primarily designed for Zsh! While it may work with bash/fish, expect some syntax weirdness
- **📂 Profile Location**: Expects Chrome profiles in `~/.config/google-chrome/`
- **🔄 Shell Reload**: Run `source ~/.zshrc` after sync to get your fresh aliases
- **🏗️ URL Handling**: Supports complex URLs with query params and special characters

## 🚧 Coming Soon

- 📦 Profile backup/restore functionality
- 🎨 Custom theme/extension sync
- 🤖 Automated workflow script generation
- 🔑 Password manager integration
- 🎪 Multiple sheet workspace support

## 👥 Contact & Support

🧑‍💻 **Chris Trauco** - Senior Data Engineer @ [OGx Consulting](https://weareogx.com)

Feel free to reach out:
- 🐙 GitHub: [@iTrauco](https://github.com/iTrauco)
- 🐦 Twitter: [@iTrauco](https://twitter.com/iTrauco)
- 📧 Email: dev@trau.co

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---
Made with 🍵 and ❤️ by [Chris Trauco](https://github.com/iTrauco)