import psutil
import requests
import time
from datetime import datetime

SERVER_URL = "http://localhost:5000/api/report"
NODE_NAME = "itachi_main_sever"

while True:
    try:
        data = {
            "node_name": NODE_NAME,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cpu": psutil.cpu_percent(interval=1),
            "mem": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent,
            "connections": len(psutil.net_connections())
        }
        r = requests.post(SERVER_URL, json=data, timeout=5)
        print(f"[{data['timestamp'][11:16]}] CPU:{data['cpu']}% Status:{r.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(30)
