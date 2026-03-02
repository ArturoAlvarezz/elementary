#!/usr/bin/env python3
"""Sherlock OSINT API Backend"""
import subprocess
import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "sherlock-backend"})

@app.route('/api/search', methods=['POST'])
def search():
    """Execute Sherlock search with --json output"""
    data = request.get_json()
    username = data.get('username', '').strip()
    if not username:
        return jsonify({"error": "Username required"}), 400

    # Archivo temporal unico por usuario para evitar conflictos
    output_file = f'/tmp/{username}_sherlock.json'

    try:
        # Run sherlock with --json flag pointing to file
        cmd = ['sherlock', username, '--json', output_file, '--timeout', '10']
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        # Leer el archivo JSON generado por Sherlock
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                sherlock_data = json.load(f)

            # Limpiar archivo temporal
            os.remove(output_file)

            # Sherlock devuelve diccionario con sitios como claves
            found_count = len([v for v in sherlock_data.values() if v.get('exists')])

            return jsonify({
                "username": username,
                "results": sherlock_data,
                "found": found_count
            })
        else:
            return jsonify({
                "username": username,
                "error": "No output file generated",
                "stderr": result.stderr
            }), 500

    except subprocess.TimeoutExpired:
        return jsonify({"error": "Search timeout"}), 504
    except json.JSONDecodeError as e:
        return jsonify({"error": f"JSON parse error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/sites', methods=['GET'])
def list_sites():
    """List supported sites"""
    try:
        result = subprocess.run(
            ['sherlock', '--list-all-sites'],
            capture_output=True,
            text=True,
            timeout=30
        )
        sites = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        return jsonify({"sites": sites, "count": len(sites)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
