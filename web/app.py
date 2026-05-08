from flask import Flask, render_template, request, jsonify
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

# تنظیمات دیتابیس
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'database': os.environ.get('DB_NAME', 'monitoring'),
    'user': os.environ.get('DB_USER', 'admin'),
    'password': os.environ.get('DB_PASS', 'secretpassword123')
}

def get_db():
    return psycopg2.connect(**DB_CONFIG)

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/api/nodes')
def get_nodes():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT node_name FROM system_metrics ORDER BY node_name")
    nodes = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(nodes)

@app.route('/api/latest')
def get_latest():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT ON (node_name) 
            node_name, timestamp, cpu_percent, memory_percent, disk_percent, connections
        FROM system_metrics 
        ORDER BY node_name, timestamp DESC
    """)
    data = []
    for row in cur.fetchall():
        data.append({
            'node': row[0],
            'timestamp': row[1].strftime('%Y-%m-%d %H:%M:%S'),
            'cpu': round(row[2], 1),
            'mem': round(row[3], 1),
            'disk': round(row[4], 1),
            'connections': row[5]
        })
    cur.close()
    conn.close()
    return jsonify(data)

@app.route('/api/history/<node>/<int:limit>')
def get_history(node, limit=50):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT timestamp, cpu_percent, memory_percent, disk_percent, connections
        FROM system_metrics
        WHERE node_name = %s
        ORDER BY timestamp DESC
        LIMIT %s
    """, (node, limit))
    data = []
    for row in cur.fetchall():
        data.append({
            'timestamp': row[0].strftime('%Y-%m-%d %H:%M:%S'),
            'cpu': round(row[1], 1),
            'mem': round(row[2], 1),
            'disk': round(row[3], 1),
            'connections': row[4]
        })
    cur.close()
    conn.close()
    return jsonify(data)

@app.route('/api/report', methods=['POST'])
def report():
    """API برای دریافت دیتا از Agent ها"""
    data = request.json
    node_name = data.get('node_name')
    cpu = data.get('cpu')
    mem = data.get('mem')
    disk = data.get('disk')
    connections = data.get('connections')
    boot_time = data.get('boot_seconds')
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO system_metrics (node_name, cpu_percent, memory_percent, disk_percent, connections, boot_time)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (node_name, cpu, mem, disk, connections, boot_time))
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

