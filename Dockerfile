# 1. از یک نسخه پایدار و سبک پایتون به عنوان پایه استفاده کن
FROM python:3.11-slim-bullseye

# 2. متغیرهای محیطی برای عملکرد بهتر پایتون در داکر
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. یک پوشه کاری به نام /app داخل کانتینر بساز
WORKDIR /app

# 4. فایل نیازمندی‌ها را کپی و پکیج‌ها را نصب کن
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 5. بقیه کدهای پروژه را به پوشه /app کپی کن
COPY . /app/

# 6. دستور نهایی برای اجرای اپلیکیشن
# (مطمئن شوید stor.wsgi با نام پروژه شما مطابقت دارد)
CMD ["gunicorn", "stor.wsgi"]