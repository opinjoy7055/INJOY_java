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
    pkg install python nodejs git cmake clang make -y
    pip install flask psutil
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo -e "${YELLOW}[*] Installing Linux Dependencies...${NC}"
    sudo apt-get update -y
    sudo apt-get install -y python3 python3-pip nodejs npm git cmake clang make
    pip3 install flask psutil
fi

# 2. Smart Git Update (DO NOT DELETE FOLDER)
echo -e "${YELLOW}[*] Updating OP INJOY Repository...${NC}"
if [ -d "$TARGET_DIR/.git" ]; then
    cd "$TARGET_DIR" || exit
    git pull origin main
else
    git clone "$REPO_URL" "$TARGET_DIR"
    cd "$TARGET_DIR" || exit
fi

# 3. Fast NPM Install (Multi-core & Cached)
echo -e "${YELLOW}[*] Installing Node.js Bot Modules...${NC}"
# This tells the C++ compiler to use all available CPU cores to build faster
export JOBS=max
export npm_config_jobs=max

npm install mineflayer@latest bedrock-protocol@latest minecraft-data@latest --no-audit --no-fund --prefer-offline --loglevel error

# 4. Create launch command
BIN_PATH="/data/data/com.termux/files/usr/bin/op-injoy"
[ ! -d "/data/data/com.termux" ] && BIN_PATH="/usr/local/bin/op-injoy"

cat << EOF > "$BIN_PATH"
#!/bin/bash
cd "$TARGET_DIR" && python3 main.py
EOF
chmod +x "$BIN_PATH"

echo -e "${GREEN}[✔] INSTALLATION COMPLETE! Type 'op-injoy' to start.${NC}"
