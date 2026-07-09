import os
import sys
import time
import socket
import threading
import psutil
import subprocess
from flask import Flask, render_template_string, jsonify, request

# =====================================================================
# OP INJOY VIP SYSTEM - MINECRAFT ENGINE (V5 UI REVAMP)
# =====================================================================

app = Flask(__name__)

# Start with ONLY 1 Slot by default
bot_servers = {
    "1": {"status": "STOPPED", "target": "", "bots": "10", "edition": "3", "pid": None}
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
# FRONTEND UI (Modern Glassmorphism + Smart Circular Buttons)
# =====================================================================
HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OP INJOY VIP SYSTEM</title>
    <style>
        body { margin: 0; padding: 0; background: #050505; color: #fff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; overflow-x: hidden; }
        canvas { display: block; position: fixed; top: 0; left: 0; z-index: 1; opacity: 0.4; }
        
        #panel-container { position: relative; z-index: 2; width: 92%; max-width: 550px; margin: 30px auto; padding-bottom: 40px; }
        
        .panel { 
            background: rgba(12, 12, 12, 0.85); 
            backdrop-filter: blur(8px); 
            border: 1px solid rgba(0, 255, 0, 0.2); 
            border-radius: 16px; 
            box-shadow: 0 8px 32px rgba(0, 255, 0, 0.1); 
            padding: 25px; 
        }
        
        .header { text-align: center; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid rgba(255,255,255,0.05); }
        .header h2 { margin: 0; color: #0f0; font-family: 'Courier New', monospace; letter-spacing: 2px; text-shadow: 0 0 10px rgba(0,255,0,0.5); }
        
        .stats { 
            display: flex; justify-content: space-between; 
            background: rgba(0, 255, 0, 0.05); padding: 12px 15px; 
            border-radius: 8px; margin-bottom: 20px; 
            font-weight: 600; font-size: 13px; color: #aaa; 
            border: 1px solid rgba(0, 255, 0, 0.1); 
        }
        .stats span { color: #0f0; }

        .server-box { 
            background: rgba(0, 0, 0, 0.6); 
            border: 1px solid #222; border-left: 4px solid #0f0; 
            border-radius: 10px; padding: 18px; margin-bottom: 15px; 
            transition: all 0.3s; 
        }
        .server-box:hover { border-color: rgba(0,255,0,0.4); box-shadow: 0 0 15px rgba(0,255,0,0.05); }
        
        .server-header { display: flex; justify-content: space-between; margin-bottom: 15px; font-weight: bold; font-size: 15px; }
        .running { color: #0f0; text-shadow: 0 0 8px #0f0; }
        .stopped { color: #f44336; text-shadow: 0 0 8px #f44336; }

        .input-row { display: flex; gap: 12px; margin-bottom: 12px; }
        input, select { 
            flex: 1; background: #0a0a0a; border: 1px solid #333; color: #0f0; 
            padding: 10px 12px; border-radius: 6px; box-sizing: border-box; 
            font-family: 'Courier New', monospace; font-size: 13px; transition: 0.3s; 
        }
        input:focus, select:focus { outline: none; border-color: #0f0; box-shadow: 0 0 8px rgba(0,255,0,0.3); background: #000; }
        .full-width { width: 100%; margin-bottom: 12px; }

        .btn-group { display: flex; gap: 12px; margin-top: 15px; }
        button { 
            flex: 1; padding: 12px; font-weight: bold; font-family: 'Segoe UI', sans-serif; 
            cursor: pointer; border: none; border-radius: 6px; text-transform: uppercase; 
            letter-spacing: 1px; transition: 0.3s; font-size: 12px; 
        }
        .btn-start { background: rgba(0, 255, 0, 0.1); color: #0f0; border: 1px solid #0f0; }
        .btn-start:hover { background: #0f0; color: #000; box-shadow: 0 0 15px rgba(0,255,0,0.4); }
        .btn-stop { background: rgba(244, 67, 54, 0.1); color: #f44336; border: 1px solid #f44336; }
        .btn-stop:hover { background: #f44336; color: #fff; box-shadow: 0 0 15px rgba(244,67,54,0.4); }

        /* The New Circular Add/Remove Slot Buttons */
        .slot-controls { display: flex; justify-content: center; gap: 20px; margin-top: 25px; }
        .circle-btn { 
            width: 50px; height: 50px; border-radius: 50%; border: 2px solid #0f0; 
            background: rgba(0,255,0,0.1); color: #0f0; font-size: 28px; font-weight: 300; 
            cursor: pointer; display: flex; align-items: center; justify-content: center; 
            transition: all 0.3s ease; flex: none; padding: 0; line-height: 1;
        }
        .circle-btn:hover { background: #0f0; color: #000; box-shadow: 0 0 20px rgba(0,255,0,0.6); transform: scale(1.1); }
        
        .circle-btn.minus { border-color: #f44336; color: #f44336; background: rgba(244,67,54,0.1); }
        .circle-btn.minus:hover { background: #f44336; color: #fff; box-shadow: 0 0 20px rgba(244,67,54,0.6); transform: scale(1.1); }
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
            <span id="cpu">CPU: --</span>
            <span id="ram">RAM: --</span>
            <span id="active">ACTIVE ENGINES: -</span>
        </div>

        <div id="servers">
            <!-- Dynamically Injected Engines -->
        </div>

        <!-- Smart Circular Buttons -->
        <div class="slot-controls">
            <button class="circle-btn" onclick="adjustSlots('add')" title="Add New Slot">+</button>
            <button class="circle-btn minus" id="btn-remove" onclick="adjustSlots('remove')" style="display: none;" title="Remove Last Slot">-</button>
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
        
        let keys = Object.keys(data).filter(k => !['cpu', 'ram', 'active'].includes(k)).sort((a, b) => parseInt(a) - parseInt(b));
        
        keys.forEach(i => {
            let srv = data[i];
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
                        <option value="1" ${srv.edition === '1' ? 'selected' : ''}>Java Only</option>
                        <option value="2" ${srv.edition === '2' ? 'selected' : ''}>Bedrock Only</option>
                        <option value="3" ${srv.edition === '3' || !srv.edition ? 'selected' : ''}>Hybrid (Both)</option>
                    </select>
                    <input type="number" id="bots_${i}" placeholder="Total Bots" value="${srv.bots}">
                </div>
                <div class="input-row">
                    <select id="speed_${i}">
                        <option value="1">Normal Speed</option>
                        <option value="2">Anti-Bot Bypass</option>
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
        });
        
        const focused = document.activeElement;
        const container = document.getElementById('servers');
        if (!container.contains(focused)) {
            container.innerHTML = html;
        }
        
        document.getElementById('cpu').innerText = `CPU: ${data.cpu}`;
        document.getElementById('ram').innerText = `RAM: ${data.ram}`;
        document.getElementById('active').innerText = `ACTIVE ENGINES: ${data.active}`;

        // Smart Visibility Logic for Minus Button
        const minusBtn = document.getElementById('btn-remove');
        if (keys.length > 1) {
            minusBtn.style.display = 'flex';
        } else {
            minusBtn.style.display = 'none';
        }
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
        cpu_usage = "N/A (Locked)"
        
    try:
        ram_usage = f"{psutil.virtual_memory().percent}%"
    except Exception:
        ram_usage = "N/A"
        
    active_count = sum(1 for s in bot_servers.values() if s['status'] == 'RUNNING')
    
    response = {"cpu": cpu_usage, "ram": ram_usage, "active": active_count}
    response.update(bot_servers)
    return jsonify(response)

@app.route('/api/slots', methods=['POST'])
def adjust_slots():
    data = request.json
    action = data.get('action')
    global bot_servers
    
    if action == 'add':
        next_id = str(len(bot_servers) + 1)
        bot_servers[next_id] = {"status": "STOPPED", "target": "", "bots": "10", "edition": "3", "pid": None}
        print(f"[+] Added Dynamic Engine Slot #{next_id}")
    elif action == 'remove':
        if len(bot_servers) > 1:
            last_id = str(len(bot_servers))
            pid = bot_servers[last_id].get('pid')
            if pid:
                try: os.kill(pid, 9)
                except: pass
            del bot_servers[last_id]
            print(f"[-] Removed Dynamic Engine Slot #{last_id}")
            
    return jsonify({"success": True})

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
    
    try:
        psutil.cpu_percent()
    except Exception:
        pass
        
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    app.run(host='0.0.0.0', port=9000, threaded=True)
