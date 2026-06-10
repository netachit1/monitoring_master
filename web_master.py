from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import os
import time
from contextlib import contextmanager

DB_FILE = os.environ.get('DB_FILE', '/app/monitoring_master.db')
app = Flask(__name__)

@contextmanager
def get_db():
    """مدیریت اتصال دیتابیس با timeout و retry"""
    conn = None
    for attempt in range(5):
        try:
            conn = sqlite3.connect(DB_FILE, timeout=30, isolation_level=None)
            conn.row_factory = sqlite3.Row
            yield conn
            break
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e) and attempt < 4:
                time.sleep(0.5 * (attempt + 1))
                continue
            raise
        finally:
            if conn:
                conn.close()

def init_db():
    with get_db() as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS metrics
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      node_name TEXT,
                      timestamp TEXT,
                      cpu REAL,
                      mem REAL,
                      disk REAL,
                      connections INTEGER,
                      temperature REAL,
                      gpu_usage REAL,
                      gpu_mem REAL,
                      gpu_temp REAL)''')
        conn.commit()

init_db()

@app.route('/')
def dashboard():
    return render_template('master.html')

@app.route('/api/nodes')
def get_nodes():
    try:
        with get_db() as conn:
            c = conn.cursor()
            c.execute("SELECT DISTINCT node_name FROM metrics")
            nodes = [row[0] for row in c.fetchall()]
        return jsonify(nodes)
    except Exception as e:
        print(f"Error in nodes: {e}")
        return jsonify([])

@app.route('/api/latest')
def get_latest():
    try:
        with get_db() as conn:
            c = conn.cursor()
            c.execute("""
                SELECT node_name, timestamp, cpu, mem, disk, connections, temperature, gpu_usage, gpu_mem, gpu_temp
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
                    'connections': row[5],
                    'temperature': row[6],
                    'gpu_usage': row[7],
                    'gpu_mem': row[8],
                    'gpu_temp': row[9]
                })
        return jsonify(data)
    except Exception as e:
        print(f"Error in latest: {e}")
        return jsonify([])

@app.route('/api/history/<node>')
@app.route('/api/history/<node>/<int:limit>')
def get_history(node, limit=100):
    try:
        with get_db() as conn:
            c = conn.cursor()
            c.execute("""
                SELECT timestamp, cpu, mem, disk, connections, temperature, gpu_usage, gpu_mem, gpu_temp
                FROM metrics 
                WHERE node_name = ?
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (node, limit))
            rows = c.fetchall()
            data = []
            for row in rows:
                data.append({
                    'timestamp': row[0],
                    'cpu': round(row[1], 1),
                    'mem': round(row[2], 1),
                    'disk': round(row[3], 1),
                    'connections': row[4],
                    'temperature': row[5],
                    'gpu_usage': row[6],
                    'gpu_mem': row[7],
                    'gpu_temp': row[8]
                })
        return jsonify(data)
    except Exception as e:
        print(f"Error in history: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/report', methods=['POST'])
def report():
    try:
        data = request.json
        with get_db() as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO metrics (node_name, timestamp, cpu, mem, disk, connections, temperature, gpu_usage, gpu_mem, gpu_temp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (data['node_name'], data['timestamp'], data['cpu'],
                  data['mem'], data['disk'], data['connections'],
                  data.get('temperature'), data.get('gpu_usage'),
                  data.get('gpu_mem'), data.get('gpu_temp')))
            conn.commit()
        return jsonify({'status': 'ok'})
    except Exception as e:
        print(f"Error in report: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=False)