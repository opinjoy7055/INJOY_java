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

# 2. Smart Git Update
echo -e "${YELLOW}[*] Updating OP INJOY Repository...${NC}"
if [ -d "$TARGET_DIR/.git" ]; then
    cd "$TARGET_DIR" || exit
    git pull origin main
else
    git clone "$REPO_URL" "$TARGET_DIR"
    cd "$TARGET_DIR" || exit
fi

# 3. High-Speed Live Compilation Build Phase
echo -e "${YELLOW}[*] Installing Bot Modules...${NC}"
export JOBS=max
export npm_config_jobs=max

# Step A: Download but DO NOT compile yet
npm install mineflayer@latest bedrock-protocol@latest minecraft-data@latest --no-audit --no-fund --ignore-scripts

# Step B: Patch the Clang -1 bug in node-addon-api
echo -e "${YELLOW}[*] Patching Clang Compiler Bug...${NC}"
find node_modules -name "napi.h" -exec sed -i 's/static_cast<napi_typedarray_type>(-1)/static_cast<napi_typedarray_type>(0)/g' {} +

# Step C: Now compile the patched code
echo -e "${YELLOW}[*] Compiling C++ Modules...${NC}"
npm rebuild --foreground-scripts

# 4. Create launch command shortcut
BIN_PATH="/data/data/com.termux/files/usr/bin/op-injoy"
[ ! -d "/data/data/com.termux" ] && BIN_PATH="/usr/local/bin/op-injoy"

cat << EOF > "$BIN_PATH"
#!/bin/bash
cd "$TARGET_DIR" && python3 main.py
EOF
chmod +x "$BIN_PATH"

echo -e "${GREEN}==================================================${NC}"
echo -e "${GREEN}[✔] INSTALLATION COMPLETE!${NC}"
echo -e "${CYAN}[*] To start the Web Panel, type: ${GREEN}op-injoy${NC}"
echo -e "${GREEN}==================================================${NC}"
