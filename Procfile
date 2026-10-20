web: python zam_core.py
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
