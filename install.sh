#!/bin/bash
# ========================================================================
# 🔥 OP INJOY VIP ENGINE - Universal Web Panel Installer
# ========================================================================

CYAN='\033[1;36m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
NC='\033[0m'

echo -e "${CYAN}==================================================${NC}"
echo -e "${CYAN}        🔥 OP INJOY MINECRAFT WEB PANEL 🔥        ${NC}"
echo -e "${CYAN}==================================================${NC}"

TARGET_DIR="$HOME/OP_INJOY_PANEL"
REPO_URL="https://github.com/opinjoy7055/INJOY_java.git"

# 1. Smart DNS Injection (Root / Non-Root Auto-Detect)
echo -e "${YELLOW}[*] Configuring local domain routing...${NC}"
if [ -d "/data/data/com.termux" ]; then
    if command -v su &> /dev/null && su -c "exit" &> /dev/null; then
        su -c "mount -o rw,remount /system 2>/dev/null; grep -q 'injoy' /system/etc/hosts || echo '127.0.0.1 injoy' >> /system/etc/hosts" 2>/dev/null
        echo -e "${GREEN}[✔] Root detected. 'injoy' domain injected into Android hosts.${NC}"
    else
        echo -e "${YELLOW}[!] Non-root Android detected. OS security blocks custom domains.${NC}"
        echo -e "${YELLOW}[!] Defaulting to standard localhost routing.${NC}"
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v sudo &> /dev/null && sudo -n true 2>/dev/null; then
        grep -q 'injoy' /etc/hosts || echo '127.0.0.1 injoy' | sudo tee -a /etc/hosts > /dev/null
        echo -e "${GREEN}[✔] Sudo access detected. 'injoy' domain injected into Linux hosts.${NC}"
    else
        echo -e "${YELLOW}[!] Non-root Linux detected. Sudo required for custom domains.${NC}"
        echo -e "${YELLOW}[!] Defaulting to standard localhost routing.${NC}"
    fi
fi

# 2. Install Dependencies
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

# 3. Clone Repository
echo -e "${YELLOW}[*] Cloning OP INJOY Repository...${NC}"
rm -rf "$TARGET_DIR"
git clone "$REPO_URL" "$TARGET_DIR"

cd "$TARGET_DIR" || exit
echo -e "${YELLOW}[*] Installing Node.js Bot Modules...${NC}"
npm install mineflayer@latest bedrock-protocol@latest minecraft-data@latest --no-audit --no-fund

# 4. Create global shortcut
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
