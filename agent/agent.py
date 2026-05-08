import psutil
import requests
import time
import os
from datetime import datetime

SERVER_URL = os.environ.get('SERVER_URL', 'http://localhost:5000/api/report')
NODE_NAME = os.environ.get('NODE_NAME', 'unknown-node')
INTERVAL = int(os.environ.get('INTERVAL', 60))

def get_metrics():
    return {
        'node_name': NODE_NAME,
        'timestamp': datetime.now().isoformat(),
        'cpu': psutil.cpu_percent(interval=1),
        'mem': psutil.virtual_memory().percent,
        'disk': psutil.disk_usage('/').percent,
        'connections': len(psutil.net_connections()),
        'boot_seconds': psutil.boot_time()
    }

while True:
    try:
        metrics = get_metrics()
        response = requests.post(SERVER_URL, json=metrics, timeout=10)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Sent: CPU:{metrics['cpu']}% - Status: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(INTERVAL)
