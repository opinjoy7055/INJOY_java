#!/bin/bash
# ========================================================================
# 🔥 OP INJOY VIP ENGINE - Universal Web Panel Installer
# ========================================================================

CYAN='\033[1;36m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}==================================================${NC}"
echo -e "${CYAN}        🔥 OP INJOY MINECRAFT WEB PANEL 🔥        ${NC}"
echo -e "${CYAN}==================================================${NC}"

TARGET_DIR="$HOME/OP_INJOY_PANEL"
# MAKE SURE THIS MATCHES YOUR GITHUB USERNAME
REPO_URL="https://github.com/opinjoy7055/INJOY_java.git"

if [ -d "/data/data/com.termux" ]; then
    echo -e "${YELLOW}[*] Installing Termux Dependencies...${NC}"
    pkg update -y && pkg upgrade -y
    pkg install python nodejs git -y
    pip install flask psutil
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo -e "${YELLOW}[*] Installing Linux Dependencies...${NC}"
    sudo apt-get update -y
    sudo apt-get install -y python3 python3-pip nodejs npm git
    pip3 install flask psutil
fi

echo -e "${YELLOW}[*] Cloning OP INJOY Repository...${NC}"
rm -rf "$TARGET_DIR"
git clone "$REPO_URL" "$TARGET_DIR"

cd "$TARGET_DIR" || exit
echo -e "${YELLOW}[*] Installing Node.js Bot Modules...${NC}"
npm install mineflayer@latest bedrock-protocol@latest minecraft-data@latest --no-audit --no-fund

# Create global shortcut
echo -e "${YELLOW}[*] Creating launch command...${NC}"
if [ -d "/data/data/com.termux" ]; then
    BIN_PATH="/data/data/com.termux/files/usr/bin/op-injoy"
else
    BIN_PATH="/usr/local/bin/op-injoy"
fi

cat << EOF > "$BIN_PATH"
#!/bin/bash
cd "$TARGET_DIR" && python3 main.py
EOF
chmod +x "$BIN_PATH"

echo -e "${GREEN}==================================================${NC}"
echo -e "${GREEN}[✔] INSTALLATION COMPLETE!${NC}"
echo -e "${CYAN}[*] To start the Web Panel, type: ${GREEN}op-injoy${NC}"
echo -e "${GREEN}==================================================${NC}"
