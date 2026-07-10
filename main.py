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
        button { flex: 1 1 45%; padding: 12px; font-weight: 600; cursor: pointer; border: none; border-radius: 6px; font-size
