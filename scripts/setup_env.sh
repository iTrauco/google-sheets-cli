#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔧 Setting up Chrome Profile Manager environment...${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${BLUE}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo -e "${BLUE}📥 Installing dependencies...${NC}"
pip install -e .

# Run environment setup
echo -e "${BLUE}⚙️ Configuring environment...${NC}"
python -c "from chrome_manager.config.env_manager import setup_environment; setup_environment()"

# Add environment sourcing to shell config if not already present
SHELL_RC="$HOME/.$(basename $SHELL)rc"
ENV_SOURCE="source $(pwd)/.env"

if ! grep -q "$ENV_SOURCE" "$SHELL_RC"; then
    echo -e "${BLUE}📝 Adding environment to shell configuration...${NC}"
    echo -e "\n# Chrome Profile Manager Environment" >> "$SHELL_RC"
    echo "$ENV_SOURCE" >> "$SHELL_RC"
fi

echo -e "${GREEN}✅ Setup complete!${NC}"
echo -e "${BLUE}🔄 Please run: source $SHELL_RC${NC}"