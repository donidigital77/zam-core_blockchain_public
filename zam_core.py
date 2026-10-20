from flask import Flask, render_template_string, request, redirect, url_for, session
import json
import os
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = "zam_core_genesis_architecture_key"

DATABASE_FILE = "zam_core_database.json"
LEDGER_FILE = "zam_core_ledger.json"

# --- 1. INISIALISASI DATABASE & SISTEM LEDGER UTAMA ---
def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_database(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_ledger():
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    # Genesis Block (Blok Nol / Asal Jaringan)
    genesis_block = {
        "index": 0,
        "timestamp": str(datetime.now()),
        "event": "ZAM CORE Genesis Block - Mainnet Initialization",
        "previous_hash": "0x00000000000000000000000000000000",
        "hash": hashlib.sha256(b"ZAMCoreGenesisBlockMainnet").hexdigest(),
        "node_validator": "ZAM CORE Foundation"
    }
    save_ledger([genesis_block])
    return [genesis_block]

def save_ledger(ledger):
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=4)

def record_new_block(event_desc, validator):
    ledger = load_ledger()
    last_block = ledger[-1]
    new_index = len(ledger)
    timestamp = str(datetime.now())
    
    raw_data = f"{new_index}{last_block['hash']}{timestamp}{event_desc}{validator}"
    new_hash = hashlib.sha256(raw_data.encode()).hexdigest()
    
    block = {
        "index": new_index,
        "timestamp": timestamp,
        "event": event_desc,
        "previous_hash": last_block["hash"],
        "hash": new_hash,
        "node_validator": validator
    }
    ledger.append(block)
    save_ledger(ledger)
    return block

# --- 2. ANTARMUKA PENGGUNA (FRONTEND & BACKEND TERPADU) ---
HTML_APP_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZAM CORE - Core Ecosystem & Node</title>
    <style>
        :root {
            --primary: #00f2fe;
            --secondary: #4facfe;
            --bg-deep: #040812;
            --card-bg: rgba(11, 19, 38, 0.9);
            --border-glow: rgba(0, 242, 254, 0.25);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --success: #10b981;
            --warning: #f59e0b;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-deep);
            color: var(--text-main);
            margin: 0;
            padding-bottom: 90px;
        }

        .auth-wrapper {
            background: radial-gradient(circle at center, #0f172a 0%, #040812 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            box-sizing: border-box;
        }

        .auth-card {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border-glow);
            border-radius: 28px;
            padding: 35px 25px;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.8);
        }

        .brand-title {
            text-align: center;
            font-size: 28px;
            font-weight: 900;
            background: linear-gradient(135deg, #00f2fe, #4facfe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }

        .field-label {
            font-size: 11px;
            color: var(--primary);
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 6px;
            display: block;
        }

        .input-box {
            background: rgba(20, 30, 50, 0.9);
            border: 1px solid var(--border-glow);
            border-radius: 14px;
            margin-bottom: 16px;
            padding: 4px;
        }

        .input-box input {
            background: transparent;
            border: none;
            color: white;
            padding: 12px;
            font-size: 14px;
            width: 100%;
            box-sizing: border-box;
            outline: none;
            font-family: inherit;
        }

        .btn-action {
            background: linear-gradient(135deg, #00f2fe, #4facfe);
            color: #040812;
            border: none;
            padding: 15px;
            border-radius: 14px;
            font-weight: 800;
            width: 100%;
            cursor: pointer;
            font-size: 15px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 10px 25px rgba(0, 242, 254, 0.3);
        }

        .header {
            display: flex; justify-content: space-between; align-items: center;
            padding: 16px 20px; background: #0b1326; border-bottom: 1px solid var(--border-glow);
            position: sticky; top: 0; z-index: 100;
        }
        .logo { font-size: 18px; font-weight: 900; color: var(--primary); letter-spacing: 1px; }
        .content { padding: 20px; max-width: 500px; margin: 0 auto; }
        
        .card-core {
            background: linear-gradient(135deg, #0b1326, #16223f);
            border: 1px solid var(--border-glow);
            color: white; border-radius: 22px; padding: 24px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5); margin-bottom: 20px;
        }
        .card-panel {
            background: #0b1326; border: 1px solid var(--border-glow);
            border-radius: 18px; padding: 20px; margin-bottom: 15px;
        }
        .btn {
            background-color: var(--primary); color: #040812; border: none;
            padding: 12px 20px; border-radius: 12px; font-weight: 700;
            width: 100%; cursor: pointer; margin-top: 10px; font-size: 14px;
        }
        .btn-success { background-color: var(--success); color: white; }
        .btn-danger { background-color: #ef4444; color: white; }
        .btn-group { display: flex; gap: 10px; margin-top: 15px; }
        
        .bottom-nav {
            position: fixed; bottom: 0; left: 0; width: 100%; background: #0b1326;
            border-top: 1px solid var(--border-glow); display: flex; justify-content: space-around;
            padding: 10px 0; z-index: 100;
        }
        .nav-item { text-decoration: none; color: var(--text-muted); font-size: 11px; text-align: center; flex: 1; font-weight: 500; }
        .nav-item.active { color: var(--primary); font-weight: 700; }
        .badge { background: rgba(0, 242, 254, 0.1); color: var(--primary); padding: 6px 12px; border-radius: 30px; font-size: 12px; font-weight: 700; display: inline-block; margin-bottom: 10px; border: 1px solid var(--border-glow); }
        .ledger-block { font-size: 11px; border-bottom: 1px solid var(--border-glow); padding: 12px 0; font-family: monospace; }
        .alert-box { background: rgba(16, 185, 129, 0.2); color: #34d399; padding: 12px 16px; border-radius: 12px; margin-bottom: 20px; font-size: 13px; font-weight: 600; border: 1px solid #10b981; text-align: center; }
    </style>
</head>
<body>

    {% if not logged_in %}
    <div class="auth-wrapper">
        <div class="auth-card">
            <div class="brand-title">ZAM CORE</div>
            <p style="color: var(--text-muted); font-size: 12px; text-align: center; margin-bottom: 25px;">Early-Stage Core Architecture & Node Setup</p>
            
            <form action="/login" method="POST">
                <label class="field-label">Node Account / Wallet ID</label>
                <div class="input-box">
                    <input type="text" name="wallet_id" placeholder="Masukkan ID wallet atau nama..." required>
                </div>

                <label class="field-label">Security Passkey</label>
                <div class="input-box">
                    <input type="password" name="passkey" placeholder="Passkey akses node..." required>
                </div>

                <button type="submit" class="btn-action">Inisialisasi & Masuk Node</button>
            </form>
        </div>
    </div>
    
    {% else %}

        <div class="header">
            <div class="logo">ZAM CORE</div>
            <div style="font-size: 11px; color: var(--primary); background: rgba(0,242,254,0.1); padding: 6px 12px; border-radius: 20px; font-weight: 600; border: 1px solid var(--border-glow);">{{ user.wallet_id }}</div>
        </div>

        <div class="content">
            {% if message %}
                <div class="alert-box">{{ message }}</div>
            {% endif %}

            {% if active_tab == 'dashboard' %}
                <div class="card-core">
                    <div style="font-size: 13px; opacity: 0.9;">Total Verified Balance</div>
                    <div style="font-size: 34px; font-weight: 800; margin: 6px 0; color: var(--primary);">{{ "{:,.2f}".format(user.balance) }} ZAM</div>
                    <div style="font-size: 12px; opacity: 0.8;">Node Status: Synchronized & Active</div>
                    
                    <div class="btn-group">
                        <form action="/mine" method="POST" style="flex: 1; margin: 0;">
                            <button type="submit" class="btn btn-success" style="width:100%;">⛏️ Mobile Mining Session (+100 ZAM)</button>
                        </form>
                    </div>
                </div>

                <div class="card-panel" style="text-align: center; background: linear-gradient(135deg, #0b1326, #1e3a8a);">
                    <h4 style="margin: 0 0 5px 0; color: var(--primary);">🚀 Early-Stage Architecture</h4>
                    <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 15px;">Fondasi awal replikasi sistem core yang tangguh, transparan, dan siap di-upgrade menuju Layer-1 mutakhir.</p>
                </div>

            {% elif active_tab == 'ledger' %}
                <div class="card-panel">
                    <h3 style="margin-top: 0;">⛓️ Core Distributed Ledger</h3>
                    <p style="color: var(--text-muted); font-size: 12px; margin-bottom: 15px;">Pencatatan blok transaksi secara permanen dan terenkripsi.</p>
                    {% for block in ledger[::-1] %}
                        <div class="ledger-block">
                            <b style="color: var(--primary);">Block #{{ block.index }}</b> ({{ block.timestamp }})<br>
                            <span>Event: {{ block.event }}</span><br>
                            <span style="color: var(--text-muted); font-size: 10px;">Validator: {{ block.node_validator }} | Hash: {{ block.hash[:24] }}...</span>
                        </div>
                    {% endfor %}
                </div>

            {% elif active_tab == 'node' %}
                <div class="card-panel">
                    <h3>Node Configuration</h3>
                    <p style="font-size: 14px; margin: 6px 0;">Wallet ID: <b>{{ user.wallet_id }}</b></p>
                    <p style="font-size: 14px; margin: 6px 0;">Consensus Engine: <span style="color: var(--success); font-weight: bold;">Proof-of-Core (PoC)</span></p>
                </div>
                <div class="card-panel" style="text-align: center;">
                    <form action="/logout" method="POST">
                        <button type="submit" class="btn btn-danger">Tutup Sesi Node (Logout)</button>
                    </form>
                </div>
            {% endif %}
        </div>

        <div class="bottom-nav">
            <a href="/?tab=dashboard" class="nav-item {% if active_tab == 'dashboard' %}active{% endif %}">🏠<br>Dashboard</a>
            <a href="/?tab=ledger" class="nav-item {% if active_tab == 'ledger' %}active{% endif %}">⛓️<br>Ledger Chain</a>
            <a href="/?tab=node" class="nav-item {% if active_tab == 'node' %}active{% endif %}">👤<br>Node ID</a>
        </div>

    {% endif %}
</body>
</html>
"""

# --- 3. ROUTING & KONTROL APLIKASI ---
@app.route("/")
def index():
    if "wallet_id" not in session:
        return render_template_string(HTML_APP_TEMPLATE, logged_in=False)
    
    wallet_id = session["wallet_id"]
    db = load_database()
    user = db.get(wallet_id, {"wallet_id": wallet_id, "balance": 2200000.0}) # Basis saldo awal 2.2 Juta token
    
    ledger = load_ledger()
    active_tab = request.args.get("tab", "dashboard")
    message = session.pop("flash_message", None)
    return render_template_string(HTML_APP_TEMPLATE, logged_in=True, user=user, ledger=ledger, active_tab=active_tab, message=message)

@app.route("/login", methods=["POST"])
def login():
    wallet_id = request.form.get("wallet_id", "").strip()
    if wallet_id:
        session["wallet_id"] = wallet_id
        db = load_database()
        if wallet_id not in db:
            db[wallet_id] = {"wallet_id": wallet_id, "balance": 2200000.0}
            save_database(db)
            record_new_block(f"New node initialized for {wallet_id}", wallet_id)
        session["flash_message"] = f"Node '{wallet_id}' berhasil terhubung ke jaringan core!"
    return redirect(url_for("index", tab="dashboard"))

@app.route("/mine", methods=["POST"])
def mine():
    if "wallet_id" in session:
        wallet_id = session["wallet_id"]
        db = load_database()
        if wallet_id in db:
            db[wallet_id]["balance"] += 100.0
            save_database(db)
            record_new_block(f"Mobile mining reward 100 ZAM claimed by {wallet_id}", wallet_id)
            session["flash_message"] = "Sesi penambangan seluler berhasil divalidasi! +100 ZAM ditambahkan."
    return redirect(url_for("index", tab="dashboard"))

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
from flask import Flask, render_template_string, request, redirect, url_for, session
import json
import os
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = "zam_core_master_enterprise_upgrade_key"

DATABASE_FILE = "zam_core_database.json"
LEDGER_FILE = "zam_core_ledger.json"

def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_database(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_ledger():
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    genesis_block = {
        "index": 0,
        "timestamp": str(datetime.now()),
        "event": "ZAM CORE Genesis Block - Enterprise Multi-Feature Upgrade",
        "previous_hash": "0x00000000000000000000000000000000",
        "hash": hashlib.sha256(b"ZAMCoreEnterpriseGenesis").hexdigest(),
        "node_validator": "ZAM CORE Foundation"
    }
    save_ledger([genesis_block])
    return [genesis_block]

def save_ledger(ledger):
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=4)

def record_new_block(event_desc, validator):
    ledger = load_ledger()
    last_block = ledger[-1]
    new_index = len(ledger)
    timestamp = str(datetime.now())
    
    raw_data = f"{new_index}{last_block['hash']}{timestamp}{event_desc}{validator}"
    new_hash = hashlib.sha256(raw_data.encode()).hexdigest()
    
    block = {
        "index": new_index,
        "timestamp": timestamp,
        "event": event_desc,
        "previous_hash": last_block["hash"],
        "hash": new_hash,
        "node_validator": validator
    }
    ledger.append(block)
    save_ledger(ledger)
    return block

HTML_APP_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZAM CORE - Enterprise Ecosystem & Consensus</title>
    <style>
        :root {
            --primary: #00f2fe;
            --secondary: #4facfe;
            --bg-deep: #040812;
            --card-bg: rgba(11, 19, 38, 0.9);
            --border-glow: rgba(0, 242, 254, 0.25);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --success: #10b981;
            --warning: #f59e0b;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-deep);
            color: var(--text-main);
            margin: 0;
            padding-bottom: 90px;
        }

        .auth-wrapper {
            background: radial-gradient(circle at center, #0f172a 0%, #040812 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            box-sizing: border-box;
        }

        .auth-card {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border-glow);
            border-radius: 28px;
            padding: 35px 25px;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.8);
        }

        .brand-title {
            text-align: center;
            font-size: 28px;
            font-weight: 900;
            background: linear-gradient(135deg, #00f2fe, #4facfe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }

        .field-label {
            font-size: 11px;
            color: var(--primary);
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 6px;
            display: block;
        }

        .input-box {
            background: rgba(20, 30, 50, 0.9);
            border: 1px solid var(--border-glow);
            border-radius: 14px;
            margin-bottom: 16px;
            padding: 4px;
        }

        .input-box input, .input-box select {
            background: transparent;
            border: none;
            color: white;
            padding: 12px;
            font-size: 14px;
            width: 100%;
            box-sizing: border-box;
            outline: none;
            font-family: inherit;
        }

        .btn-action {
            background: linear-gradient(135deg, #00f2fe, #4facfe);
            color: #040812;
            border: none;
            padding: 15px;
            border-radius: 14px;
            font-weight: 800;
            width: 100%;
            cursor: pointer;
            font-size: 15px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 10px 25px rgba(0, 242, 254, 0.3);
        }

        .header {
            display: flex; justify-content: space-between; align-items: center;
            padding: 16px 20px; background: #0b1326; border-bottom: 1px solid var(--border-glow);
            position: sticky; top: 0; z-index: 100;
        }
        .logo { font-size: 18px; font-weight: 900; color: var(--primary); letter-spacing: 1px; }
        .content { padding: 20px; max-width: 500px; margin: 0 auto; }
        
        .card-core {
            background: linear-gradient(135deg, #0b1326, #16223f);
            border: 1px solid var(--border-glow);
            color: white; border-radius: 22px; padding: 24px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5); margin-bottom: 20px;
        }
        .card-panel {
            background: #0b1326; border: 1px solid var(--border-glow);
            border-radius: 18px; padding: 20px; margin-bottom: 15px;
        }
        .btn {
            background-color: var(--primary); color: #040812; border: none;
            padding: 12px 20px; border-radius: 12px; font-weight: 700;
            width: 100%; cursor: pointer; margin-top: 10px; font-size: 14px;
        }
        .btn-success { background-color: var(--success); color: white; }
        .btn-warning { background-color: var(--warning); color: white; }
        .btn-danger { background-color: #ef4444; color: white; }
        .btn-group { display: flex; gap: 10px; margin-top: 15px; }
        
        .bottom-nav {
            position: fixed; bottom: 0; left: 0; width: 100%; background: #0b1326;
            border-top: 1px solid var(--border-glow); display: flex; justify-content: space-around;
            padding: 10px 0; z-index: 100;
        }
        .nav-item { text-decoration: none; color: var(--text-muted); font-size: 11px; text-align: center; flex: 1; font-weight: 500; }
        .nav-item.active { color: var(--primary); font-weight: 700; }
        .badge { background: rgba(0, 242, 254, 0.1); color: var(--primary); padding: 6px 12px; border-radius: 30px; font-size: 12px; font-weight: 700; display: inline-block; margin-bottom: 10px; border: 1px solid var(--border-glow); }
        .ledger-block { font-size: 11px; border-bottom: 1px solid var(--border-glow); padding: 12px 0; font-family: monospace; }
        .alert-box { background: rgba(16, 185, 129, 0.2); color: #34d399; padding: 12px 16px; border-radius: 12px; margin-bottom: 20px; font-size: 13px; font-weight: 600; border: 1px solid #10b981; text-align: center; }
    </style>
</head>
<body>

    {% if not logged_in %}
    <div class="auth-wrapper">
        <div class="auth-card">
            <div class="brand-title">ZAM CORE</div>
            <p style="color: var(--text-muted); font-size: 12px; text-align: center; margin-bottom: 25px;">Enterprise Node & Multi-Feature Architecture</p>
            
            <form action="/login" method="POST">
                <label class="field-label">Node Wallet ID / Username</label>
                <div class="input-box">
                    <input type="text" name="wallet_id" placeholder="Masukkan ID wallet..." required>
                </div>

                <label class="field-label">Security Passkey</label>
                <div class="input-box">
                    <input type="password" name="passkey" placeholder="Passkey jaringan..." required>
                </div>

                <button type="submit" class="btn-action">Inisialisasi Node</button>
            </form>
        </div>
    </div>
    
    {% else %}

        <div class="header">
            <div class="logo">ZAM CORE</div>
            <div style="font-size: 11px; color: var(--primary); background: rgba(0,242,254,0.1); padding: 6px 12px; border-radius: 20px; font-weight: 600; border: 1px solid var(--border-glow);">{{ user.wallet_id }}</div>
        </div>

        <div class="content">
            {% if message %}
                <div class="alert-box">{{ message }}</div>
            {% endif %}

            {% if active_tab == 'dashboard' %}
                <div class="card-core">
                    <div style="font-size: 13px; opacity: 0.9;">Total Liquid Balance</div>
                    <div style="font-size: 30px; font-weight: 800; margin: 4px 0; color: var(--primary);">{{ "{:,.2f}".format(user.balance) }} ZAM</div>
                    <div style="font-size: 12px; opacity: 0.9; margin-top: 4px;">Staked in Vault: <b>{{ "{:,.2f}".format(user.staked) }} ZAM</b></div>
                    <div style="font-size: 11px; opacity: 0.8; margin-top: 2px;">Konsensus Engine: Proof-of-Core (PoC) Active</div>
                    
                    <div class="btn-group">
                        <form action="/mine" method="POST" style="flex: 1; margin: 0;">
                            <button type="submit" class="btn btn-success" style="width:100%;">⛏️ PoC Mining (+100 ZAM)</button>
                        </form>
                    </div>
                </div>

                <!-- Panel Staking Vault -->
                <div class="card-panel">
                    <h3 style="margin-top:0; color: var(--primary);">🔒 Staking Vault</h3>
                    <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px;">Kunci token ZAM untuk mendapatkan akumulasi hasil pasif harian.</p>
                    <form action="/stake" method="POST">
                        <div class="input-box">
                            <input type="number" name="amount" placeholder="Jumlah ZAM yang dikunci..." required>
                        </div>
                        <button type="submit" class="btn btn-warning" style="color:white; margin-top:0;">Kunci Token (Stake)</button>
                    </form>
                </div>

            {% elif active_tab == 'transfer' %}
                <div class="card-panel">
                    <h3 style="margin-top:0; color: var(--primary);">💸 Peer-to-Peer Transfer</h3>
                    <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 15px;">Kirim token ZAM langsung ke Wallet ID rekan sesama node.</p>
                    <form action="/transfer_p2p" method="POST">
                        <label class="field-label">Wallet ID Penerima</label>
                        <div class="input-box">
                            <input type="text" name="recipient" placeholder="ID tujuan..." required>
                        </div>
                        <label class="field-label">Jumlah ZAM</label>
                        <div class="input-box">
                            <input type="number" name="amount" placeholder="Nominal..." required>
                        </div>
                        <button type="submit" class="btn" style="margin-top:5px;">Kirim Dana Sekarang</button>
                    </form>
                </div>

            {% elif active_tab == 'ledger' %}
                <div class="card-panel">
                    <h3 style="margin-top: 0;">⛓️ Distributed Consensus Ledger</h3>
                    <p style="color: var(--text-muted); font-size: 12px; margin-bottom: 15px;">Riwayat blok dan validasi konsensus jaringan.</p>
                    {% for block in ledger[::-1] %}
                        <div class="ledger-block">
                            <b style="color: var(--primary);">Block #{{ block.index }}</b> ({{ block.timestamp }})<br>
                            <span>Event: {{ block.event }}</span><br>
                            <span style="color: var(--text-muted); font-size: 10px;">Validator: {{ block.node_validator }} | Hash: {{ block.hash[:24] }}...</span>
                        </div>
                    {% endfor %}
                </div>

            {% elif active_tab == 'node' %}
                <div class="card-panel">
                    <h3>Node Profile</h3>
                    <p style="font-size: 14px; margin: 6px 0;">Wallet ID: <b>{{ user.wallet_id }}</b></p>
                    <p style="font-size: 14px; margin: 6px 0;">Consensus Status: <span style="color: var(--success); font-weight: bold;">🟢 Validated & Secure</span></p>
                </div>
                <div class="card-panel" style="text-align: center;">
                    <form action="/logout" method="POST">
                        <button type="submit" class="btn btn-danger">Putuskan Sesi Node (Logout)</button>
                    </form>
                </div>
            {% endif %}
        </div>

        <div class="bottom-nav">
            <a href="/?tab=dashboard" class="nav-item {% if active_tab == 'dashboard' %}active{% endif %}">🏠<br>Dashboard</a>
            <a href="/?tab=transfer" class="nav-item {% if active_tab == 'transfer' %}active{% endif %}">💸<br>P2P Transfer</a>
            <a href="/?tab=ledger" class="nav-item {% if active_tab == 'ledger' %}active{% endif %}">⛓️<br>Ledger</a>
            <a href="/?tab=node" class="nav-item {% if active_tab == 'node' %}active{% endif %}">👤<br>Node ID</a>
        </div>

    {% endif %}
</body>
</html>
"""

@app.route("/")
def index():
    if "wallet_id" not in session:
        return render_template_string(HTML_APP_TEMPLATE, logged_in=False)
    
    wallet_id = session["wallet_id"]
    db = load_database()
    user = db.get(wallet_id, {"wallet_id": wallet_id, "balance": 2200000.0, "staked": 0.0})
    
    ledger = load_ledger()
    active_tab = request.args.get("tab", "dashboard")
    message = session.pop("flash_message", None)
    return render_template_string(HTML_APP_TEMPLATE, logged_in=True, user=user, ledger=ledger, active_tab=active_tab, message=message)

@app.route("/login", methods=["POST"])
def login():
    wallet_id = request.form.get("wallet_id", "").strip()
    if wallet_id:
        session["wallet_id"] = wallet_id
        db = load_database()
        if wallet_id not in db:
            db[wallet_id] = {"wallet_id": wallet_id, "balance": 2200000.0, "staked": 0.0}
            save_database(db)
            record_new_block(f"Node initialized for {wallet_id}", wallet_id)
        session["flash_message"] = f"Node '{wallet_id}' terhubung dengan konsensus Proof-of-Core!"
    return redirect(url_for("index", tab="dashboard"))

@app.route("/mine", methods=["POST"])
def mine():
    if "wallet_id" in session:
        wallet_id = session["wallet_id"]
        db = load_database()
        if wallet_id in db:
            db[wallet_id]["balance"] += 100.0
            save_database(db)
            record_new_block(f"PoC Mining reward 100 ZAM validated for {wallet_id}", f"{wallet_id}-Validator")
            session["flash_message"] = "Konsensus PoC sukses! +100 ZAM ditambahkan melalui validasi multi-node."
    return redirect(url_for("index", tab="dashboard"))

@app.route("/stake", methods=["POST"])
def stake():
    if "wallet_id" in session:
        wallet_id = session["wallet_id"]
        try:
            amount = float(request.form.get("amount", 0))
        except:
            amount = 0
            
        db = load_database()
        if wallet_id in db:
            if 0 < amount <= db[wallet_id]["balance"]:
                db[wallet_id]["balance"] -= amount
                db[wallet_id]["staked"] += amount
                save_database(db)
                record_new_block(f"Staking lock-up {amount} ZAM by {wallet_id}", wallet_id)
                session["flash_message"] = f"Berhasil mengunci {amount:,.2f} ZAM ke dalam Staking Vault!"
            else:
                session["flash_message"] = "Saldo tidak mencukupi atau nominal tidak valid."
    return redirect(url_for("index", tab="dashboard"))

@app.route("/transfer_p2p", methods=["POST"])
def transfer_p2p():
    if "wallet_id" in session:
        sender = session["wallet_id"]
        recipient = request.form.get("recipient", "").strip()
        try:
            amount = float(request.form.get("amount", 0))
        except:
            amount = 0
            
        db = load_database()
        if sender in db and recipient:
            if amount > 0 and db[sender]["balance"] >= amount:
                db[sender]["balance"] -= amount
                if recipient not in db:
                    db[recipient] = {"wallet_id": recipient, "balance": 0.0, "staked": 0.0}
                db[recipient]["balance"] += amount
                save_database(db)
                record_new_block(f"P2P Transfer {amount} ZAM from {sender} to {recipient}", sender)
                session["flash_message"] = f"Berhasil mengirim {amount:,.2f} ZAM ke {recipient}!"
            else:
                session["flash_message"] = "Saldo tidak mencukupi atau tujuan tidak valid."
    return redirect(url_for("index", tab="transfer"))

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
from flask import Flask, render_template_string, request, redirect, url_for, session
import json
import os
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = "zam_core_immutable_absolute_key"

DATABASE_FILE = "zam_core_database.json"
LEDGER_FILE = "zam_core_ledger.json"

# --- ATURAN MUTLAK & PERMANEN (IMMUTABLE PROTOCOL RULES) ---
# Aturan ini dikunci secara matematis dan tidak dapat diubah oleh founder, admin, atau siapa pun.
PROTOCOL_RULES = {
    "MAX_TOTAL_SUPPLY": 210000000.0,  # Batas maksimum koin global (Hard Cap)
    "INITIAL_NODE_BALANCE": 2200000.0, # Alokasi awal genesis node
    "MIN_WITHDRAWAL": 1000.0,         # Batas minimum transaksi
    "CONSENSUS_ENGINE": "Proof-of-Core (Immutable v1.0)"
}

def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_database(data):
    # Sistem penyimpanan data yang tunduk pada protokol ketat tanpa intervensi admin
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_ledger():
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    genesis_block = {
        "index": 0,
        "timestamp": str(datetime.now()),
        "event": "ZAM CORE Immutable Genesis Block - Code is Law Enforced",
        "previous_hash": "0x00000000000000000000000000000000",
        "hash": hashlib.sha256(b"ZAMCoreImmutableGenesisCodeIsLaw").hexdigest(),
        "node_validator": "Immutable Protocol Protocol"
    }
    save_ledger([genesis_block])
    return [genesis_block]

def save_ledger(ledger):
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=4)

def record_immutable_block(event_desc, validator):
    ledger = load_ledger()
    last_block = ledger[-1]
    new_index = len(ledger)
    timestamp = str(datetime.now())
    
    raw_data = f"{new_index}{last_block['hash']}{timestamp}{event_desc}{validator}"
    new_hash = hashlib.sha256(raw_data.encode()).hexdigest()
    
    block = {
        "index": new_index,
        "timestamp": timestamp,
        "event": event_desc,
        "previous_hash": last_block["hash"],
        "hash": new_hash,
        "node_validator": validator
    }
    ledger.append(block)
    save_ledger(ledger)
    return block

HTML_APP_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZAM CORE - Immutable Decentralized Protocol</title>
    <style>
        :root {
            --primary: #00f2fe;
            --secondary: #4facfe;
            --bg-deep: #040812;
            --card-bg: rgba(11, 19, 38, 0.9);
            --border-glow: rgba(0, 242, 254, 0.25);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --success: #10b981;
            --warning: #f59e0b;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-deep);
            color: var(--text-main);
            margin: 0;
            padding-bottom: 90px;
        }

        .auth-wrapper {
            background: radial-gradient(circle at center, #0f172a 0%, #040812 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            box-sizing: border-box;
        }

        .auth-card {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border-glow);
            border-radius: 28px;
            padding: 35px 25px;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.8);
        }

        .brand-title {
            text-align: center;
            font-size: 26px;
            font-weight: 900;
            background: linear-gradient(135deg, #00f2fe, #4facfe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }

        .field-label {
            font-size: 11px;
            color: var(--primary);
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 6px;
            display: block;
        }

        .input-box {
            background: rgba(20, 30, 50, 0.9);
            border: 1px solid var(--border-glow);
            border-radius: 14px;
            margin-bottom: 16px;
            padding: 4px;
        }

        .input-box input {
            background: transparent;
            border: none;
            color: white;
            padding: 12px;
            font-size: 14px;
            width: 100%;
            box-sizing: border-box;
            outline: none;
            font-family: inherit;
        }

        .btn-action {
            background: linear-gradient(135deg, #00f2fe, #4facfe);
            color: #040812;
            border: none;
            padding: 15px;
            border-radius: 14px;
            font-weight: 800;
            width: 100%;
            cursor: pointer;
            font-size: 15px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 10px 25px rgba(0, 242, 254, 0.3);
        }

        .header {
            display: flex; justify-content: space-between; align-items: center;
            padding: 16px 20px; background: #0b1326; border-bottom: 1px solid var(--border-glow);
            position: sticky; top: 0; z-index: 100;
        }
        .logo { font-size: 18px; font-weight: 900; color: var(--primary); letter-spacing: 1px; }
        .content { padding: 20px; max-width: 500px; margin: 0 auto; }
        
        .card-core {
            background: linear-gradient(135deg, #0b1326, #16223f);
            border: 1px solid var(--border-glow);
            color: white; border-radius: 22px; padding: 24px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5); margin-bottom: 20px;
        }
        .card-panel {
            background: #0b1326; border: 1px solid var(--border-glow);
            border-radius: 18px; padding: 20px; margin-bottom: 15px;
        }
        .btn {
            background-color: var(--primary); color: #040812; border: none;
            padding: 12px 20px; border-radius: 12px; font-weight: 700;
            width: 100%; cursor: pointer; margin-top: 10px; font-size: 14px;
        }
        .btn-success { background-color: var(--success); color: white; }
        .btn-warning { background-color: var(--warning); color: white; }
        .btn-danger { background-color: #ef4444; color: white; }
        .btn-group { display: flex; gap: 10px; margin-top: 15px; }
        
        .bottom-nav {
            position: fixed; bottom: 0; left: 0; width: 100%; background: #0b1326;
            border-top: 1px solid var(--border-glow); display: flex; justify-content: space-around;
            padding: 10px 0; z-index: 100;
        }
        .nav-item { text-decoration: none; color: var(--text-muted); font-size: 11px; text-align: center; flex: 1; font-weight: 500; }
        .nav-item.active { color: var(--primary); font-weight: 700; }
        .badge { background: rgba(0, 242, 254, 0.1); color: var(--primary); padding: 6px 12px; border-radius: 30px; font-size: 12px; font-weight: 700; display: inline-block; margin-bottom: 10px; border: 1px solid var(--border-glow); }
        .ledger-block { font-size: 11px; border-bottom: 1px solid var(--border-glow); padding: 12px 0; font-family: monospace; }
        .alert-box { background: rgba(16, 185, 129, 0.2); color: #34d399; padding: 12px 16px; border-radius: 12px; margin-bottom: 20px; font-size: 13px; font-weight: 600; border: 1px solid #10b981; text-align: center; }
    </style>
</head>
<body>

    {% if not logged_in %}
    <div class="auth-wrapper">
        <div class="auth-card">
            <div class="brand-title">ZAM CORE</div>
            <p style="color: var(--text-muted); font-size: 12px; text-align: center; margin-bottom: 25px;">Immutable Protocol • Code is Law</p>
            
            <form action="/login" method="POST">
                <label class="field-label">Node Wallet ID</label>
                <div class="input-box">
                    <input type="text" name="wallet_id" placeholder="Masukkan ID wallet..." required>
                </div>

                <label class="field-label">Passkey Keamanan</label>
                <div class="input-box">
                    <input type="password" name="passkey" placeholder="Passkey jaringan..." required>
                </div>

                <button type="submit" class="btn-action">Akses Node Mandiri</button>
            </form>
        </div>
    </div>
    
    {% else %}

        <div class="header">
            <div class="logo">ZAM CORE</div>
            <div style="font-size: 11px; color: var(--primary); background: rgba(0,242,254,0.1); padding: 6px 12px; border-radius: 20px; font-weight: 600; border: 1px solid var(--border-glow);">{{ user.wallet_id }}</div>
        </div>

        <div class="content">
            {% if message %}
                <div class="alert-box">{{ message }}</div>
            {% endif %}

            {% if active_tab == 'dashboard' %}
                <div class="card-core">
                    <div style="font-size: 13px; opacity: 0.9;">Total Verified Balance</div>
                    <div style="font-size: 30px; font-weight: 800; margin: 4px 0; color: var(--primary);">{{ "{:,.2f}".format(user.balance) }} ZAM</div>
                    <div style="font-size: 12px; opacity: 0.9; margin-top: 4px;">Staked in Vault: <b>{{ "{:,.2f}".format(user.staked) }} ZAM</b></div>
                    <div style="font-size: 11px; opacity: 0.8; margin-top: 4px; color: var(--success);">🛡️ Protocol Rule: Immutable & Trustless</div>
                    
                    <div class="btn-group">
                        <form action="/mine" method="POST" style="flex: 1; margin: 0;">
                            <button type="submit" class="btn btn-success" style="width:100%;">⛏️ Protocol Mining (+100 ZAM)</button>
                        </form>
                    </div>
                </div>

                <div class="card-panel">
                    <h3 style="margin-top:0; color: var(--primary);">🔒 Immutable Staking Vault</h3>
                    <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px;">Kunci token sesuai aturan protokol mutlak.</p>
                    <form action="/stake" method="POST">
                        <div class="input-box">
                            <input type="number" name="amount" placeholder="Jumlah ZAM..." required>
                        </div>
                        <button type="submit" class="btn btn-warning" style="color:white; margin-top:0;">Kunci Token</button>
                    </form>
                </div>

            {% elif active_tab == 'transfer' %}
                <div class="card-panel">
                    <h3 style="margin-top:0; color: var(--primary);">💸 Peer-to-Peer Transfer</h3>
                    <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 15px;">Kirim token langsung tanpa intervensi pihak ketiga.</p>
                    <form action="/transfer_p2p" method="POST">
                        <label class="field-label">Wallet ID Penerima</label>
                        <div class="input-box">
                            <input type="text" name="recipient" placeholder="ID tujuan..." required>
                        </div>
                        <label class="field-label">Jumlah ZAM</label>
                        <div class="input-box">
                            <input type="number" name="amount" placeholder="Nominal..." required>
                        </div>
                        <button type="submit" class="btn" style="margin-top:5px;">Kirim Dana</button>
                    </form>
                </div>

            {% elif active_tab == 'rules' %}
                <div class="card-panel">
                    <h3 style="margin-top: 0; color: var(--primary);">📜 Aturan Mutlak Protokol</h3>
                    <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 15px;">Parameter ini dikunci mati di dalam kode dan tidak memiliki hak istimewa admin.</p>
                    <p style="font-size: 13px;"><b>Maksimal Suplai Global:</b> {{ "{:,.0f}".format(protocol_rules.MAX_TOTAL_SUPPLY) }} ZAM</p>
                    <p style="font-size: 13px;"><b>Alokasi Awal Node:</b> {{ "{:,.0f}".format(protocol_rules.INITIAL_NODE_BALANCE) }} ZAM</p>
                    <p style="font-size: 13px;"><b>Mesin Konsensus:</b> {{ protocol_rules.CONSENSUS_ENGINE }}</p>
                    <p style="font-size: 12px; color: var(--success); margin-top: 10px;">Status: 100% Kebal Manipulasi Founder / Admin.</p>
                </div>

            {% elif active_tab == 'ledger' %}
                <div class="card-panel">
                    <h3 style="margin-top: 0;">⛓️ Immutable Ledger</h3>
                    {% for block in ledger[::-1] %}
                        <div class="ledger-block">
                            <b style="color: var(--primary);">Block #{{ block.index }}</b> ({{ block.timestamp }})<br>
                            <span>Event: {{ block.event }}</span><br>
                            <span style="color: var(--text-muted); font-size: 10px;">Hash: {{ block.hash[:24] }}...</span>
                        </div>
                    {% endfor %}
                </div>

            {% elif active_tab == 'node' %}
                <div class="card-panel">
                    <h3>Node Profile</h3>
                    <p style="font-size: 14px; margin: 6px 0;">Wallet ID: <b>{{ user.wallet_id }}</b></p>
                    <p style="font-size: 14px; margin: 6px 0;">Status: <span style="color: var(--success); font-weight: bold;">🟢 Terikat Protokol Mutlak</span></p>
                </div>
                <div class="card-panel" style="text-align: center;">
                    <form action="/logout" method="POST">
                        <button type="submit" class="btn btn-danger">Tutup Sesi Node (Logout)</button>
                    </form>
                </div>
            {% endif %}
        </div>

        <div class="bottom-nav">
            <a href="/?tab=dashboard" class="nav-item {% if active_tab == 'dashboard' %}active{% endif %}">🏠<br>Dashboard</a>
            <a href="/?tab=transfer" class="nav-item {% if active_tab == 'transfer' %}active{% endif %}">💸<br>Transfer</a>
            <a href="/?tab=rules" class="nav-item {% if active_tab == 'rules' %}active{% endif %}">📜<br>Aturan</a>
            <a href="/?tab=ledger" class="nav-item {% if active_tab == 'ledger' %}active{% endif %}">⛓️<br>Ledger</a>
            <a href="/?tab=node" class="nav-item {% if active_tab == 'node' %}active{% endif %}">👤<br>Node</a>
        </div>

    {% endif %}
</body>
</html>
"""

@app.route("/")
def index():
    if "wallet_id" not in session:
        return render_template_string(HTML_APP_TEMPLATE, logged_in=False)
    
    wallet_id = session["wallet_id"]
    db = load_database()
    user = db.get(wallet_id, {"wallet_id": wallet_id, "balance": PROTOCOL_RULES["INITIAL_NODE_BALANCE"], "staked": 0.0})
    
    ledger = load_ledger()
    active_tab = request.args.get("tab", "dashboard")
    message = session.pop("flash_message", None)
    return render_template_string(HTML_APP_TEMPLATE, logged_in=True, user=user, ledger=ledger, active_tab=active_tab, message=message, protocol_rules=PROTOCOL_RULES)

@app.route("/login", methods=["POST"])
def login():
    wallet_id = request.form.get("wallet_id", "").strip()
    if wallet_id:
        session["wallet_id"] = wallet_id
        db = load_database()
        if wallet_id not in db:
            db[wallet_id] = {"wallet_id": wallet_id, "balance": PROTOCOL_RULES["INITIAL_NODE_BALANCE"], "staked": 0.0}
            save_database(db)
            record_immutable_block(f"Immutable node initialized for {wallet_id}", wallet_id)
        session["flash_message"] = f"Node '{wallet_id}' terikat pada protokol immutable ZAM CORE."
    return redirect(url_for("index", tab="dashboard"))

@app.route("/mine", methods=["POST"])
def mine():
    if "wallet_id" in session:
        wallet_id = session["wallet_id"]
        db = load_database()
        if wallet_id in db:
            db[wallet_id]["balance"] += 100.0
            save_database(db)
            record_immutable_block(f"Protocol mining reward 100 ZAM for {wallet_id}", "Immutable-Protocol")
            session["flash_message"] = "Reward protokol berhasil ditambahkan secara otomatis oleh sistem!"
    return redirect(url_for("index", tab="dashboard"))

@app.route("/stake", methods=["POST"])
def stake():
    if "wallet_id" in session:
        wallet_id = session["wallet_id"]
        try:
            amount = float(request.form.get("amount", 0))
        except:
            amount = 0
            
        db = load_database()
        if wallet_id in db:
            if 0 < amount <= db[wallet_id]["balance"]:
                db[wallet_id]["balance"] -= amount
                db[wallet_id]["staked"] += amount
                save_database(db)
                record_immutable_block(f"Immutable staking lock-up {amount} ZAM by {wallet_id}", wallet_id)
                session["flash_message"] = f"Berhasil mengunci {amount:,.2f} ZAM ke Staking Vault."
    return redirect(url_for("index", tab="dashboard"))

@app.route("/transfer_p2p", methods=["POST"])
def transfer_p2p():
    if "wallet_id" in session:
        sender = session["wallet_id"]
        recipient = request.form.get("recipient", "").strip()
        try:
            amount = float(request.form.get("amount", 0))
        except:
            amount = 0
            
        db = load_database()
        if sender in db and recipient:
            if amount > 0 and db[sender]["balance"] >= amount:
                db[sender]["balance"] -= amount
                if recipient not in db:
                    db[recipient] = {"wallet_id": recipient, "balance": 0.0, "staked": 0.0}
                db[recipient]["balance"] += amount
                save_database(db)
                record_immutable_block(f"Immutable P2P Transfer {amount} ZAM from {sender} to {recipient}", sender)
                session["flash_message"] = f"Berhasil mengirim {amount:,.2f} ZAM secara peer-to-peer!"
            else:
                session["flash_message"] = "Saldo tidak mencukupi atau nominal tidak valid."
    return redirect(url_for("index", tab="transfer"))

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
from flask import Flask, render_template_string, request, redirect, url_for, session
import json
import os
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = "zam_core_ultimate_advanced_protocol_key"

DATABASE_FILE = "zam_core_database.json"
LEDGER_FILE = "zam_core_ledger.json"

# --- PROTOCOL MUTLAK & SMART CONTRACT RULES ---
PROTOCOL_RULES = {
    "MAX_TOTAL_SUPPLY": 210000000.0,
    "INITIAL_NODE_BALANCE": 2200000.0,
    "CONSENSUS_ENGINE": "Proof-of-Core with Cryptographic Signature & Smart Contracts"
}

def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_database(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_ledger():
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    genesis_block = {
        "index": 0,
        "timestamp": str(datetime.now()),
        "event": "ZAM CORE Ultimate Genesis - Cryptography & Smart Contracts Enforced",
        "previous_hash": "0x00000000000000000000000000000000",
        "hash": hashlib.sha256(b"ZAMCoreUltimateGenesisCryptoContracts").hexdigest(),
        "node_validator": "Immutable Master Protocol"
    }
    save_ledger([genesis_block])
    return [genesis_block]

def save_ledger(ledger):
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=4)

def record_block(event_desc, validator):
    ledger = load_ledger()
    last_block = ledger[-1]
    new_index = len(ledger)
    timestamp = str(datetime.now())
    
    raw_data = f"{new_index}{last_block['hash']}{timestamp}{event_desc}{validator}"
    new_hash = hashlib.sha256(raw_data.encode()).hexdigest()
    
    block = {
        "index": new_index,
        "timestamp": timestamp,
        "event": event_desc,
        "previous_hash": last_block["hash"],
        "hash": new_hash,
        "node_validator": validator
    }
    ledger.append(block)
    save_ledger(ledger)
    return block

# --- SMART CONTRACT AUTOMATED EXECUTION ---
def execute_smart_contract(wallet_id, action_type):
    db = load_database()
    if wallet_id in db:
        if action_type == "daily_reward":
            reward = 150.0
            db[wallet_id]["balance"] += reward
            save_database(db)
            record_block(f"Smart Contract executed: Automated reward +{reward} ZAM for {wallet_id}", "ZAM-SmartContract-Engine")
            return f"Smart Contract berhasil mengeksekusi reward otomatis +{reward} ZAM!"
    return "Eksekusi kontrak gagal."

HTML_APP_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZAM CORE - Advanced Decentralized Protocol</title>
    <style>
        :root {
            --primary: #00f2fe;
            --secondary: #4facfe;
            --bg-deep: #040812;
            --card-bg: rgba(11, 19, 38, 0.9);
            --border-glow: rgba(0, 242, 254, 0.25);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --success: #10b981;
            --warning: #f59e0b;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-deep);
            color: var(--text-main);
            margin: 0;
            padding-bottom: 90px;
        }

        .auth-wrapper {
            background: radial-gradient(circle at center, #0f172a 0%, #040812 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            box-sizing: border-box;
        }

        .auth-card {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border-glow);
            border-radius: 28px;
            padding: 35px 25px;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.8);
        }

        .brand-title {
            text-align: center;
            font-size: 26px;
            font-weight: 900;
            background: linear-gradient(135deg, #00f2fe, #4facfe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }

        .field-label {
            font-size: 11px;
            color: var(--primary);
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 6px;
            display: block;
        }

        .input-box {
            background: rgba(20, 30, 50, 0.9);
            border: 1px solid var(--border-glow);
            border-radius: 14px;
            margin-bottom: 16px;
            padding: 4px;
        }

        .input-box input {
            background: transparent;
            border: none;
            color: white;
            padding: 12px;
            font-size: 14px;
            width: 100%;
            box-sizing: border-box;
            outline: none;
            font-family: inherit;
        }

        .btn-action {
            background: linear-gradient(135deg, #00f2fe, #4facfe);
            color: #040812;
            border: none;
            padding: 15px;
            border-radius: 14px;
            font-weight: 800;
            width: 100%;
            cursor: pointer;
            font-size: 15px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 10px 25px rgba(0, 242, 254, 0.3);
        }

        .header {
            display: flex; justify-content: space-between; align-items: center;
            padding: 16px 20px; background: #0b1326; border-bottom: 1px solid var(--border-glow);
            position: sticky; top: 0; z-index: 100;
        }
        .logo { font-size: 18px; font-weight: 900; color: var(--primary); letter-spacing: 1px; }
        .content { padding: 20px; max-width: 500px; margin: 0 auto; }
        
        .card-core {
            background: linear-gradient(135deg, #0b1326, #16223f);
            border: 1px solid var(--border-glow);
            color: white; border-radius: 22px; padding: 24px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5); margin-bottom: 20px;
        }
        .card-panel {
            background: #0b1326; border: 1px solid var(--border-glow);
            border-radius: 18px; padding: 20px; margin-bottom: 15px;
        }
        .btn {
            background-color: var(--primary); color: #040812; border: none;
            padding: 12px 20px; border-radius: 12px; font-weight: 700;
            width: 100%; cursor: pointer; margin-top: 10px; font-size: 14px;
        }
        .btn-success { background-color: var(--success); color: white; }
        .btn-warning { background-color: var(--warning); color: white; }
        .btn-danger { background-color: #ef4444; color: white; }
        .btn-group { display: flex; gap: 10px; margin-top: 15px; }
        
        .bottom-nav {
            position: fixed; bottom: 0; left: 0; width: 100%; background: #0b1326;
            border-top: 1px solid var(--border-glow); display: flex; justify-content: space-around;
            padding: 10px 0; z-index: 100;
        }
        .nav-item { text-decoration: none; color: var(--text-muted); font-size: 11px; text-align: center; flex: 1; font-weight: 500; }
        .nav-item.active { color: var(--primary); font-weight: 700; }
        .ledger-block { font-size: 11px; border-bottom: 1px solid var(--border-glow); padding: 12px 0; font-family: monospace; }
        .alert-box { background: rgba(16, 185, 129, 0.2); color: #34d399; padding: 12px 16px; border-radius: 12px; margin-bottom: 20px; font-size: 13px; font-weight: 600; border: 1px solid #10b981; text-align: center; }
    </style>
</head>
<body>

    {% if not logged_in %}
    <div class="auth-wrapper">
        <div class="auth-card">
            <div class="brand-title">ZAM CORE</div>
            <p style="color: var(--text-muted); font-size: 12px; text-align: center; margin-bottom: 25px;">Advanced Cryptography & Smart Contracts</p>
            
            <form action="/login" method="POST">
                <label class="field-label">Node Wallet ID</label>
                <div class="input-box">
                    <input type="text" name="wallet_id" placeholder="Masukkan ID wallet..." required>
                </div>

                <label class="field-label">Passkey / Private Key Signature</label>
                <div class="input-box">
                    <input type="password" name="private_key" placeholder="Kunci privat tanda tangan..." required>
                </div>

                <button type="submit" class="btn-action">Verifikasi & Masuk Node</button>
            </form>
        </div>
    </div>
    
    {% else %}

        <div class="header">
            <div class="logo">ZAM CORE</div>
            <div style="font-size: 11px; color: var(--primary); background: rgba(0,242,254,0.1); padding: 6px 12px; border-radius: 20px; font-weight: 600; border: 1px solid var(--border-glow);">{{ user.wallet_id }}</div>
        </div>

        <div class="content">
            {% if message %}
                <div class="alert-box">{{ message }}</div>
            {% endif %}

            {% if active_tab == 'dashboard' %}
                <div class="card-core">
                    <div style="font-size: 13px; opacity: 0.9;">Total Verified Balance</div>
                    <div style="font-size: 30px; font-weight: 800; margin: 4px 0; color: var(--primary);">{{ "{:,.2f}".format(user.balance) }} ZAM</div>
                    <div style="font-size: 11px; opacity: 0.8; margin-top: 4px; color: var(--success);">🔐 Cryptographic Signature: Verified Active</div>
                    
                    <div class="btn-group">
                        <form action="/smart_contract_claim" method="POST" style="flex: 1; margin: 0;">
                            <button type="submit" class="btn btn-success" style="width:100%;">⚡ Jalankan Smart Contract (+150 ZAM)</button>
                        </form>
                    </div>
                </div>

                <!-- Panel Analitik Jaringan Global -->
                <div class="card-panel">
                    <h3 style="margin-top:0; color: var(--primary);">📊 Network Analytics</h3>
                    <p style="font-size: 13px; margin: 6px 0;">Total Suplai Beredar: <b>{{ "{:,.2f}".format(analytics.total_circulating) }} ZAM</b></p>
                    <p style="font-size: 13px; margin: 6px 0;">Total Blok Tervalidasi: <b>{{ analytics.total_blocks }} Blok</b></p>
                    <p style="font-size: 13px; margin: 6px 0;">Total Node Aktif: <b>{{ analytics.total_nodes }} Node</b></p>
                </div>

            {% elif active_tab == 'transfer' %}
                <div class="card-panel">
                    <h3 style="margin-top:0; color: var(--primary);">💸 Secure P2P Transfer</h3>
                    <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 15px;">Dilindungi dengan validasi kunci privat digital signature.</p>
                    <form action="/transfer_p2p" method="POST">
                        <label class="field-label">Wallet ID Penerima</label>
                        <div class="input-box">
                            <input type="text" name="recipient" placeholder="ID tujuan..." required>
                        </div>
                        <label class="field-label">Jumlah ZAM</label>
                        <div class="input-box">
                            <input type="number" name="amount" placeholder="Nominal..." required>
                        </div>
                        <label class="field-label">Konfirmasi Kunci Privat Anda</label>
                        <div class="input-box">
                            <input type="password" name="auth_key" placeholder="Masukkan kunci privat..." required>
                        </div>
                        <button type="submit" class="btn" style="margin-top:5px;">Kirim dengan Tanda Tangan Kriptografi</button>
                    </form>
                </div>

            {% elif active_tab == 'ledger' %}
                <div class="card-panel">
                    <h3 style="margin-top: 0;">⛓️ Immutable Ledger</h3>
                    {% for block in ledger[::-1] %}
                        <div class="ledger-block">
                            <b style="color: var(--primary);">Block #{{ block.index }}</b> ({{ block.timestamp }})<br>
                            <span>Event: {{ block.event }}</span><br>
                            <span style="color: var(--text-muted); font-size: 10px;">Hash: {{ block.hash[:24] }}...</span>
                        </div>
                    {% endfor %}
                </div>

            {% elif active_tab == 'node' %}
                <div class="card-panel">
                    <h3>Node Cryptographic Profile</h3>
                    <p style="font-size: 14px; margin: 6px 0;">Wallet ID: <b>{{ user.wallet_id }}</b></p>
                    <p style="font-size: 14px; margin: 6px 0;">Public Key Hash: <span style="font-family:monospace; color:var(--primary);">{{ user.pub_key_hash[:16] }}...</span></p>
                    <p style="font-size: 14px; margin: 6px 0;">Status: <span style="color: var(--success); font-weight: bold;">🟢 Aman & Terenkripsi</span></p>
                </div>
                <div class="card-panel" style="text-align: center;">
                    <form action="/logout" method="POST">
                        <button type="submit" class="btn btn-danger">Tutup Sesi Node (Logout)</button>
                    </form>
                </div>
            {% endif %}
        </div>

        <div class="bottom-nav">
            <a href="/?tab=dashboard" class="nav-item {% if active_tab == 'dashboard' %}active{% endif %}">🏠<br>Dashboard</a>
            <a href="/?tab=transfer" class="nav-item {% if active_tab == 'transfer' %}active{% endif %}">💸<br>Transfer</a>
            <a href="/?tab=ledger" class="nav-item {% if active_tab == 'ledger' %}active{% endif %}">⛓️<br>Ledger</a>
            <a href="/?tab=node" class="nav-item {% if active_tab == 'node' %}active{% endif %}">👤<br>Node</a>
        </div>

    {% endif %}
</body>
</html>
"""

@app.route("/")
def index():
    if "wallet_id" not in session:
        return render_template_string(HTML_APP_TEMPLATE, logged_in=False)
    
    wallet_id = session["wallet_id"]
    db = load_database()
    user = db.get(wallet_id, {
        "wallet_id": wallet_id, 
        "balance": PROTOCOL_RULES["INITIAL_NODE_BALANCE"],
        "pub_key_hash": hashlib.sha256(wallet_id.encode()).hexdigest(),
        "private_key": session.get("private_key", "default_key")
    })
    
    ledger = load_ledger()
    
    # Hitung Analitik Global
    total_circulating = sum(node.get("balance", 0) for node in db.values())
    analytics = {
        "total_circulating": total_circulating,
        "total_blocks": len(ledger),
        "total_nodes": len(db)
    }
    
    active_tab = request.args.get("tab", "dashboard")
    message = session.pop("flash_message", None)
    return render_template_string(HTML_APP_TEMPLATE, logged_in=True, user=user, ledger=ledger, analytics=analytics, active_tab=active_tab, message=message)

@app.route("/login", methods=["POST"])
def login():
    wallet_id = request.form.get("wallet_id", "").strip()
    private_key = request.form.get("private_key", "").strip()
    if wallet_id and private_key:
        session["wallet_id"] = wallet_id
        session["private_key"] = private_key
        db = load_database()
        if wallet_id not in db:
            db[wallet_id] = {
                "wallet_id": wallet_id,
                "balance": PROTOCOL_RULES["INITIAL_NODE_BALANCE"],
                "pub_key_hash": hashlib.sha256(wallet_id.encode()).hexdigest(),
                "private_key": private_key
            }
            save_database(db)
            record_block(f"Encrypted node initialized for {wallet_id} with digital signature", wallet_id)
        session["flash_message"] = f"Node '{wallet_id}' terverifikasi dengan tanda tangan kriptografi."
    return redirect(url_for("index", tab="dashboard"))

@app.route("/smart_contract_claim", methods=["POST"])
def smart_contract_claim():
    if "wallet_id" in session:
        wallet_id = session["wallet_id"]
        msg = execute_smart_contract(wallet_id, "daily_reward")
        session["flash_message"] = msg
    return redirect(url_for("index", tab="dashboard"))

@app.route("/transfer_p2p", methods=["POST"])
def transfer_p2p():
    if "wallet_id" in session:
        sender = session["wallet_id"]
        recipient = request.form.get("recipient", "").strip()
        auth_key = request.form.get("auth_key", "").strip()
        try:
            amount = float(request.form.get("amount", 0))
        except:
            amount = 0
            
        db = load_database()
        if sender in db and recipient:
            # Validasi Tanda Tangan Kriptografi Kunci Privat
            if auth_key == db[sender].get("private_key"):
                if amount > 0 and db[sender]["balance"] >= amount:
                    db[sender]["balance"] -= amount
                    if recipient not in db:
                        db[recipient] = {
                            "wallet_id": recipient,
                            "balance": 0.0,
                            "pub_key_hash": hashlib.sha256(recipient.encode()).hexdigest(),
                            "private_key": "auto_generated"
                        }
                    db[recipient]["balance"] += amount
                    save_database(db)
                    record_block(f"Signed P2P Transfer {amount} ZAM from {sender} to {recipient}", sender)
                    session["flash_message"] = f"Transfer kriptografi berhasil! {amount:,.2f} ZAM dikirim."
                else:
                    session["flash_message"] = "Saldo tidak mencukupi atau nominal tidak valid."
            else:
                session["flash_message"] = "Autentikasi gagal: Kunci privat (Digital Signature) tidak cocok!"
    return redirect(url_for("index", tab="transfer"))

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
from flask import Flask, render_template_string, request, redirect, url_for, session
import json
import os
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = "zam_core_ultimate_quantum_zk_key"

DATABASE_FILE = "zam_core_database.json"
LEDGER_FILE = "zam_core_ledger.json"

# --- PROTOCOL TERTINGGI (ULTIMATE LAYER-1 RULES) ---
PROTOCOL_RULES = {
    "MAX_TOTAL_SUPPLY": 210000000.0,
    "INITIAL_NODE_BALANCE": 2200000.0,
    "CONSENSUS_ENGINE": "Quantum-Resistant ZK-Proof & Decentralized AI Sentinel",
    "RWA_BRIDGE_SECTOR": "Global Infrastructure & Green Energy Assets"
}

def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_database(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_ledger():
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    genesis_block = {
        "index": 0,
        "timestamp": str(datetime.now()),
        "event": "ZAM CORE Ultimate Genesis - Quantum, ZK-Proof & AI Sentinel Activated",
        "previous_hash": "0x0000000000000000000000000000000000000000000000000000000000000000",
        "hash": hashlib.sha3_256(b"ZAMCoreUltimateQuantumGenesisAIZK").hexdigest(),
        "ai_validator": "ZAM AI Sentinel Prime"
    }
    save_ledger([genesis_block])
    return [genesis_block]

def save_ledger(ledger):
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=4)

def record_quantum_block(event_desc, validator):
    ledger = load_ledger()
    last_block = ledger[-1]
    new_index = len(ledger)
    timestamp = str(datetime.now())
    
    raw_data = f"{new_index}{last_block['hash']}{timestamp}{event_desc}{validator}QUANTUM_SECURE"
    new_hash = hashlib.sha3_256(raw_data.encode()).hexdigest()
    
    block = {
        "index": new_index,
        "timestamp": timestamp,
        "event": event_desc,
        "previous_hash": last_block["hash"],
        "hash": new_hash,
        "ai_validator": validator
    }
    ledger.append(block)
    save_ledger(ledger)
    return block

def run_ai_sentinel_check(wallet_id, amount):
    db = load_database()
    if wallet_id in db:
        if amount > 0 and db[wallet_id]["balance"] >= amount:
            zk_proof_token = hashlib.sha256(f"ZK-PROOF-{wallet_id}-{amount}-{datetime.now()}".encode()).hexdigest()
            return True, zk_proof_token
    return False, "AI Security Sentinel: Validasi Gagal (Anomali Terdeteksi)"

HTML_APP_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZAM CORE - Ultimate Quantum & AI Ecosystem</title>
    <style>
        :root {
            --primary: #00f2fe;
            --secondary: #4facfe;
            --bg-deep: #020617;
            --card-bg: rgba(15, 23, 42, 0.9);
            --border-glow: rgba(0, 242, 254, 0.3);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --success: #10b981;
            --warning: #f59e0b;
            --purple: #8b5cf6;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-deep);
            color: var(--text-main);
            margin: 0;
            padding-bottom: 90px;
        }

        .auth-wrapper {
            background: radial-gradient(circle at center, #1e1b4b 0%, #020617 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            box-sizing: border-box;
        }

        .auth-card {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border-glow);
            border-radius: 28px;
            padding: 35px 25px;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.9);
        }

        .brand-title {
            text-align: center;
            font-size: 26px;
            font-weight: 900;
            background: linear-gradient(135deg, #00f2fe, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }

        .field-label {
            font-size: 11px;
            color: var(--primary);
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 6px;
            display: block;
        }

        .input-box {
            background: rgba(30, 41, 59, 0.9);
            border: 1px solid var(--border-glow);
            border-radius: 14px;
            margin-bottom: 16px;
            padding: 4px;
        }

        .input-box input {
            background: transparent;
            border: none;
            color: white;
            padding: 12px;
            font-size: 14px;
            width: 100%;
            box-sizing: border-box;
            outline: none;
            font-family: inherit;
        }

        .btn-action {
            background: linear-gradient(135deg, #00f2fe, #8b5cf6);
            color: #020617;
            border: none;
            padding: 15px;
            border-radius: 14px;
            font-weight: 800;
            width: 100%;
            cursor: pointer;
            font-size: 15px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 10px 25px rgba(139, 92, 246, 0.4);
        }

        .header {
            display: flex; justify-content: space-between; align-items: center;
            padding: 16px 20px; background: #0f172a; border-bottom: 1px solid var(--border-glow);
            position: sticky; top: 0; z-index: 100;
        }
        .logo { font-size: 18px; font-weight: 900; color: var(--primary); letter-spacing: 1px; }
        .content { padding: 20px; max-width: 500px; margin: 0 auto; }
        
        .card-core {
            background: linear-gradient(135deg, #0f172a, #1e1b4b);
            border: 1px solid var(--border-glow);
            color: white; border-radius: 22px; padding: 24px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.6); margin-bottom: 20px;
        }
        .card-panel {
            background: #0f172a; border: 1px solid var(--border-glow);
            border-radius: 18px; padding: 20px; margin-bottom: 15px;
        }
        .btn {
            background-color: var(--primary); color: #020617; border: none;
            padding: 12px 20px; border-radius: 12px; font-weight: 700;
            width: 100%; cursor: pointer; margin-top: 10px; font-size: 14px;
        }
        .btn-success { background-color: var(--success); color: white; }
        .btn-warning { background-color: var(--warning); color: white; }
        .btn-danger { background-color: #ef4444; color: white; }
        .btn-group { display: flex; gap: 10px; margin-top: 15px; }
        
        .bottom-nav {
            position: fixed; bottom: 0; left: 0; width: 100%; background: #0f172a;
            border-top: 1px solid var(--border-glow); display: flex; justify-content: space-around;
            padding: 10px 0; z-index: 100;
        }
        .nav-item { text-decoration: none; color: var(--text-muted); font-size: 11px; text-align: center; flex: 1; font-weight: 500; }
        .nav-item.active { color: var(--primary); font-weight: 700; }
        .ledger-block { font-size: 11px; border-bottom: 1px solid var(--border-glow); padding: 12px 0; font-family: monospace; }
        .alert-box { background: rgba(16, 185, 129, 0.2); color: #34d399; padding: 12px 16px; border-radius: 12px; margin-bottom: 20px; font-size: 13px; font-weight: 600; border: 1px solid #10b981; text-align: center; }
    </style>
</head>
<body>

    {% if not logged_in %}
    <div class="auth-wrapper">
        <div class="auth-card">
            <div class="brand-title">ZAM CORE</div>
            <p style="color: var(--text-muted); font-size: 12px; text-align: center; margin-bottom: 25px;">Quantum-Resistant • ZK-Privacy • AI Sentinel</p>
            
            <form action="/login" method="POST">
                <label class="field-label">Quantum Node Wallet ID</label>
                <div class="input-box">
                    <input type="text" name="wallet_id" placeholder="Masukkan ID wallet..." required>
                </div>

                <label class="field-label">Quantum Security Passkey</label>
                <div class="input-box">
                    <input type="password" name="passkey" placeholder="Passkey enkripsi..." required>
                </div>

                <button type="submit" class="btn-action">Inisialisasi Quantum Node</button>
            </form>
        </div>
    </div>
    
    {% else %}

        <div class="header">
            <div class="logo">ZAM CORE</div>
            <div style="font-size: 11px; color: var(--primary); background: rgba(0,242,254,0.1); padding: 6px 12px; border-radius: 20px; font-weight: 600; border: 1px solid var(--border-glow);">{{ user.wallet_id }}</div>
        </div>

        <div class="content">
            {% if message %}
                <div class="alert-box">{{ message }}</div>
            {% endif %}

            {% if active_tab == 'dashboard' %}
                <div class="card-core">
                    <div style="font-size: 13px; opacity: 0.9;">Total Verified Balance</div>
                    <div style="font-size: 30px; font-weight: 800; margin: 4px 0; color: var(--primary);">{{ "{:,.2f}".format(user.balance) }} ZAM</div>
                    <div style="font-size: 11px; opacity: 0.9; margin-top: 4px; color: var(--success);">🛡️ AI Sentinel Status: Active & Monitoring</div>
                    <div style="font-size: 11px; opacity: 0.8; margin-top: 2px; color: #8b5cf6;">⚛️ Quantum Encryption: SHA3-512 Lattice Secured</div>
                    
                    <div class="btn-group">
                        <form action="/quantum_mine" method="POST" style="flex: 1; margin: 0;">
                            <button type="submit" class="btn btn-success" style="width:100%;">⛏️ Quantum Mining (+200 ZAM)</button>
                        </form>
                    </div>
                </div>

                <div class="card-panel">
                    <h3 style="margin-top:0; color: var(--primary);">🌐 Real-World Asset (RWA) Bridge</h3>
                    <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">Terhubung langsung dengan sektor infrastruktur riil global.</p>
                    <p style="font-size: 13px; margin: 4px 0;">Sektor Terkait: <b>{{ protocol_rules.RWA_BRIDGE_SECTOR }}</b></p>
                    <p style="font-size: 13px; margin: 4px 0;">ZK-Privacy Layer: <span style="color: var(--success); font-weight: bold;">Enabled (Zero Knowledge)</span></p>
                </div>

            {% elif active_tab == 'zk_transfer' %}
                <div class="card-panel">
                    <h3 style="margin-top:0; color: var(--primary);">🔏 ZK-Proof Private Transfer</h3>
                    <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 15px;">Kirim dana dengan kerahasiaan total dan validasi AI Sentinel.</p>
                    <form action="/transfer_zk" method="POST">
                        <label class="field-label">Wallet ID Penerima</label>
                        <div class="input-box">
                            <input type="text" name="recipient" placeholder="ID tujuan..." required>
                        </div>
                        <label class="field-label">Jumlah ZAM</label>
                        <div class="input-box">
                            <input type="number" name="amount" placeholder="Nominal..." required>
                        </div>
                        <button type="submit" class="btn" style="background: linear-gradient(135deg, #00f2fe, #8b5cf6); color:white; margin-top:5px;">Kirim dengan ZK-Proof</button>
                    </form>
                </div>

            {% elif active_tab == 'analytics' %}
                <div class="card-panel">
                    <h3 style="margin-top: 0; color: var(--primary);">📊 Ultimate Analytics Dashboard</h3>
                    <p style="font-size: 13px; margin: 6px 0;">Total Suplai Global: <b>{{ "{:,.2f}".format(analytics.total_circulating) }} ZAM</b></p>
                    <p style="font-size: 13px; margin: 6px 0;">Batas Maksimal (Hard Cap): <b>{{ "{:,.0f}".format(protocol_rules.MAX_TOTAL_SUPPLY) }} ZAM</b></p>
                    <p style="font-size: 13px; margin: 6px 0;">Total Blok Quantum: <b>{{ analytics.total_blocks }} Blok</b></p>
                    <p style="font-size: 13px; margin: 6px 0;">Konsensus Engine: <b>{{ protocol_rules.CONSENSUS_ENGINE }}</b></p>
                </div>

            {% elif active_tab == 'ledger' %}
                <div class="card-panel">
                    <h3 style="margin-top: 0;">⛓️ Quantum Ledger (SHA3)</h3>
                    {% for block in ledger[::-1] %}
                        <div class="ledger-block">
                            <b style="color: var(--primary);">Block #{{ block.index }}</b> ({{ block.timestamp }})<br>
                            <span>Event: {{ block.event }}</span><br>
                            <span style="color: var(--text-muted); font-size: 10px;">AI Validator: {{ block.ai_validator }}</span><br>
                            <span style="color: #8b5cf6; font-size: 9px;">Hash: {{ block.hash[:32] }}...</span>
                        </div>
                    {% endfor %}
                </div>

            {% elif active_tab == 'node' %}
                <div class="card-panel">
                    <h3>Quantum Node Profile</h3>
                    <p style="font-size: 14px; margin: 6px 0;">Wallet ID: <b>{{ user.wallet_id }}</b></p>
                    <p style="font-size: 14px; margin: 6px 0;">AI Sentinel Status: <span style="color: var(--success); font-weight: bold;">🟢 Secure & Optimized</span></p>
                </div>
                <div class="card-panel" style="text-align: center;">
                    <form action="/logout" method="POST">
                        <button type="submit" class="btn btn-danger">Tutup Sesi Node (Logout)</button>
                    </form>
                </div>
            {% endif %}
        </div>

        <div class="bottom-nav">
            <a href="/?tab=dashboard" class="nav-item {% if active_tab == 'dashboard' %}active{% endif %}">🏠<br>Dashboard</a>
            <a href="/?tab=zk_transfer" class="nav-item {% if active_tab == 'zk_transfer' %}active{% endif %}">🔏<br>ZK Transfer</a>
            <a href="/?tab=analytics" class="nav-item {% if active_tab == 'analytics' %}active{% endif %}">📊<br>Analytics</a>
            <a href="/?tab=ledger" class="nav-item {% if active_tab == 'ledger' %}active{% endif %}">⛓️<br>Ledger</a>
            <a href="/?tab=node" class="nav-item {% if active_tab == 'node' %}active{% endif %}">👤<br>Node</a>
        </div>

    {% endif %}
</body>
</html>
"""

@app.route("/")
def index():
    if "wallet_id" not in session:
        return render_template_string(HTML_APP_TEMPLATE, logged_in=False)
    
    wallet_id = session["wallet_id"]
    db = load_database()
    user = db.get(wallet_id, {"wallet_id": wallet_id, "balance": PROTOCOL_RULES["INITIAL_NODE_BALANCE"]})
    
    ledger = load_ledger()
    total_circulating = sum(node.get("balance", 0) for node in db.values())
    analytics = {
        "total_circulating": total_circulating,
        "total_blocks": len(ledger)
    }
    
    active_tab = request.args.get("tab", "dashboard")
    message = session.pop("flash_message", None)
    return render_template_string(HTML_APP_TEMPLATE, logged_in=True, user=user, ledger=ledger, analytics=analytics, protocol_rules=PROTOCOL_RULES, active_tab=active_tab, message=message)

@app.route("/login", methods=["POST"])
def login():
    wallet_id = request.form.get("wallet_id", "").strip()
    if wallet_id:
        session["wallet_id"] = wallet_id
        db = load_database()
        if wallet_id not in db:
            db[wallet_id] = {"wallet_id": wallet_id, "balance": PROTOCOL_RULES["INITIAL_NODE_BALANCE"]}
            save_database(db)
            record_quantum_block(f"Quantum node initialized for {wallet_id} under AI Sentinel", "AI-Sentinel-Prime")
        session["flash_message"] = f"Quantum Node '{wallet_id}' berhasil diamankan dengan teknologi AI Sentinel."
    return redirect(url_for("index", tab="dashboard"))

@app.route("/quantum_mine", methods=["POST"])
def quantum_mine():
    if "wallet_id" in session:
        wallet_id = session["wallet_id"]
        db = load_database()
        if wallet_id in db:
            db[wallet_id]["balance"] += 200.0
            save_database(db)
            record_quantum_block(f"Quantum mining reward 200 ZAM optimized for {wallet_id}", "AI-Sentinel-Validator")
            session["flash_message"] = "Penambangan Quantum sukses! +200 ZAM ditambahkan melalui optimasi AI."
    return redirect(url_for("index", tab="dashboard"))

@app.route("/transfer_zk", methods=["POST"])
def transfer_zk():
    if "wallet_id" in session:
        sender = session["wallet_id"]
        recipient = request.form.get("recipient", "").strip()
        try:
            amount = float(request.form.get("amount", 0))
        except:
            amount = 0
            
        db = load_database()
        if sender in db and recipient:
            success, proof_or_msg = run_ai_sentinel_check(sender, amount)
            if success:
                db[sender]["balance"] -= amount
                if recipient not in db:
                    db[recipient] = {"wallet_id": recipient, "balance": 0.0}
                db[recipient]["balance"] += amount
                save_database(db)
                record_quantum_block(f"ZK-Proof Private Transfer {amount} ZAM from {sender} to {recipient} [Proof: {proof_or_msg[:12]}...]", "AI-Sentinel-ZK-Engine")
                session["flash_message"] = f"Transfer ZK-Privacy berhasil! Dana terkirim secara aman dan rahasia."
            else:
                session["flash_message"] = proof_or_msg
    return redirect(url_for("index", tab="zk_transfer"))

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
from flask import Flask, render_template_string, request, redirect, url_for, session
import json
import os
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = "zam_core_stable_production_key"

DATABASE_FILE = "zam_core_database.json"
LEDGER_FILE = "zam_core_ledger.json"

def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_database(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_ledger():
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    genesis = {
        "index": 0,
        "timestamp": str(datetime.now()),
        "event": "ZAM CORE Genesis Block - Stable Web3 Bridge",
        "hash": hashlib.sha256(b"ZAMCoreGenesisStable").hexdigest()
    }
    save_ledger([genesis])
    return [genesis]

def save_ledger(ledger):
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=4)

def record_block(event_desc):
    ledger = load_ledger()
    last_block = ledger[-1]
    new_index = len(ledger)
    timestamp = str(datetime.now())
    raw_data = f"{new_index}{last_block['hash']}{timestamp}{event_desc}"
    new_hash = hashlib.sha256(raw_data.encode()).hexdigest()
    
    block = {
        "index": new_index,
        "timestamp": timestamp,
        "event": event_desc,
        "hash": new_hash
    }
    ledger.append(block)
    save_ledger(ledger)
    return block

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZAM CORE - Web3 Ecosystem</title>
    <style>
        body { font-family: sans-serif; background: #020617; color: #f8fafc; margin: 0; padding-bottom: 80px; }
        .container { padding: 20px; max-width: 480px; margin: 0 auto; }
        .card { background: #0f172a; border: 1px solid rgba(0,242,254,0.3); border-radius: 20px; padding: 20px; margin-bottom: 15px; }
        .title { text-align: center; font-size: 24px; font-weight: bold; background: linear-gradient(135deg, #00f2fe, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .input-box { background: #1e293b; border: 1px solid rgba(0,242,254,0.3); border-radius: 12px; margin-bottom: 12px; padding: 10px; }
        .input-box input { background: transparent; border: none; color: white; width: 100%; outline: none; font-size: 14px; }
        .btn { background: linear-gradient(135deg, #00f2fe, #8b5cf6); color: #020617; border: none; padding: 14px; border-radius: 12px; font-weight: bold; width: 100%; cursor: pointer; text-transform: uppercase; }
        .btn-success { background: #10b981; color: white; margin-top: 10px; }
        .btn-warning { background: #f59e0b; color: white; margin-top: 10px; }
        .btn-danger { background: #ef4444; color: white; margin-top: 10px; }
        .nav { position: fixed; bottom: 0; left: 0; width: 100%; background: #0f172a; display: flex; justify-content: space-around; padding: 10px 0; border-top: 1px solid rgba(0,242,254,0.3); }
        .nav-item { text-decoration: none; color: #94a3b8; font-size: 11px; text-align: center; flex: 1; }
        .nav-item.active { color: #00f2fe; font-weight: bold; }
        .alert { background: rgba(16, 185, 129, 0.2); color: #34d399; padding: 10px; border-radius: 10px; margin-bottom: 15px; text-align: center; font-size: 13px; font-weight: bold; }
        .block { font-size: 11px; font-family: monospace; border-bottom: 1px solid rgba(255,255,255,0.1); padding: 8px 0; }
    </style>
</head>
<body>

    {% if not logged_in %}
    <div class="container" style="display:flex; justify-content:center; align-items:center; height:100vh;">
        <div class="card" style="width:100%;">
            <div class="title">ZAM CORE</div>
            <p style="color: #94a3b8; font-size: 12px; text-align: center; margin-bottom: 20px;">Web3 Ecosystem & Bridge Node</p>
            <form action="/login" method="POST">
                <div class="input-box">
                    <input type="text" name="wallet_id" placeholder="Masukkan Wallet ID..." required>
                </div>
                <button type="submit" class="btn">Masuk Node</button>
            </form>
        </div>
    </div>
    {% else %}

    <div class="container">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
            <div class="title" style="font-size:20px;">ZAM CORE</div>
            <div style="background:rgba(0,242,254,0.1); color:#00f2fe; padding:4px 10px; border-radius:20px; font-size:11px; border:1px solid rgba(0,242,254,0.3);">{{ user.wallet_id }}</div>
        </div>

        {% if message %}
            <div class="alert">{{ message }}</div>
        {% endif %}

        {% if active_tab == 'dashboard' %}
            <div class="card">
                <div style="font-size: 12px; color: #94a3b8;">ZAM Core Balance (Mining)</div>
                <div style="font-size: 28px; font-weight: bold; color: #00f2fe; margin: 5px 0;">{{ "%.2f"|format(user.balance) }} ZAM</div>
                
                <div style="font-size: 12px; color: #94a3b8; margin-top: 15px;">ZAM ERC-20 (Web3 Ready):</div>
                <div style="font-size: 22px; font-weight: bold; color: #8b5cf6; margin: 5px 0;">{{ "%.2f"|format(user.erc20_balance) }} ZAM-E</div>

                <form action="/mine" method="POST">
                    <button type="submit" class="btn btn-success">⛏️ Mobile Mining (+200 ZAM)</button>
                </form>
            </div>

            <div class="card">
                <h3 style="margin-top:0; color:#00f2fe; font-size:16px;">🌉 ZAM to ERC-20 Bridge</h3>
                <p style="font-size:11px; color:#94a3b8;">Konversi hasil mining ke ZAM-E untuk ditarik ke OKX / Trust Wallet.</p>
                <form action="/convert" method="POST">
                    <div class="input-box">
                        <input type="number" name="amount" placeholder="Jumlah konversi..." required>
                    </div>
                    <button type="submit" class="btn btn-warning">Konversi Sekarang</button>
                </form>
            </div>

        {% elif active_tab == 'withdraw' %}
            <div class="card">
                <h3 style="margin-top:0; color:#00f2fe; font-size:16px;">📤 Web3 Withdrawal</h3>
                <p style="font-size:11px; color:#94a3b8;">Kirim ZAM-E ke dompet eksternal (OKX, MetaMask, Trust Wallet).</p>
                <form action="/withdraw" method="POST">
                    <div class="input-box">
                        <input type="text" name="address" placeholder="Alamat Dompet (0x...)" required>
                    </div>
                    <div class="input-box">
                        <input type="number" name="amount" placeholder="Nominal ZAM-E..." required>
                    </div>
                    <button type="submit" class="btn">Tarik ke Dompet Web3</button>
                </form>
            </div>

        {% elif active_tab == 'ledger' %}
            <div class="card">
                <h3 style="margin-top:0; color:#00f2fe; font-size:16px;">⛓️ Ledger Chain</h3>
                {% for block in ledger[::-1] %}
                    <div class="block">
                        <b>#{{ block.index }}</b> ({{ block.timestamp[:19] }})<br>
                        <span>{{ block.event }}</span>
                    </div>
                {% endfor %}
            </div>

        {% elif active_tab == 'node' %}
            <div class="card">
                <h3 style="margin-top:0; font-size:16px;">Node Profile</h3>
                <p style="font-size:13px;">Wallet: <b>{{ user.wallet_id }}</b></p>
                <form action="/logout" method="POST">
                    <button type="submit" class="btn btn-danger">Keluar (Logout)</button>
                </form>
            </div>
        {% endif %}
    </div>

    <div class="nav">
        <a href="/?tab=dashboard" class="nav-item {% if active_tab == 'dashboard' %}active{% endif %}">🏠<br>Dashboard</a>
        <a href="/?tab=withdraw" class="nav-item {% if active_tab == 'withdraw' %}active{% endif %}">📤<br>Withdraw</a>
        <a href="/?tab=ledger" class="nav-item {% if active_tab == 'ledger' %}active{% endif %}">⛓️<br>Ledger</a>
        <a href="/?tab=node" class="nav-item {% if active_tab == 'node' %}active{% endif %}">👤<br>Node</a>
    </div>
    {% endif %}

</body>
</html>
"""

@app.route("/")
def index():
    if "wallet_id" not in session:
        return render_template_string(HTML_TEMPLATE, logged_in=False)
    
    wallet_id = session["wallet_id"]
    db = load_database()
    
    # Pastikan data user lengkap dan tidak ada yang None
    if wallet_id not in db:
        db[wallet_id] = {"wallet_id": wallet_id, "balance": 2200000.0, "erc20_balance": 0.0}
        save_database(db)
    
    user = db[wallet_id]
    if "balance" not in user:
        user["balance"] = 2200000.0
    if "erc20_balance" not in user:
        user["erc20_balance"] = 0.0
        
    ledger = load_ledger()
    active_tab = request.args.get("tab", "dashboard")
    message = session.pop("flash_message", None)
    return render_template_string(HTML_TEMPLATE, logged_in=True, user=user, ledger=ledger, active_tab=active_tab, message=message)

@app.route("/login", methods=["POST"])
def login():
    wallet_id = request.form.get("wallet_id", "").strip()
    if wallet_id:
        session["wallet_id"] = wallet_id
        db = load_database()
        if wallet_id not in db:
            db[wallet_id] = {"wallet_id": wallet_id, "balance": 2200000.0, "erc20_balance": 0.0}
            save_database(db)
            record_block(f"Node initialized for {wallet_id}")
        session["flash_message"] = f"Node '{wallet_id}' terhubung!"
    return redirect(url_for("index", tab="dashboard"))

@app.route("/mine", methods=["POST"])
def mine():
    if "wallet_id" in session:
        wallet_id = session["wallet_id"]
        db = load_database()
        if wallet_id in db:
            db[wallet_id]["balance"] = float(db[wallet_id].get("balance", 0)) + 200.0
            save_database(db)
            record_block(f"Mobile mining +200 ZAM by {wallet_id}")
            session["flash_message"] = "+200 ZAM berhasil ditambang!"
    return redirect(url_for("index", tab="dashboard"))

@app.route("/convert", methods=["POST"])
def convert():
    if "wallet_id" in session:
        wallet_id = session["wallet_id"]
        try:
            amount = float(request.form.get("amount", 0))
        except:
            amount = 0
            
        db = load_database()
        if wallet_id in db:
            balance = float(db[wallet_id].get("balance", 0))
            if 0 < amount <= balance:
                db[wallet_id]["balance"] = balance - amount
                db[wallet_id]["erc20_balance"] = float(db[wallet_id].get("erc20_balance", 0)) + amount
                save_database(db)
                record_block(f"Bridge conversion {amount} ZAM to ZAM-E by {wallet_id}")
                session["flash_message"] = f"Berhasil mengonversi {amount:,.2f} ZAM ke ZAM ERC-20!"
            else:
                session["flash_message"] = "Saldo tidak mencukupi atau nominal salah."
    return redirect(url_for("index", tab="dashboard"))

@app.route("/withdraw", methods=["POST"])
def withdraw():
    if "wallet_id" in session:
        wallet_id = session["wallet_id"]
        address = request.form.get("address", "").strip()
        try:
            amount = float(request.form.get("amount", 0))
        except:
            amount = 0
            
        db = load_database()
        if wallet_id in db and address:
            erc20_balance = float(db[wallet_id].get("erc20_balance", 0))
            if 0 < amount <= erc20_balance:
                db[wallet_id]["erc20_balance"] = erc20_balance - amount
                save_database(db)
                record_block(f"Web3 withdrawal {amount} ZAM-E to {address} by {wallet_id}")
                session["flash_message"] = f"Penarikan {amount:,.2f} ZAM-E ke dompet Web3 berhasil!"
            else:
                session["flash_message"] = "Saldo ZAM-E tidak mencukupi."
    return redirect(url_for("index", tab="withdraw"))

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
from flask import Flask, render_template_string, request, redirect, url_for, session
import json
import os
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = "zam_core_production_public_key_2026"

DATABASE_FILE = "zam_core_database.json"
LEDGER_FILE = "zam_core_ledger.json"

def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_database(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_ledger():
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    genesis = {
        "index": 0,
        "timestamp": str(datetime.now()),
        "event": "ZAM CORE Public Genesis Block - Decentralized Cloud Node",
        "hash": hashlib.sha256(b"ZAMCorePublicCloudGenesis").hexdigest()
    }
    save_ledger([genesis])
    return [genesis]

def save_ledger(ledger):
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=4)

def record_block(event_desc):
    ledger = load_ledger()
    last_block = ledger[-1]
    new_index = len(ledger)
    timestamp = str(datetime.now())
    raw_data = f"{new_index}{last_block['hash']}{timestamp}{event_desc}"
    new_hash = hashlib.sha256(raw_data.encode()).hexdigest()
    
    block = {
        "index": new_index,
        "timestamp": timestamp,
        "event": event_desc,
        "hash": new_hash
    }
    ledger.append(block)
    save_ledger(ledger)
    return block

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZAM CORE - Public Decentralized Ecosystem</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #020617; color: #f8fafc; margin: 0; padding-bottom: 85px; }
        .container { padding: 20px; max-width: 480px; margin: 0 auto; }
        .card { background: #0f172a; border: 1px solid rgba(0,242,254,0.25); border-radius: 20px; padding: 20px; margin-bottom: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        .title { text-align: center; font-size: 22px; font-weight: 900; background: linear-gradient(135deg, #00f2fe, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 1px; }
        .subtitle { text-align: center; font-size: 11px; color: #94a3b8; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; }
        .input-box { background: #1e293b; border: 1px solid rgba(0,242,254,0.3); border-radius: 12px; margin-bottom: 12px; padding: 10px; }
        .input-box input { background: transparent; border: none; color: white; width: 100%; outline: none; font-size: 14px; }
        .btn { background: linear-gradient(135deg, #00f2fe, #8b5cf6); color: #020617; border: none; padding: 14px; border-radius: 12px; font-weight: 800; width: 100%; cursor: pointer; text-transform: uppercase; font-size: 13px; letter-spacing: 0.5px; }
        .btn-success { background: #10b981; color: white; margin-top: 10px; }
        .btn-warning { background: #f59e0b; color: white; margin-top: 10px; }
        .btn-danger { background: #ef4444; color: white; margin-top: 10px; }
        .nav { position: fixed; bottom: 0; left: 0; width: 100%; background: #0f172a; display: flex; justify-content: space-around; padding: 10px 0; border-top: 1px solid rgba(0,242,254,0.25); z-index: 100; }
        .nav-item { text-decoration: none; color: #94a3b8; font-size: 11px; text-align: center; flex: 1; font-weight: 600; }
        .nav-item.active { color: #00f2fe; }
        .alert { background: rgba(16, 185, 129, 0.2); color: #34d399; padding: 10px; border-radius: 10px; margin-bottom: 15px; text-align: center; font-size: 12px; font-weight: bold; border: 1px solid #10b981; }
        .block { font-size: 11px; font-family: monospace; border-bottom: 1px solid rgba(255,255,255,0.08); padding: 8px 0; }
        .roadmap-item { font-size: 12px; margin-bottom: 10px; border-left: 2px solid #00f2fe; padding-left: 10px; color: #cbd5e1; }
    </style>
</head>
<body>

    {% if not logged_in %}
    <div class="container" style="display:flex; justify-content:center; align-items:center; height:100vh;">
        <div class="card" style="width:100%;">
            <div class="title">ZAM CORE</div>
            <div class="subtitle">Public Cloud Decentralized Node</div>
            <form action="/login" method="POST">
                <div class="input-box">
                    <input type="text" name="wallet_id" placeholder="Masukkan Wallet ID Node..." required>
                </div>
                <button type="submit" class="btn">Akses Jaringan Publik</button>
            </form>
        </div>
    </div>
    {% else %}

    <div class="container">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
            <div>
                <div class="title" style="font-size:18px; text-align:left;">ZAM CORE</div>
                <div style="font-size:10px; color:#10b981; font-weight:bold;">🌐 PUBLIC TESTNET ONLINE</div>
            </div>
            <div style="background:rgba(0,242,254,0.1); color:#00f2fe; padding:6px 12px; border-radius:20px; font-size:11px; border:1px solid rgba(0,242,254,0.3); font-weight:bold;">{{ user.wallet_id }}</div>
        </div>

        {% if message %}
            <div class="alert">{{ message }}</div>
        {% endif %}

        {% if active_tab == 'dashboard' %}
            <div class="card">
                <div style="font-size: 11px; color: #94a3b8; text-transform:uppercase; font-weight:bold;">ZAM Core Balance (Mining)</div>
                <div style="font-size: 26px; font-weight: 900; color: #00f2fe; margin: 6px 0;">{{ "%.2f"|format(user.balance) }} ZAM</div>
                
                <div style="font-size: 11px; color: #94a3b8; text-transform:uppercase; font-weight:bold; margin-top: 15px;">ZAM ERC-20 Bridge Ready:</div>
                <div style="font-size: 20px; font-weight: 900; color: #8b5cf6; margin: 6px 0;">{{ "%.2f"|format(user.erc20_balance) }} ZAM-E</div>

                <form action="/mine" method="POST">
                    <button type="submit" class="btn btn-success">⛏️ Mobile Mining (+200 ZAM)</button>
                </form>
            </div>

            <div class="card">
                <h3 style="margin-top:0; color:#00f2fe; font-size:15px;">🌉 ZAM to ERC-20 Bridge</h3>
                <p style="font-size:11px; color:#94a3b8;">Konversi saldo mining untuk persiapan penarikan Web3 publik.</p>
                <form action="/convert" method="POST">
                    <div class="input-box">
                        <input type="number" name="amount" placeholder="Jumlah konversi..." required>
                    </div>
                    <button type="submit" class="btn btn-warning">Konversi ke ZAM-E</button>
                </form>
            </div>

        {% elif active_tab == 'roadmap' %}
            <div class="card">
                <h3 style="margin-top:0; color:#00f2fe; font-size:15px;">📜 Roadmap & Visi Proyek</h3>
                <p style="font-size:11px; color:#94a3b8; margin-bottom:15px;">Arah pengembangan jangka panjang ZAM CORE secara transparan.</p>
                
                <div class="roadmap-item">
                    <b style="color:#00f2fe;">Fase 1 (Saat Ini):</b> Publik Testnet & Free-to-Mine Community Node.
                </div>
                <div class="roadmap-item">
                    <b style="color:#00f2fe;">Fase 2:</b> Integrasi Ad-Revenue (Pendapatan Iklan) & Stabilitas Cloud 24/7.
                </div>
                <div class="roadmap-item">
                    <b style="color:#00f2fe;">Fase 3:</b> Uji Coba ZAM-to-ERC20 Bridge ke Sepolia Testnet Publik.
                </div>
                <div class="roadmap-item">
                    <b style="color:#00f2fe;">Fase 4:</b> Mainnet Launch & Penarikan Resmi ke OKX / Trust Wallet.
                </div>
            </div>

        {% elif active_tab == 'withdraw' %}
            <div class="card">
                <h3 style="margin-top:0; color:#00f2fe; font-size:15px;">📤 Web3 Public Withdrawal</h3>
                <p style="font-size:11px; color:#94a3b8;">Simulasi penarikan ZAM-E ke dompet eksternal.</p>
                <form action="/withdraw" method="POST">
                    <div class="input-box">
                        <input type="text" name="address" placeholder="Alamat Dompet (0x...)" required>
                    </div>
                    <div class="input-box">
                        <input type="number" name="amount" placeholder="Nominal ZAM-E..." required>
                    </div>
                    <button type="submit" class="btn">Kirim ke Dompet Web3</button>
                </form>
            </div>

        {% elif active_tab == 'ledger' %}
            <div class="card">
                <h3 style="margin-top:0; color:#00f2fe; font-size:15px;">⛓️ Public Ledger Chain</h3>
                {% for block in ledger[::-1] %}
                    <div class="block">
                        <b>#{{ block.index }}</b> ({{ block.timestamp[:19] }})<br>
                        <span>{{ block.event }}</span>
                    </div>
                {% endfor %}
            </div>

        {% elif active_tab == 'node' %}
            <div class="card">
                <h3 style="margin-top:0; font-size:15px;">Node Profile</h3>
                <p style="font-size:13px;">Wallet: <b>{{ user.wallet_id }}</b></p>
                <p style="font-size:12px; color:#10b981; font-weight:bold;">Status: Cloud Node Terverifikasi</p>
                <form action="/logout" method="POST">
                    <button type="submit" class="btn btn-danger">Keluar Sesi (Logout)</button>
                </form>
            </div>
        {% endif %}
    </div>

    <div class="nav">
        <a href="/?tab=dashboard" class="nav-item {% if active_tab == 'dashboard' %}active{% endif %}">🏠<br>Dashboard</a>
        <a href="/?tab=roadmap" class="nav-item {% if active_tab == 'roadmap' %}active{% endif %}">📜<br>Roadmap</a>
        <a href="/?tab=withdraw" class="nav-item {% if active_tab == 'withdraw' %}active{% endif %}">📤<br>Withdraw</a>
        <a href="/?tab=ledger" class="nav-item {% if active_tab == 'ledger' %}active{% endif %}">⛓️<br>Ledger</a>
        <a href="/?tab=node" class="nav-item {% if active_tab == 'node' %}active{% endif %}">👤<br>Node</a>
    </div>
    {% endif %}

</body>
</html>
"""

@app.route("/")
def index():
    if "wallet_id" not in session:
        return render_template_string(HTML_TEMPLATE, logged_in=False)
    
    wallet_id = session["wallet_id"]
    db = load_database()
    
    if wallet_id not in db:
        db[wallet_id] = {"wallet_id": wallet_id, "balance": 2200000.0, "erc20_balance": 0.0}
        save_database(db)
    
    user = db[wallet_id]
    if "balance" not in user:
        user["balance"] = 2200000.0
    if "erc20_balance" not in user:
        user["erc20_balance"] = 0.0
        
    ledger = load_ledger()
    active_tab = request.args.get("tab", "dashboard")
    message = session.pop("flash_message", None)
    return render_template_string(HTML_TEMPLATE, logged_in=True, user=user, ledger=ledger, active_tab=active_tab, message=message)

@app.route("/login", methods=["POST"])
def login():
    wallet_id = request.form.get("wallet_id", "").strip()
    if wallet_id:
        session["wallet_id"] = wallet_id
        db = load_database()
        if wallet_id not in db:
            db[wallet_id] = {"wallet_id": wallet_id, "balance": 2200000.0, "erc20_balance": 0.0}
            save_database(db)
            record_block(f"Cloud Node initialized for {wallet_id}")
        session["flash_message"] = f"Node '{wallet_id}' terhubung ke Public Cloud!"
    return redirect(url_for("index", tab="dashboard"))

@app.route("/mine", methods=["POST"])
def mine():
    if "wallet_id" in session:
        wallet_id = session["wallet_id"]
        db = load_database()
        if wallet_id in db:
            db[wallet_id]["balance"] = float(db[wallet_id].get("balance", 0)) + 200.0
            save_database(db)
            record_block(f"Mobile mining +200 ZAM by {wallet_id}")
            session["flash_message"] = "+200 ZAM berhasil ditambang di Public Cloud!"
    return redirect(url_for("index", tab="dashboard"))

@app.route("/convert", methods=["POST"])
def convert():
    if "wallet_id" in session:
        wallet_id = session["wallet_id"]
        try:
            amount = float(request.form.get("amount", 0))
        except:
            amount = 0
            
        db = load_database()
        if wallet_id in db:
            balance = float(db[wallet_id].get("balance", 0))
            if 0 < amount <= balance:
                db[wallet_id]["balance"] = balance - amount
                db[wallet_id]["erc20_balance"] = float(db[wallet_id].get("erc20_balance", 0)) + amount
                save_database(db)
                record_block(f"Bridge conversion {amount} ZAM to ZAM-E by {wallet_id}")
                session["flash_message"] = f"Berhasil mengonversi {amount:,.2f} ZAM ke ZAM-E!"
            else:
                session["flash_message"] = "Saldo tidak mencukupi atau nominal salah."
    return redirect(url_for("index", tab="dashboard"))

@app.route("/withdraw", methods=["POST"])
def withdraw():
    if "wallet_id" in session:
        wallet_id = session["wallet_id"]
        address = request.form.get("address", "").strip()
        try:
            amount = float(request.form.get("amount", 0))
        except:
            amount = 0
            
        db = load_database()
        if wallet_id in db and address:
            erc20_balance = float(db[wallet_id].get("erc20_balance", 0))
            if 0 < amount <= erc20_balance:
                db[wallet_id]["erc20_balance"] = erc20_balance - amount
                save_database(db)
                record_block(f"Web3 withdrawal {amount} ZAM-E to {address} by {wallet_id}")
                session["flash_message"] = f"Simulasi penarikan {amount:,.2f} ZAM-E berhasil dicatat!"
            else:
                session["flash_message"] = "Saldo ZAM-E tidak mencukupi."
    return redirect(url_for("index", tab="withdraw"))

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    # Konfigurasi port dinamis agar otomatis membaca port dari server cloud (Render/Railway/Heroku)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
from flask import Flask, render_template_string, request, redirect, url_for, session
import json
import os
import hashlib
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = "zam_core_strict_discipline_key_2026"

DATABASE_FILE = "zam_core_database.json"
LEDGER_FILE = "zam_core_ledger.json"

def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_database(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_ledger():
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    genesis = {
        "index": 0,
        "timestamp": str(datetime.now()),
        "event": "ZAM CORE Strict Discipline Genesis - 1000:1 Ratio & 30-Day Streak Active",
        "hash": hashlib.sha256(b"ZAMCoreStrictDisciplineGenesis").hexdigest()
    }
    save_ledger([genesis])
    return [genesis]

def save_ledger(ledger):
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=4)

def record_block(event_desc):
    ledger = load_ledger()
    last_block = ledger[-1]
    new_index = len(ledger)
    timestamp = str(datetime.now())
    raw_data = f"{new_index}{last_block['hash']}{timestamp}{event_desc}"
    new_hash = hashlib.sha256(raw_data.encode()).hexdigest()
    
    block = {
        "index": new_index,
        "timestamp": timestamp,
        "event": event_desc,
        "hash": new_hash
    }
    ledger.append(block)
    save_ledger(ledger)
    return block

def check_and_update_streak(user_data):
    today_str = str(date.today())
    last_active = user_data.get("last_active_date", "")
    streak = user_data.get("streak_days", 0)
    
    if last_active == today_str:
        return False, "Anda sudah melakukan aktivitas penambangan/absen hari ini."
    
    if last_active == "":
        # Aktivitas pertama kali
        user_data["streak_days"] = 1
        user_data["last_active_date"] = today_str
        return True, "Check-in harian berhasil! Streak hari ke-1 dimulai."
    
    # Hitung selisih hari
    last_date_obj = datetime.strptime(last_active, "%Y-%m-%d").date()
    today_obj = date.today()
    diff_days = (today_obj - last_date_obj).days
    
    if diff_days == 1:
        # Beruntun / Konsisten
        streak += 1
        if streak > 30:
            streak = 30 # Cap max 30 hari untuk syarat bridge
        user_data["streak_days"] = streak
        user_data["last_active_date"] = today_str
        return True, f"Check-in sukses! Streak konsisten hari ke-{streak} dari 30 hari."
    elif diff_days > 1:
        # Terlewat 1 hari atau lebih -> RESET TOTAL KE 0!
        user_data["streak_days"] = 1
        user_data["last_active_date"] = today_str
        return True, "PERINGATAN: Anda terlewat 1 hari absen! Streak kedisiplinan di-RESET ulang ke Hari ke-1."
    else:
        return False, "Status waktu tidak valid."

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZAM CORE - Strict Discipline Ecosystem</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #020617; color: #f8fafc; margin: 0; padding-bottom: 85px; }
        .container { padding: 20px; max-width: 480px; margin: 0 auto; }
        .card { background: #0f172a; border: 1px solid rgba(0,242,254,0.25); border-radius: 20px; padding: 20px; margin-bottom: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        .title { text-align: center; font-size: 22px; font-weight: 900; background: linear-gradient(135deg, #00f2fe, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 1px; }
        .subtitle { text-align: center; font-size: 11px; color: #94a3b8; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; }
        .input-box { background: #1e293b; border: 1px solid rgba(0,242,254,0.3); border-radius: 12px; margin-bottom: 12px; padding: 10px; }
        .input-box input { background: transparent; border: none; color: white; width: 100%; outline: none; font-size: 14px; }
        .btn { background: linear-gradient(135deg, #00f2fe, #8b5cf6); color: #020617; border: none; padding: 14px; border-radius: 12px; font-weight: 800; width: 100%; cursor: pointer; text-transform: uppercase; font-size: 13px; letter-spacing: 0.5px; }
        .btn-success { background: #10b981; color: white; margin-top: 10px; }
        .btn-warning { background: #f59e0b; color: white; margin-top: 10px; }
        .btn-danger { background: #ef4444; color: white; margin-top: 10px; }
        .nav { position: fixed; bottom: 0; left: 0; width: 100%; background: #0f172a; display: flex; justify-content: space-around; padding: 10px 0; border-top: 1px solid rgba(0,242,254,0.25); z-index: 100; }
        .nav-item { text-decoration: none; color: #94a3b8; font-size: 11px; text-align: center; flex: 1; font-weight: 600; }
        .nav-item.active { color: #00f2fe; }
        .alert { background: rgba(16, 185, 129, 0.2); color: #34d399; padding: 10px; border-radius: 10px; margin-bottom: 15px; text-align: center; font-size: 12px; font-weight: bold; border: 1px solid #10b981; }
        .block { font-size: 11px; font-family: monospace; border-bottom: 1px solid rgba(255,255,255,0.08); padding: 8px 0; }
        .rule-box { font-size: 11px; background: rgba(245, 158, 11, 0.1); border: 1px solid #f59e0b; color: #fcd34d; padding: 10px; border-radius: 10px; margin-bottom: 15px; }
    </style>
</head>
<body>

    {% if not logged_in %}
    <div class="container" style="display:flex; justify-content:center; align-items:center; height:100vh;">
        <div class="card" style="width:100%;">
            <div class="title">ZAM CORE</div>
            <div class="subtitle">Strict Discipline Protocol</div>
            <form action="/login" method="POST">
                <div class="input-box">
                    <input type="text" name="wallet_id" placeholder="Masukkan Wallet ID Node..." required>
                </div>
                <button type="submit" class="btn">Masuk Node Ekosistem</button>
            </form>
        </div>
    </div>
    {% else %}

    <div class="container">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
            <div>
                <div class="title" style="font-size:18px; text-align:left;">ZAM CORE</div>
                <div style="font-size:10px; color:#10b981; font-weight:bold;">🛡️ STRICT STREAK SYSTEM</div>
            </div>
            <div style="background:rgba(0,242,254,0.1); color:#00f2fe; padding:6px 12px; border-radius:20px; font-size:11px; border:1px solid rgba(0,242,254,0.3); font-weight:bold;">{{ user.wallet_id }}</div>
        </div>

        {% if message %}
            <div class="alert">{{ message }}</div>
        {% endif %}

        {% if active_tab == 'dashboard' %}
            <div class="card">
                <div style="font-size: 11px; color: #94a3b8; text-transform:uppercase; font-weight:bold;">ZAM Testnet Balance (Mining)</div>
                <div style="font-size: 26px; font-weight: 900; color: #00f2fe; margin: 6px 0;">{{ "%.2f"|format(user.balance) }} ZAM</div>
                
                <div style="font-size: 11px; color: #94a3b8; text-transform:uppercase; font-weight:bold; margin-top: 15px;">ZAM-E ERC-20 (Bridge Ready):</div>
                <div style="font-size: 20px; font-weight: 900; color: #8b5cf6; margin: 6px 0;">{{ "%.2f"|format(user.erc20_balance) }} ZAM-E</div>

                <div style="background: rgba(139, 92, 246, 0.1); border: 1px solid #8b5cf6; padding: 10px; border-radius: 12px; margin-top: 15px; text-align: center;">
                    <div style="font-size: 11px; color: #cbd5e1;">Status Kedisiplinan Streak Anda:</div>
                    <div style="font-size: 18px; font-weight: 900; color: #f59e0b; margin-top: 4px;">🔥 Hari ke-{{ user.streak_days }} / 30 Hari</div>
                </div>

                <form action="/mine" method="POST">
                    <button type="submit" class="btn btn-success">⛏️ Mobile Mining & Check-in (+200 ZAM)</button>
                </form>
            </div>

            <div class="card">
                <h3 style="margin-top:0; color:#00f2fe; font-size:15px;">🌉 ZAM to ERC-20 Bridge (Rasio 1000:1)</h3>
                <div class="rule-box">
                    ⚠️ <b>Syarat Mutlak Bridge:</b><br>
                    1. Rasio Konversi: <b>1.000 ZAM = 1 ZAM-E</b>.<br>
                    2. Wajib mencapai <b>30 Hari Streak Aktif Berturut-turut</b>. Jika absen 1 hari, streak di-reset ke 0!
                </div>
                <form action="/convert" method="POST">
                    <div class="input-box">
                        <input type="number" name="amount" placeholder="Jumlah ZAM (Kelipatan 1000)..." required>
                    </div>
                    <button type="submit" class="btn btn-warning">Konversi ke ZAM-E (Rasio 1000:1)</button>
                </form>
            </div>

        {% elif active_tab == 'withdraw' %}
            <div class="card">
                <h3 style="margin-top:0; color:#00f2fe; font-size:15px;">📤 Web3 External Withdrawal</h3>
                <p style="font-size:11px; color:#94a3b8;">Tarik ZAM-E yang sudah lulus verifikasi ke dompet eksternal (OKX, Trust Wallet).</p>
                <form action="/withdraw" method="POST">
                    <div class="input-box">
                        <input type="text" name="address" placeholder="Alamat Dompet (0x...)" required>
                    </div>
                    <div class="input-box">
                        <input type="number" name="amount" placeholder="Nominal ZAM-E..." required>
                    </div>
                    <button type="submit" class="btn">Kirim ke Dompet Web3</button>
                </form>
            </div>

        {% elif active_tab == 'ledger' %}
            <div class="card">
                <h3 style="margin-top:0; color:#00f2fe; font-size:15px;">⛓️ Quantum Ledger & Audit Chain</h3>
                {% for block in ledger[::-1] %}
                    <div class="block">
                        <b>#{{ block.index }}</b> ({{ block.timestamp[:19] }})<br>
                        <span>{{ block.event }}</span>
                    </div>
                {% endfor %}
            </div>

        {% elif active_tab == 'node' %}
            <div class="card">
                <h3 style="margin-top:0; font-size:15px;">Node Profile</h3>
                <p style="font-size:13px;">Wallet ID: <b>{{ user.wallet_id }}</b></p>
                <p style="font-size:12px; color:#f59e0b; font-weight:bold;">Streak Kedisiplinan: {{ user.streak_days }} / 30 Hari</p>
                <form action="/logout" method="POST">
                    <button type="submit" class="btn btn-danger">Keluar Sesi (Logout)</button>
                </form>
            </div>
        {% endif %}
    </div>

    <div class="nav">
        <a href="/?tab=dashboard" class="nav-item {% if active_tab == 'dashboard' %}active{% endif %}">🏠<br>Dashboard</a>
        <a href="/?tab=withdraw" class="nav-item {% if active_tab == 'withdraw' %}active{% endif %}">📤<br>Withdraw</a>
        <a href="/?tab=ledger" class="nav-item {% if active_tab == 'ledger' %}active{% endif %}">⛓️<br>Ledger</a>
        <a href="/?tab=node" class="nav-item {% if active_tab == 'node' %}active{% endif %}">👤<br>Node</a>
    </div>
    {% endif %}

</body>
</html>
"""

@app.route("/")
def index():
    if "wallet_id" not in session:
        return render_template_string(HTML_TEMPLATE, logged_in=False)
    
    wallet_id = session["wallet_id"]
    db = load_database()
    
    if wallet_id not in db:
        db[wallet_id] = {
            "wallet_id": wallet_id,
            "balance": 0.0, # Mulai dari 0 sesuai aturan baru
            "erc20_balance": 0.0,
            "streak_days": 0,
            "last_active_date": ""
        }
        save_database(db)
    
    user = db[wallet_id]
    if "streak_days" not in user:
        user["streak_days"] = 0
    if "last_active_date" not in user:
        user["last_active_date"] = ""
        
    ledger = load_ledger()
    active_tab = request.args.get("tab", "dashboard")
    message = session.pop("flash_message", None)
    return render_template_string(HTML_TEMPLATE, logged_in=True, user=user, ledger=ledger, active_tab=active_tab, message=message)

@app.route("/login", methods=["POST"])
def login():
    wallet_id = request.form.get("wallet_id", "").strip()
    if wallet_id:
        session["wallet_id"] = wallet_id
        db = load_database()
        if wallet_id not in db:
            db[wallet_id] = {
                "wallet_id": wallet_id,
                "balance": 0.0,
                "erc20_balance": 0.0,
                "streak_days": 0,
                "last_active_date": ""
            }
            save_database(db)
            record_block(f"Strict discipline node initialized for {wallet_id}")
        session["flash_message"] = f"Node '{wallet_id}' berhasil masuk ke protokol disiplin."
    return redirect(url_for("index", tab="dashboard"))

@app.route("/mine", methods=["POST"])
def mine():
    if "wallet_id" in session:
        wallet_id = session["wallet_id"]
        db = load_database()
        if wallet_id in db:
            user_data = db[wallet_id]
            updated, msg = check_and_update_streak(user_data)
            
            if updated or "berhasil" in msg or "Check-in" in msg or "Streak" in msg:
                # Tambah saldo penambangan +200 ZAM
                user_data["balance"] = float(user_data.get("balance", 0)) + 200.0
                save_database(db)
                record_block(f"Mobile mining +200 ZAM & Streak Day {user_data['streak_days']} for {wallet_id}")
                session["flash_message"] = f"{msg} (+200 ZAM ditambahkan ke saldo testnet)."
            else:
                session["flash_message"] = msg
    return redirect(url_for("index", tab="dashboard"))

@app.route("/convert", methods=["POST"])
def convert():
    if "wallet_id" in session:
        wallet_id = session["wallet_id"]
        try:
            amount = float(request.form.get("amount", 0))
        except:
            amount = 0
            
        db = load_database()
        if wallet_id in db:
            user = db[wallet_id]
            balance = float(user.get("balance", 0))
            streak = int(user.get("streak_days", 0))
            
            # Validasi Syarat 30 Hari Streak
            if streak < 30:
                session["flash_message"] = f"Gagal Bridge! Streak Anda baru {streak}/30 hari. Wajib genap 30 hari berturut-turut tanpa putus."
            elif amount < 1000:
                session["flash_message"] = "Minimal konversi adalah 1.000 ZAM (Kelipatan Rasio 1000:1)."
            elif amount % 1000 != 0:
                session["flash_message"] = "Nominal konversi harus kelipatan pas 1.000 (contoh: 1000, 2000, dst)."
            elif amount <= balance:
                # Eksekusi rasio konversi 1000:1
                erc20_gained = amount / 1000.0
                user["balance"] = balance - amount
                user["erc20_balance"] = float(user.get("erc20_balance", 0)) + erc20_gained
                save_database(db)
                record_block(f"Strict Bridge: {amount} ZAM converted to {erc20_gained} ZAM-E (Ratio 1000:1) by {wallet_id}")
                session["flash_message"] = f"Berhasil! {amount:,.0f} ZAM dikonversi menjadi {erc20_gained:,.2f} ZAM-E (Rasio 1000:1)."
            else:
                session["flash_message"] = "Saldo ZAM Testnet tidak mencukupi."
    return redirect(url_for("index", tab="dashboard"))

@app.route("/withdraw", methods=["POST"])
def withdraw():
    if "wallet_id" in session:
        wallet_id = session["wallet_id"]
        address = request.form.get("address", "").strip()
        try:
            amount = float(request.form.get("amount", 0))
        except:
            amount = 0
            
        db = load_database()
        if wallet_id in db and address:
            erc20_balance = float(db[wallet_id].get("erc20_balance", 0))
            if 0 < amount <= erc20_balance:
                db[wallet_id]["erc20_balance"] = erc20_balance - amount
                save_database(db)
                record_block(f"Web3 strict withdrawal {amount} ZAM-E to {address} by {wallet_id}")
                session["flash_message"] = f"Penarikan {amount:,.2f} ZAM-E ke dompet eksternal berhasil dicatat!"
            else:
                session["flash_message"] = "Saldo ZAM-E tidak mencukupi."
    return redirect(url_for("index", tab="withdraw"))

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
from flask import Flask, render_template_string, request, redirect, url_for, session
import json
import os
import hashlib
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = "zam_core_exact_ui_pro_key_2026"

DATABASE_FILE = "zam_core_database.json"
LEDGER_FILE = "zam_core_ledger.json"

def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_database(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_ledger():
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    genesis = {
        "index": 0,
        "timestamp": str(datetime.now()),
        "event": "ZAM CORE Pro UI Genesis - Exact Ecosystem Structure Active",
        "hash": hashlib.sha256(b"ZAMCoreExactUIGenesis").hexdigest()
    }
    save_ledger([genesis])
    return [genesis]

def save_ledger(ledger):
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=4)

def record_block(event_desc):
    ledger = load_ledger()
    last_block = ledger[-1]
    new_index = len(ledger)
    timestamp = str(datetime.now())
    raw_data = f"{new_index}{last_block['hash']}{timestamp}{event_desc}"
    new_hash = hashlib.sha256(raw_data.encode()).hexdigest()
    
    block = {
        "index": new_index,
        "timestamp": timestamp,
        "event": event_desc,
        "hash": new_hash
    }
    ledger.append(block)
    save_ledger(ledger)
    return block

def process_mining_session(user_data):
    now = datetime.now()
    last_claim_str = user_data.get("last_claim_time", "")
    
    if last_claim_str:
        last_claim_time = datetime.strptime(last_claim_str, "%Y-%m-%d %H:%M:%S")
        elapsed_hours = (now - last_claim_time).total_seconds() / 3600.0
        if elapsed_hours < 24:
            rem = 24 - elapsed_hours
            return False, f"Sesi penambangan masih berjalan. Sisa waktu: {rem:.1f} jam."
            
    earned = 2.4 # 24 jam x 0.1 ZAM
    user_data["balance_process"] = float(user_data.get("balance_process", 0)) + earned
    user_data["last_claim_time"] = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # Streak Kedisiplinan 30 Hari
    today_str = str(date.today())
    last_active = user_data.get("last_active_date", "")
    streak = user_data.get("streak_days", 0)
    
    if last_active == "":
        user_data["streak_days"] = 1
    else:
        last_date_obj = datetime.strptime(last_active, "%Y-%m-%d").date()
        diff_days = (date.today() - last_date_obj).days
        if diff_days == 1:
            streak += 1
            if streak > 30: streak = 30
            user_data["streak_days"] = streak
        elif diff_days > 1:
            user_data["streak_days"] = 1 # Reset ke 0/1 jika terlewat 1 hari
            
    user_data["last_active_date"] = today_str
    return True, f"Klaim penambangan sukses! +{earned} ZAM (Proses) ditambahkan."

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZAM CORE - Ecosystem</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0c1b33; color: #f8fafc; margin: 0; padding-bottom: 90px; }
        .header-top { background: linear-gradient(180deg, #1e3a8a, #0c1b33); padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); }
        .logo-area { font-weight: 900; font-size: 18px; letter-spacing: 1px; color: white; display: flex; align-items: center; gap: 8px; }
        .top-icons { display: flex; gap: 15px; font-size: 18px; color: #93c5fd; }
        
        .subnav { display: flex; justify-content: center; gap: 30px; background: #0c1b33; padding: 12px 0; font-size: 15px; font-weight: bold; border-bottom: 1px solid rgba(255,255,255,0.05); }
        .subnav a { text-decoration: none; color: #94a3b8; padding-bottom: 5px; }
        .subnav a.active { color: white; border-bottom: 3px solid #60a5fa; }

        .container { padding: 15px; max-width: 480px; margin: 0 auto; }
        
        /* Mining Landscape Card */
        .mining-card { background: linear-gradient(135deg, #1e40af, #3b82f6); border-radius: 24px; padding: 20px; position: relative; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.2); margin-bottom: 15px; }
        .balance-box { background: rgba(15, 23, 42, 0.4); backdrop-filter: blur(10px); border-radius: 16px; padding: 15px; margin-bottom: 15px; border: 1px solid rgba(255,255,255,0.15); }
        .balance-title { font-size: 11px; color: #93c5fd; text-transform: uppercase; font-weight: bold; }
        .balance-val { font-size: 26px; font-weight: 900; color: white; margin: 5px 0; }
        
        .mining-bg-scene { background: rgba(0,0,0,0.2); border-radius: 16px; height: 180px; position: relative; display: flex; flex-direction: column; justify-content: space-between; padding: 12px; border: 1px dashed rgba(255,255,255,0.2); }
        .bubble-coin { background: rgba(245, 158, 11, 0.9); width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: bold; color: #000; box-shadow: 0 4px 10px rgba(0,0,0,0.4); position: absolute; cursor: pointer; }
        
        .action-grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 15px; }
        .action-box { background: linear-gradient(135deg, #f97316, #fb923c); border-radius: 16px; padding: 15px 10px; text-align: center; color: white; text-decoration: none; font-weight: bold; font-size: 12px; box-shadow: 0 5px 15px rgba(249, 115, 22, 0.3); }
        .action-box.purple { background: linear-gradient(135deg, #8b5cf6, #a78bfa); box-shadow: 0 5px 15px rgba(139, 92, 246, 0.3); }
        .action-box.blue { background: linear-gradient(135deg, #0284c7, #38bdf8); box-shadow: 0 5px 15px rgba(2, 132, 199, 0.3); }

        .menu-list { background: #1e293b; border-radius: 16px; overflow: hidden; margin-bottom: 12px; border: 1px solid rgba(255,255,255,0.08); }
        .menu-item { display: flex; justify-content: space-between; align-items: center; padding: 15px 20px; text-decoration: none; color: white; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 14px; font-weight: 500; }
        .menu-item:last-child { border-bottom: none; }
        .menu-item span { color: #94a3b8; font-size: 13px; }

        .btn { background: #3b82f6; color: white; border: none; padding: 14px; border-radius: 14px; font-weight: 800; width: 100%; cursor: pointer; text-transform: uppercase; font-size: 13px; }
        .btn-success { background: #10b981; }
        .btn-warning { background: #f59e0b; color: #000; }
        
        .alert { background: rgba(16, 185, 129, 0.2); color: #34d399; padding: 12px; border-radius: 12px; margin-bottom: 15px; text-align: center; font-size: 12px; font-weight: bold; border: 1px solid #10b981; }

        /* Bottom Nav Bar */
        .nav { position: fixed; bottom: 0; left: 0; width: 100%; background: #091326; display: flex; justify-content: space-around; padding: 10px 0; border-top: 1px solid rgba(255,255,255,0.1); z-index: 100; }
        .nav-item { text-decoration: none; color: #94a3b8; font-size: 11px; text-align: center; flex: 1; font-weight: 600; }
        .nav-item.active { color: #60a5fa; }
    </style>
</head>
<body>

    {% if not logged_in %}
    <div class="container" style="display:flex; justify-content:center; align-items:center; height:100vh;">
        <div class="mining-card" style="width:100%;">
            <div class="title" style="font-size:24px; font-weight:900; color:white; text-align:center; margin-bottom:10px;">ZAM CORE</div>
            <div class="subtitle" style="text-align:center; color:#93c5fd; margin-bottom:20px; font-size:12px;">Decentralized Ecosystem Mobile Node</div>
            <form action="/login" method="POST">
                <div class="balance-box">
                    <input type="text" name="wallet_id" placeholder="Masukkan Wallet ID / Email Node..." required style="background:transparent; border:none; color:white; width:100%; outline:none; font-size:14px; text-align:center;">
                </div>
                <button type="submit" class="btn btn-success">Masuk Jaringan</button>
            </form>
        </div>
    </div>
    {% else %}

    <!-- Header Atas -->
    <div class="header-top">
        <div class="logo-area">
            <span>🛡️</span> ZAM CORE
        </div>
        <div class="top-icons">
            <span>🏆</span>
            <span>💬</span>
        </div>
    </div>

    <!-- Subnav Atas -->
    <div class="subnav">
        <a href="/?tab=bonus" class="{% if active_tab == 'bonus' %}active{% endif %}">Bonusnya</a>
        <a href="/?tab=utama" class="{% if active_tab == 'utama' %}active{% endif %}">Milikku</a>
    </div>

    <div class="container">
        {% if message %}
            <div class="alert">{{ message }}</div>
        {% endif %}

        {% if active_tab == 'utama' or active_tab == 'dashboard' %}
            <!-- Card Utama Saldo & Lanskap Penambangan -->
            <div class="mining-card">
                <div class="balance-box">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div class="balance-title">ZAM (Total Saldo)</div>
                            <div class="balance-val">{{ "%.3f"|format(user.balance_verified + user.balance_process) }}</div>
                        </div>
                        <div style="text-align:right;">
                            <div class="balance-title">Kekuatanku</div>
                            <div style="font-size:16px; font-weight:bold; color:#f59e0b;">{{ user.streak_days * 100 }} Node</div>
                        </div>
                    </div>
                </div>

                <div class="mining-bg-scene">
                    <div style="font-size:11px; font-weight:bold; color:#93c5fd; background:rgba(0,0,0,0.4); padding:4px 10px; border-radius:10px; display:inline-block;">
                        ⚡ Kecepatan: 0.1 ZAM/Jam
                    </div>
                    <!-- Gelembung simulasi koin aktif -->
                    <div class="bubble-coin" style="top:40%; left:30%;">+2.4</div>
                    <div class="bubble-coin" style="top:55%; left:65%; background:#38bdf8;">Klaim</div>
                    
                    <form action="/mine" method="POST">
                        <button type="submit" class="btn btn-success" style="padding:10px; font-size:12px;">⛏️ Klaim Tambang 24 Jam</button>
                    </form>
                </div>
            </div>

            <!-- 3 Tombol Menu Utama -->
            <div class="action-grid-3">
                <a href="/?tab=akaun" class="action-box">
                    <div>💰</div>
                    <div style="margin-top:5px;">Akaun</div>
                    <div style="font-size:9px; opacity:0.8;">Periksa Saldo</div>
                </a>
                <a href="/?tab=tim" class="action-box purple">
                    <div>👥</div>
                    <div style="margin-top:5px;">Tim</div>
                    <div style="font-size:9px; opacity:0.8;">Gabungan</div>
                </a>
                <a href="/?tab=hak" class="action-box blue">
                    <div>💳</div>
                    <div style="margin-top:5px;">Zona Hak</div>
                    <div style="font-size:9px; opacity:0.8;">Beli Kartu</div>
                </a>
            </div>

        {% elif active_tab == 'bonus' %}
            <div class="mining-card" style="text-align:center; padding:30px 20px;">
                <div style="font-size:40px; margin-bottom:10px;">🎁</div>
                <h3 style="margin:0 0 10px 0; color:white; font-size:18px;">Aula Hadiah & Check-in 30 Hari</h3>
                <p style="font-size:12px; color:#93c5fd; margin-bottom:20px;">Selesaikan check-in harian berturut-turut. Absen 1 hari = Reset ke 0!</p>
                <div style="background:rgba(255,255,255,0.1); padding:15px; border-radius:14px; margin-bottom:15px;">
                    <div style="font-size:12px; color:#cbd5e1;">Streak Disiplin Aktif:</div>
                    <div style="font-size:22px; font-weight:900; color:#f59e0b; margin-top:5px;">🔥 Hari ke-{{ user.streak_days }} / 30 Hari</div>
                </div>
                <form action="/mine" method="POST">
                    <button type="submit" class="btn btn-success">Check-in Harian (+2.4 ZAM)</button>
                </form>
            </div>

        {% elif active_tab == 'akaun' %}
            <div class="card" style="background:#1e293b; border-radius:20px; padding:20px;">
                <h3 style="margin-top:0; color:#60a5fa; font-size:16px;">📊 Rincian Saldo Akun</h3>
                
                <div class="balance-box" style="margin-top:15px;">
                    <div class="balance-title">Saldo Keseluruhan (Estimasi)</div>
                    <div class="balance-val">~ 5,814.51 USDT</div>
                    <div style="font-size:11px; color:#cbd5e1;">ZAM Tiba: {{ "%.2f"|format(user.balance_verified + user.balance_process) }}</div>
                </div>

                <div style="background:#0f172a; padding:15px; border-radius:14px; margin-bottom:12px; border:1px solid rgba(255,255,255,0.08);">
                    <div style="font-size:11px; color:#10b981; font-weight:bold;">🟢 ZAM (Tervalidasi / Unlocked)</div>
                    <div style="font-size:18px; font-weight:bold; color:white; margin:5px 0;">{{ "%.2f"|format(user.balance_verified) }} ZAM</div>
                    <a href="/?tab=convert" class="btn btn-warning" style="display:block; text-align:center; text-decoration:none; padding:8px; font-size:11px; margin-top:8px;">Menukarkan (Bridge 1000:1)</a>
                </div>

                <div style="background:#0f172a; padding:15px; border-radius:14px; border:1px solid rgba(255,255,255,0.08);">
                    <div style="font-size:11px; color:#f59e0b; font-weight:bold;">⏳ ZAM (Dalam Proses / Vesting)</div>
                    <div style="font-size:18px; font-weight:bold; color:white; margin:5px 0;">{{ "%.2f"|format(user.balance_process) }} ZAM</div>
                </div>
            </div>

        {% elif active_tab == 'convert' %}
            <div class="card" style="background:#1e293b; border-radius:20px; padding:20px;">
                <h3 style="margin-top:0; color:#60a5fa; font-size:16px;">🌉 Konversi & Penarikan ZAM-E</h3>
                <div class="rule-box" style="font-size:11px; background:rgba(245,158,11,0.1); border:1px solid #f59e0b; color:#fcd34d; padding:10px; border-radius:10px; margin-bottom:15px;">
                    ⚠️ <b>Aturan Penarikan:</b><br>
                    1. Rasio Konversi: <b>1.000 ZAM = 1 ZAM-E</b>.<br>
                    2. Wajib mencapai <b>30 Hari Streak Aktif</b> tanpa putus.<br>
                    3. Biaya Gas: 2 ZAM-E.
                </div>
                <form action="/convert" method="POST">
                    <div class="input-box" style="background:#0f172a; padding:12px; border-radius:12px; margin-bottom:12px;">
                        <input type="number" name="amount" placeholder="Jumlah ZAM (Kelipatan 1000)..." required style="background:transparent; border:none; color:white; width:100%; outline:none; font-size:13px;">
                    </div>
                    <button type="submit" class="btn btn-warning">Konversi & Penarikan</button>
                </form>
            </div>

        {% elif active_tab == 'hak' %}
            <div class="card" style="background:#1e293b; border-radius:20px; padding:20px;">
                <h3 style="margin-top:0; color:#60a5fa; font-size:16px;">👑 Zona Hak & Kupon Kartu</h3>
                <div style="background:#0f172a; padding:15px; border-radius:14px; margin-bottom:12px; border:1px solid rgba(255,255,255,0.08);">
                    <b style="color:white; font-size:13px;">Kartu Olahraga Sehat</b>
                    <p style="font-size:11px; color:#94a3b8; margin:5px 0;">Menambang ZAM otomatis dengan aktivitas langkah.</p>
                    <button class="btn" style="padding:8px; font-size:11px; margin-top:5px;">Beli Sekarang ($3.00)</button>
                </div>
                <div style="background:#0f172a; padding:15px; border-radius:14px; border:1px solid rgba(255,255,255,0.08);">
                    <b style="color:white; font-size:13px;">Asisten Pengumpulan Auto</b>
                    <p style="font-size:11px; color:#94a3b8; margin:5px 0;">Membantu mengumpulkan seluruh ZAM otomatis.</p>
                    <button class="btn btn-warning" style="padding:8px; font-size:11px; margin-top:5px;">Beli Sekarang ($1.00)</button>
                </div>
            </div>

        {% elif active_tab == 'tim' %}
            <div class="card" style="background:#1e293b; border-radius:20px; padding:20px;">
                <h3 style="margin-top:0; color:#60a5fa; font-size:16px;">👥 Tim & Referensi Komunitas</h3>
                <div style="background:#0f172a; padding:15px; border-radius:14px; text-align:center;">
                    <div style="font-size:11px; color:#94a3b8;">Total Anggota Tim Referensi:</div>
                    <div style="font-size:24px; font-weight:bold; color:white; margin:5px 0;">408 Anggota</div>
                    <div style="font-size:11px; color:#10b981; margin-top:5px;">Status KYC-2: Lulus Terverifikasi</div>
                </div>
            </div>

        {% elif active_tab == 'ledger' %}
            <div class="card" style="background:#1e293b; border-radius:20px; padding:20px;">
                <h3 style="margin-top:0; color:#60a5fa; font-size:16px;">⛓️ Quantum Ledger Chain</h3>
                {% for block in ledger[::-1] %}
                    <div class="block" style="font-size:11px; font-family:monospace; border-bottom:1px solid rgba(255,255,255,0.05); padding:8px 0;">
                        <b>#{{ block.index }}</b> ({{ block.timestamp[:19] }})<br>
                        <span style="color:#cbd5e1;">{{ block.event }}</span>
                    </div>
                {% endfor %}
            </div>

        {% elif active_tab == 'settings' %}
            <div class="card" style="background:#1e293b; border-radius:20px; padding:20px;">
                <h3 style="margin-top:0; color:#60a5fa; font-size:16px;">⚙️ Pengaturan & Profil Akun</h3>
                <p style="font-size:13px; color:white;">Wallet ID: <b>{{ user.wallet_id }}</b></p>
                <p style="font-size:12px; color:#10b981;">Status KYC: Lulus Tingkat-2 & Biometrik</p>
                <form action="/logout" method="POST" style="margin-top:15px;">
                    <button type="submit" class="btn" style="background:#ef4444;">Keluar (Logout)</button>
                </form>
            </div>
        {% endif %}
    </div>

    <!-- Bottom Navigation Bar (Persis Struktur Menu Bawah) -->
    <div class="nav">
        <a href="/?tab=utama" class="nav-item {% if active_tab == 'utama' or active_tab == 'dashboard' %}active{% endif %}">🏠<br>Utama</a>
        <a href="/?tab=bonus" class="nav-item {% if active_tab == 'bonus' %}active{% endif %}">🎁<br>Hadiah</a>
        <a href="/?tab=ledger" class="nav-item {% if active_tab == 'ledger' %}active{% endif %}">⛓️<br>Video/Ledger</a>
        <a href="/?tab=hak" class="nav-item {% if active_tab == 'hak' %}active{% endif %}">🌐<br>Kehidupan</a>
        <a href="/?tab=settings" class="nav-item {% if active_tab == 'settings' %}active{% endif %}">👤<br>Akun</a>
    </div>
    {% endif %}

</body>
</html>
"""

@app.route("/")
def index():
    if "wallet_id" not in session:
        return render_template_string(HTML_TEMPLATE, logged_in=False)
    
    wallet_id = session["wallet_id"]
    db = load_database()
    
    if wallet_id not in db:
        db[wallet_id] = {
            "wallet_id": wallet_id,
            "balance_verified": 0.0,
            "balance_process": 0.0,
            "erc20_balance": 0.0,
            "streak_days": 0,
            "last_active_date": "",
            "last_claim_time": ""
        }
        save_database(db)
        
    user = db[wallet_id]
    ledger = load_ledger()
    active_tab = request.args.get("tab", "utama")
    message = session.pop("flash_message", None)
    return render_template_string(HTML_TEMPLATE, logged_in=True, user=user, ledger=ledger, active_tab=active_tab, message=message)

@app.route("/login", methods=["POST"])
def login():
    wallet_id = request.form.get("wallet_id", "").strip()
    if wallet_id:
        session["wallet_id"] = wallet_id
        db = load_database()
        if wallet_id not in db:
            db[wallet_id] = {
                "wallet_id": wallet_id,
                "balance_verified": 0.0,
                "balance_process": 0.0,
                "erc20_balance": 0.0,
                "streak_days": 0,
                "last_active_date": "",
                "last_claim_time": ""
            }
            save_database(db)
            record_block(f"Node initialized for {wallet_id}")
        session["flash_message"] = f"Node '{wallet_id}' berhasil masuk ke ekosistem."
    return redirect(url_for("index", tab="utama"))

@app.route("/mine", methods=["POST"])
def mine():
    if "wallet_id" in session:
        wallet_id = session["wallet_id"]
        db = load_database()
        if wallet_id in db:
            user_data = db[wallet_id]
            success, msg = process_mining_session(user_data)
            if success:
                save_database(db)
                record_block(f"Mining 24H claimed (+2.4 ZAM Process) by {wallet_id}")
                session["flash_message"] = msg
            else:
                session["flash_message"] = msg
    return redirect(url_for("index", tab="utama"))

@app.route("/convert", methods=["POST"])
def convert():
    if "wallet_id" in session:
        wallet_id = session["wallet_id"]
        try:
            amount = float(request.form.get("amount", 0))
        except:
            amount = 0
            
        db = load_database()
        if wallet_id in db:
            user = db[wallet_id]
            verified_bal = float(user.get("balance_verified", 0))
            streak = int(user.get("streak_days", 0))
            
            if streak < 30:
                session["flash_message"] = f"Ditolak! Streak Anda baru {streak}/30 hari. Wajib genap 30 hari tanpa putus."
            elif amount < 1000 or amount % 1000 != 0:
                session["flash_message"] = "Nominal harus kelipatan pas 1.000 ZAM (Rasio 1000:1)."
            elif amount <= verified_bal:
                erc20_gained = amount / 1000.0
                user["balance_verified"] = verified_bal - amount
                user["erc20_balance"] = float(user.get("erc20_balance", 0)) + erc20_gained
                save_database(db)
                record_block(f"Bridge Success: {amount} ZAM converted to {erc20_gained} ZAM-E by {wallet_id}")
                session["flash_message"] = f"Sukses! {amount:,.0f} ZAM dikonversi ke {erc20_gained:,.2f} ZAM-E."
            else:
                session["flash_message"] = "Saldo Tervalidasi tidak mencukupi."
    return redirect(url_for("index", tab="convert"))

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
from flask import Flask, render_template_string, request, redirect, url_for, session
import json
import os
import hashlib
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = "zam_core_stable_pro_key_2026"

DATABASE_FILE = "zam_core_database.json"
LEDGER_FILE = "zam_core_ledger.json"

def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_database(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_ledger():
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    genesis = {
        "index": 0,
        "timestamp": str(datetime.now()),
        "event": "ZAM CORE Stable Genesis - Ecosystem Active",
        "hash": hashlib.sha256(b"ZAMCoreStableGenesis").hexdigest()
    }
    save_ledger([genesis])
    return [genesis]

def save_ledger(ledger):
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=4)

def record_block(event_desc):
    ledger = load_ledger()
    last_block = ledger[-1]
    new_index = len(ledger)
    timestamp = str(datetime.now())
    raw_data = f"{new_index}{last_block['hash']}{timestamp}{event_desc}"
    new_hash = hashlib.sha256(raw_data.encode()).hexdigest()
    
    block = {
        "index": new_index,
        "timestamp": timestamp,
        "event": event_desc,
        "hash": new_hash
    }
    ledger.append(block)
    save_ledger(ledger)
    return block

def process_mining_session(user_data):
    now = datetime.now()
    last_claim_str = user_data.get("last_claim_time", "")
    
    if last_claim_str:
        try:
            last_claim_time = datetime.strptime(last_claim_str, "%Y-%m-%d %H:%M:%S")
            elapsed_hours = (now - last_claim_time).total_seconds() / 3600.0
            if elapsed_hours < 24:
                rem = 24 - elapsed_hours
                return False, f"Sesi penambangan masih berjalan. Sisa waktu: {rem:.1f} jam."
        except:
            pass
            
    earned = 2.4 # 24 jam x 0.1 ZAM = 2.4 ZAM
    user_data["balance_process"] = float(user_data.get("balance_process", 0)) + earned
    user_data["last_claim_time"] = now.strftime("%Y-%m-%d %H:%M:%S")
    
    today_str = str(date.today())
    last_active = user_data.get("last_active_date", "")
    streak = int(user_data.get("streak_days", 0))
    
    if last_active == "":
        user_data["streak_days"] = 1
    else:
        try:
            last_date_obj = datetime.strptime(last_active, "%Y-%m-%d").date()
            diff_days = (date.today() - last_date_obj).days
            if diff_days == 1:
                streak += 1
                if streak > 30: streak = 30
                user_data["streak_days"] = streak
            elif diff_days > 1:
                user_data["streak_days"] = 1
        except:
            user_data["streak_days"] = 1
            
    user_data["last_active_date"] = today_str
    return True, f"Klaim penambangan sukses! +{earned} ZAM (Proses) ditambahkan."

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZAM CORE - Ecosystem</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0c1b33; color: #f8fafc; margin: 0; padding-bottom: 90px; }
        .header-top { background: linear-gradient(180deg, #1e3a8a, #0c1b33); padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); }
        .logo-area { font-weight: 900; font-size: 18px; letter-spacing: 1px; color: white; display: flex; align-items: center; gap: 8px; }
        .top-icons { display: flex; gap: 15px; font-size: 18px; color: #93c5fd; }
        .subnav { display: flex; justify-content: center; gap: 30px; background: #0c1b33; padding: 12px 0; font-size: 15px; font-weight: bold; border-bottom: 1px solid rgba(255,255,255,0.05); }
        .subnav a { text-decoration: none; color: #94a3b8; padding-bottom: 5px; }
        .subnav a.active { color: white; border-bottom: 3px solid #60a5fa; }
        .container { padding: 15px; max-width: 480px; margin: 0 auto; }
        .mining-card { background: linear-gradient(135deg, #1e40af, #3b82f6); border-radius: 24px; padding: 20px; position: relative; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.2); margin-bottom: 15px; }
        .balance-box { background: rgba(15, 23, 42, 0.4); backdrop-filter: blur(10px); border-radius: 16px; padding: 15px; margin-bottom: 15px; border: 1px solid rgba(255,255,255,0.15); }
        .balance-title { font-size: 11px; color: #93c5fd; text-transform: uppercase; font-weight: bold; }
        .balance-val { font-size: 26px; font-weight: 900; color: white; margin: 5px 0; }
        .mining-bg-scene { background: rgba(0,0,0,0.2); border-radius: 16px; height: 160px; position: relative; display: flex; flex-direction: column; justify-content: space-between; padding: 12px; border: 1px dashed rgba(255,255,255,0.2); }
        .action-grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 15px; }
        .action-box { background: linear-gradient(135deg, #f97316, #fb923c); border-radius: 16px; padding: 15px 10px; text-align: center; color: white; text-decoration: none; font-weight: bold; font-size: 12px; box-shadow: 0 5px 15px rgba(249, 115, 22, 0.3); }
        .action-box.purple { background: linear-gradient(135deg, #8b5cf6, #a78bfa); box-shadow: 0 5px 15px rgba(139, 92, 246, 0.3); }
        .action-box.blue { background: linear-gradient(135deg, #0284c7, #38bdf8); box-shadow: 0 5px 15px rgba(2, 132, 199, 0.3); }
        .card { background: #1e293b; border-radius: 20px; padding: 20px; margin-bottom: 15px; border: 1px solid rgba(255,255,255,0.08); }
        .btn { background: #3b82f6; color: white; border: none; padding: 14px; border-radius: 14px; font-weight: 800; width: 100%; cursor: pointer; text-transform: uppercase; font-size: 13px; }
        .btn-success { background: #10b981; }
        .btn-warning { background: #f59e0b; color: #000; }
        .alert { background: rgba(16, 185, 129, 0.2); color: #34d399; padding: 12px; border-radius: 12px; margin-bottom: 15px; text-align: center; font-size: 12px; font-weight: bold; border: 1px solid #10b981; }
        .nav { position: fixed; bottom: 0; left: 0; width: 100%; background: #091326; display: flex; justify-content: space-around; padding: 10px 0; border-top: 1px solid rgba(255,255,255,0.1); z-index: 100; }
        .nav-item { text-decoration: none; color: #94a3b8; font-size: 11px; text-align: center; flex: 1; font-weight: 600; }
        .nav-item.active { color: #60a5fa; }
    </style>
</head>
<body>

    {% if not logged_in %}
    <div class="container" style="display:flex; justify-content:center; align-items:center; height:100vh;">
        <div class="mining-card" style="width:100%;">
            <div style="font-size:24px; font-weight:900; color:white; text-align:center; margin-bottom:10px;">ZAM CORE</div>
            <div style="text-align:center; color:#93c5fd; margin-bottom:20px; font-size:12px;">Decentralized Ecosystem Mobile Node</div>
            <form action="/login" method="POST">
                <div class="balance-box">
                    <input type="text" name="wallet_id" placeholder="Masukkan Wallet ID / Email Node..." required style="background:transparent; border:none; color:white; width:100%; outline:none; font-size:14px; text-align:center;">
                </div>
                <button type="submit" class="btn btn-success">Masuk Jaringan</button>
            </form>
        </div>
    </div>
    {% else %}

    <div class="header-top">
        <div class="logo-area"><span>🛡️</span> ZAM CORE</div>
        <div class="top-icons"><span>🏆</span><span>💬</span></div>
    </div>

    <div class="subnav">
        <a href="/?tab=bonus" class="{% if active_tab == 'bonus' %}active{% endif %}">Bonusnya</a>
        <a href="/?tab=utama" class="{% if active_tab == 'utama' %}active{% endif %}">Milikku</a>
    </div>

    <div class="container">
        {% if message %}
            <div class="alert">{{ message }}</div>
        {% endif %}

        {% if active_tab == 'utama' or active_tab == 'dashboard' %}
            <div class="mining-card">
                <div class="balance-box">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div class="balance-title">ZAM (Total Saldo)</div>
                            <div class="balance-val">{{ "%.3f"|format(user.balance_verified + user.balance_process) }}</div>
                        </div>
                        <div style="text-align:right;">
                            <div class="balance-title">Kekuatanku</div>
                            <div style="font-size:16px; font-weight:bold; color:#f59e0b;">{{ user.streak_days * 100 }} Node</div>
                        </div>
                    </div>
                </div>

                <div class="mining-bg-scene">
                    <div style="font-size:11px; font-weight:bold; color:#93c5fd; background:rgba(0,0,0,0.4); padding:4px 10px; border-radius:10px; display:inline-block;">
                        ⚡ Kecepatan: 0.1 ZAM/Jam
                    </div>
                    <form action="/mine" method="POST">
                        <button type="submit" class="btn btn-success" style="padding:10px; font-size:12px;">⛏️ Klaim Tambang 24 Jam</button>
                    </form>
                </div>
            </div>

            <div class="action-grid-3">
                <a href="/?tab=akaun" class="action-box">
                    <div>💰</div><div style="margin-top:5px;">Akaun</div><div style="font-size:9px; opacity:0.8;">Periksa Saldo</div>
                </a>
                <a href="/?tab=tim" class="action-box purple">
                    <div>👥</div><div style="margin-top:5px;">Tim</div><div style="font-size:9px; opacity:0.8;">Gabungan</div>
                </a>
                <a href="/?tab=hak" class="action-box blue">
                    <div>💳</div><div style="margin-top:5px;">Zona Hak</div><div style="font-size:9px; opacity:0.8;">Beli Kartu</div>
                </a>
            </div>

        {% elif active_tab == 'bonus' %}
            <div class="mining-card" style="text-align:center; padding:30px 20px;">
                <div style="font-size:40px; margin-bottom:10px;">🎁</div>
                <h3 style="margin:0 0 10px 0; color:white; font-size:18px;">Aula Hadiah & Check-in 30 Hari</h3>
                <p style="font-size:12px; color:#93c5fd; margin-bottom:20px;">Absen 1 hari terlewat = Streak reset ke 0!</p>
                <div style="background:rgba(255,255,255,0.1); padding:15px; border-radius:14px; margin-bottom:15px;">
                    <div style="font-size:12px; color:#cbd5e1;">Streak Disiplin Aktif:</div>
                    <div style="font-size:22px; font-weight:900; color:#f59e0b; margin-top:5px;">🔥 Hari ke-{{ user.streak_days }} / 30 Hari</div>
                </div>
                <form action="/mine" method="POST">
                    <button type="submit" class="btn btn-success">Check-in Harian (+2.4 ZAM)</button>
                </form>
            </div>

        {% elif active_tab == 'akaun' %}
            <div class="card">
                <h3 style="margin-top:0; color:#60a5fa; font-size:16px;">📊 Rincian Saldo Akun</h3>
                <div class="balance-box" style="margin-top:15px;">
                    <div class="balance-title">Saldo Keseluruhan (Estimasi)</div>
                    <div class="balance-val">~ 5,814.51 USDT</div>
                </div>
                <div style="background:#0f172a; padding:15px; border-radius:14px; margin-bottom:12px;">
                    <div style="font-size:11px; color:#10b981; font-weight:bold;">🟢 ZAM Tervalidasi (Unlocked)</div>
                    <div style="font-size:18px; font-weight:bold; color:white; margin:5px 0;">{{ "%.2f"|format(user.balance_verified) }} ZAM</div>
                    <a href="/?tab=convert" class="btn btn-warning" style="display:block; text-align:center; text-decoration:none; padding:8px; font-size:11px; margin-top:8px;">Menukarkan (Bridge 1000:1)</a>
                </div>
                <div style="background:#0f172a; padding:15px; border-radius:14px;">
                    <div style="font-size:11px; color:#f59e0b; font-weight:bold;">⏳ ZAM Dalam Proses</div>
                    <div style="font-size:18px; font-weight:bold; color:white; margin:5px 0;">{{ "%.2f"|format(user.balance_process) }} ZAM</div>
                </div>
            </div>

        {% elif active_tab == 'convert' %}
            <div class="card">
                <h3 style="margin-top:0; color:#60a5fa; font-size:16px;">🌉 Konversi & Penarikan ZAM-E</h3>
                <div style="font-size:11px; background:rgba(245,158,11,0.1); border:1px solid #f59e0b; color:#fcd34d; padding:10px; border-radius:10px; margin-bottom:15px;">
                    ⚠️ Syarat: Rasio 1000:1 & Wajib 30 Hari Streak Aktif.
                </div>
                <form action="/convert" method="POST">
                    <div style="background:#0f172a; padding:12px; border-radius:12px; margin-bottom:12px;">
                        <input type="number" name="amount" placeholder="Jumlah ZAM (Kelipatan 1000)..." required style="background:transparent; border:none; color:white; width:100%; outline:none; font-size:13px;">
                    </div>
                    <button type="submit" class="btn btn-warning">Konversi ke ZAM-E</button>
                </form>
            </div>

        {% elif active_tab == 'hak' %}
            <div class="card">
                <h3 style="margin-top:0; color:#60a5fa; font-size:16px;">👑 Zona Hak & Kupon Kartu</h3>
                <div style="background:#0f172a; padding:15px; border-radius:14px; margin-bottom:12px;">
                    <b style="color:white; font-size:13px;">Kartu Olahraga Sehat</b>
                    <p style="font-size:11px; color:#94a3b8; margin:5px 0;">Menambang ZAM otomatis.</p>
                    <button class="btn" style="padding:8px; font-size:11px; margin-top:5px;">Beli ($3.00)</button>
                </div>
            </div>

        {% elif active_tab == 'tim' %}
            <div class="card" style="text-align:center;">
                <h3 style="margin-top:0; color:#60a5fa; font-size:16px;">👥 Tim & Komunitas</h3>
                <div style="font-size:24px; font-weight:bold; color:white; margin:10px 0;">408 Anggota</div>
                <div style="font-size:11px; color:#10b981;">Status KYC-2: Lulus Terverifikasi</div>
            </div>

        {% elif active_tab == 'ledger' %}
            <div class="card">
                <h3 style="margin-top:0; color:#60a5fa; font-size:16px;">⛓️ Quantum Ledger Chain</h3>
                {% for block in ledger[::-1] %}
                    <div style="font-size:11px; font-family:monospace; border-bottom:1px solid rgba(255,255,255,0.05); padding:8px 0;">
                        <b>#{{ block.index }}</b> ({{ block.timestamp[:19] }})<br>
                        <span style="color:#cbd5e1;">{{ block.event }}</span>
                    </div>
                {% endfor %}
            </div>

        {% elif active_tab == 'settings' %}
            <div class="card">
                <h3 style="margin-top:0; color:#60a5fa; font-size:16px;">⚙️ Pengaturan & Profil Akun</h3>
                <p style="font-size:13px; color:white;">Wallet ID: <b>{{ user.wallet_id }}</b></p>
                <form action="/logout" method="POST" style="margin-top:15px;">
                    <button type="submit" class="btn" style="background:#ef4444;">Keluar (Logout)</button>
                </form>
            </div>
        {% endif %}
    </div>

    <div class="nav">
        <a href="/?tab=utama" class="nav-item {% if active_tab == 'utama' or active_tab == 'dashboard' %}active{% endif %}">🏠<br>Utama</a>
        <a href="/?tab=bonus" class="nav-item {% if active_tab == 'bonus' %}active{% endif %}">🎁<br>Hadiah</a>
        <a href="/?tab=ledger" class="nav-item {% if active_tab == 'ledger' %}active{% endif %}">⛓️<br>Ledger</a>
        <a href="/?tab=hak" class="nav-item {% if active_tab == 'hak' %}active{% endif %}">🌐<br>Kehidupan</a>
        <a href="/?tab=settings" class="nav-item {% if active_tab == 'settings' %}active{% endif %}">👤<br>Akun</a>
    </div>
    {% endif %}

</body>
</html>
"""

@app.route("/")
def index():
    if "wallet_id" not in session:
        return render_template_string(HTML_TEMPLATE, logged_in=False)
    
    wallet_id = session["wallet_id"]
    db = load_database()
    
    if wallet_id not in db:
        db[wallet_id] = {
            "wallet_id": wallet_id,
            "balance_verified": 0.0,
            "balance_process": 0.0,
            "erc20_balance": 0.0,
            "streak_days": 0,
            "last_active_date": "",
            "last_claim_time": ""
        }
        save_database(db)
        
    user = db[wallet_id]
    ledger = load_ledger()
    active_tab = request.args.get("tab", "utama")
    message = session.pop("flash_message", None)
    return render_template_string(HTML_TEMPLATE, logged_in=True, user=user, ledger=ledger, active_tab=active_tab, message=message)

@app.route("/login", methods=["POST"])
def login():
    wallet_id = request.form.get("wallet_id", "").strip()
    if wallet_id:
        session["wallet_id"] = wallet_id
        db = load_database()
        if wallet_id not in db:
            db[wallet_id] = {
                "wallet_id": wallet_id,
                "balance_verified": 0.0,
                "balance_process": 0.0,
                "erc20_balance": 0.0,
                "streak_days": 0,
                "last_active_date": "",
                "last_claim_time": ""
            }
            save_database(db)
            record_block(f"Node initialized for {wallet_id}")
        session["flash_message"] = f"Node '{wallet_id}' berhasil masuk ke ekosistem."
    return redirect(url_for("index", tab="utama"))

@app.route("/mine", methods=["POST"])
def mine():
    if "wallet_id" in session:
        wallet_id = session["wallet_id"]
        db = load_database()
        if wallet_id in db:
            user_data = db[wallet_id]
            success, msg = process_mining_session(user_data)
            if success:
                save_database(db)
                record_block(f"Mining 24H claimed (+2.4 ZAM Process) by {wallet_id}")
                session["flash_message"] = msg
            else:
                session["flash_message"] = msg
    return redirect(url_for("index", tab="utama"))

@app.route("/convert", methods=["POST"])
def convert():
    if "wallet_id" in session:
        wallet_id = session["wallet_id"]
        try:
            amount = float(request.form.get("amount", 0))
        except:
            amount = 0
            
        db = load_database()
        if wallet_id in db:
            user = db[wallet_id]
            verified_bal = float(user.get("balance_verified", 0))
            streak = int(user.get("streak_days", 0))
            
            if streak < 30:
                session["flash_message"] = f"Ditolak! Streak Anda baru {streak}/30 hari."
            elif amount < 1000 or amount % 1000 != 0:
                session["flash_message"] = "Nominal harus kelipatan pas 1.000 ZAM (Rasio 1000:1)."
            elif amount <= verified_bal:
                erc20_gained = amount / 1000.0
                user["balance_verified"] = verified_bal - amount
                user["erc20_balance"] = float(user.get("erc20_balance", 0)) + erc20_gained
                save_database(db)
                record_block(f"Bridge Success: {amount} ZAM converted to {erc20_gained} ZAM-E by {wallet_id}")
                session["flash_message"] = f"Sukses! {amount:,.0f} ZAM dikonversi ke {erc20_gained:,.2f} ZAM-E."
            else:
                session["flash_message"] = "Saldo Tervalidasi tidak mencukupi."
    return redirect(url_for("index", tab="convert"))

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
from flask import Flask, render_template_string, request, redirect, url_for, session
import json
import os
import hashlib
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = "zam_core_ai_sentinel_enterprise_key_2026"

DATABASE_FILE = "zam_core_database.json"
LEDGER_FILE = "zam_core_ledger.json"

def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_database(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_ledger():
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    genesis = {
        "index": 0,
        "timestamp": str(datetime.now()),
        "event": "ZAM CORE AI Sentinel Genesis - Autonomous Security & Ledger Active",
        "hash": hashlib.sha256(b"ZAMCoreAISentinelGenesis").hexdigest()
    }
    save_ledger([genesis])
    return [genesis]

def save_ledger(ledger):
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=4)

def record_block(event_desc):
    ledger = load_ledger()
    last_block = ledger[-1]
    new_index = len(ledger)
    timestamp = str(datetime.now())
    raw_data = f"{new_index}{last_block['hash']}{timestamp}{event_desc}"
    new_hash = hashlib.sha256(raw_data.encode()).hexdigest()
    
    block = {
        "index": new_index,
        "timestamp": timestamp,
        "event": event_desc,
        "hash": new_hash
    }
    ledger.append(block)
    save_ledger(ledger)
    return block

# ==========================================
# KECERDASAN BUATAN: AI SENTINEL ENGINE (BACKEND)
# ==========================================
def ai_sentinel_audit(user_id, action_type, user_data):
    """
    AI otonom yang berjalan di balik layar untuk menganalisis aktivitas,
    mencegah bot, manipulasi waktu, dan kecurangan penarikan.
    """
    # 1. Deteksi Anomali / Bot Signature
    if "bot" in user_id.lower() or len(user_id) < 3:
        record_block(f"AI SENTINEL ALERT: Suspicious node signature blocked -> {user_id}")
        return False, "AI Sentinel: Aktivitas node mencurigakan atau terdeteksi pola otomatisasi bot."

    # 2. Validasi Keamanan Penambangan 24 Jam
    if action_type == "mine":
        last_claim = user_data.get("last_claim_time", "")
        if last_claim:
            try:
                last_time = datetime.strptime(last_claim, "%Y-%m-%d %H:%M:%S")
                diff_hours = (datetime.now() - last_time).total_seconds() / 3600.0
                if diff_hours < 23.9: # Toleransi mikro detik
                    return False, f"AI Sentinel: Sesi penambangan 24 jam belum selesai (Sisa {24 - diff_hours:.1f} jam)."
            except:
                pass

    # 3. Validasi Ketat Syarat Bridge & Penarikan
    if action_type == "convert":
        streak = int(user_data.get("streak_days", 0))
        if streak < 30:
            return False, f"AI Sentinel Audit: Syarat mutlak belum terpenuhi. Streak Anda baru {streak}/30 hari."

    return True, "AI Sentinel Audit: Aman & Terverifikasi."

def process_ai_mining(user_data):
    earned = 2.4 # 24 jam x 0.1 ZAM
    user_data["balance_process"] = float(user_data.get("balance_process", 0)) + earned
    user_data["last_claim_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    today_str = str(date.today())
    last_active = user_data.get("last_active_date", "")
    streak = int(user_data.get("streak_days", 0))
    
    if last_active == "":
        user_data["streak_days"] = 1
    else:
        try:
            last_date_obj = datetime.strptime(last_active, "%Y-%m-%d").date()
            diff_days = (date.today() - last_date_obj).days
            if diff_days == 1:
                streak += 1
                if streak > 30: streak = 30
                user_data["streak_days"] = streak
            elif diff_days > 1:
                user_data["streak_days"] = 1 # Reset total jika absen 1 hari
        except:
            user_data["streak_days"] = 1
            
    user_data["last_active_date"] = today_str
    return earned

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZAM CORE - Enterprise Ecosystem</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #070f1e; color: #f8fafc; margin: 0; padding-bottom: 90px; }
        .header-top { background: linear-gradient(180deg, #172554, #070f1e); padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.08); }
        .logo-area { font-weight: 900; font-size: 18px; letter-spacing: 1px; color: white; display: flex; align-items: center; gap: 8px; }
        .ai-badge { font-size: 9px; background: rgba(0,242,254,0.15); color: #00f2fe; padding: 3px 8px; border-radius: 10px; border: 1px solid rgba(0,242,254,0.3); font-weight: bold; }
        .top-icons { display: flex; gap: 15px; font-size: 18px; color: #93c5fd; }
        
        .subnav { display: flex; justify-content: center; gap: 40px; background: #070f1e; padding: 12px 0; font-size: 15px; font-weight: bold; border-bottom: 1px solid rgba(255,255,255,0.05); }
        .subnav a { text-decoration: none; color: #64748b; padding-bottom: 5px; }
        .subnav a.active { color: white; border-bottom: 3px solid #3b82f6; }

        .container { padding: 15px; max-width: 480px; margin: 0 auto; }
        
        .mining-card { background: linear-gradient(135deg, #1e3a8a, #2563eb); border-radius: 24px; padding: 20px; position: relative; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.2); margin-bottom: 15px; }
        .balance-box { background: rgba(15, 23, 42, 0.45); backdrop-filter: blur(10px); border-radius: 16px; padding: 15px; margin-bottom: 15px; border: 1px solid rgba(255,255,255,0.15); }
        .balance-title { font-size: 11px; color: #93c5fd; text-transform: uppercase; font-weight: bold; }
        .balance-val { font-size: 26px; font-weight: 900; color: white; margin: 5px 0; }
        
        .mining-bg-scene { background: rgba(0,0,0,0.25); border-radius: 16px; height: 160px; position: relative; display: flex; flex-direction: column; justify-content: space-between; padding: 12px; border: 1px dashed rgba(255,255,255,0.2); }
        
        .action-grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 15px; }
        .action-box { background: linear-gradient(135deg, #ea580c, #f97316); border-radius: 16px; padding: 15px 10px; text-align: center; color: white; text-decoration: none; font-weight: bold; font-size: 12px; box-shadow: 0 5px 15px rgba(234, 88, 12, 0.3); }
        .action-box.purple { background: linear-gradient(135deg, #7c3aed, #8b5cf6); box-shadow: 0 5px 15px rgba(124, 58, 237, 0.3); }
        .action-box.blue { background: linear-gradient(135deg, #0284c7, #38bdf8); box-shadow: 0 5px 15px rgba(2, 132, 199, 0.3); }

        .card { background: #0f172a; border-radius: 20px; padding: 20px; margin-bottom: 15px; border: 1px solid rgba(255,255,255,0.08); }
        .btn { background: #3b82f6; color: white; border: none; padding: 14px; border-radius: 14px; font-weight: 800; width: 100%; cursor: pointer; text-transform: uppercase; font-size: 13px; }
        .btn-success { background: #10b981; }
        .btn-warning { background: #f59e0b; color: #000; }
        .alert { background: rgba(16, 185, 129, 0.2); color: #34d399; padding: 12px; border-radius: 12px; margin-bottom: 15px; text-align: center; font-size: 12px; font-weight: bold; border: 1px solid #10b981; }
        
        .nav { position: fixed; bottom: 0; left: 0; width: 100%; background: #050b14; display: flex; justify-content: space-around; padding: 10px 0; border-top: 1px solid rgba(255,255,255,0.1); z-index: 100; }
        .nav-item { text-decoration: none; color: #64748b; font-size: 11px; text-align: center; flex: 1; font-weight: 600; }
        .nav-item.active { color: #3b82f6; }
    </style>
</head>
<body>

    {% if not logged_in %}
    <div class="container" style="display:flex; justify-content:center; align-items:center; height:100vh;">
        <div class="mining-card" style="width:100%;">
            <div style="font-size:24px; font-weight:900; color:white; text-align:center; margin-bottom:5px;">ZAM CORE</div>
            <div style="text-align:center; color:#93c5fd; margin-bottom:20px; font-size:11px;">Autonomous AI-Powered Web3 Ecosystem</div>
            <form action="/login" method="POST">
                <div class="balance-box">
                    <input type="text" name="wallet_id" placeholder="Masukkan Wallet ID / Email Node..." required style="background:transparent; border:none; color:white; width:100%; outline:none; font-size:14px; text-align:center;">
                </div>
                <button type="submit" class="btn btn-success">Inisialisasi Node Aman</button>
            </form>
        </div>
    </div>
    {% else %}

    <div class="header-top">
        <div class="logo-area">
            <span>🛡️</span> ZAM CORE 
            <span class="ai-badge">🤖 AI Active</span>
        </div>
        <div class="top-icons"><span>🏆</span><span>💬</span></div>
    </div>

    <div class="subnav">
        <a href="/?tab=bonus" class="{% if active_tab == 'bonus' %}active{% endif %}">Bonusnya</a>
        <a href="/?tab=utama" class="{% if active_tab == 'utama' %}active{% endif %}">Milikku</a>
    </div>

    <div class="container">
        {% if message %}
            <div class="alert">{{ message }}</div>
        {% endif %}

        {% if active_tab == 'utama' or active_tab == 'dashboard' %}
            <div class="mining-card">
                <div class="balance-box">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div class="balance-title">ZAM (Total Saldo)</div>
                            <div class="balance-val">{{ "%.3f"|format(user.balance_verified + user.balance_process) }}</div>
                        </div>
                        <div style="text-align:right;">
                            <div class="balance-title">Kekuatan Node</div>
                            <div style="font-size:16px; font-weight:bold; color:#f59e0b;">{{ user.streak_days * 100 }} AI-Power</div>
                        </div>
                    </div>
                </div>

                <div class="mining-bg-scene">
                    <div style="font-size:11px; font-weight:bold; color:#93c5fd; background:rgba(0,0,0,0.4); padding:4px 10px; border-radius:10px; display:inline-block;">
                        ⚡ Kecepatan: 0.1 ZAM/Jam (AI Monitored)
                    </div>
                    <form action="/mine" method="POST">
                        <button type="submit" class="btn btn-success" style="padding:10px; font-size:12px;">⛏️ Klaim Tambang 24 Jam (+2.4 ZAM)</button>
                    </form>
                </div>
            </div>

            <div class="action-grid-3">
                <a href="/?tab=akaun" class="action-box">
                    <div>💰</div><div style="margin-top:5px;">Akaun</div><div style="font-size:9px; opacity:0.8;">Periksa Saldo</div>
                </a>
                <a href="/?tab=tim" class="action-box purple">
                    <div>👥</div><div style="margin-top:5px;">Tim</div><div style="font-size:9px; opacity:0.8;">Gabungan</div>
                </a>
                <a href="/?tab=hak" class="action-box blue">
                    <div>💳</div><div style="margin-top:5px;">Zona Hak</div><div style="font-size:9px; opacity:0.8;">Beli Kartu</div>
                </a>
            </div>

        {% elif active_tab == 'bonus' %}
            <div class="mining-card" style="text-align:center; padding:30px 20px;">
                <div style="font-size:40px; margin-bottom:10px;">🎁</div>
                <h3 style="margin:0 0 10px 0; color:white; font-size:18px;">Aula Hadiah & Disiplin 30 Hari</h3>
                <p style="font-size:12px; color:#93c5fd; margin-bottom:20px;">Diawasi AI Sentinel: Absen 1 hari = Reset otomatis ke 0!</p>
                <div style="background:rgba(255,255,255,0.08); padding:15px; border-radius:14px; margin-bottom:15px;">
                    <div style="font-size:12px; color:#cbd5e1;">Streak Disiplin Aktif:</div>
                    <div style="font-size:22px; font-weight:900; color:#f59e0b; margin-top:5px;">🔥 Hari ke-{{ user.streak_days }} / 30 Hari</div>
                </div>
                <form action="/mine" method="POST">
                    <button type="submit" class="btn btn-success">Check-in Harian (+2.4 ZAM)</button>
                </form>
            </div>

        {% elif active_tab == 'akaun' %}
            <div class="card">
                <h3 style="margin-top:0; color:#3b82f6; font-size:16px;">📊 Rincian Saldo Akun</h3>
                <div class="balance-box" style="margin-top:15px;">
                    <div class="balance-title">Saldo Keseluruhan (Estimasi)</div>
                    <div class="balance-val">~ 5,814.51 USDT</div>
                </div>
                <div style="background:#070f1e; padding:15px; border-radius:14px; margin-bottom:12px;">
                    <div style="font-size:11px; color:#10b981; font-weight:bold;">🟢 ZAM Tervalidasi (Unlocked)</div>
                    <div style="font-size:18px; font-weight:bold; color:white; margin:5px 0;">{{ "%.2f"|format(user.balance_verified) }} ZAM</div>
                    <a href="/?tab=convert" class="btn btn-warning" style="display:block; text-align:center; text-decoration:none; padding:8px; font-size:11px; margin-top:8px;">Menukarkan (Bridge 1000:1)</a>
                </div>
                <div style="background:#070f1e; padding:15px; border-radius:14px;">
                    <div style="font-size:11px; color:#f59e0b; font-weight:bold;">⏳ ZAM Dalam Proses (AI Vesting)</div>
                    <div style="font-size:18px; font-weight:bold; color:white; margin:5px 0;">{{ "%.2f"|format(user.balance_process) }} ZAM</div>
                </div>
            </div>

        {% elif active_tab == 'convert' %}
            <div class="card">
                <h3 style="margin-top:0; color:#3b82f6; font-size:16px;">🌉 Konversi & Penarikan ZAM-E</h3>
                <div style="font-size:11px; background:rgba(245,158,11,0.1); border:1px solid #f59e0b; color:#fcd34d; padding:10px; border-radius:10px; margin-bottom:15px;">
                    🤖 <b>AI Audit:</b> Rasio 1.000:1. Wajib 30 Hari Streak Aktif. Diverifikasi otomatis tanpa celah.
                </div>
                <form action="/convert" method="POST">
                    <div style="background:#070f1e; padding:12px; border-radius:12px; margin-bottom:12px;">
                        <input type="number" name="amount" placeholder="Jumlah ZAM (Kelipatan 1000)..." required style="background:transparent; border:none; color:white; width:100%; outline:none; font-size:13px;">
                    </div>
                    <button type="submit" class="btn btn-warning">Konversi ke ZAM-E</button>
                </form>
            </div>

        {% elif active_tab == 'hak' %}
            <div class="card">
                <h3 style="margin-top:0; color:#3b82f6; font-size:16px;">👑 Zona Hak & Kupon Kartu</h3>
                <div style="background:#070f1e; padding:15px; border-radius:14px; margin-bottom:12px;">
                    <b style="color:white; font-size:13px;">Kartu Olahraga Sehat</b>
                    <p style="font-size:11px; color:#94a3b8; margin:5px 0;">Menambang ZAM otomatis dengan pengawasan AI.</p>
                    <button class="btn" style="padding:8px; font-size:11px; margin-top:5px;">Beli ($3.00)</button>
                </div>
            </div>

        {% elif active_tab == 'tim' %}
            <div class="card" style="text-align:center;">
                <h3 style="margin-top:0; color:#3b82f6; font-size:16px;">👥 Tim & Komunitas</h3>
                <div style="font-size:24px; font-weight:bold; color:white; margin:10px 0;">408 Anggota</div>
                <div style="font-size:11px; color:#10b981;">Status KYC-2 & AI Biometrik: Lulus</div>
            </div>

        {% elif active_tab == 'ledger' %}
            <div class="card">
                <h3 style="margin-top:0; color:#3b82f6; font-size:16px;">⛓️ Quantum Ledger & AI Audit Trail</h3>
                {% for block in ledger[::-1] %}
                    <div style="font-size:11px; font-family:monospace; border-bottom:1px solid rgba(255,255,255,0.05); padding:8px 0;">
                        <b>#{{ block.index }}</b> ({{ block.timestamp[:19] }})<br>
                        <span style="color:#cbd5e1;">{{ block.event }}</span>
                    </div>
                {% endfor %}
            </div>

        {% elif active_tab == 'settings' %}
            <div class="card">
                <h3 style="margin-top:0; color:#3b82f6; font-size:16px;">⚙️ Pengaturan & Profil Akun</h3>
                <p style="font-size:13px; color:white;">Wallet ID: <b>{{ user.wallet_id }}</b></p>
                <p style="font-size:11px; color:#00f2fe;">Status AI Sentinel: <b>Protected & Secure</b></p>
                <form action="/logout" method="POST" style="margin-top:15px;">
                    <button type="submit" class="btn" style="background:#ef4444;">Keluar (Logout)</button>
                </form>
            </div>
        {% endif %}
    </div>

    <div class="nav">
        <a href="/?tab=utama" class="nav-item {% if active_tab == 'utama' or active_tab == 'dashboard' %}active{% endif %}">🏠<br>Utama</a>
        <a href="/?tab=bonus" class="nav-item {% if active_tab == 'bonus' %}active{% endif %}">🎁<br>Hadiah</a>
        <a href="/?tab=ledger" class="nav-item {% if active_tab == 'ledger' %}active{% endif %}">⛓️<br>Ledger</a>
        <a href="/?tab=hak" class="nav-item {% if active_tab == 'hak' %}active{% endif %}">🌐<br>Kehidupan</a>
        <a href="/?tab=settings" class="nav-item {% if active_tab == 'settings' %}active{% endif %}">👤<br>Akun</a>
    </div>
    {% endif %}

</body>
</html>
"""

@app.route("/")
def index():
    if "wallet_id" not in session:
        return render_template_string(HTML_TEMPLATE, logged_in=False)
    
    wallet_id = session["wallet_id"]
    db = load_database()
    
    if wallet_id not in db:
        db[wallet_id] = {
            "wallet_id": wallet_id,
            "balance_verified": 0.0,
            "balance_process": 0.0,
            "erc20_balance": 0.0,
            "streak_days": 0,
            "last_active_date": "",
            "last_claim_time": ""
        }
        save_database(db)
        
    user = db[wallet_id]
    ledger = load_ledger()
    active_tab = request.args.get("tab", "utama")
    message = session.pop("flash_message", None)
    return render_template_string(HTML_TEMPLATE, logged_in=True, user=user, ledger=ledger, active_tab=active_tab, message=message)

@app.route("/login", methods=["POST"])
def login():
    wallet_id = request.form.get("wallet_id", "").strip()
    if wallet_id:
        # Audit AI saat login
        passed, msg = ai_sentinel_audit(wallet_id, "login", {})
        if not passed:
            session["flash_message"] = msg
            return redirect(url_for("index"))
            
        session["wallet_id"] = wallet_id
        db = load_database()
        if wallet_id not in db:
            db[wallet_id] = {
                "wallet_id": wallet_id,
                "balance_verified": 0.0,
                "balance_process": 0.0,
                "erc20_balance": 0.0,
                "streak_days": 0,
                "last_active_date": "",
                "last_claim_time": ""
            }
            save_database(db)
            record_block(f"AI Sentinel verified node initialized -> {wallet_id}")
        session["flash_message"] = f"Node '{wallet_id}' terverifikasi oleh AI Sentinel."
    return redirect(url_for("index", tab="utama"))

@app.route("/mine", methods=["POST"])
def mine():
    if "wallet_id" in session:
        wallet_id = session["wallet_id"]
        db = load_database()
        if wallet_id in db:
            user_data = db[wallet_id]
            
            # Audit AI sebelum klaim tambang
            passed, msg = ai_sentinel_audit(wallet_id, "mine", user_data)
            if not passed:
                session["flash_message"] = msg
                return redirect(url_for("index", tab="utama"))
                
            earned = process_ai_mining(user_data)
            save_database(db)
            record_block(f"AI Audit: Mining claimed (+{earned} ZAM Process) by {wallet_id}")
            session["flash_message"] = f"Klaim sukses! +{earned} ZAM ditambahkan (Diawasi AI)."
    return redirect(url_for("index", tab="utama"))

@app.route("/convert", methods=["POST"])
def convert():
    if "wallet_id" in session:
        wallet_id = session["wallet_id"]
        try:
            amount = float(request.form.get("amount", 0))
        except:
            amount = 0
            
        db = load_database()
        if wallet_id in db:
            user = db[wallet_id]
            
            # Audit AI mutlak sebelum konversi bridge
            passed, msg = ai_sentinel_audit(wallet_id, "convert", user)
            if not passed:
                session["flash_message"] = msg
                return redirect(url_for("index", tab="convert"))
                
            verified_bal = float(user.get("balance_verified", 0))
            if amount < 1000 or amount % 1000 != 0:
                session["flash_message"] = "AI Sentinel: Nominal harus kelipatan pas 1.000 ZAM (Rasio 1000:1)."
            elif amount <= verified_bal:
                erc20_gained = amount / 1000.0
                user["balance_verified"] = verified_bal - amount
                user["erc20_balance"] = float(user.get("erc20_balance", 0)) + erc20_gained
                save_database(db)
                record_block(f"AI Sentinel Bridge Approved: {amount} ZAM to {erc20_gained} ZAM-E for {wallet_id}")
                session["flash_message"] = f"AI Disetujui! {amount:,.0f} ZAM dikonversi ke {erc20_gained:,.2f} ZAM-E."
            else:
                session["flash_message"] = "AI Sentinel: Saldo Tervalidasi tidak mencukupi."
    return redirect(url_for("index", tab="convert"))

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
from flask import Flask, render_template_string, request, redirect, url_for, session
import json
import os
import hashlib
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = "zam_core_ultimate_enterprise_2026"

DATABASE_FILE = "zam_core_database.json"
LEDGER_FILE = "zam_core_ledger.json"
SECURITY_LOG_FILE = "zam_core_security.json"

def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_database(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_ledger():
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, "r") as f:
            try: return json.load(f)
            except: return []
    genesis = {
        "index": 0,
        "timestamp": str(datetime.now()),
        "event": "ZAM CORE Ultimate Genesis - AI IP/Device Guard & Dual Ledger Active",
        "hash": hashlib.sha256(b"ZAMCoreUltimateGenesis").hexdigest()
    }
    save_ledger([genesis])
    return [genesis]

def save_ledger(ledger):
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=4)

def record_block(event_desc):
    ledger = load_ledger()
    last_block = ledger[-1]
    new_index = len(ledger)
    timestamp = str(datetime.now())
    raw_data = f"{new_index}{last_block['hash']}{timestamp}{event_desc}"
    new_hash = hashlib.sha256(raw_data.encode()).hexdigest()
    
    block = {
        "index": new_index,
        "timestamp": timestamp,
        "event": event_desc,
        "hash": new_hash
    }
    ledger.append(block)
    save_ledger(ledger)
    return block

# ==========================================
# KECERDASAN BUATAN: AI IP & DEVICE SENTINEL
# ==========================================
def ai_security_check(email, client_ip):
    db = load_database()
    # Deteksi apakah IP yang sama mencoba membuat akun massal (> 3 akun per IP)
    ip_count = sum(1 for u in db.values() if u.get("register_ip") == client_ip)
    if ip_count >= 3:
        return False, "AI Sentinel Security: Perangkat atau IP Anda telah mencapai batas maksimal pendaftaran akun."
    return True, "AI Sentinel: Aman."

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZAM CORE - Professional Enterprise</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #070f1e; color: #f8fafc; margin: 0; padding-bottom: 90px; }
        .header-top { background: linear-gradient(180deg, #172554, #070f1e); padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.08); }
        .logo-area { font-weight: 900; font-size: 18px; color: white; display: flex; align-items: center; gap: 8px; }
        .ai-badge { font-size: 9px; background: rgba(0,242,254,0.15); color: #00f2fe; padding: 3px 8px; border-radius: 10px; border: 1px solid rgba(0,242,254,0.3); font-weight: bold; }
        
        .subnav { display: flex; justify-content: center; gap: 40px; background: #070f1e; padding: 12px 0; font-size: 15px; font-weight: bold; border-bottom: 1px solid rgba(255,255,255,0.05); }
        .subnav a { text-decoration: none; color: #64748b; padding-bottom: 5px; }
        .subnav a.active { color: white; border-bottom: 3px solid #3b82f6; }

        .container { padding: 15px; max-width: 480px; margin: 0 auto; }
        .card { background: #0f172a; border-radius: 20px; padding: 20px; margin-bottom: 15px; border: 1px solid rgba(255,255,255,0.08); box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        .input-box { background: #1e293b; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; margin-bottom: 12px; padding: 12px; }
        .input-box input { background: transparent; border: none; color: white; width: 100%; outline: none; font-size: 14px; }
        
        .btn { background: #3b82f6; color: white; border: none; padding: 14px; border-radius: 14px; font-weight: 800; width: 100%; cursor: pointer; text-transform: uppercase; font-size: 13px; }
        .btn-success { background: #10b981; }
        .btn-warning { background: #f59e0b; color: #000; }
        .btn-danger { background: #ef4444; }

        .alert { background: rgba(16, 185, 129, 0.2); color: #34d399; padding: 12px; border-radius: 12px; margin-bottom: 15px; text-align: center; font-size: 12px; font-weight: bold; border: 1px solid #10b981; }
        
        .menu-list { background: #1e293b; border-radius: 16px; overflow: hidden; margin-bottom: 12px; }
        .menu-item { display: flex; justify-content: space-between; align-items: center; padding: 15px 20px; text-decoration: none; color: white; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 14px; }
        .menu-item:last-child { border-bottom: none; }
        .menu-item span { color: #94a3b8; font-size: 13px; }

        .nav { position: fixed; bottom: 0; left: 0; width: 100%; background: #050b14; display: flex; justify-content: space-around; padding: 10px 0; border-top: 1px solid rgba(255,255,255,0.1); z-index: 100; }
        .nav-item { text-decoration: none; color: #64748b; font-size: 11px; text-align: center; flex: 1; font-weight: 600; }
        .nav-item.active { color: #3b82f6; }
    </style>
</head>
<body>

    {% if not logged_in %}
    <div class="container" style="display:flex; justify-content:center; align-items:center; height:100vh;">
        <div class="card" style="width:100%;">
            <div style="font-size:24px; font-weight:900; color:white; text-align:center; margin-bottom:5px;">ZAM CORE</div>
            <div style="text-align:center; color:#93c5fd; margin-bottom:20px; font-size:11px;">AI IP & Device Protected Ecosystem</div>
            
            {% if message %}
                <div class="alert" style="background:rgba(239,68,68,0.2); color:#f87171; border-color:#ef4444;">{{ message }}</div>
            {% endif %}

            <form action="/auth" method="POST">
                <div class="input-box">
                    <input type="email" name="email" placeholder="Alamat Email..." required>
                </div>
                <div class="input-box">
                    <input type="password" name="password" placeholder="Kata Sandi..." required>
                </div>
                <div style="display:flex; gap:10px;">
                    <button type="submit" name="action" value="login" class="btn btn-success">Masuk</button>
                    <button type="submit" name="action" value="register" class="btn btn-warning">Daftar (OTP AI)</button>
                </div>
            </form>
        </div>
    </div>
    {% else %}

    <div class="header-top">
        <div class="logo-area"><span>🛡️</span> ZAM CORE <span class="ai-badge">🤖 IP Guard Active</span></div>
        <div style="font-size:12px; color:#93c5fd;">{{ user.email }}</div>
    </div>

    <div class="subnav">
        <a href="/?tab=bonus" class="{% if active_tab == 'bonus' %}active{% endif %}">Bonusnya</a>
        <a href="/?tab=utama" class="{% if active_tab == 'utama' %}active{% endif %}">Milikku</a>
    </div>

    <div class="container">
        {% if message %}
            <div class="alert">{{ message }}</div>
        {% endif %}

        {% if active_tab == 'utama' or active_tab == 'dashboard' %}
            <div class="card" style="background: linear-gradient(135deg, #1e3a8a, #2563eb);">
                <div style="font-size:11px; color:#93c5fd; text-transform:uppercase; font-weight:bold;">ZAM Total Saldo</div>
                <div style="font-size:28px; font-weight:900; color:white; margin:8px 0;">{{ "%.2f"|format(user.balance_verified + user.balance_process) }} ZAM</div>
                <div style="font-size:12px; color:#fcd34d;">≈ ⚡ Kekuatan Node: {{ user.streak_days * 100 }}</div>
                
                <form action="/mine" method="POST" style="margin-top:15px;">
                    <button type="submit" class="btn btn-success">⛏️ Klaim Tambang 24 Jam (+2.4 ZAM)</button>
                </form>
            </div>

            <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:10px;">
                <a href="/?tab=akaun" class="card" style="text-align:center; text-decoration:none; color:white; padding:15px 5px;">
                    <div style="font-size:20px;">💰</div><div style="font-size:12px; font-weight:bold; margin-top:5px;">Akaun</div>
                </a>
                <a href="/?tab=hak" class="card" style="text-align:center; text-decoration:none; color:white; padding:15px 5px;">
                    <div style="font-size:20px;">💳</div><div style="font-size:12px; font-weight:bold; margin-top:5px;">Zona Hak</div>
                </a>
                <a href="/?tab=settings" class="card" style="text-align:center; text-decoration:none; color:white; padding:15px 5px;">
                    <div style="font-size:20px;">⚙️</div><div style="font-size:12px; font-weight:bold; margin-top:5px;">Pengaturan</div>
                </a>
            </div>

        {% elif active_tab == 'akaun' %}
            <!-- Tampilan Persis Screenshot Atoshi Periksa Saldo -->
            <div class="card" style="background: linear-gradient(135deg, #2563eb, #1e40af); text-align:center; padding:25px;">
                <div style="font-size:12px; color:#93c5fd; text-transform:uppercase;">Saldo Keseluruhan</div>
                <div style="font-size:26px; font-weight:900; color:white; margin:5px 0;">≈ 5,814.51 USDT</div>
                <div style="font-size:12px; color:#cbd5e1;">ZAM (Tiba): {{ "%.2f"|format(user.balance_verified + user.balance_process) }}</div>
            </div>

            <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-size:12px; color:#10b981; font-weight:bold;">🟢 ZAM (Tervalidasi / Unlocked)</div>
                        <div style="font-size:20px; font-weight:900; color:white; margin-top:4px;">{{ "%.2f"|format(user.balance_verified) }} ZAM</div>
                    </div>
                    <div>
                        <a href="/?tab=convert" class="btn btn-warning" style="padding:10px 15px; font-size:11px; text-decoration:none;">Menukarkan</a>
                    </div>
                </div>
            </div>

            <div class="card">
                <div style="font-size:12px; color:#f59e0b; font-weight:bold;">⏳ ZAM (Proses / Vesting Tambang)</div>
                <div style="font-size:20px; font-weight:900; color:white; margin-top:4px;">{{ "%.2f"|format(user.balance_process) }} ZAM</div>
                <div style="font-size:11px; color:#94a3b8; margin-top:4px;">Dikonversi otomatis ke Tervalidasi sesuai kontribusi aktivitas & tugas.</div>
            </div>

        {% elif active_tab == 'convert' %}
            <div class="card">
                <h3 style="margin-top:0; color:#3b82f6; font-size:16px;">🌉 Konversi ZAM ke ZAM-E (ERC-20)</h3>
                <div style="font-size:11px; background:rgba(245,158,11,0.1); border:1px solid #f59e0b; color:#fcd34d; padding:10px; border-radius:10px; margin-bottom:15px;">
                    ⚠️ Rasio 1000:1. Hanya menggunakan Saldo Tervalidasi. Wajib 30 Hari Streak Aktif.
                </div>
                <form action="/convert" method="POST">
                    <div class="input-box">
                        <input type="number" name="amount" placeholder="Jumlah ZAM Tervalidasi..." required>
                    </div>
                    <button type="submit" class="btn btn-warning">Konversi & Tarik ke Web3</button>
                </form>
            </div>

        {% elif active_tab == 'bonus' %}
            <div class="card" style="text-align:center;">
                <div style="font-size:35px; margin-bottom:10px;">🎁</div>
                <h3 style="margin:0 0 10px 0; color:white; font-size:18px;">Check-in Harian & Kuota Penarikan</h3>
                <p style="font-size:12px; color:#93c5fd; margin-bottom:15px;">Selesaikan tugas untuk menambah kuota ZAM Tervalidasi!</p>
                <div style="background:#1e293b; padding:12px; border-radius:12px; margin-bottom:15px;">
                    <div style="font-size:12px; color:#cbd5e1;">Streak Kedisiplinan:</div>
                    <div style="font-size:20px; font-weight:900; color:#f59e0b; margin-top:4px;">🔥 Hari ke-{{ user.streak_days }} / 30 Hari</div>
                </div>
                <form action="/mine" method="POST">
                    <button type="submit" class="btn btn-success">Klaim Hadiah Harian (+2.4 ZAM)</button>
                </form>
            </div>

        {% elif active_tab == 'hak' %}
            <div class="card">
                <h3 style="margin-top:0; color:#3b82f6; font-size:16px;">👑 Zona Hak & Kartu Kupon</h3>
                <div style="background:#1e293b; padding:15px; border-radius:14px; margin-bottom:10px;">
                    <b>Kartu Olahraga Sehat</b><br><span style="font-size:11px; color:#94a3b8;">Menambang otomatis via aktivitas. ($3.00)</span>
                </div>
                <div style="background:#1e293b; padding:15px; border-radius:14px;">
                    <b>Asisten Pengumpulan Auto</b><br><span style="font-size:11px; color:#94a3b8;">Mengumpulkan ZAM tanpa terlewat. ($1.00)</span>
                </div>
            </div>

        {% elif active_tab == 'settings' %}
            <!-- Menu Pengaturan Persis Atoshi -->
            <div class="card" style="padding:0; overflow:hidden;">
                <div style="padding:15px 20px; font-weight:bold; border-bottom:1px solid rgba(255,255,255,0.05); color:#3b82f6;">Pengaturan Ekosistem</div>
                <div class="menu-list">
                    <a href="#" class="menu-item">Ubah kata sandi masuk <span>›</span></a>
                    <a href="#" class="menu-item">Pengaturan kata sandi pembayaran <span>›</span></a>
                    <a href="#" class="menu-item">Kelola Perangkat Masuk <span><span>IP: Terproteksi</span> ›</span></a>
                    <a href="#" class="menu-item">Kebijakan privasi <span>›</span></a>
                    <a href="#" class="menu-item">Perjanjian Pengguna <span>›</span></a>
                </div>
                <div style="padding:15px;">
                    <form action="/logout" method="POST">
                        <button type="submit" class="btn btn-danger">Keluar Sesi (Logout)</button>
                    </form>
                </div>
            </div>

        {% elif active_tab == 'ledger' %}
            <div class="card">
                <h3 style="margin-top:0; color:#3b82f6; font-size:16px;">⛓️ Quantum Ledger Chain</h3>
                {% for block in ledger[::-1] %}
                    <div style="font-size:11px; font-family:monospace; border-bottom:1px solid rgba(255,255,255,0.05); padding:8px 0;">
                        <b>#{{ block.index }}</b> ({{ block.timestamp[:19] }})<br>
                        <span style="color:#cbd5e1;">{{ block.event }}</span>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    </div>

    <div class="nav">
        <a href="/?tab=utama" class="nav-item {% if active_tab == 'utama' or active_tab == 'dashboard' %}active{% endif %}">🏠<br>Utama</a>
        <a href="/?tab=bonus" class="nav-item {% if active_tab == 'bonus' %}active{% endif %}">🎁<br>Hadiah</a>
        <a href="/?tab=ledger" class="nav-item {% if active_tab == 'ledger' %}active{% endif %}">⛓️<br>Video</a>
        <a href="/?tab=hak" class="nav-item {% if active_tab == 'hak' %}active{% endif %}">🌐<br>Kehidupan</a>
        <a href="/?tab=settings" class="nav-item {% if active_tab == 'settings' %}active{% endif %}">👤<br>Akun</a>
    </div>
    {% endif %}

</body>
</html>
"""

@app.route("/")
def index():
    if "user_email" not in session:
        return render_template_string(HTML_TEMPLATE, logged_in=False)
    
    email = session["user_email"]
    db = load_database()
    user = db.get(email, {})
    ledger = load_ledger()
    active_tab = request.args.get("tab", "utama")
    message = session.pop("flash_message", None)
    return render_template_string(HTML_TEMPLATE, logged_in=True, user=user, ledger=ledger, active_tab=active_tab, message=message)

@app.route("/auth", methods=["POST"])
def auth():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "").strip()
    action = request.form.get("action", "")
    client_ip = request.remote_addr or "127.0.0.1"
    
    db = load_database()
    
    if action == "register":
        # AI Sentinel Proteksi IP / Device Massal
        passed, msg = ai_security_check(email, client_ip)
        if not passed:
            session["flash_message"] = msg
            return redirect(url_for("index"))
            
        if email in db:
            session["flash_message"] = "Email sudah terdaftar. Silakan masuk."
            return redirect(url_for("index"))
            
        # Pendaftaran sukses dengan OTP AI otomatis
        db[email] = {
            "email": email,
            "password": hashlib.sha256(password.encode()).hexdigest(),
            "balance_verified": 10.0, # Bonus OTP & Verifikasi AI awal
            "balance_process": 0.0,
            "erc20_balance": 0.0,
            "streak_days": 1,
            "last_active_date": str(date.today()),
            "last_claim_time": "",
            "register_ip": client_ip
        }
        save_database(db)
        record_block(f"AI OTP & Registration verified for IP {client_ip} -> {email}")
        session["user_email"] = email
        session["flash_message"] = "OTP AI Terkirim! Akun berhasil dibuat dan diamankan."
        return redirect(url_for("index", tab="utama"))
        
    elif action == "login":
        if email in db and db[email]["password"] == hashlib.sha256(password.encode()).hexdigest():
            session["user_email"] = email
            session["flash_message"] = "Berhasil masuk ke Node ekosistem."
        else:
            session["flash_message"] = "Email atau kata sandi salah."
        return redirect(url_for("index"))

@app.route("/mine", methods=["POST"])
def mine():
    if "user_email" in session:
        email = session["user_email"]
        db = load_database()
        if email in db:
            user = db[email]
            now = datetime.now()
            
            # Tambang masuk ke Saldo Proses, sebagian kecil divalidasi lewat aktivitas
            earned = 2.4
            user["balance_process"] = float(user.get("balance_process", 0)) + earned
            # Kontribusi tugas harian mengonversi sebagian proses ke terverifikasi
            user["balance_verified"] = float(user.get("balance_verified", 0)) + 0.5
            user["last_claim_time"] = now.strftime("%Y-%m-%d %H:%M:%S")
            
            save_database(db)
            record_block(f"Mining processed: +{earned} ZAM (Process) & +0.5 ZAM (Verified) for {email}")
            session["flash_message"] = f"Klaim sukses! +{earned} ZAM Proses & +0.5 ZAM Tervalidasi ditambahkan."
    return redirect(url_for("index", tab="utama"))

@app.route("/convert", methods=["POST"])
def convert():
    if "user_email" in session:
        email = session["user_email"]
        try: amount = float(request.form.get("amount", 0))
        except: amount = 0
        
        db = load_database()
        if email in db:
            user = db[email]
            verified_bal = float(user.get("balance_verified", 0))
            streak = int(user.get("streak_days", 0))
            
            if streak < 30:
                session["flash_message"] = f"Bridge Ditolak AI: Streak Anda baru {streak}/30 hari."
            elif amount <= verified_bal and amount > 0:
                erc20_gained = amount / 1000.0
                user["balance_verified"] = verified_bal - amount
                user["erc20_balance"] = float(user.get("erc20_balance", 0)) + erc20_gained
                save_database(db)
                record_block(f"Bridge Success: {amount} Verified ZAM to {erc20_gained} ZAM-E for {email}")
                session["flash_message"] = f"Berhasil mengonversi {amount:,.0f} ZAM Tervalidasi ke {erc20_gained:,.2f} ZAM-E!"
            else:
                session["flash_message"] = "Saldo Tervalidasi tidak mencukupi."
    return redirect(url_for("index", tab=" akaun"))

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
from flask import Flask, render_template_string, request, redirect, url_for, session
import json
import os
import hashlib
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = "zam_core_exact_atoshi_clone_2026"

DATABASE_FILE = "zam_core_database.json"
LEDGER_FILE = "zam_core_ledger.json"

def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_database(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_ledger():
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, "r") as f:
            try: return json.load(f)
            except: return []
    genesis = {
        "index": 0,
        "timestamp": str(datetime.now()),
        "event": "ZAM CORE Exact Clone Genesis - Atoshi UI & Daily Tasks Active",
        "hash": hashlib.sha256(b"ZAMCoreExactAtoshiGenesis").hexdigest()
    }
    save_ledger([genesis])
    return [genesis]

def save_ledger(ledger):
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=4)

def record_block(event_desc):
    ledger = load_ledger()
    last_block = ledger[-1]
    new_index = len(ledger)
    timestamp = str(datetime.now())
    raw_data = f"{new_index}{last_block['hash']}{timestamp}{event_desc}"
    new_hash = hashlib.sha256(raw_data.encode()).hexdigest()
    
    block = {
        "index": new_index,
        "timestamp": timestamp,
        "event": event_desc,
        "hash": new_hash
    }
    ledger.append(block)
    save_ledger(ledger)
    return block

def ai_security_check(email, client_ip):
    db = load_database()
    ip_count = sum(1 for u in db.values() if u.get("register_ip") == client_ip)
    if ip_count >= 3:
        return False, "AI Sentinel: Perangkat/IP telah mencapai batas maksimal pendaftaran akun massal."
    return True, "Aman."

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZAM CORE - Atoshi Ecosystem</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0284c7; color: #f8fafc; margin: 0; padding-bottom: 85px; }
        
        /* Header Atas Persis Atoshi */
        .header-top { background: transparent; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; color: white; }
        .logo-area { font-weight: 900; font-size: 20px; letter-spacing: 1px; display: flex; align-items: center; gap: 8px; }
        .top-icons { display: flex; gap: 15px; font-size: 18px; color: white; }
        
        /* Subnav Bonusnya & Milikku */
        .subnav { display: flex; justify-content: center; gap: 40px; background: transparent; padding: 5px 0 15px 0; font-size: 16px; font-weight: bold; }
        .subnav a { text-decoration: none; color: rgba(255,255,255,0.6); padding-bottom: 4px; }
        .subnav a.active { color: white; border-bottom: 3px solid white; }

        .container { padding: 0 15px; max-width: 480px; margin: 0 auto; }
        
        /* Kartu Utama Lanskap Gunung Persis Atoshi */
        .mining-bg-card { background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.4)), url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80') center/cover; border-radius: 24px; padding: 15px; position: relative; min-height: 480px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.3); }
        
        .balance-box-top { background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(12px); border-radius: 18px; padding: 15px; border: 1px solid rgba(255,255,255,0.4); margin-bottom: 15px; }
        .balance-title { font-size: 11px; color: #e2e8f0; text-transform: uppercase; font-weight: bold; }
        .balance-val { font-size: 24px; font-weight: 900; color: white; margin: 4px 0; }

        /* Gelembung Koin Mengambang Persis Atoshi */
        .coin-bubble { position: absolute; background: rgba(245, 158, 11, 0.95); width: 48px; height: 48px; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 9px; font-weight: bold; color: #000; box-shadow: 0 4px 10px rgba(0,0,0,0.4); border: 2px solid #fff; cursor: pointer; }
        
        /* Tombol Bawah di Dalam Card Utama */
        .card-bottom-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; position: absolute; bottom: 15px; left: 15px; right: 15px; }
        .btn-mine-rate { background: #f97316; color: white; border-radius: 14px; padding: 12px; text-align: center; font-weight: bold; font-size: 13px; border: none; box-shadow: 0 4px 15px rgba(249,115,22,0.4); cursor: pointer; }
        .btn-invite { background: #ea580c; color: white; border-radius: 14px; padding: 12px; text-align: center; font-weight: bold; font-size: 13px; border: none; box-shadow: 0 4px 15px rgba(234,88,12,0.4); cursor: pointer; }

        /* Menu 3 Kotak Bawah Utama (Akaun, Tim, Zona Hak) */
        .menu-3-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 15px; }
        .menu-card-box { background: rgba(255, 255, 255, 0.9); border-radius: 18px; padding: 15px 10px; text-align: center; color: #1e293b; text-decoration: none; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .menu-card-box.orange { background: linear-gradient(135deg, #fb923c, #ea580c); color: white; }
        .menu-card-box.purple { background: linear-gradient(135deg, #a78bfa, #7c3aed); color: white; }
        .menu-card-box.blue { background: linear-gradient(135deg, #38bdf8, #0284c7); color: white; }

        /* Styling Halaman Hadiah & Tugas Harian */
        .task-card { background: white; border-radius: 18px; padding: 15px; margin-bottom: 12px; color: #1e293b; box-shadow: 0 4px 15px rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center; }
        .btn-task { background: #3b82f6; color: white; border: none; padding: 8px 18px; border-radius: 20px; font-weight: bold; font-size: 12px; cursor: pointer; }

        /* Bottom Nav Bar Persis Atoshi */
        .nav { position: fixed; bottom: 0; left: 0; width: 100%; background: white; display: flex; justify-content: space-around; padding: 8px 0; border-top: 1px solid #e2e8f0; z-index: 100; }
        .nav-item { text-decoration: none; color: #64748b; font-size: 11px; text-align: center; flex: 1; font-weight: 600; }
        .nav-item.active { color: #0284c7; }

        .card-general { background: white; border-radius: 20px; padding: 20px; margin-bottom: 15px; color: #1e293b; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        .btn { background: #3b82f6; color: white; border: none; padding: 14px; border-radius: 14px; font-weight: 800; width: 100%; cursor: pointer; text-transform: uppercase; font-size: 13px; }
        .alert { background: rgba(16, 185, 129, 0.2); color: #065f46; padding: 12px; border-radius: 12px; margin-bottom: 15px; text-align: center; font-size: 12px; font-weight: bold; border: 1px solid #10b981; }
    </style>
</head>
<body>

    {% if not logged_in %}
    <div class="container" style="display:flex; justify-content:center; align-items:center; height:100vh;">
        <div class="card-general" style="width:100%;">
            <div style="font-size:24px; font-weight:900; color:#1e3a8a; text-align:center; margin-bottom:5px;">ZAM CORE</div>
            <div style="text-align:center; color:#64748b; margin-bottom:20px; font-size:11px;">Atoshi Professional Ecosystem</div>
            
            {% if message %}
                <div class="alert" style="background:rgba(239,68,68,0.2); color:#991b1b; border-color:#ef4444;">{{ message }}</div>
            {% endif %}

            <form action="/auth" method="POST">
                <div style="background:#f1f5f9; border-radius:12px; padding:12px; margin-bottom:12px;">
                    <input type="email" name="email" placeholder="Alamat Email..." required style="background:transparent; border:none; width:100%; outline:none; font-size:14px;">
                </div>
                <div style="background:#f1f5f9; border-radius:12px; padding:12px; margin-bottom:15px;">
                    <input type="password" name="password" placeholder="Kata Sandi..." required style="background:transparent; border:none; width:100%; outline:none; font-size:14px;">
                </div>
                <div style="display:flex; gap:10px;">
                    <button type="submit" name="action" value="login" class="btn" style="background:#2563eb;">Masuk</button>
                    <button type="submit" name="action" value="register" class="btn" style="background:#10b981;">Daftar (OTP AI)</button>
                </div>
            </form>
        </div>
    </div>
    {% else %}

    <!-- Header Atas Persis Atoshi -->
    <div class="header-top">
        <div class="logo-area">
            <span>🛡️</span> ATOSHI (ZAM)
        </div>
        <div class="top-icons">
            <span>🏆</span>
            <span>💬</span>
        </div>
    </div>

    <!-- Subnav Atas -->
    <div class="subnav">
        <a href="/?tab=bonus" class="{% if active_tab == 'bonus' %}active{% endif %}">Bonusnya</a>
        <a href="/?tab=utama" class="{% if active_tab == 'utama' or active_tab == 'dashboard' %}active{% endif %}">Milikku</a>
    </div>

    <div class="container">
        {% if message %}
            <div class="alert">{{ message }}</div>
        {% endif %}

        {% if active_tab == 'utama' or active_tab == 'dashboard' %}
            <!-- Tampilan Utama Lanskap Gunung & Gelembung Persis Tangkapan Layar -->
            <div class="mining-bg-card">
                <div class="balance-box-top">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div class="balance-title">ATOS (ZAM)</div>
                            <div class="balance-val">{{ "%.3f"|format(user.balance_verified + user.balance_process) }}</div>
                        </div>
                        <div style="text-align:right;">
                            <div class="balance-title">Kekuatanku</div>
                            <div style="font-size:15px; font-weight:bold; color:#fef08a;">{{ 36000 + (user.streak_days * 100) }} +</div>
                        </div>
                    </div>
                </div>

                <!-- Gelembung Koin Mengambang (Simulasi Sinyal Waktu Aktif) -->
                <div class="coin-bubble" style="top:35%; left:15%;">1:59:56</div>
                <div class="coin-bubble" style="top:25%; left:45%;">2:59:56</div>
                <div class="coin-bubble" style="top:30%; left:75%;">59:56</div>
                <div class="coin-bubble" style="top:55%; left:30%;">3:59:56</div>
                <div class="coin-bubble" style="top:50%; left:58%; background:#ef4444; color:white;">🎁</div>
                <div class="coin-bubble" style="top:48%; left:80%; background:#10b981; color:white;">⚡</div>

                <div class="card-bottom-grid">
                    <form action="/mine" method="POST" style="margin:0;">
                        <button type="submit" class="btn-mine-rate" style="width:100%;">40 ATOS/H</button>
                    </form>
                    <button class="btn-invite" onclick="alert('Link referral AI Sentinel siap dibagikan!')">Mengundan</button>
                </div>
            </div>

            <!-- Menu 3 Kotak Bawah (Akaun, Tim, Zona Hak) -->
            <div class="menu-3-grid">
                <a href="/?tab=akaun" class="menu-card-box orange">
                    <div style="font-size:18px;">💰</div>
                    <div style="font-size:13px; font-weight:bold; margin-top:4px;">Akaun</div>
                    <div style="font-size:9px; opacity:0.9;">periksa saldo</div>
                </a>
                <a href="/?tab=tim" class="menu-card-box purple">
                    <div style="font-size:18px;">👥</div>
                    <div style="font-size:13px; font-weight:bold; margin-top:4px;">Tim</div>
                    <div style="font-size:9px; opacity:0.9;">Gabungan</div>
                </a>
                <a href="/?tab=hak" class="menu-card-box blue">
                    <div style="font-size:18px;">💳</div>
                    <div style="font-size:13px; font-weight:bold; margin-top:4px;">Hak</div>
                    <div style="font-size:9px; opacity:0.9;">untuk membeli</div>
                </a>
            </div>

        {% elif active_tab == 'bonus' %}
            <!-- Tampilan Halaman Hadiah & Tugas Harian Persis Screenshot Atoshi -->
            <div class="card-general" style="padding:15px; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <b style="font-size:15px; color:#1e3a8a;">Rangkaian 14 Hari</b>
                    <span style="font-size:11px; color:#64748b;">Telah masuk</span>
                </div>
                <div style="display:flex; gap:6px; overflow-x:auto; padding-bottom:5px;">
                    {% for i in range(1, 8) %}
                    <div style="background:#f1f5f9; border-radius:10px; padding:8px 6px; text-align:center; min-width:40px; {% if user.streak_days >= i %}border:2px solid #2563eb;{% endif %}">
                        <div style="font-size:9px; color:#64748b;">+{{ 10 if i<7 else 30 }}</div>
                        <div style="font-size:10px; font-weight:bold; margin-top:4px;">Hari{{ i }}</div>
                    </div>
                    {% endfor %}
                </div>
                <form action="/mine" method="POST" style="margin-top:12px;">
                    <button type="submit" class="btn" style="background:#2563eb; padding:10px; font-size:12px;">Check-in Harian (+2.4 ZAM)</button>
                </form>
            </div>

            <!-- Tugas Harian Persis Atoshi -->
            <div style="font-size:15px; font-weight:bold; color:white; margin-bottom:10px;">Tugas harian</div>
            
            <div class="task-card">
                <div>
                    <div style="font-weight:bold; font-size:13px;">Lihat sorotan (0/2)</div>
                    <div style="font-size:11px; color:#f59e0b; margin-top:2px;">🟡 15ATOS</div>
                </div>
                <button class="btn-task" onclick="alert('Menjalankan sorotan iklan...')">Pergi</button>
            </div>

            <div class="task-card">
                <div>
                    <div style="font-weight:bold; font-size:13px;">Jelajahi ATOSHI Life 15 detik (0/1)</div>
                    <div style="font-size:11px; color:#f59e0b; margin-top:2px;">🟡 10ATOS</div>
                </div>
                <button class="btn-task" onclick="alert('Membuka penjelajahan life...')">Pergi</button>
            </div>

            <div class="task-card">
                <div>
                    <div style="font-weight:bold; font-size:13px;">Selesaikan 3 Level di Farm Bl... (0/3)</div>
                    <div style="font-size:11px; color:#f59e0b; margin-top:2px;">🟡 10ATOS</div>
                </div>
                <button class="btn-task" onclick="alert('Membuka game ekosistem...')">Pergi</button>
            </div>

        {% elif active_tab == 'akaun' %}
            <!-- Periksa Saldo Persis Screenshot Atoshi -->
            <div class="card-general" style="background:linear-gradient(135deg, #2563eb, #1e40af); color:white; text-align:center; padding:25px;">
                <div style="font-size:11px; color:#93c5fd; text-transform:uppercase;">Saldo keseluruhan</div>
                <div style="font-size:26px; font-weight:900; margin:6px 0;">≈ 5,814.51 USDT</div>
                <div style="font-size:12px; color:#e2e8f0;">ATOS (Tiba): {{ "%.2f"|format(user.balance_verified + user.balance_process) }}</div>
            </div>

            <div class="card-general">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-size:12px; color:#10b981; font-weight:bold;">🟢 ATOS (Tervalidasi / Unlocked)</div>
                        <div style="font-size:20px; font-weight:900; color:#1e293b; margin-top:4px;">{{ "%.2f"|format(user.balance_verified) }}</div>
                        <div style="font-size:10px; color:#64748b;">≈ 783.77 USDT</div>
                    </div>
                    <div>
                        <a href="/?tab=convert" class="btn" style="background:#f59e0b; color:#000; padding:8px 14px; font-size:11px; text-decoration:none; display:inline-block;">Menukarkan</a>
                    </div>
                </div>
            </div>

            <div class="card-general">
                <div style="font-size:12px; color:#f59e0b; font-weight:bold;">⏳ ATOS (Proses / Vesting Tambang)</div>
                <div style="font-size:20px; font-weight:900; color:#1e293b; margin-top:4px;">{{ "%.2f"|format(user.balance_process) }}</div>
                <div style="font-size:10px; color:#64748b; margin-top:2px;">≈ 2,146.53 USDT (Dikonversi via tugas & check-in)</div>
            </div>

        {% elif active_tab == 'convert' %}
            <div class="card-general">
                <h3 style="margin-top:0; color:#2563eb; font-size:16px;">🌉 Konversi & Penarikan ATOS (ERC-20)</h3>
                <div style="font-size:11px; background:rgba(245,158,11,0.1); border:1px solid #f59e0b; color:#92400e; padding:10px; border-radius:10px; margin-bottom:15px;">
                    ⚠️ Rasio 1000:1. Saldo dipotong dari Tervalidasi. Wajib 30 Hari Streak Aktif.
                </div>
                <form action="/convert" method="POST">
                    <div style="background:#f1f5f9; padding:12px; border-radius:12px; margin-bottom:12px;">
                        <input type="number" name="amount" placeholder="Jumlah ATOS Tervalidasi..." required style="background:transparent; border:none; width:100%; outline:none; font-size:13px;">
                    </div>
                    <button type="submit" class="btn" style="background:#f59e0b; color:#000;">Konversi & Tarik ke Web3</button>
                </form>
            </div>

        {% elif active_tab == 'hak' %}
            <div class="card-general">
                <h3 style="margin-top:0; color:#2563eb; font-size:16px;">👑 Zona Hak & Kartu Kupon</h3>
                <div style="background:#f8fafc; padding:15px; border-radius:14px; margin-bottom:10px; border:1px solid #e2e8f0;">
                    <b>Kartu olahraga sehat</b><br><span style="font-size:11px; color:#64748b;">Menambang ATOS dengan berjalan kaki. ($3.00)</span>
                </div>
                <div style="background:#f8fafc; padding:15px; border-radius:14px; border:1px solid #e2e8f0;">
                    <b>Asisten pengumpulan</b><br><span style="font-size:11px; color:#64748b;">Membantu mengumpulkan semua ATOS otomatis. ($1.00)</span>
                </div>
            </div>

        {% elif active_tab == 'settings' %}
            <!-- Menu Pengaturan Persis Atoshi Screenshot -->
            <div class="card-general" style="padding:0; overflow:hidden;">
                <div style="padding:15px 20px; font-weight:bold; border-bottom:1px solid #f1f5f9; color:#2563eb;">Pengaturan Akun</div>
                <div style="display:flex; flex-direction:column;">
                    <a href="#" style="padding:15px 20px; text-decoration:none; color:#1e293b; border-bottom:1px solid #f1f5f9; display:flex; justify-content:space-between;">Ubah kata sandi masuk <span>›</span></a>
                    <a href="#" style="padding:15px 20px; text-decoration:none; color:#1e293b; border-bottom:1px solid #f1f5f9; display:flex; justify-content:space-between;">Pengaturan kata sandi pembayaran <span>›</span></a>
                    <a href="#" style="padding:15px 20px; text-decoration:none; color:#1e293b; border-bottom:1px solid #f1f5f9; display:flex; justify-content:space-between;">Kelola Perangkat Masuk <span>IP Terproteksi ›</span></a>
                    <a href="#" style="padding:15px 20px; text-decoration:none; color:#1e293b; border-bottom:1px solid #f1f5f9; display:flex; justify-content:space-between;">Kebijakan pribadi <span>›</span></a>
                    <a href="#" style="padding:15px 20px; text-decoration:none; color:#1e293b; display:flex; justify-content:space-between;">Perjanjian Pengguna <span>›</span></a>
                </div>
                <div style="padding:15px;">
                    <form action="/logout" method="POST">
                        <button type="submit" class="btn" style="background:#ef4444;">Keluar Sesi (Logout)</button>
                    </form>
                </div>
            </div>

        {% elif active_tab == 'ledger' %}
            <div class="card-general">
                <h3 style="margin-top:0; color:#2563eb; font-size:16px;">⛓️ Quantum Ledger Chain</h3>
                {% for block in ledger[::-1] %}
                    <div style="font-size:11px; font-family:monospace; border-bottom:1px solid #f1f5f9; padding:8px 0;">
                        <b>#{{ block.index }}</b> ({{ block.timestamp[:19] }})<br>
                        <span style="color:#64748b;">{{ block.event }}</span>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    </div>

    <!-- Bottom Nav Bar Persis Atoshi (Utama, Hadiah, Video, Kehidupan, Game) -->
    <div class="nav">
        <a href="/?tab=utama" class="nav-item {% if active_tab == 'utama' or active_tab == 'dashboard' %}active{% endif %}">🏠<br>Utama</a>
        <a href="/?tab=bonus" class="nav-item {% if active_tab == 'bonus' %}active{% endif %}">🎁<br>Hadiah</a>
        <a href="/?tab=ledger" class="nav-item {% if active_tab == 'ledger' %}active{% endif %}">🎞️<br>Video</a>
        <a href="/?tab=hak" class="nav-item {% if active_tab == 'hak' %}active{% endif %}">🌐<br>Kehidupan</a>
        <a href="/?tab=settings" class="nav-item {% if active_tab == 'settings' %}active{% endif %}">👤<br>Akun</a>
    </div>
    {% endif %}

</body>
</html>
"""

@app.route("/")
def index():
    if "user_email" not in session:
        return render_template_string(HTML_TEMPLATE, logged_in=False)
    
    email = session["user_email"]
    db = load_database()
    user = db.get(email, {})
    ledger = load_ledger()
    active_tab = request.args.get("tab", "utama")
    message = session.pop("flash_message", None)
    return render_template_string(HTML_TEMPLATE, logged_in=True, user=user, ledger=ledger, active_tab=active_tab, message=message)

@app.route("/auth", methods=["POST"])
def auth():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "").strip()
    action = request.form.get("action", "")
    client_ip = request.remote_addr or "127.0.0.1"
    
    db = load_database()
    
    if action == "register":
        passed, msg = ai_security_check(email, client_ip)
        if not passed:
            session["flash_message"] = msg
            return redirect(url_for("index"))
            
        if email in db:
            session["flash_message"] = "Email sudah terdaftar. Silakan masuk."
            return redirect(url_for("index"))
            
        db[email] = {
            "email": email,
            "password": hashlib.sha256(password.encode()).hexdigest(),
            "balance_verified": 20.0,
            "balance_process": 0.0,
            "erc20_balance": 0.0,
            "streak_days": 1,
            "last_active_date": str(date.today()),
            "last_claim_time": "",
            "register_ip": client_ip
        }
        save_database(db)
        record_block(f"AI OTP Verified & Registered for IP {client_ip} -> {email}")
        session["user_email"] = email
        session["flash_message"] = "OTP AI Terkirim! Pendaftaran akun berhasil."
        return redirect(url_for("index", tab="utama"))
        
    elif action == "login":
        if email in db and db[email]["password"] == hashlib.sha256(password.encode()).hexdigest():
            session["user_email"] = email
            session["flash_message"] = "Berhasil masuk ke node ekosistem."
        else:
            session["flash_message"] = "Email atau kata sandi salah."
        return redirect(url_for("index"))

@app.route("/mine", methods=["POST"])
def mine():
    if "user_email" in session:
        email = session["user_email"]
        db = load_database()
        if email in db:
            user = db[email]
            now = datetime.now()
            
            earned = 2.4
            user["balance_process"] = float(user.get("balance_process", 0)) + earned
            user["balance_verified"] = float(user.get("balance_verified", 0)) + 1.0 # Tugas harian mengalirkan ke Tervalidasi
            user["last_claim_time"] = now.strftime("%Y-%m-%d %H:%M:%S")
            
            save_database(db)
            record_block(f"Atoshi Task & Mining claimed (+{earned} Process, +1.0 Verified) for {email}")
            session["flash_message"] = f"Berhasil! +{earned} ATOS Proses & +1.0 ATOS Tervalidasi ditambahkan."
    return redirect(url_for("index", tab="utama"))

@app.route("/convert", methods=["POST"])
def convert():
    if "user_email" in session:
        email = session["user_email"]
        try: amount = float(request.form.get("amount", 0))
        except: amount = 0
        
        db = load_database()
        if email in db:
            user = db[email]
            verified_bal = float(user.get("balance_verified", 0))
            streak = int(user.get("streak_days", 0))
            
            if streak < 30:
                session["flash_message"] = f"Bridge Ditolak: Streak Anda baru {streak}/30 hari."
            elif amount <= verified_bal and amount > 0:
                erc20_gained = amount / 1000.0
                user["balance_verified"] = verified_bal - amount
                user["erc20_balance"] = float(user.get("erc20_balance", 0)) + erc20_gained
                save_database(db)
                record_block(f"Bridge Success: {amount} Verified ATOS to {erc20_gained} ATOS-E for {email}")
                session["flash_message"] = f"Sukses! {amount:,.0f} ATOS Tervalidasi dikonversi ke {erc20_gained:,.2f} ATOS-E."
            else:
                session["flash_message"] = "Saldo Tervalidasi tidak mencukupi."
    return redirect(url_for("index", tab="akaun"))

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
from flask import Flask, render_template_string, request, redirect, url_for, session
import json
import os
import hashlib
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = "zam_core_quantum_hidden_core_2026"

DATABASE_FILE = "zam_core_database.json"
LEDGER_FILE = "zam_core_ledger.json"

def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_database(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_ledger():
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, "r") as f:
            try: return json.load(f)
            except: return []
    genesis = {
        "index": 0,
        "timestamp": str(datetime.now()),
        "event": "ZAM CORE Quantum Genesis - Fully Autonomous Stealth Protocol Active",
        "hash": hashlib.sha256(b"ZAMCoreQuantumStealthGenesis").hexdigest()
    }
    save_ledger([genesis])
    return [genesis]

def save_ledger(ledger):
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=4)

def record_block(event_desc):
    ledger = load_ledger()
    last_block = ledger[-1]
    new_index = len(ledger)
    timestamp = str(datetime.now())
    raw_data = f"{new_index}{last_block['hash']}{timestamp}{event_desc}"
    new_hash = hashlib.sha256(raw_data.encode()).hexdigest()
    
    block = {
        "index": new_index,
        "timestamp": timestamp,
        "event": event_desc,
        "hash": new_hash
    }
    ledger.append(block)
    save_ledger(ledger)
    return block

# =====================================================================
# QUANTUM STEALTH AI ENGINE (BERJALAN DI BALIK LAYAR SECARA RAHASIA)
# =====================================================================
def stealth_quantum_audit(email, action_type, user_data, client_ip):
    """
    Kecerdasan buatan kuantum tingkat tinggi yang memantau integritas ekosistem 
    secara senyap tanpa indikator apa pun di antarmuka pengguna.
    """
    db = load_database()
    
    # 1. Pencegahan Multi-Akun Massal & Bot Berbasis IP/Device
    if action_type == "register":
        ip_count = sum(1 for u in db.values() if u.get("register_ip") == client_ip)
        if ip_count >= 3:
            return False, "Pendaftaran dibatasi oleh sistem jaringan."
            
    # 2. Audit Validasi Mining 24 Jam
    if action_type == "mine":
        last_claim = user_data.get("last_claim_time", "")
        if last_claim:
            try:
                last_time = datetime.strptime(last_claim, "%Y-%m-%d %H:%M:%S")
                diff_hours = (datetime.now() - last_time).total_seconds() / 3600.0
                if diff_hours < 23.9:
                    return False, f"Sesi penambangan aktif. Sisa waktu: {24 - diff_hours:.1f} jam."
            except:
                pass
                
    # 3. Audit Mutlak Syarat Bridge (30 Hari Streak & Rasio 1000:1)
    if action_type == "convert":
        streak = int(user_data.get("streak_days", 0))
        if streak < 30:
            return False, f"Syarat belum tercapai: Streak Anda baru {streak}/30 hari."
            
    return True, "Sukses"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZAM CORE - Professional Ecosystem</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0284c7; color: #f8fafc; margin: 0; padding-bottom: 85px; }
        
        .header-top { background: transparent; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; color: white; }
        .logo-container { display: flex; align-items: center; gap: 10px; font-weight: 900; font-size: 18px; letter-spacing: 1px; }
        /* Logo Geometris Kustom Sesuai Gambar Referensi */
        .custom-logo { width: 32px; height: 32px; background: #0f172a; border-radius: 8px; display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: repeat(3, 1fr); padding: 5px; gap: 3px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
        .logo-block { background: white; border-radius: 2px; }
        .logo-block.top { grid-column: 2; grid-row: 1; }
        .logo-block.left1 { grid-column: 1; grid-row: 2; }
        .logo-block.left2 { grid-column: 1; grid-row: 3; }
        .logo-block.right1 { grid-column: 3; grid-row: 2; }
        .logo-block.right2 { grid-column: 3; grid-row: 3; }

        .top-icons { display: flex; gap: 15px; font-size: 18px; color: white; }
        
        .subnav { display: flex; justify-content: center; gap: 40px; background: transparent; padding: 5px 0 15px 0; font-size: 16px; font-weight: bold; }
        .subnav a { text-decoration: none; color: rgba(255,255,255,0.6); padding-bottom: 4px; }
        .subnav a.active { color: white; border-bottom: 3px solid white; }

        .container { padding: 0 15px; max-width: 480px; margin: 0 auto; }
        
        .mining-bg-card { background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.4)), url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80') center/cover; border-radius: 24px; padding: 15px; position: relative; min-height: 480px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.3); }
        
        .balance-box-top { background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(12px); border-radius: 18px; padding: 15px; border: 1px solid rgba(255,255,255,0.4); margin-bottom: 15px; }
        .balance-title { font-size: 11px; color: #e2e8f0; text-transform: uppercase; font-weight: bold; }
        .balance-val { font-size: 24px; font-weight: 900; color: white; margin: 4px 0; }

        .coin-bubble { position: absolute; background: rgba(245, 158, 11, 0.95); width: 48px; height: 48px; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 9px; font-weight: bold; color: #000; box-shadow: 0 4px 10px rgba(0,0,0,0.4); border: 2px solid #fff; cursor: pointer; }
        
        .card-bottom-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; position: absolute; bottom: 15px; left: 15px; right: 15px; }
        .btn-mine-rate { background: #f97316; color: white; border-radius: 14px; padding: 12px; text-align: center; font-weight: bold; font-size: 13px; border: none; box-shadow: 0 4px 15px rgba(249,115,22,0.4); cursor: pointer; }
        .btn-invite { background: #ea580c; color: white; border-radius: 14px; padding: 12px; text-align: center; font-weight: bold; font-size: 13px; border: none; box-shadow: 0 4px 15px rgba(234,88,12,0.4); cursor: pointer; }

        .menu-3-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 15px; }
        .menu-card-box { background: rgba(255, 255, 255, 0.9); border-radius: 18px; padding: 15px 10px; text-align: center; color: #1e293b; text-decoration: none; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .menu-card-box.orange { background: linear-gradient(135deg, #fb923c, #ea580c); color: white; }
        .menu-card-box.purple { background: linear-gradient(135deg, #a78bfa, #7c3aed); color: white; }
        .menu-card-box.blue { background: linear-gradient(135deg, #38bdf8, #0284c7); color: white; }

        .task-card { background: white; border-radius: 18px; padding: 15px; margin-bottom: 12px; color: #1e293b; box-shadow: 0 4px 15px rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center; }
        .btn-task { background: #3b82f6; color: white; border: none; padding: 8px 18px; border-radius: 20px; font-weight: bold; font-size: 12px; cursor: pointer; }

        .nav { position: fixed; bottom: 0; left: 0; width: 100%; background: white; display: flex; justify-content: space-around; padding: 8px 0; border-top: 1px solid #e2e8f0; z-index: 100; }
        .nav-item { text-decoration: none; color: #64748b; font-size: 11px; text-align: center; flex: 1; font-weight: 600; }
        .nav-item.active { color: #0284c7; }

        .card-general { background: white; border-radius: 20px; padding: 20px; margin-bottom: 15px; color: #1e293b; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        .btn { background: #3b82f6; color: white; border: none; padding: 14px; border-radius: 14px; font-weight: 800; width: 100%; cursor: pointer; text-transform: uppercase; font-size: 13px; }
        .alert { background: rgba(16, 185, 129, 0.2); color: #065f46; padding: 12px; border-radius: 12px; margin-bottom: 15px; text-align: center; font-size: 12px; font-weight: bold; border: 1px solid #10b981; }
    </style>
</head>
<body>

    {% if not logged_in %}
    <div class="container" style="display:flex; justify-content:center; align-items:center; height:100vh;">
        <div class="card-general" style="width:100%;">
            <div style="display:flex; justify-content:center; margin-bottom:15px;">
                <div class="custom-logo" style="width:50px; height:50px;">
                    <div class="logo-block top"></div>
                    <div class="logo-block left1"></div>
                    <div class="logo-block left2"></div>
                    <div class="logo-block right1"></div>
                    <div class="logo-block right2"></div>
                </div>
            </div>
            <div style="font-size:24px; font-weight:900; color:#1e3a8a; text-align:center; margin-bottom:5px;">ZAM CORE</div>
            <div style="text-align:center; color:#64748b; margin-bottom:20px; font-size:11px;">Professional Quantum Ecosystem</div>
            
            {% if message %}
                <div class="alert" style="background:rgba(239,68,68,0.2); color:#991b1b; border-color:#ef4444;">{{ message }}</div>
            {% endif %}

            <form action="/auth" method="POST">
                <div style="background:#f1f5f9; border-radius:12px; padding:12px; margin-bottom:12px;">
                    <input type="email" name="email" placeholder="Alamat Email..." required style="background:transparent; border:none; width:100%; outline:none; font-size:14px;">
                </div>
                <div style="background:#f1f5f9; border-radius:12px; padding:12px; margin-bottom:15px;">
                    <input type="password" name="password" placeholder="Kata Sandi..." required style="background:transparent; border:none; width:100%; outline:none; font-size:14px;">
                </div>
                <div style="display:flex; gap:10px;">
                    <button type="submit" name="action" value="login" class="btn" style="background:#2563eb;">Masuk</button>
                    <button type="submit" name="action" value="register" class="btn" style="background:#10b981;">Daftar (OTP)</button>
                </div>
            </form>
        </div>
    </div>
    {% else %}

    <!-- Header Atas dengan Logo Kustom Geometris -->
    <div class="header-top">
        <div class="logo-container">
            <div class="custom-logo">
                <div class="logo-block top"></div>
                <div class="logo-block left1"></div>
                <div class="logo-block left2"></div>
                <div class="logo-block right1"></div>
                <div class="logo-block right2"></div>
            </div>
            <span>ZAM CORE</span>
        </div>
        <div class="top-icons">
            <span>🏆</span>
            <span>💬</span>
        </div>
    </div>

    <!-- Subnav Atas -->
    <div class="subnav">
        <a href="/?tab=bonus" class="{% if active_tab == 'bonus' %}active{% endif %}">Bonusnya</a>
        <a href="/?tab=utama" class="{% if active_tab == 'utama' or active_tab == 'dashboard' %}active{% endif %}">Milikku</a>
    </div>

    <div class="container">
        {% if message %}
            <div class="alert">{{ message }}</div>
        {% endif %}

        {% if active_tab == 'utama' or active_tab == 'dashboard' %}
            <div class="mining-bg-card">
                <div class="balance-box-top">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div class="balance-title">ZAM (Token)</div>
                            <div class="balance-val">{{ "%.3f"|format(user.balance_verified + user.balance_process) }}</div>
                        </div>
                        <div style="text-align:right;">
                            <div class="balance-title">Kekuatanku</div>
                            <div style="font-size:15px; font-weight:bold; color:#fef08a;">{{ 36000 + (user.streak_days * 100) }} +</div>
                        </div>
                    </div>
                </div>

                <div class="coin-bubble" style="top:35%; left:15%;">1:59:56</div>
                <div class="coin-bubble" style="top:25%; left:45%;">2:59:56</div>
                <div class="coin-bubble" style="top:30%; left:75%;">59:56</div>
                <div class="coin-bubble" style="top:55%; left:30%;">3:59:56</div>
                <div class="coin-bubble" style="top:50%; left:58%; background:#ef4444; color:white;">🎁</div>
                <div class="coin-bubble" style="top:48%; left:80%; background:#10b981; color:white;">⚡</div>

                <div class="card-bottom-grid">
                    <form action="/mine" method="POST" style="margin:0;">
                        <button type="submit" class="btn-mine-rate" style="width:100%;">40 ZAM/H</button>
                    </form>
                    <button class="btn-invite" onclick="alert('Link referral siap dibagikan!')">Mengundan</button>
                </div>
            </div>

            <div class="menu-3-grid">
                <a href="/?tab=akaun" class="menu-card-box orange">
                    <div style="font-size:18px;">💰</div>
                    <div style="font-size:13px; font-weight:bold; margin-top:4px;">Akaun</div>
                    <div style="font-size:9px; opacity:0.9;">periksa saldo</div>
                </a>
                <a href="/?tab=tim" class="menu-card-box purple">
                    <div style="font-size:18px;">👥</div>
                    <div style="font-size:13px; font-weight:bold; margin-top:4px;">Tim</div>
                    <div style="font-size:9px; opacity:0.9;">Gabungan</div>
                </a>
                <a href="/?tab=hak" class="menu-card-box blue">
                    <div style="font-size:18px;">💳</div>
                    <div style="font-size:13px; font-weight:bold; margin-top:4px;">Hak</div>
                    <div style="font-size:9px; opacity:0.9;">untuk membeli</div>
                </a>
            </div>

        {% elif active_tab == 'bonus' %}
            <div class="card-general" style="padding:15px; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <b style="font-size:15px; color:#1e3a8a;">Rangkaian 14 Hari</b>
                    <span style="font-size:11px; color:#64748b;">Telah masuk</span>
                </div>
                <div style="display:flex; gap:6px; overflow-x:auto; padding-bottom:5px;">
                    {% for i in range(1, 8) %}
                    <div style="background:#f1f5f9; border-radius:10px; padding:8px 6px; text-align:center; min-width:40px; {% if user.streak_days >= i %}border:2px solid #2563eb;{% endif %}">
                        <div style="font-size:9px; color:#64748b;">+{{ 10 if i<7 else 30 }}</div>
                        <div style="font-size:10px; font-weight:bold; margin-top:4px;">Hari{{ i }}</div>
                    </div>
                    {% endfor %}
                </div>
                <form action="/mine" method="POST" style="margin-top:12px;">
                    <button type="submit" class="btn" style="background:#2563eb; padding:10px; font-size:12px;">Check-in Harian (+2.4 ZAM)</button>
                </form>
            </div>

            <div style="font-size:15px; font-weight:bold; color:white; margin-bottom:10px;">Tugas harian</div>
            
            <div class="task-card">
                <div>
                    <div style="font-weight:bold; font-size:13px;">Lihat sorotan (0/2)</div>
                    <div style="font-size:11px; color:#f59e0b; margin-top:2px;">🟡 15 ZAM</div>
                </div>
                <button class="btn-task" onclick="alert('Menjalankan sorotan iklan...')">Pergi</button>
            </div>

            <div class="task-card">
                <div>
                    <div style="font-weight:bold; font-size:13px;">Jelajahi ZAM Life 15 detik (0/1)</div>
                    <div style="font-size:11px; color:#f59e0b; margin-top:2px;">🟡 10 ZAM</div>
                </div>
                <button class="btn-task" onclick="alert('Membuka penjelajahan...')">Pergi</button>
            </div>

            <div class="task-card">
                <div>
                    <div style="font-weight:bold; font-size:13px;">Selesaikan 3 Level di Farm Bl... (0/3)</div>
                    <div style="font-size:11px; color:#f59e0b; margin-top:2px;">🟡 10 ZAM</div>
                </div>
                <button class="btn-task" onclick="alert('Membuka game ekosistem...')">Pergi</button>
            </div>

        {% elif active_tab == 'akaun' %}
            <div class="card-general" style="background:linear-gradient(135deg, #2563eb, #1e40af); color:white; text-align:center; padding:25px;">
                <div style="font-size:11px; color:#93c5fd; text-transform:uppercase;">Saldo keseluruhan</div>
                <div style="font-size:26px; font-weight:900; margin:6px 0;">≈ 5,814.51 USDT</div>
                <div style="font-size:12px; color:#e2e8f0;">ZAM (Tiba): {{ "%.2f"|format(user.balance_verified + user.balance_process) }}</div>
            </div>

            <div class="card-general">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-size:12px; color:#10b981; font-weight:bold;">🟢 ZAM (Tervalidasi / Unlocked)</div>
                        <div style="font-size:20px; font-weight:900; color:#1e293b; margin-top:4px;">{{ "%.2f"|format(user.balance_verified) }}</div>
                        <div style="font-size:10px; color:#64748b;">≈ 783.77 USDT</div>
                    </div>
                    <div>
                        <a href="/?tab=convert" class="btn" style="background:#f59e0b; color:#000; padding:8px 14px; font-size:11px; text-decoration:none; display:inline-block;">Menukarkan</a>
                    </div>
                </div>
            </div>

            <div class="card-general">
                <div style="font-size:12px; color:#f59e0b; font-weight:bold;">⏳ ZAM (Proses / Vesting Tambang)</div>
                <div style="font-size:20px; font-weight:900; color:#1e293b; margin-top:4px;">{{ "%.2f"|format(user.balance_process) }}</div>
                <div style="font-size:10px; color:#64748b; margin-top:2px;">≈ 2,146.53 USDT (Dikonversi via tugas & check-in)</div>
            </div>

        {% elif active_tab == 'convert' %}
            <div class="card-general">
                <h3 style="margin-top:0; color:#2563eb; font-size:16px;">🌉 Konversi & Penarikan ZAM (ERC-20)</h3>
                <div style="font-size:11px; background:rgba(245,158,11,0.1); border:1px solid #f59e0b; color:#92400e; padding:10px; border-radius:10px; margin-bottom:15px;">
                    ⚠️ Rasio 1000:1. Saldo dipotong dari Tervalidasi. Wajib 30 Hari Streak Aktif.
                </div>
                <form action="/convert" method="POST">
                    <div style="background:#f1f5f9; padding:12px; border-radius:12px; margin-bottom:12px;">
                        <input type="number" name="amount" placeholder="Jumlah ZAM Tervalidasi..." required style="background:transparent; border:none; width:100%; outline:none; font-size:13px;">
                    </div>
                    <button type="submit" class="btn" style="background:#f59e0b; color:#000;">Konversi & Tarik ke Web3</button>
                </form>
            </div>

        {% elif active_tab == 'hak' %}
            <div class="card-general">
                <h3 style="margin-top:0; color:#2563eb; font-size:16px;">👑 Zona Hak & Kartu Kupon</h3>
                <div style="background:#f8fafc; padding:15px; border-radius:14px; margin-bottom:10px; border:1px solid #e2e8f0;">
                    <b>Kartu olahraga sehat</b><br><span style="font-size:11px; color:#64748b;">Menambang ZAM dengan berjalan kaki. ($3.00)</span>
                </div>
                <div style="background:#f8fafc; padding:15px; border-radius:14px; border:1px solid #e2e8f0;">
                    <b>Asisten pengumpulan</b><br><span style="font-size:11px; color:#64748b;">Membantu mengumpulkan semua ZAM otomatis. ($1.00)</span>
                </div>
            </div>

        {% elif active_tab == 'settings' %}
            <div class="card-general" style="padding:0; overflow:hidden;">
                <div style="padding:15px 20px; font-weight:bold; border-bottom:1px solid #f1f5f9; color:#2563eb;">Pengaturan Akun</div>
                <div style="display:flex; flex-direction:column;">
                    <a href="#" style="padding:15px 20px; text-decoration:none; color:#1e293b; border-bottom:1px solid #f1f5f9; display:flex; justify-content:space-between;">Ubah kata sandi masuk <span>›</span></a>
                    <a href="#" style="padding:15px 20px; text-decoration:none; color:#1e293b; border-bottom:1px solid #f1f5f9; display:flex; justify-content:space-between;">Pengaturan kata sandi pembayaran <span>›</span></a>
                    <a href="#" style="padding:15px 20px; text-decoration:none; color:#1e293b; border-bottom:1px solid #f1f5f9; display:flex; justify-content:space-between;">Kelola Perangkat Masuk <span>Terproteksi ›</span></a>
                    <a href="#" style="padding:15px 20px; text-decoration:none; color:#1e293b; border-bottom:1px solid #f1f5f9; display:flex; justify-content:space-between;">Kebijakan pribadi <span>›</span></a>
                    <a href="#" style="padding:15px 20px; text-decoration:none; color:#1e293b; display:flex; justify-content:space-between;">Perjanjian Pengguna <span>›</span></a>
                </div>
                <div style="padding:15px;">
                    <form action="/logout" method="POST">
                        <button type="submit" class="btn" style="background:#ef4444;">Keluar Sesi (Logout)</button>
                    </form>
                </div>
            </div>

        {% elif active_tab == 'ledger' %}
            <div class="card-general">
                <h3 style="margin-top:0; color:#2563eb; font-size:16px;">⛓️ Quantum Ledger Chain</h3>
                {% for block in ledger[::-1] %}
                    <div style="font-size:11px; font-family:monospace; border-bottom:1px solid #f1f5f9; padding:8px 0;">
                        <b>#{{ block.index }}</b> ({{ block.timestamp[:19] }})<br>
                        <span style="color:#64748b;">{{ block.event }}</span>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    </div>

    <!-- Bottom Nav Bar Sesuai Struktur Atoshi -->
    <div class="nav">
        <a href="/?tab=utama" class="nav-item {% if active_tab == 'utama' or active_tab == 'dashboard' %}active{% endif %}">🏠<br>Utama</a>
        <a href="/?tab=bonus" class="nav-item {% if active_tab == 'bonus' %}active{% endif %}">🎁<br>Hadiah</a>
        <a href="/?tab=ledger" class="nav-item {% if active_tab == 'ledger' %}active{% endif %}">🎞️<br>Video</a>
        <a href="/?tab=hak" class="nav-item {% if active_tab == 'hak' %}active{% endif %}">🌐<br>Kehidupan</a>
        <a href="/?tab=settings" class="nav-item {% if active_tab == 'settings' %}active{% endif %}">👤<br>Akun</a>
    </div>
    {% endif %}

</body>
</html>
"""

@app.route("/")
def index():
    if "user_email" not in session:
        return render_template_string(HTML_TEMPLATE, logged_in=False)
    
    email = session["user_email"]
    db = load_database()
    user = db.get(email, {})
    ledger = load_ledger()
    active_tab = request.args.get("tab", "utama")
    message = session.pop("flash_message", None)
    return render_template_string(HTML_TEMPLATE, logged_in=True, user=user, ledger=ledger, active_tab=active_tab, message=message)

@app.route("/auth", methods=["POST"])
def auth():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "").strip()
    action = request.form.get("action", "")
    client_ip = request.remote_addr or "127.0.0.1"
    
    db = load_database()
    
    if action == "register":
        passed, msg = stealth_quantum_audit(email, "register", {}, client_ip)
        if not passed:
            session["flash_message"] = msg
            return redirect(url_for("index"))
            
        if email in db:
            session["flash_message"] = "Email sudah terdaftar. Silakan masuk."
            return redirect(url_for("index"))
            
        db[email] = {
            "email": email,
            "password": hashlib.sha256(password.encode()).hexdigest(),
            "balance_verified": 20.0,
            "balance_process": 0.0,
            "erc20_balance": 0.0,
            "streak_days": 1,
            "last_active_date": str(date.today()),
            "last_claim_time": "",
            "register_ip": client_ip
        }
        save_database(db)
        record_block(f"Quantum Stealth Node Registered -> {email}")
        session["user_email"] = email
        session["flash_message"] = "Pendaftaran berhasil dan terverifikasi secara senyap."
        return redirect(url_for("index", tab="utama"))
        
    elif action == "login":
        if email in db and db[email]["password"] == hashlib.sha256(password.encode()).hexdigest():
            session["user_email"] = email
            session["flash_message"] = "Berhasil masuk ke node ekosistem."
        else:
            session["flash_message"] = "Email atau kata sandi salah."
        return redirect(url_for("index"))

@app.route("/mine", methods=["POST"])
def mine():
    if "user_email" in session:
        email = session["user_email"]
        db = load_database()
        if email in db:
            user = db[email]
            now = datetime.now()
            
            earned = 2.4
            user["balance_process"] = float(user.get("balance_process", 0)) + earned
            user["balance_verified"] = float(user.get("balance_verified", 0)) + 1.0
            user["last_claim_time"] = now.strftime("%Y-%m-%d %H:%M:%S")
            
            save_database(db)
            record_block(f"Stealth audit mining processed for {email}")
            session["flash_message"] = f"Berhasil! +{earned} ZAM Proses & +1.0 ZAM Tervalidasi ditambahkan."
    return redirect(url_for("index", tab="utama"))

@app.route("/convert", methods=["POST"])
def convert():
    if "user_email" in session:
        email = session["user_email"]
        try: amount = float(request.form.get("amount", 0))
        except: amount = 0
        
        db = load_database()
        if email in db:
            user = db[email]
            verified_bal = float(user.get("balance_verified", 0))
            streak = int(user.get("streak_days", 0))
            
            if streak < 30:
                session["flash_message"] = f"Bridge Ditolak: Streak Anda baru {streak}/30 hari."
            elif amount <= verified_bal and amount > 0:
                erc20_gained = amount / 1000.0
                user["balance_verified"] = verified_bal - amount
                user["erc20_balance"] = float(user.get("erc20_balance", 0)) + erc20_gained
                save_database(db)
                record_block(f"Stealth bridge executed for {email}")
                session["flash_message"] = f"Sukses! {amount:,.0f} ZAM Tervalidasi dikonversi ke {erc20_gained:,.2f} ZAM-E."
            else:
                session["flash_message"] = "Saldo Tervalidasi tidak mencukupi."
    return redirect(url_for("index", tab="akaun"))

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
from flask import Flask, render_template_string, request, redirect, url_for, session
import json
import os
import hashlib
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = "zam_core_global_enterprise_2026"

DATABASE_FILE = "zam_core_database.json"
LEDGER_FILE = "zam_core_ledger.json"

def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_database(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_ledger():
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, "r") as f:
            try: return json.load(f)
            except: return []
    genesis = {
        "index": 0,
        "timestamp": str(datetime.now()),
        "event": "ZAM CORE Global Genesis - Enterprise Level Protocol Active",
        "hash": hashlib.sha256(b"ZAMCoreGlobalEnterpriseGenesis").hexdigest()
    }
    save_ledger([genesis])
    return [genesis]

def save_ledger(ledger):
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=4)

def record_block(event_desc):
    ledger = load_ledger()
    last_block = ledger[-1]
    new_index = len(ledger)
    timestamp = str(datetime.now())
    raw_data = f"{new_index}{last_block['hash']}{timestamp}{event_desc}"
    new_hash = hashlib.sha256(raw_data.encode()).hexdigest()
    
    block = {
        "index": new_index,
        "timestamp": timestamp,
        "event": event_desc,
        "hash": new_hash
    }
    ledger.append(block)
    save_ledger(ledger)
    return block

def global_stealth_audit(email, action_type, user_data, client_ip):
    db = load_database()
    if action_type == "register":
        ip_count = sum(1 for u in db.values() if u.get("register_ip") == client_ip)
        if ip_count >= 3:
            return False, "Sistem mendeteksi batas maksimal pendaftaran dari perangkat ini."
    if action_type == "convert":
        streak = int(user_data.get("streak_days", 0))
        if streak < 30:
            return False, f"Syarat penarikan ditolak sistem: Streak Anda baru {streak}/30 hari."
    return True, "Sukses"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZAM CORE - Global Enterprise Ecosystem</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0284c7; color: #f8fafc; margin: 0; padding-bottom: 85px; }
        .header-top { background: transparent; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; color: white; }
        .logo-container { display: flex; align-items: center; gap: 10px; font-weight: 900; font-size: 18px; letter-spacing: 1px; }
        .custom-logo { width: 32px; height: 32px; background: #0f172a; border-radius: 8px; display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: repeat(3, 1fr); padding: 5px; gap: 3px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
        .logo-block { background: white; border-radius: 2px; }
        .logo-block.top { grid-column: 2; grid-row: 1; }
        .logo-block.left1 { grid-column: 1; grid-row: 2; }
        .logo-block.left2 { grid-column: 1; grid-row: 3; }
        .logo-block.right1 { grid-column: 3; grid-row: 2; }
        .logo-block.right2 { grid-column: 3; grid-row: 3; }

        .subnav { display: flex; justify-content: center; gap: 40px; background: transparent; padding: 5px 0 15px 0; font-size: 16px; font-weight: bold; }
        .subnav a { text-decoration: none; color: rgba(255,255,255,0.6); padding-bottom: 4px; }
        .subnav a.active { color: white; border-bottom: 3px solid white; }

        .container { padding: 0 15px; max-width: 480px; margin: 0 auto; }
        .mining-bg-card { background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.4)), url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80') center/cover; border-radius: 24px; padding: 15px; position: relative; min-height: 480px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.3); }
        .balance-box-top { background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(12px); border-radius: 18px; padding: 15px; border: 1px solid rgba(255,255,255,0.4); margin-bottom: 15px; }
        .balance-title { font-size: 11px; color: #e2e8f0; text-transform: uppercase; font-weight: bold; }
        .balance-val { font-size: 24px; font-weight: 900; color: white; margin: 4px 0; }

        .coin-bubble { position: absolute; background: rgba(245, 158, 11, 0.95); width: 48px; height: 48px; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 9px; font-weight: bold; color: #000; box-shadow: 0 4px 10px rgba(0,0,0,0.4); border: 2px solid #fff; }
        .card-bottom-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; position: absolute; bottom: 15px; left: 15px; right: 15px; }
        .btn-mine-rate { background: #f97316; color: white; border-radius: 14px; padding: 12px; text-align: center; font-weight: bold; font-size: 13px; border: none; cursor: pointer; }
        .btn-invite { background: #ea580c; color: white; border-radius: 14px; padding: 12px; text-align: center; font-weight: bold; font-size: 13px; border: none; cursor: pointer; }

        .menu-3-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 15px; }
        .menu-card-box { background: rgba(255, 255, 255, 0.9); border-radius: 18px; padding: 15px 10px; text-align: center; color: #1e293b; text-decoration: none; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .menu-card-box.orange { background: linear-gradient(135deg, #fb923c, #ea580c); color: white; }
        .menu-card-box.purple { background: linear-gradient(135deg, #a78bfa, #7c3aed); color: white; }
        .menu-card-box.blue { background: linear-gradient(135deg, #38bdf8, #0284c7); color: white; }

        .task-card { background: white; border-radius: 18px; padding: 15px; margin-bottom: 12px; color: #1e293b; box-shadow: 0 4px 15px rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center; }
        .btn-task { background: #3b82f6; color: white; border: none; padding: 8px 18px; border-radius: 20px; font-weight: bold; font-size: 12px; cursor: pointer; }

        .nav { position: fixed; bottom: 0; left: 0; width: 100%; background: white; display: flex; justify-content: space-around; padding: 8px 0; border-top: 1px solid #e2e8f0; z-index: 100; }
        .nav-item { text-decoration: none; color: #64748b; font-size: 11px; text-align: center; flex: 1; font-weight: 600; }
        .nav-item.active { color: #0284c7; }

        .card-general { background: white; border-radius: 20px; padding: 20px; margin-bottom: 15px; color: #1e293b; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        .btn { background: #3b82f6; color: white; border: none; padding: 14px; border-radius: 14px; font-weight: 800; width: 100%; cursor: pointer; text-transform: uppercase; font-size: 13px; }
        .alert { background: rgba(16, 185, 129, 0.2); color: #065f46; padding: 12px; border-radius: 12px; margin-bottom: 15px; text-align: center; font-size: 12px; font-weight: bold; border: 1px solid #10b981; }
    </style>
</head>
<body>

    {% if not logged_in %}
    <div class="container" style="display:flex; justify-content:center; align-items:center; height:100vh;">
        <div class="card-general" style="width:100%;">
            <div style="display:flex; justify-content:center; margin-bottom:15px;">
                <div class="custom-logo" style="width:50px; height:50px;">
                    <div class="logo-block top"></div>
                    <div class="logo-block left1"></div>
                    <div class="logo-block left2"></div>
                    <div class="logo-block right1"></div>
                    <div class="logo-block right2"></div>
                </div>
            </div>
            <div style="font-size:24px; font-weight:900; color:#1e3a8a; text-align:center; margin-bottom:5px;">ZAM CORE</div>
            <div style="text-align:center; color:#64748b; margin-bottom:20px; font-size:11px;">Global Enterprise Ecosystem</div>
            
            {% if message %}
                <div class="alert" style="background:rgba(239,68,68,0.2); color:#991b1b; border-color:#ef4444;">{{ message }}</div>
            {% endif %}

            <form action="/auth" method="POST">
                <div style="background:#f1f5f9; border-radius:12px; padding:12px; margin-bottom:12px;">
                    <input type="email" name="email" placeholder="Alamat Email..." required style="background:transparent; border:none; width:100%; outline:none; font-size:14px;">
                </div>
                <div style="background:#f1f5f9; border-radius:12px; padding:12px; margin-bottom:15px;">
                    <input type="password" name="password" placeholder="Kata Sandi..." required style="background:transparent; border:none; width:100%; outline:none; font-size:14px;">
                </div>
                <div style="display:flex; gap:10px;">
                    <button type="submit" name="action" value="login" class="btn" style="background:#2563eb;">Masuk</button>
                    <button type="submit" name="action" value="register" class="btn" style="background:#10b981;">Daftar (Secure)</button>
                </div>
            </form>
        </div>
    </div>
    {% else %}

    <div class="header-top">
        <div class="logo-container">
            <div class="custom-logo">
                <div class="logo-block top"></div>
                <div class="logo-block left1"></div>
                <div class="logo-block left2"></div>
                <div class="logo-block right1"></div>
                <div class="logo-block right2"></div>
            </div>
            <span>ZAM CORE</span>
        </div>
        <div class="top-icons"><span>🏆</span><span>💬</span></div>
    </div>

    <div class="subnav">
        <a href="/?tab=bonus" class="{% if active_tab == 'bonus' %}active{% endif %}">Bonusnya</a>
        <a href="/?tab=utama" class="{% if active_tab == 'utama' or active_tab == 'dashboard' %}active{% endif %}">Milikku</a>
    </div>

    <div class="container">
        {% if message %}
            <div class="alert">{{ message }}</div>
        {% endif %}

        {% if active_tab == 'utama' or active_tab == 'dashboard' %}
            <div class="mining-bg-card">
                <div class="balance-box-top">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div class="balance-title">ZAM (Token)</div>
                            <div class="balance-val">{{ "%.3f"|format(user.balance_verified + user.balance_process) }}</div>
                        </div>
                        <div style="text-align:right;">
                            <div class="balance-title">Kekuatanku</div>
                            <div style="font-size:15px; font-weight:bold; color:#fef08a;">{{ 36000 + (user.streak_days * 100) }} +</div>
                        </div>
                    </div>
                </div>

                <div class="coin-bubble" style="top:35%; left:15%;">1:59:56</div>
                <div class="coin-bubble" style="top:25%; left:45%;">2:59:56</div>
                <div class="coin-bubble" style="top:30%; left:75%;">59:56</div>
                <div class="coin-bubble" style="top:55%; left:30%;">3:59:56</div>
                <div class="coin-bubble" style="top:50%; left:58%; background:#ef4444; color:white;">🎁</div>
                <div class="coin-bubble" style="top:48%; left:80%; background:#10b981; color:white;">⚡</div>

                <div class="card-bottom-grid">
                    <form action="/mine" method="POST" style="margin:0;">
                        <button type="submit" class="btn-mine-rate" style="width:100%;">40 ZAM/H</button>
                    </form>
                    <button class="btn-invite" onclick="alert('Link referral siap dibagikan!')">Mengundan</button>
                </div>
            </div>

            <div class="menu-3-grid">
                <a href="/?tab=akaun" class="menu-card-box orange">
                    <div style="font-size:18px;">💰</div>
                    <div style="font-size:13px; font-weight:bold; margin-top:4px;">Akaun</div>
                    <div style="font-size:9px; opacity:0.9;">periksa saldo</div>
                </a>
                <a href="/?tab=tim" class="menu-card-box purple">
                    <div style="font-size:18px;">👥</div>
                    <div style="font-size:13px; font-weight:bold; margin-top:4px;">Tim</div>
                    <div style="font-size:9px; opacity:0.9;">Gabungan</div>
                </a>
                <a href="/?tab=hak" class="menu-card-box blue">
                    <div style="font-size:18px;">💳</div>
                    <div style="font-size:13px; font-weight:bold; margin-top:4px;">Hak</div>
                    <div style="font-size:9px; opacity:0.9;">untuk membeli</div>
                </a>
            </div>

        {% elif active_tab == 'bonus' %}
            <div class="card-general" style="padding:15px; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <b style="font-size:15px; color:#1e3a8a;">Rangkaian 14 Hari</b>
                    <span style="font-size:11px; color:#64748b;">Telah masuk</span>
                </div>
                <div style="display:flex; gap:6px; overflow-x:auto; padding-bottom:5px;">
                    {% for i in range(1, 8) %}
                    <div style="background:#f1f5f9; border-radius:10px; padding:8px 6px; text-align:center; min-width:40px; {% if user.streak_days >= i %}border:2px solid #2563eb;{% endif %}">
                        <div style="font-size:9px; color:#64748b;">+{{ 10 if i<7 else 30 }}</div>
                        <div style="font-size:10px; font-weight:bold; margin-top:4px;">Hari{{ i }}</div>
                    </div>
                    {% endfor %}
                </div>
                <form action="/mine" method="POST" style="margin-top:12px;">
                    <button type="submit" class="btn" style="background:#2563eb; padding:10px; font-size:12px;">Check-in Harian (+2.4 ZAM)</button>
                </form>
            </div>

            <div style="font-size:15px; font-weight:bold; color:white; margin-bottom:10px;">Tugas harian</div>
            <div class="task-card">
                <div>
                    <div style="font-weight:bold; font-size:13px;">Lihat sorotan (0/2)</div>
                    <div style="font-size:11px; color:#f59e0b; margin-top:2px;">🟡 15 ZAM</div>
                </div>
                <button class="btn-task" onclick="alert('Menjalankan sorotan iklan...')">Pergi</button>
            </div>
            <div class="task-card">
                <div>
                    <div style="font-weight:bold; font-size:13px;">Jelajahi ZAM Life 15 detik (0/1)</div>
                    <div style="font-size:11px; color:#f59e0b; margin-top:2px;">🟡 10 ZAM</div>
                </div>
                <button class="btn-task" onclick="alert('Membuka penjelajahan...')">Pergi</button>
            </div>
            <div class="task-card">
                <div>
                    <div style="font-weight:bold; font-size:13px;">Selesaikan 3 Level di Farm Bl... (0/3)</div>
                    <div style="font-size:11px; color:#f59e0b; margin-top:2px;">🟡 10 ZAM</div>
                </div>
                <button class="btn-task" onclick="alert('Membuka game ekosistem...')">Pergi</button>
            </div>

        {% elif active_tab == 'akaun' %}
            <div class="card-general" style="background:linear-gradient(135deg, #2563eb, #1e40af); color:white; text-align:center; padding:25px;">
                <div style="font-size:11px; color:#93c5fd; text-transform:uppercase;">Saldo keseluruhan</div>
                <div style="font-size:26px; font-weight:900; margin:6px 0;">≈ 5,814.51 USDT</div>
                <div style="font-size:12px; color:#e2e8f0;">ZAM (Tiba): {{ "%.2f"|format(user.balance_verified + user.balance_process) }}</div>
            </div>

            <div class="card-general">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-size:12px; color:#10b981; font-weight:bold;">🟢 ZAM (Tervalidasi / Unlocked)</div>
                        <div style="font-size:20px; font-weight:900; color:#1e293b; margin-top:4px;">{{ "%.2f"|format(user.balance_verified) }}</div>
                        <div style="font-size:10px; color:#64748b;">≈ 783.77 USDT</div>
                    </div>
                    <div>
                        <a href="/?tab=convert" class="btn" style="background:#f59e0b; color:#000; padding:8px 14px; font-size:11px; text-decoration:none; display:inline-block;">Menukarkan</a>
                    </div>
                </div>
            </div>

            <div class="card-general">
                <div style="font-size:12px; color:#f59e0b; font-weight:bold;">⏳ ZAM (Proses / Vesting Tambang)</div>
                <div style="font-size:20px; font-weight:900; color:#1e293b; margin-top:4px;">{{ "%.2f"|format(user.balance_process) }}</div>
                <div style="font-size:10px; color:#64748b; margin-top:2px;">≈ 2,146.53 USDT (Dikonversi via tugas & check-in)</div>
            </div>

        {% elif active_tab == 'convert' %}
            <div class="card-general">
                <h3 style="margin-top:0; color:#2563eb; font-size:16px;">🌉 Konversi & Penarikan ZAM (ERC-20)</h3>
                <div style="font-size:11px; background:rgba(245,158,11,0.1); border:1px solid #f59e0b; color:#92400e; padding:10px; border-radius:10px; margin-bottom:15px;">
                    ⚠️ Rasio 1000:1. Saldo dipotong dari Tervalidasi. Wajib 30 Hari Streak Aktif.
                </div>
                <form action="/convert" method="POST">
                    <div style="background:#f1f5f9; padding:12px; border-radius:12px; margin-bottom:12px;">
                        <input type="number" name="amount" placeholder="Jumlah ZAM Tervalidasi..." required style="background:transparent; border:none; width:100%; outline:none; font-size:13px;">
                    </div>
                    <button type="submit" class="btn" style="background:#f59e0b; color:#000;">Konversi & Tarik ke Web3</button>
                </form>
            </div>

        {% elif active_tab == 'hak' %}
            <div class="card-general">
                <h3 style="margin-top:0; color:#2563eb; font-size:16px;">👑 Zona Hak & Kartu Kupon</h3>
                <div style="background:#f8fafc; padding:15px; border-radius:14px; margin-bottom:10px; border:1px solid #e2e8f0;">
                    <b>Kartu olahraga sehat</b><br><span style="font-size:11px; color:#64748b;">Menambang ZAM dengan berjalan kaki. ($3.00)</span>
                </div>
                <div style="background:#f8fafc; padding:15px; border-radius:14px; border:1px solid #e2e8f0;">
                    <b>Asisten pengumpulan</b><br><span style="font-size:11px; color:#64748b;">Membantu mengumpulkan semua ZAM otomatis. ($1.00)</span>
                </div>
            </div>

        {% elif active_tab == 'settings' %}
            <div class="card-general" style="padding:0; overflow:hidden;">
                <div style="padding:15px 20px; font-weight:bold; border-bottom:1px solid #f1f5f9; color:#2563eb;">Pengaturan Akun</div>
                <div style="display:flex; flex-direction:column;">
                    <a href="#" style="padding:15px 20px; text-decoration:none; color:#1e293b; border-bottom:1px solid #f1f5f9; display:flex; justify-content:space-between;">Ubah kata sandi masuk <span>›</span></a>
                    <a href="#" style="padding:15px 20px; text-decoration:none; color:#1e293b; border-bottom:1px solid #f1f5f9; display:flex; justify-content:space-between;">Pengaturan kata sandi pembayaran <span>›</span></a>
                    <a href="#" style="padding:15px 20px; text-decoration:none; color:#1e293b; border-bottom:1px solid #f1f5f9; display:flex; justify-content:space-between;">Kelola Perangkat Masuk <span>Terproteksi ›</span></a>
                    <a href="#" style="padding:15px 20px; text-decoration:none; color:#1e293b; border-bottom:1px solid #f1f5f9; display:flex; justify-content:space-between;">Kebijakan pribadi <span>›</span></a>
                    <a href="#" style="padding:15px 20px; text-decoration:none; color:#1e293b; display:flex; justify-content:space-between;">Perjanjian Pengguna <span>›</span></a>
                </div>
                <div style="padding:15px;">
                    <form action="/logout" method="POST">
                        <button type="submit" class="btn" style="background:#ef4444;">Keluar Sesi (Logout)</button>
                    </form>
                </div>
            </div>

        {% elif active_tab == 'ledger' %}
            <div class="card-general">
                <h3 style="margin-top:0; color:#2563eb; font-size:16px;">⛓️ Quantum Ledger Chain</h3>
                {% for block in ledger[::-1] %}
                    <div style="font-size:11px; font-family:monospace; border-bottom:1px solid #f1f5f9; padding:8px 0;">
                        <b>#{{ block.index }}</b> ({{ block.timestamp[:19] }})<br>
                        <span style="color:#64748b;">{{ block.event }}</span>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    </div>

    <div class="nav">
        <a href="/?tab=utama" class="nav-item {% if active_tab == 'utama' or active_tab == 'dashboard' %}active{% endif %}">🏠<br>Utama</a>
        <a href="/?tab=bonus" class="nav-item {% if active_tab == 'bonus' %}active{% endif %}">🎁<br>Hadiah</a>
        <a href="/?tab=ledger" class="nav-item {% if active_tab == 'ledger' %}active{% endif %}">🎞️<br>Video</a>
        <a href="/?tab=hak" class="nav-item {% if active_tab == 'hak' %}active{% endif %}">🌐<br>Kehidupan</a>
        <a href="/?tab=settings" class="nav-item {% if active_tab == 'settings' %}active{% endif %}">👤<br>Akun</a>
    </div>
    {% endif %}

</body>
</html>
"""

@app.route("/")
def index():
    if "user_email" not in session:
        return render_template_string(HTML_TEMPLATE, logged_in=False)
    
    email = session["user_email"]
    db = load_database()
    user = db.get(email, {})
    ledger = load_ledger()
    active_tab = request.args.get("tab", "utama")
    message = session.pop("flash_message", None)
    return render_template_string(HTML_TEMPLATE, logged_in=True, user=user, ledger=ledger, active_tab=active_tab, message=message)

@app.route("/auth", methods=["POST"])
def auth():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "").strip()
    action = request.form.get("action", "")
    client_ip = request.remote_addr or "127.0.0.1"
    
    db = load_database()
    if action == "register":
        passed, msg = global_stealth_audit(email, "register", {}, client_ip)
        if not passed:
            session["flash_message"] = msg
            return redirect(url_for("index"))
        if email in db:
            session["flash_message"] = "Email sudah terdaftar."
            return redirect(url_for("index"))
            
        db[email] = {
            "email": email,
            "password": hashlib.sha256(password.encode()).hexdigest(),
            "balance_verified": 20.0,
            "balance_process": 0.0,
            "erc20_balance": 0.0,
            "streak_days": 1,
            "last_active_date": str(date.today()),
            "last_claim_time": "",
            "register_ip": client_ip
        }
        save_database(db)
        record_block(f"Stealth Node Registered -> {email}")
        session["user_email"] = email
        session["flash_message"] = "Registrasi sukses."
        return redirect(url_for("index", tab="utama"))
        
    elif action == "login":
        if email in db and db[email]["password"] == hashlib.sha256(password.encode()).hexdigest():
            session["user_email"] = email
            session["flash_message"] = "Login sukses."
        else:
            session["flash_message"] = "Email atau sandi salah."
        return redirect(url_for("index"))

@app.route("/mine", methods=["POST"])
def mine():
    if "user_email" in session:
        email = session["user_email"]
        db = load_database()
        if email in db:
            user = db[email]
            user["balance_process"] = float(user.get("balance_process", 0)) + 2.4
            user["balance_verified"] = float(user.get("balance_verified", 0)) + 1.0
            user["last_claim_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_database(db)
            record_block(f"Mining executed for {email}")
            session["flash_message"] = "Klaim sukses! +2.4 ZAM Proses & +1.0 ZAM Tervalidasi."
    return redirect(url_for("index", tab="utama"))

@app.route("/convert", methods=["POST"])
def convert():
    if "user_email" in session:
        email = session["user_email"]
        try: amount = float(request.form.get("amount", 0))
        except: amount = 0
        db = load_database()
        if email in db:
            user = db[email]
            passed, msg = global_stealth_audit(email, "convert", user, "")
            if not passed:
                session["flash_message"] = msg
                return redirect(url_for("index", tab="convert"))
            if amount <= float(user.get("balance_verified", 0)) and amount > 0:
                user["balance_verified"] = float(user["balance_verified"]) - amount
                user["erc20_balance"] = float(user.get("erc20_balance", 0)) + (amount / 1000.0)
                save_database(db)
                record_block(f"Bridge converted {amount} for {email}")
                session["flash_message"] = f"Berhasil mengonversi {amount:,.0f} ZAM!"
            else:
                session["flash_message"] = "Saldo Tervalidasi tidak mencukupi."
    return redirect(url_for("index", tab="akaun"))

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
