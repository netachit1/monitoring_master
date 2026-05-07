#!/usr/bin/env python3
import psutil
import json
import time
import os
import sys
from datetime import datetime

# برای اینکه لاگ‌ها حتماً نمایش داده بشن
sys.stdout.reconfigure(line_buffering=True)


def get_system_data():
    """گرفتن دیتای کامل سیستم"""
    net = psutil.net_io_counters()
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu": psutil.cpu_percent(interval=1),
        "mem": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "connections": len(psutil.net_connections()),
        "boot_seconds": psutil.boot_time(),
        "net": {
            "bytes_sent": net.bytes_sent,
            "bytes_recv": net.bytes_recv,
            "packets_sent": net.packets_sent,
            "packets_recv": net.packets_recv
        }
    }


def main():
    JSON_FILE = "/home/itachi/pyprojects/monitoring_data.json"
    MAX_RECORDS = 100
    INTERVAL = 300  # 5 دقیقه

    print(f"✅ مانیتورینگ شروع شد - ذخیره هر {INTERVAL // 60} دقیقه یکبار", flush=True)
    print(f"📁 فایل: {JSON_FILE}", flush=True)
    print(f"📊 حداکثر رکورد: {MAX_RECORDS}", flush=True)
    print("-" * 50, flush=True)

    while True:
        try:
            # خوندن دیتای قبلی
            if os.path.exists(JSON_FILE) and os.path.getsize(JSON_FILE) > 0:
                with open(JSON_FILE, 'r') as f:
                    try:
                        history = json.load(f)
                        if not isinstance(history, list):
                            history = []
                    except:
                        history = []
            else:
                history = []

            # گرفتن دیتای جدید
            new_data = get_system_data()
            history.append(new_data)

            # نگهداری فقط MAX_RECORDS آخر
            if len(history) > MAX_RECORDS:
                history = history[-MAX_RECORDS:]

            # ذخیره در فایل
            with open(JSON_FILE, 'w') as f:
                json.dump(history, f, indent=2)

            # نمایش وضعیت
            cpu = new_data['cpu']
            mem = new_data['mem']
            disk = new_data['disk']
            conn = new_data['connections']

            print(
                f"[{datetime.now().strftime('%H:%M:%S')}] CPU:{cpu}%  RAM:{mem}%  DISK:{disk}%  Conn:{conn}  Total:{len(history)}",
                flush=True)

            time.sleep(INTERVAL)

        except Exception as e:
            print(f"❌ خطا: {e}", flush=True)
            time.sleep(60)


if __name__ == "__main__":
    main()