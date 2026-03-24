"""
TTC Damme - Lokale Flask Server
Serveert de dashboard app en biedt een /api/update endpoint
om data vers op te halen van VTTL.

Start met: python server.py
Open dan: http://localhost:5000
"""

import os
import sys
import json
import subprocess
import threading
from pathlib import Path

try:
    from flask import Flask, send_from_directory, jsonify, send_file
except ImportError:
    print("Flask niet gevonden. Installeren...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    from flask import Flask, send_from_directory, jsonify, send_file

BASE_DIR = Path(__file__).parent.resolve()

app = Flask(__name__, static_folder=str(BASE_DIR))

# Status tracking for update process (using dict with Any values for flexibility)
update_status: dict = {
    "running": False,
    "last_result": None,
    "last_update": None
}


def run_update():
    """Run all data scraping scripts in sequence."""
    update_status["running"] = True
    update_status["last_result"] = None
    logs = []
    
    scripts = [
        ("Rangschikkingen ophalen", "get_all_rankings.py"),
        ("Teamkalenders ophalen", "get_team_calendars.py"),
        ("Wedstrijddetails ophalen", "get_match_details.py"),
        ("Data.js aanmaken", "json_to_js.py"),
    ]
    
    try:
        for label, script in scripts:
            logs.append(f"▶ {label}...")
            result = subprocess.run(
                [sys.executable, str(BASE_DIR / script)],
                capture_output=True,
                text=True,
                cwd=str(BASE_DIR),
                timeout=300
            )
            if result.returncode != 0:
                logs.append(f"✗ FOUT in {script}:\n{result.stderr}")
                update_status["last_result"] = {"success": False, "logs": logs}
                return
            logs.append(f"✓ {label} geslaagd")
        
        from datetime import datetime
        update_status["last_update"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        update_status["last_result"] = {
            "success": True,
            "logs": logs,
            "timestamp": update_status["last_update"]
        }
    except subprocess.TimeoutExpired:
        logs.append("✗ FOUT: Timeout (script duurde te lang)")
        update_status["last_result"] = {"success": False, "logs": logs}
    except Exception as e:
        logs.append(f"✗ Onverwachte fout: {e}")
        update_status["last_result"] = {"success": False, "logs": logs}
    finally:
        update_status["running"] = False


@app.route("/")
def index():
    return send_file(str(BASE_DIR / "index.html"))


@app.route("/api/update", methods=["POST"])
def api_update():
    """Trigger a data update. Returns immediately; client can poll /api/update/status."""
    if update_status["running"]:
        return jsonify({"status": "already_running"}), 200
    
    thread = threading.Thread(target=run_update, daemon=True)
    thread.start()
    return jsonify({"status": "started"}), 200


@app.route("/api/update/status", methods=["GET"])
def api_update_status():
    """Poll this endpoint to check if an update is complete."""
    return jsonify({
        "running": update_status["running"],
        "result": update_status["last_result"],
        "last_update": update_status["last_update"]
    })


@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(str(BASE_DIR), filename)


if __name__ == "__main__":
    print("=" * 50)
    print("  TTC Damme - Lokale Server")
    print("=" * 50)
    print(f"  Dashboard: http://localhost:5000")
    print(f"  Data map:  {BASE_DIR}")
    print("=" * 50)
    print("  Druk op CTRL+C om te stoppen")
    print()
    app.run(host="0.0.0.0", port=5000, debug=False)
