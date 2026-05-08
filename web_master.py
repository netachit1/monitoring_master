from flask import Flask, render_template, request, jsonify
import sqlite3
import json
import os
from datetime import datetime

app = Flask(__name__)
DB_FILE = "monitoring_master.db"

# راه‌اندازی دیتابیس
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS metrics
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  node_name TEXT,
                  timestamp TEXT,
                  cpu REAL,
                  mem REAL,
                  disk REAL,
                  connections INTEGER)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def dashboard():
    return render_template('master.html')

@app.route('/api/nodes')
def get_nodes():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT DISTINCT node_name FROM metrics")
    nodes = [row[0] for row in c.fetchall()]
    conn.close()
    return jsonify(nodes)

@app.route('/api/latest')
def get_latest():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        SELECT node_name, timestamp, cpu, mem, disk, connections
        FROM metrics m1
        WHERE timestamp = (SELECT MAX(timestamp) FROM metrics m2 WHERE m2.node_name = m1.node_name)
    """)
    data = []
    for row in c.fetchall():
        data.append({
            'node': row[0],
            'timestamp': row[1],
            'cpu': round(row[2], 1),
            'mem': round(row[3], 1),
            'disk': round(row[4], 1),
            'connections': row[5]
        })
    conn.close()
    return jsonify(data)

@app.route('/api/history/<node>')
def get_history(node):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        SELECT timestamp, cpu, mem, disk, connections
        FROM metrics WHERE node_name = ?
        ORDER BY timestamp DESC
    """, (node,))   # ← حذف LIMIT، یعنی همه رکوردها

@app.route('/api/report', methods=['POST'])
def report():
    data = request.json
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO metrics (node_name, timestamp, cpu, mem, disk, connections)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (data['node_name'], data['timestamp'], data['cpu'], data['mem'], data['disk'], data['connections']))
    conn.commit()
    conn.close()
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

