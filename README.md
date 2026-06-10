# 🖥️ Monitoring Master

سیستم مانیتورینگ جامع و سبک برای سرورها و سیستم‌های لینوکسی با قابلیت نمایش لحظه‌ای اطلاعات سخت‌افزاری، دما، مصرف GPU و ذخیره‌سازی تاریخچه در دیتابیس SQLite.

---

## ✨ امکانات

- نمایش لحظه‌ای:
  - میزان مصرف **CPU**
  - میزان مصرف **RAM**
  - میزان مصرف **Disk**
  - تعداد **Connections** فعال
  - دمای **CPU** و **GPU**
  - میزان مصرف و دمای **GPU** (با پشتیبانی از NVIDIA)

- ذخیره‌سازی خودکار تاریخچه در SQLite
- نمایش نمودار تاریخچه مصرف
- رابط کاربری وب واکنش‌گرا (Responsive)
- آماده برای اجرا با **Docker** و پشتیبانی از **GPU**
- راه‌اندازی خودکار بعد از ریستارت سرور

---

## 🛠️ تکنولوژی‌ها

- Python 3.12
- Flask (Web Framework)
- psutil (گرفتن اطلاعات سیستم)
- NVIDIA SMI (برای سیستم‌های دارای GPU)
- SQLite (پایگاه داده)
- Docker & Supervisor
- HTML/CSS/JavaScript

---

## 📁 ساختار پروژه


monitoring_master/
├── agent_local.py # جمع‌آوری اطلاعات سیستم و ارسال به API
├── web_master.py # سرور Flask و مدیریت API‌ها
├── templates/
│ └── master.html # داشبورد گرافیکی
├── requirements.txt # وابستگی‌های پایتون
├── Dockerfile # فایل ساخت ایمیج داکر
├── supervisord.conf # مدیریت همزمان Agent و Web Server
├── docker-compose.yml # راه‌اندازی با Docker Compose
└── monitoring_master.db # دیتابیس SQLite (پس از اجرا ساخته می‌شود)






---

## 🚀 نحوه اجرا

### ۱. اجرا با Docker (پیشنهادی)

```bash
# clone کردن پروژه
git clone https://github.com/netachit1/monitoring_master.git
cd monitoring_master

# ساخت ایمیج
docker build -t monitoring-master .

# اجرا با پشتیبانی GPU
docker run -d \
  --name monitoring \
  --gpus all \
  -p 5000:5000 \
  -v $(pwd)/monitoring_master.db:/app/monitoring_master.db \
  --restart unless-stopped \
  monitoring-master

پس از اجرا:
http://localhost:5000



