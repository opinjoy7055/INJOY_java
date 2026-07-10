import os
import sys
import time
import json
import socket
import threading
import psutil
import subprocess
import urllib.request
from flask import Flask, render_template_string, jsonify, request

# =====================================================================
# OP INJOY VIP BOT - V4 ULTIMATE EDITION (NGROK SMART BOOT)
# =====================================================================

app = Flask(__name__)

bot_servers = {
    "1": {"status": "STOPPED", "target": "", "bots": "10", "edition": "3", "pid": None}
}

NGROK_TOKEN = "3GJ5D4g5OuBxCgqu0LbGo40mjn3_49YVQFhdVTy36jHdmugN8"

def auto_restart_sequence():
    time.sleep(7200)
    print("\n[!] 2 Hours reached. OP INJOY System Auto-Restarting...")
    os.system("pkill -9 node; pkill -9 ngrok")
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

def start_ngrok_background():
    try:
        # Check absolute path for Termux
        ngrok_cmd = "/data/data/com.termux/files/usr/bin/ngrok"
        if not os.path.exists(ngrok_cmd):
            ngrok_cmd = "ngrok" # Fallback for PC/Linux
            
        # Authenticate and kill any old sessions
        os.system(f"{ngrok_cmd} config add-authtoken {NGROK_TOKEN} > /dev/null 2>&1")
        os.system("pkill -9 ngrok > /dev/null 2>&1")
        
        # Start tunnel silently
        subprocess.Popen([ngrok_cmd, 'http', '9000'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Smart Wait Loop (Waits up to 10 seconds for the tunnel to go live)
        for _ in range(10):
            time.sleep(1)
            try:
                req = urllib.request.Request("http://127.0.0.1:4040/api/tunnels")
                with urllib.request.urlopen(req, timeout=2) as response:
                    data = json.loads(response.read().decode())
                    if data.get('tunnels'):
                        public_url = data['tunnels'][0]['public_url']
                        print(f"\033[92m\033[1m[*] GLOBAL ACCESS (Ngrok): {public_url}\033[0m\n")
                        return
            except Exception:
                continue
                
        print("\033[93m[*] Ngrok API timeout. Connection is too slow right now.\033[0m\n")
    except Exception as e:
        print(f"\033[93m[*] Ngrok failed to start: {e}\033[0m\n")

# =====================================================================
# FRONTEND UI
# =====================================================================
HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>OP INJOY VIP BOT</title>
    <style>
        :root {
            --bg-main: #0B0F19; --bg-panel: #111827; --bg-input: #1F2937;
            --border-color: #374151; --text-main: #F3F4F6; --text-muted: #9CA3AF;
            --brand-primary: #3B82F6; --success: #10B981; --danger: #EF4444;
        }
        body { margin: 0; padding: 0; background-color: var(--bg-main); color: var(--text-main); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        #panel-container { width: 94%; max-width: 650px; margin: 40px auto; padding-bottom: 40px; box-sizing: border-box; }
        .panel { background: var(--bg-panel); border: 1px solid var(--border-color); border-radius: 12px; padding: 24px; position: relative; overflow: hidden; }
        .panel::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, var(--brand-primary), #8B5CF6); }
        .header { text-align: center; margin-bottom: 24px; padding-bottom: 20px; border-bottom: 1px solid var(--border-color); }
        .header h2 { margin: 0; color: #fff; font-weight: 700; font-size: 24px; }
        .header p { margin: 5px 0 0 0; color: var(--text-muted); font-size: 13px; font-weight: 500; text-transform: uppercase; }
        .stats { display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; background: var(--bg-main); padding: 14px; border-radius: 8px; margin-bottom: 24px; font-weight: 600; font-size: 13px; color: var(--text-muted); border: 1px solid var(--border-color); }
        .stats span { color: #fff; font-weight: 700; }
        .server-box { background: var(--bg-main); border: 1px solid var(--border-color); border-radius: 8px; padding: 20px; margin-bottom: 16px; width: 100%; box-sizing: border-box; transition: 0.2s; }
        .server-box:hover { border-color: #4B5563; }
        .server-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; font-weight: 700; font-size: 14px; color: #fff; }
        .running { color: var(--success); background: rgba(16, 185, 129, 0.1); padding: 4px 8px; border-radius: 4px; font-size: 12px; }
        .stopped { color: var(--danger); background: rgba(239, 68, 68, 0.1); padding: 4px 8px; border-radius: 4px; font-size: 12px; }
        .input-row { display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 12px; width: 100%; }
        input, select { flex: 1 1 40%; background: var(--bg-input); border: 1px solid var(--border-color); color: var(--text-main); padding: 12px 14px; border-radius: 6px; box-sizing: border-box; font-family: inherit; font-size: 14px; outline: none; transition: 0.2s; }
        input:focus, select:focus { border-color: var(--brand-primary); box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2); }
        input::placeholder { color: #6B7280; }
        .full-width { width: 100%; flex: 1 1 100%; margin-bottom: 12px; }
        .btn-group { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 20px; width: 100%; }
        button { flex: 1 1 45%; padding: 12px; font-weight: 600; cursor: pointer; border: none; border-radius: 6px; font-size: 13px; transition: 0.2s; text-transform: uppercase; }
        .btn-start { background: var(--success); color: #fff; }
        .btn-start:hover { background: #059669; }
        .btn-stop { background: transparent; color: var(--danger); border: 1px solid var(--danger); }
        .btn-stop:hover { background: var(--danger); color: #fff; }
        .slot-controls { display: flex; justify-content: center; gap: 24px; margin-top: 32px; }
        .circle-btn { width: 48px; height: 48px; border-radius: 50%; border: none; background: var(--brand-primary); color: #fff; font-size: 24px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: 0.2s; }
        .circle-btn:hover { background: #2563EB; transform: translateY(-2px); }
        .circle-btn.minus { background: var(--bg-input); color: var(--text-muted); border: 1px solid var(--border-color); }
        .circle-btn.minus:hover { background: var(--danger); color: #fff; border-color: var(--danger); }
    </style>
</head>
<body>

<div id="panel-container">
    <div class="panel">
        <div class="header">
            <h2>OP INJOY VIP BOT</h2>
            <p>V4 Ultimate Dashboard</p>
        </div>
        
        <div class="stats">
            <span id="cpu">CPU: --</span>
            <span id="ram">RAM: --</span>
            <span id="slots">TOTAL SLOTS: -</span>
            <span id="active">RUNNING: -</span>
        </div>

        <div id="servers"></div>

        <div class="slot-controls">
            <button class="circle-btn" onclick="adjustSlots('add')" title="Add New Slot">+</button>
            <button class="circle-btn minus" id="btn-remove" onclick="adjustSlots('remove')" style="display: none;" title="Remove Last Slot">-</button>
        </div>
    </div>
</div>

<script>
    function renderServers(data) {
        let html = '';
        let keys = Object.keys(data).filter(k => !['cpu', 'ram', 'active', 'total_slots'].includes(k)).sort((a, b) => parseInt(a) - parseInt(b));
        
        keys.forEach(i => {
            let srv = data[i];
            let statusClass = srv.status === 'RUNNING' ? 'running' : 'stopped';
            
            html += `
            <div class="server-box">
                <div class="server-header">
                    <span>MINECRAFT SERVER #${i}</span>
                    <span class="${statusClass}">${srv.status}</span>
                </div>
                
                <input class="full-width" type="text" id="target_${i}" placeholder="IP:Port (e.g. play.example.com:19132)" value="${srv.target}">
                
                <div class="input-row">
                    <select id="edition_${i}">
                        <option value="1" ${srv.edition === '1' ? 'selected' : ''}>Java (Auto 1.21.4)</option>
                        <option value="2" ${srv.edition === '2' ? 'selected' : ''}>Bedrock (Auto 1.26.30)</option>
                        <option value="3" ${srv.edition === '3' || !srv.edition ? 'selected' : ''}>Hybrid (Auto-Detect)</option>
                    </select>
                    <input type="number" id="bots_${i}" placeholder="Bot Count" value="${srv.bots}">
                </div>
                
                <div class="input-row">
                    <input type="text" id="botname_${i}" placeholder="Custom Bot Name (Blank = AI Gen)">
                    <input type="text" id="pass_${i}" placeholder="Auth Pass (Blank = AI Gen)">
                </div>

                <input class="full-width" type="text" id="follow_${i}" placeholder="Target Player (Required for Follow Mode)">

                <div class="input-row">
                    <select id="speed_${i}">
                        <option value="1">Normal Connect</option>
                        <option value="3">Ultra Fast Connect</option>
                    </select>
                    <select id="afk_${i}">
                        <option value="1">AFK: Walk Randomly</option>
                        <option value="2">AFK: Jump & Sneak</option>
                        <option value="3">AFK: Follow Target Player</option>
                        <option value="4">AFK: Freeze</option>
                    </select>
                </div>
                
                <input class="full-width" type="text" id="spam_${i}" placeholder="Automated Chat / Spam Message (Optional)" value="">
                
                <div class="btn-group">
                    <button class="btn-start" onclick="sendAction(${i}, 'start')">Deploy Bots</button>
                    <button class="btn-stop" onclick="sendAction(${i}, 'stop')">Stop Engine</button>
                </div>
            </div>`;
        });
        
        const focused = document.activeElement;
        const container = document.getElementById('servers');
        if (!container.contains(focused)) {
            container.innerHTML = html;
        }
        
        document.getElementById('cpu').innerText = `CPU: ${data.cpu}`;
        document.getElementById('ram').innerText = `RAM: ${data.ram}`;
        document.getElementById('slots').innerText = `TOTAL SLOTS: ${data.total_slots}`;
        document.getElementById('active').innerText = `RUNNING: ${data.active}`;

        const minusBtn = document.getElementById('btn-remove');
        if (keys.length > 1) {
            minusBtn.style.display = 'flex';
        } else {
            minusBtn.style.display = 'none';
        }
    }

    function fetchStats() { 
        fetch('/api/stats')
            .then(res => res.json())
            .then(data => renderServers(data))
            .catch(err => console.log(err)); 
    }

    function sendAction(id, action) {
        fetch('/api/action', {
            method: 'POST', 
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                id: id, 
                action: action, 
                target: document.getElementById(`target_${id}`).value, 
                bots: document.getElementById(`bots_${id}`).value, 
                edition: document.getElementById(`edition_${id}`).value, 
                speed: document.getElementById(`speed_${id}`).value, 
                afk: document.getElementById(`afk_${id}`).value, 
                spam: document.getElementById(`spam_${id}`).value,
                botname: document.getElementById(`botname_${id}`).value,
                password: document.getElementById(`pass_${id}`).value,
                follow: document.getElementById(`follow_${id}`).value
            })
        }).then(() => fetchStats());
    }

    function adjustSlots(action) {
        fetch('/api/slots', { 
            method: 'POST', 
            headers: {'Content-Type': 'application/json'}, 
            body: JSON.stringify({action: action}) 
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
    try: 
        cpu_usage = f"{psutil.cpu_percent(interval=None)}%"
    except Exception: 
        cpu_usage = "Locked"
        
    try: 
        ram_usage = f"{psutil.virtual_memory().percent}%"
    except Exception: 
        ram_usage = "N/A"
    
    active_count = sum(1 for s in bot_servers.values() if s['status'] == 'RUNNING')
    
    response = {
        "cpu": cpu_usage, 
        "ram": ram_usage, 
        "active": active_count, 
        "total_slots": len(bot_servers)
    }
    response.update(bot_servers)
    return jsonify(response)

@app.route('/api/slots', methods=['POST'])
def adjust_slots():
    action = request.json.get('action')
    global bot_servers
    
    if action == 'add':
        bot_servers[str(len(bot_servers) + 1)] = {"status": "STOPPED", "target": "", "bots": "10", "edition": "3", "pid": None}
    elif action == 'remove' and len(bot_servers) > 1:
        last_id = str(len(bot_servers))
        if bot_servers[last_id].get('pid'):
            try: 
                os.kill(bot_servers[last_id]['pid'], 9)
            except Exception: 
                pass
        del bot_servers[last_id]
        
    return jsonify({"success": True})

@app.route('/api/action', methods=['POST'])
def action():
    data = request.json
    s_id = str(data.get('id'))
    
    if s_id in bot_servers:
        if data.get('action') == 'start':
            if bot_servers[s_id].get('pid'):
                try: 
                    os.kill(bot_servers[s_id]['pid'], 9)
                except Exception: 
                    pass
            
            bot_servers[s_id]['status'] = 'RUNNING'
            bot_servers[s_id]['target'] = data.get('target', '')
            bot_servers[s_id]['bots'] = data.get('bots', '10')
            
            env = os.environ.copy()
            env.update({
                'TARGET_IP': bot_servers[s_id]['target'],
                'BOT_COUNT': str(bot_servers[s_id]['bots']),
                'EDITION': str(data.get('edition', '3')),
                'SPEED': str(data.get('speed', '1')),
                'AFK_MODE': str(data.get('afk', '1')),
                'SPAM_MSG': str(data.get('spam', '')),
                'BOT_NAME': str(data.get('botname', '')),
                'BOT_PASSWORD': str(data.get('password', '')),
                'FOLLOW_TARGET': str(data.get('follow', ''))
            })

            try: 
                bot_servers[s_id]['pid'] = subprocess.Popen(['node', 'index.js'], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).pid
            except Exception as e: 
                print(f"[-] Error: {e}")
            
        elif data.get('action') == 'stop':
            bot_servers[s_id]['status'] = 'STOPPED'
            if bot_servers[s_id].get('pid'):
                try: 
                    os.kill(bot_servers[s_id]['pid'], 9)
                except Exception: 
                    pass
                bot_servers[s_id]['pid'] = None
                
    return jsonify({"success": True})

# =====================================================================
# START ENGINE
# =====================================================================
if __name__ == '__main__':
    os.system('clear' if os.name == 'posix' else 'cls')
    network_ip = get_local_ip()
    
    print("\033[94m\033[1m========================================\033[0m")
    print("\033[97m\033[1m      OP INJOY VIP BOT PANEL      \033[0m")
    print("\033[94m\033[1m========================================\033[0m")
    print("\033[92m[*] LOCAL (Non-Root):  http://localhost:9000\033[0m")
    print("\033[92m[*] ROOT ACCESS:       http://injoy:9000\033[0m")
    print(f"\033[92m[*] LAN / WiFi ACCESS: http://{network_ip}:9000\033[0m")
    print("\033[93m[*] Establishing Ngrok Global Link...\033[0m")
    
    # Start ngrok in background and print public link
    threading.Thread(target=start_ngrok_background, daemon=True).start()
    
    try:
        psutil.cpu_percent()
    except Exception:
        pass
        
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    app.run(host='0.0.0.0', port=9000, threaded=True)
