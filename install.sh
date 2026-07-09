#!/bin/bash
CYAN='\033[1;36m'; GREEN='\033[1;32m'; YELLOW='\033[1;33m'; RED='\033[1;31m'; NC='\033[0m'
echo -e "${CYAN}==================================================${NC}"
echo -e "${CYAN}        🔥 OP INJOY MINECRAFT WEB PANEL 🔥        ${NC}"
echo -e "${CYAN}==================================================${NC}"

TARGET_DIR="$HOME/OP_INJOY_PANEL"
REPO_URL="https://github.com/opinjoy7055/INJOY_java.git"

# 1. Install Dependencies
if [ -d "/data/data/com.termux" ]; then
    echo -e "${YELLOW}[*] Installing Termux Dependencies...${NC}"
    pkg update -y && pkg upgrade -y
    # Added cmake, clang, make for native module compilation
    pkg install python nodejs git cmake clang make -y
    pip install flask psutil
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo -e "${YELLOW}[*] Installing Linux Dependencies...${NC}"
    sudo apt-get update -y
    sudo apt-get install -y python3 python3-pip nodejs npm git cmake clang make
    pip3 install flask psutil
fi

# 2. Clone Repository
echo -e "${YELLOW}[*] Cloning OP INJOY Repository...${NC}"
rm -rf "$TARGET_DIR"
git clone "$REPO_URL" "$TARGET_DIR"
cd "$TARGET_DIR" || exit

# 3. Install Node.js Bot Modules
echo -e "${YELLOW}[*] Installing Node.js Bot Modules...${NC}"
npm install mineflayer@latest bedrock-protocol@latest minecraft-data@latest --no-audit --no-fund

# 4. Create launch command
BIN_PATH="/data/data/com.termux/files/usr/bin/op-injoy"
[ ! -d "/data/data/com.termux" ] && BIN_PATH="/usr/local/bin/op-injoy"

cat << EOF > "$BIN_PATH"
#!/bin/bash
cd "$TARGET_DIR" && python3 main.py
EOF
chmod +x "$BIN_PATH"

echo -e "${GREEN}[✔] INSTALLATION COMPLETE! Type 'op-injoy' to start.${NC}"
