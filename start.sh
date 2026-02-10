#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════╗"
echo "║  Telegram Unzip Bot - Startup Script         ║"
echo "║  Made with ❤️ by Zerodev                      ║"
echo "╚═══════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${RED}❌ Error: .env file not found!${NC}"
    echo -e "${YELLOW}Please create .env file from .env.example${NC}"
    echo ""
    echo "Run: cp .env.example .env"
    echo "Then edit .env with your configuration"
    exit 1
fi

# Check if SESSION_STRING is set
if ! grep -q "SESSION_STRING=" .env || grep -q "SESSION_STRING=$" .env || grep -q "SESSION_STRING=your_session_string_here" .env; then
    echo -e "${YELLOW}⚠️  Warning: SESSION_STRING not configured!${NC}"
    echo ""
    echo "Large file uploads (>50MB) will not work without SESSION_STRING"
    echo ""
    read -p "Do you want to generate SESSION_STRING now? (y/n): " choice
    if [ "$choice" == "y" ] || [ "$choice" == "Y" ]; then
        echo -e "${BLUE}Starting session generator...${NC}"
        python3 generate_session.py
        echo ""
        echo -e "${GREEN}✅ Session generated! Please add it to .env file${NC}"
        exit 0
    fi
fi

echo -e "${BLUE}Starting bot...${NC}"
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "Python version: ${GREEN}$python_version${NC}"

# Check if requirements are installed
if ! python3 -c "import pyrogram" 2>/dev/null; then
    echo -e "${YELLOW}📦 Installing dependencies...${NC}"
    pip3 install -r requirements.txt
fi

# Create downloads directory
mkdir -p downloads

echo ""
echo -e "${GREEN}✅ All checks passed!${NC}"
echo -e "${BLUE}🚀 Starting Telegram Unzip Bot...${NC}"
echo ""

# Run the bot
python3 bot.py
