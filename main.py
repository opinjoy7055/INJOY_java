import os
import sys
import time
import socket
import threading
import psutil
import subprocess
from flask import Flask, render_template_string, jsonify, request

# =====================================================================
# OP INJOY VIP SYSTEM - MINECRAFT ENGINE
# =====================================================================

app = Flask(__name__)

# State management for 4 concurrent OP INJOY deployments
bot_servers = {
    "1": {"status": "STOPPED", "target": "", "bots": "10", "edition": "3", "pid": None},
    "2": {"status": "STOPPED", "target": "", "bots": "10", "edition": "3", "pid": None},
    "3": {"status": "STOPPED", "target": "", "bots": "10", "edition": "3", "pid": None},
    "4": {"status": "STOPPED", "target": "", "bots": "10", "edition": "3", "pid": None}
}

def auto_restart_sequence():
    time.sleep(7200)
    print("\n[!] 2 Hours reached. OP INJOY System Auto-Restarting...")
    os.system("pkill -f node")
    os.execv(sys.executable, ['python3'] + sys.argv)

threading.Thread(target=auto_restart_sequence, daemon=True).start()

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

# =====================================================================
# FRONTEND UI (Matrix Rain + Minecraft V4 Configuration)
# =====================================================================
HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OP INJOY VIP SYSTEM</title>
    <style>
        body { margin: 0; padding: 0; background: #000; color: #0f0; font-family: 'Courier New', Courier, monospace; overflow-x: hidden; }
        canvas { display: block; position: fixed; top: 0; left: 0; z-index: 1; }
        #panel-container { position: relative; z-index: 2; width: 100%; max-width: 550px; margin: 40px auto; }
        .panel { border: 2px solid #0f0; background: rgba(0, 0, 0, 0.85); box-shadow: 0 0 20px rgba(0, 255, 0, 0.4); padding: 20px; }
        .header { text-align: center; border-bottom: 2px solid #0f0; padding-bottom: 10px; margin-bottom: 20px; }
        .header h2 { margin: 0; text-shadow: 0 0 10px #0f0; }
        .stats { display: flex; justify-content: space-between; font-weight: bold; font-size: 14px; margin-bottom: 20px; }
        .server-box { border: 1px dashed #0f0; padding: 15px; margin-bottom: 15px; }
        .server-header { display: flex; justify-content: space-between; margin-bottom: 10px; font-weight: bold; }
        .running { color: #0f0; text-shadow: 0 0 5px #0f0; }
        .stopped { color: #f00; text-shadow: 0 0 5px #f00; }
        .input-row { display: flex; gap: 10px; margin-bottom: 10px; }
        input, select { flex: 1; background: #111; border: 1px solid #0f0; color: #0f0; padding: 8px; box-sizing: border-box; font-family: monospace; }
        input:focus, select:focus { outline: none; box-shadow: 0 0 10px #0f0; }
        .full-width { width: 100%; margin-bottom: 10px; }
        .btn-group { display: flex; gap: 10px; margin-top: 10px; }
        button { flex: 1; padding: 8px; font-weight: bold; font-family: monospace; cursor: pointer; border: none; text-transform: uppercase; transition: 0.2s; }
        .btn-start { background: #0f0; color: #000; }
        .btn-start:hover { background: #fff; box-shadow: 0 0 10px #0f0; }
        .btn-stop { background: #f00; color: #fff; }
        .btn-stop:hover { background: #fff; color: #f00; box-shadow: 0 0 10px #f00; }
    </style>
</head>
<body>

<canvas id="matrix"></canvas>

<div id="panel-container">
    <div class="panel">
        <div class="header">
            <h2>OP INJOY VIP ENGINE</h2>
        </div>
        
        <div class="stats">
            <span id="cpu">CPU: --%</span>
            <span id="ram">RAM: --%</span>
            <span id="active">ACTIVE ENGINES: -</span>
        </div>

        <div id="servers">
            </div>
    </div>
</div>

<script>
    const canvas = document.getElementById('matrix');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$+-*/=%""\\'#&_(),.;:?!\\\\|{}<>[]^~';
    const fontSize = 14;
    const columns = canvas.width / fontSize;
    const drops = Array.from({length: columns}).fill(1);

    function drawMatrix() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#0F0';
        ctx.font = fontSize + 'px monospace';
        for (let i = 0; i < drops.length; i++) {
            const text = chars.charAt(Math.floor(Math.random() * chars.length));
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        }
    }
    setInterval(drawMatrix, 33);
    window.addEventListener('resize', () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight; });

    function renderServers(data) {
        let html = '';
        for (let i = 1; i <= 4; i++) {
            let srv = data[i.toString()];
            let statusClass = srv.status === 'RUNNING' ? 'running' : 'stopped';
            let icon = srv.status === 'RUNNING' ? '✔' : '✗';
            
            html += `
            <div class="server-box">
                <div class="server-header">
                    <span>OP INJOY SERVER #${i}</span>
                    <span class="${statusClass}">[ ${srv.status} ${icon} ]</span>
                </div>
                <input class="full-width" type="text" id="target_${i}" placeholder="IP:Port (e.g. play.example.com:19132)" value="${srv.target}">
                <div class="input-row">
                    <select id="edition_${i}">
                        <option value="1">Java Only</option>
                        <option value="2">Bedrock Only</option>
                        <option value="3" selected>Hybrid (Both)</option>
                    </select>
                    <input type="number" id="bots_${i}" placeholder="Total Bots" value="10">
                </div>
                <div class="input-row">
                    <select id="speed_${i}">
                        <option value="1">Normal Speed</option>
                        <option value="2">Anti-Bot Bypass (Sonar)</option>
                        <option value="3">Ultra Fast</option>
                    </select>
                    <select id="afk_${i}">
                        <option value="1">Walk Randomly</option>
                        <option value="2">Jump+Sneak</option>
                        <option value="4">Freeze</option>
                    </select>
                </div>
                <input class="full-width" type="text" id="spam_${i}" placeholder="Spam Message (Optional)" value="">
                <div class="btn-group">
                    <button class="btn-start" onclick="sendAction(${i}, 'start')">[ DEPLOY BOTS ]</button>
                    <button class="btn-stop" onclick="sendAction(${i}, 'stop')">[ KILL BOTS ]</button>
                </div>
            </div>`;
        }
        
        const focused = document.activeElement;
        const container = document.getElementById('servers');
        if (!container.contains(focused)) {
            container.innerHTML = html;
        }
        
        document.getElementById('cpu').innerText = `CPU: ${data.cpu}%`;
        document.getElementById('ram').innerText = `RAM: ${data.ram}%`;
        document.getElementById('active').innerText = `ACTIVE ENGINES: ${data.active}`;
    }

    function fetchStats() {
        fetch('/api/stats').then(res => res.json()).then(data => renderServers(data)).catch(err => console.log(err));
    }

    function sendAction(id, action) {
        const target = document.getElementById(`target_${id}`).value;
        const bots = document.getElementById(`bots_${id}`).value;
        const edition = document.getElementById(`edition_${id}`).value;
        const speed = document.getElementById(`speed_${id}`).value;
        const afk = document.getElementById(`afk_${id}`).value;
        const spam = document.getElementById(`spam_${id}`).value;
        
        fetch('/api/action', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                id: id, action: action, target: target, bots: bots, 
                edition: edition, speed: speed, afk: afk, spam: spam
            })
        }).then(() => fetchStats());
    }

    setInterval(fetchStats, 2000);
    fetchStats();
</script>
</body>
</html>
"""

# =====================================================================
# API ROUTES
# =====================================================================

@app.route('/')
def index():
    return render_template_string(HTML_UI)

@app.route('/api/stats')
def stats():
    cpu_usage = psutil.cpu_percent(interval=None)
    ram_usage = psutil.virtual_memory().percent
    active_count = sum(1 for s in bot_servers.values() if s['status'] == 'RUNNING')
    
    response = {"cpu": cpu_usage, "ram": ram_usage, "active": active_count}
    response.update(bot_servers)
    return jsonify(response)

@app.route('/api/action', methods=['POST'])
def action():
    data = request.json
    s_id = str(data.get('id'))
    act = data.get('action')
    
    if s_id in bot_servers:
        if act == 'start':
            if bot_servers[s_id]['status'] == 'RUNNING' and bot_servers[s_id]['pid']:
                try: os.kill(bot_servers[s_id]['pid'], 9)
                except: pass
                
            bot_servers[s_id]['status'] = 'RUNNING'
            bot_servers[s_id]['target'] = data.get('target', '')
            bot_servers[s_id]['bots'] = data.get('bots', '10')
            
            print(f"[+] Deploying OP INJOY #{s_id} -> {bot_servers[s_id]['target']} | Bots: {bot_servers[s_id]['bots']}")
            
            env_vars = os.environ.copy()
            env_vars['TARGET_IP'] = bot_servers[s_id]['target']
            env_vars['BOT_COUNT'] = str(bot_servers[s_id]['bots'])
            env_vars['EDITION'] = str(data.get('edition', '3'))
            env_vars['SPEED'] = str(data.get('speed', '1'))
            env_vars['AFK_MODE'] = str(data.get('afk', '1'))
            env_vars['SPAM_MSG'] = str(data.get('spam', ''))

            try:
                proc = subprocess.Popen(['node', 'index.js'], env=env_vars, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                bot_servers[s_id]['pid'] = proc.pid
            except Exception as e:
                print(f"[-] Failed to launch Node.js engine: {e}")
            
        elif act == 'stop':
            bot_servers[s_id]['status'] = 'STOPPED'
            pid = bot_servers[s_id].get('pid')
            if pid:
                print(f"[-] Killing OP INJOY #{s_id} (PID: {pid})")
                try: os.kill(pid, 9)
                except: pass
                bot_servers[s_id]['pid'] = None
            
    return jsonify({"success": True})

# =====================================================================
# START ENGINE
# =====================================================================
if __name__ == '__main__':
    os.system('clear' if os.name == 'posix' else 'cls')
    
    network_ip = get_local_ip()
    
    print("\033[96m\033[1m========================================\033[0m")
    print("\033[92m\033[1m  OP INJOY MINECRAFT WEB PANEL \033[0m")
    print("\033[96m\033[1m========================================\033[0m")
    print("\033[93m[*] LOCAL (Non-Root):  http://localhost:9000\033[0m")
    print("\033[93m[*] ROOT ACCESS:       http://injoy:9000\033[0m")
    print(f"\033[93m[*] LAN / WiFi ACCESS: http://{network_ip}:9000\033[0m\n")
    
    psutil.cpu_percent()
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    app.run(host='0.0.0.0', port=9000, threaded=True)
