#!/bin/bash
# ========================================================================
# 🔥 OP INJOY VIP ENGINE - Universal Installer
# ========================================================================

# Colors
CYAN='\033[1;36m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
NC='\033[0m'

echo -e "${CYAN}==================================================${NC}"
echo -e "${CYAN}             🔥 OP INJOY VIP ENGINE 🔥            ${NC}"
echo -e "${CYAN}==================================================${NC}"
echo -e "${YELLOW}[*] System check initialized...${NC}"

# Define paths
TARGET_DIR="$HOME/OP_INJOY_ENGINE"
# NOTE: Maker, change this URL to point to where you upload your engine code
REPO_URL="https://raw.githubusercontent.com/opinjoy7055/OPINJOY_/main/index.js"

# Detect OS
if [ -d "/data/data/com.termux" ]; then
    echo -e "${GREEN}[✔] Termux (Android) Detected!${NC}"
    
    # Request storage permission if not granted
    if [ ! -d "$HOME/storage" ]; then
        termux-setup-storage
    fi

    echo -e "${YELLOW}[*] Updating Termux packages...${NC}"
    pkg update -y && pkg upgrade -y
    pkg install nodejs git -y
    
    BIN_PATH="/data/data/com.termux/files/usr/bin/op-injoy"

elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo -e "${GREEN}[✔] Linux Detected!${NC}"
    echo -e "${YELLOW}[*] Updating Linux packages...${NC}"
    sudo apt-get update -y
    sudo apt-get install -y curl nodejs npm git
    
    BIN_PATH="/usr/local/bin/op-injoy"
else
    echo -e "${RED}[✗] Unsupported OS. Use Windows script instead.${NC}"
    exit 1
fi

# Create Directory & Install
mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR" || exit

echo -e "${YELLOW}[*] Initializing Engine & Dependencies...${NC}"
npm init -y > /dev/null
npm install mineflayer@latest bedrock-protocol@latest minecraft-data@latest --no-audit --no-fund

echo -e "${YELLOW}[*] Downloading Core Engine...${NC}"
curl -fsSL "$REPO_URL" -o index.js

# Create global command shortcut
echo -e "${YELLOW}[*] Creating global shortcut...${NC}"
cat << EOF > "$BIN_PATH"
#!/bin/bash
cd "$TARGET_DIR" && node index.js
EOF
chmod +x "$BIN_PATH"

echo -e "${GREEN}==================================================${NC}"
echo -e "${GREEN}[✔] INSTALLATION COMPLETE!${NC}"
echo -e "${CYAN}[*] To launch the engine, just type: ${GREEN}op-injoy${NC}"
echo -e "${GREEN}==================================================${NC}"
