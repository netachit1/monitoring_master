import psutil
import json
from datetime import datetime

def current_monitoring_data():
    net = psutil.net_io_counters()
    cpu = psutil.cpu_percent(interval=1, percpu=False)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    boot_seconds = psutil.boot_time()
    users = psutil.users()

    my_date = {
        "net": net,
        "cpu": cpu,
        "mem": mem,
        "disk": disk,
        "boot_seconds": boot_seconds,
        "users": users
    }

    return my_date
my_data = current_monitoring_data()

print(my_data)


try:
    with open("monitoring_data.json", "a") as f:
        json.dump(my_data, f, indent=4)
        f.write("\n")

except FileNotFoundError:
    with open("monitoring_data.json", "w") as f:
        json.dump(my_data, f, indent=4)
        f.write("\n,\n")

