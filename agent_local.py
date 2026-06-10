import psutil
import requests
import time
import subprocess  # اضافه شد
from datetime import datetime

SERVER_URL = "http://127.0.0.1:5000/api/report"
NODE_NAME = "itachi_main_sever"


def get_cpu_temperature():
    """گرفتن دمای CPU از سنسور coretemp"""
    try:
        temps = psutil.sensors_temperatures()

        if 'coretemp' in temps:
            for sensor in temps['coretemp']:
                if 'Package' in sensor.label:
                    return sensor.current
            return temps['coretemp'][0].current
        elif 'k10temp' in temps:
            return temps['k10temp'][0].current
        elif 'cpu_thermal' in temps:
            return temps['cpu_thermal'][0].current
        else:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                return int(f.read().strip()) / 1000.0
    except Exception as e:
        print(f"Error reading temperature: {e}")
        return None


def get_gpu_stats():
    """گرفتن آمار GPU با nvidia-smi"""
    try:
        output = subprocess.check_output(
            ['nvidia-smi', '--query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu',
             '--format=csv,noheader,nounits'],
            text=True
        ).strip()
        parts = output.split(', ')

        if len(parts) >= 4:
            gpu_usage = int(parts[0])
            mem_used = int(parts[1])
            mem_total = int(parts[2])
            gpu_temp = int(parts[3])
            mem_percent = (mem_used / mem_total) * 100 if mem_total > 0 else 0

            return {
                "gpu_usage": gpu_usage,
                "gpu_mem_percent": round(mem_percent, 1),
                "gpu_temp": gpu_temp
            }
        return None
    except Exception as e:
        print(f"GPU Error: {e}")
        return None


while True:
    try:
        # گرفتن دما و GPU
        cpu_temp = get_cpu_temperature()
        gpu_stats = get_gpu_stats()

        data = {
            "node_name": NODE_NAME,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cpu": psutil.cpu_percent(interval=1),
            "mem": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent,
            "connections": len(psutil.net_connections()),
            "temperature": cpu_temp,
            "gpu_usage": gpu_stats['gpu_usage'] if gpu_stats else None,
            "gpu_mem": gpu_stats['gpu_mem_percent'] if gpu_stats else None,
            "gpu_temp": gpu_stats['gpu_temp'] if gpu_stats else None
        }

        r = requests.post(SERVER_URL, json=data, timeout=5)

        # نمایش در خروجی
        temp_str = f"{cpu_temp:.1f}°C" if cpu_temp else "N/A"
        gpu_str = f"GPU:{gpu_stats['gpu_usage']}% Mem:{gpu_stats['gpu_mem_percent']}% Temp:{gpu_stats['gpu_temp']}°C" if gpu_stats else "GPU:N/A"
        print(f"[{data['timestamp'][11:16]}] CPU:{data['cpu']}% | TEMP:{temp_str} | {gpu_str} | Status:{r.status_code}")

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(30)