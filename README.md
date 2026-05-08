# 📊 مانیتورینگ سرور (Server Monitoring)

سیستم مانیتورینگ چند سروره با Flask و SQLite

## 🚀 شروع سریع

```bash
# نصب وابستگی‌ها
pip install flask requests psutil

# اجرای سرور مرکزی
python web_master.py

# اجرای Agent (روی هر سروری که میخوای مانیتور کنی)
python agent_local.py
