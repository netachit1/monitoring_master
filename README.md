# 🖥️ Monitoring Master

سیستم مانیتورینگ جامع و سبک برای سرورها و سیستم‌های لینوکسی با قابلیت نمایش لحظه‌ای اطلاعات سخت‌افزاری، دما، مصرف GPU و ذخیره‌سازی تاریخچه در دیتابیس SQLite.

---

## ✨ امکانات

- **نمایش لحظه‌ای**:
  - میزان مصرف **CPU**
  - میزان مصرف **RAM**
  - میزان مصرف **Disk**
  - تعداد **Connections** فعال
  - دمای **CPU** و **GPU**
  - میزان مصرف و دمای **GPU** (با پشتیبانی از NVIDIA)

- **ذخیره‌سازی خودکار** تاریخچه در SQLite
- **نمایش نمودار** تاریخچه مصرف
- **رابط کاربری وب واکنش‌گرا** (Responsive)
- **آماده برای اجرا با Docker** و پشتیبانی از GPU
- **راه‌اندازی خودکار** بعد از ریستارت سرور
- **APIهای RESTful** برای یکپارچه‌سازی با سایر سرویس‌ها

---

## 🛠️ تکنولوژی‌ها

| فناوری | کاربرد |
|--------|--------|
| Python 3.12 | زبان اصلی برنامه |
| Flask | Web Framework |
| psutil | گرفتن اطلاعات سیستم |
| NVIDIA SMI | برای سیستم‌های دارای GPU |
| SQLite | پایگاه داده |
| Docker & Supervisor | کانتینریزیشن و مدیریت فرآیندها |
| HTML/CSS/JavaScript | فرانت‌اند داشبورد |

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

## 🗄️ دیتابیس و مدیریت داده‌ها

### ساختار دیتابیس (SQLite)

پروژه از **SQLite** برای ذخیره‌سازی اطلاعات استفاده می‌کند. فایل دیتابیس (`monitoring_master.db`) به صورت خودکار در همان مسیر پروژه ساخته می‌شود.

**جدول metrics شامل فیلدهای زیر است:**

| فیلد | نوع | توضیح |
|------|------|-------|
| id | INTEGER | کلید اصلی |
| node_name | TEXT | نام سرور یا نود |
| timestamp | TEXT | زمان ذخیره داده |
| cpu | REAL | درصد مصرف CPU |
| mem | REAL | درصد مصرف RAM |
| disk | REAL | درصد مصرف دیسک |
| connections | INTEGER | تعداد اتصالات شبکه |
| temperature | REAL | دمای CPU (سانتی‌گراد) |
| gpu_usage | REAL | درصد مصرف GPU |
| gpu_mem | REAL | درصد مصرف حافظه GPU |
| gpu_temp | REAL | دمای GPU (سانتی‌گراد) |

### نحوه ذخیره و بازیابی داده

- **Agent** هر ۳۰ ثانیه یکبار اطلاعات سیستم را گرفته و از طریق `POST /api/report` به **Web Server** ارسال می‌کند.
- **Web Server** داده را دریافت کرده و در جدول `metrics` ذخیره می‌کند.
- **داشبورد** با فراخوانی `GET /api/latest` جدیدترین رکورد و با `GET /api/history/<node>/20` آخرین ۲۰ رکورد را دریافت می‌کند.

### ایندکس‌ها (برای سرعت بالا)

برای جلوگیری از کندی کوئری‌ها، ایندکس‌های زیر روی دیتابیس ایجاد شده است:

```sql
CREATE INDEX idx_node_name ON metrics(node_name);
CREATE INDEX idx_timestamp ON metrics(timestamp);
CREATE INDEX idx_node_timestamp ON metrics(node_name, timestamp);

این ایندکس‌ها باعث شده‌اند که زمان پاسخ‌دهی API از چند ثانیه به کمتر از ۲۰ میلی‌ثانیه کاهش یابد.

پشتیبان‌گیری از دیتابیس
برای تهیه نسخه پشتیبان:

cp monitoring_master.db monitoring_master.db.backup

🚀 نحوه اجرا
۱. اجرا با Docker (پیشنهادی)

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


۲. اجرا با Docker Compose
  docker-compose up -d

۳. اجرا بدون Docker (روی خود سیستم)
# نصب وابستگی‌ها
pip install -r requirements.txt

# اجرای Agent و Web Server (در دو ترمینال مجزا)
python agent_local.py
python web_master.py

🌐 دسترسی به داشبورد
پس از اجرا، در مرورگر آدرس زیر را باز کنید:

text
http://localhost:5000


🐳 دستورات مفید Docker
bash
# مشاهده لاگ‌ها
docker logs -f monitoring

# ریستارت سرویس
docker restart monitoring

# توقف سرویس
docker stop monitoring

# شروع مجدد
docker start monitoring

# ورود به container برای عیب‌یابی
docker exec -it monitoring /bin/bash

# مشاهده وضعیت container
docker ps
🧪 تست GPU (در صورت داشتن NVIDIA)
bash
# تست دسترسی به GPU در داکر
docker run --rm --gpus all monitoring-master nvidia-smi

# بررسی اطلاعات GPU
nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu --format=csv


🔧 عیب‌یابی
خطای database is locked
bash
# ورود به container
docker exec -it monitoring /bin/bash

# نصب sqlite3 (در صورت نیاز)
apt-get update && apt-get install -y sqlite3

# بازسازی ایندکس‌ها
sqlite3 /app/monitoring_master.db "CREATE INDEX IF NOT EXISTS idx_node_name ON metrics(node_name);"
sqlite3 /app/monitoring_master.db "CREATE INDEX IF NOT EXISTS idx_timestamp ON metrics(timestamp);"
sqlite3 /app/monitoring_master.db "VACUUM;"
خطای اتصال به GPU
اگر سیستم شما GPU NVIDIA ندارد، خطای مربوط به nvidia-smi را نادیده بگیرید. برنامه بدون GPU هم کار می‌کند.

پورت 5000 از قبل استفاده می‌شود
bash
# پیدا کردن فرآیندی که روی پورت 5000 کار می‌کند
sudo lsof -i :5000

# توقف فرآیند (با توجه به PID دریافتی)
sudo kill -9 <PID>
🧹 پاکسازی و ساخت مجدد
bash
# توقف و حذف container
docker stop monitoring
docker rm monitoring

# حذف image قبلی
docker rmi monitoring-master

# ساخت مجدد
docker build -t monitoring-master .

# اجرا
docker run -d --name monitoring --gpus all -p 5000:5000 --restart unless-stopped monitoring-master



🤝 مشارکت در توسعه
اگر می‌خواهید پروژه را بهبود ببخشید:

Fork کنید

یک branch جدید بسازید (git checkout -b feature/amazing-feature)

تغییرات خود را commit کنید (git commit -m 'Add some amazing feature')

Push کنید (git push origin feature/amazing-feature)

یک Pull Request ارسال کنید

📜 مجوز
این پروژه تحت مجوز MIT منتشر شده است. برای مشاهده جزئیات به فایل LICENSE مراجعه کنید.

👨‍💻 توسعه‌دهنده
itachi (netachit1) - GitHub

⭐ حمایت
اگر این پروژه برای شما مفید بود، لطفاً یک Star ⭐ به آن بدهید تا من هم برای ادامه توسعه انگیزه بگیرم! 😊

📞 ارتباط با من
GitHub Issues: برای گزارش باگ‌ها و درخواست ویژگی‌های جدید

Email: stimnmt1@gmail.com
Telegram: @Netachit


ساخته شده با ❤️ برای جامعه متن‌باز ایران
