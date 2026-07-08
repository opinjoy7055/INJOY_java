const colors = {
    reset: "\x1b[0m", bold: "\x1b[1m", red: "\x1b[31m",
    green: "\x1b[32m", yellow: "\x1b[33m", blue: "\x1b[34m",
    magenta: "\x1b[35m", cyan: "\x1b[36m"
};

module.exports = {
    banner: () => {
        console.log(`${colors.cyan}${colors.bold}==================================================`);
        console.log(`             🔥 OP INJOY VIP ENGINE 🔥            `);
        console.log(`==================================================${colors.reset}`);
    },
    info: (msg) => console.log(`${colors.blue}[*] ${msg}${colors.reset}`),
    success: (msg) => console.log(`${colors.green}[✔] ${msg}${colors.reset}`),
    warn: (msg) => console.log(`${colors.yellow}[!] ${msg}${colors.reset}`),
    error: (msg) => console.log(`${colors.red}[✗] ${msg}${colors.reset}`),
    chat: (msg) => console.log(`${colors.magenta}[CHAT] ${msg}${colors.reset}`)
};
