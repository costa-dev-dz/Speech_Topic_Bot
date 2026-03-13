# 🎤 بوت مواضيع الخطابة الارتجالية

بوت تيليجرام مستوحى من speechtopicgen.com
يدعم العربية والإنجليزية | Supports Arabic & English

---

## 🚀 خطوات التشغيل

### 1. أنشئ بوت تيليجرام جديد
1. افتح [@BotFather](https://t.me/BotFather) على تيليجرام
2. أرسل `/newbot`
3. اختر اسمًا ومعرفًا للبوت
4. انسخ **التوكن** الذي ستحصل عليه

### 2. ضع التوكن في الكود
افتح `bot.py` وعدّل السطر:
```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
```
استبدل `YOUR_BOT_TOKEN_HERE` بتوكنك الفعلي.

### 3. ثبّت المتطلبات
```bash
pip install -r requirements.txt
```

### 4. شغّل البوت
```bash
python bot.py
```

---

## 📋 الأوامر المتاحة

| الأمر | الوظيفة |
|-------|---------|
| `/start` | القائمة الرئيسية |
| `/topic` | موضوع عشوائي فوري |
| `/framework` | اختر إطارًا خطابيًا |
| `/help` | عرض المساعدة |

---

## 🗂️ الفئات

- 💬 عام / General
- 💻 تقنية / Tech
- 💰 مالية / Finance
- 🎯 مقابلات عمل / Interview Prep
- 🌶️ آراء جريئة / Hot Takes

## 🧱 الأطر الخطابية

- ⭐ **STAR** — مثالي للمقابلات
- 📝 **PREP** — مثالي للإقناع
- ⏳ **PPF** — ماضي / حاضر / مستقبل
- 🧠 **MECE** — مثالي لحل المشكلات

---

## ☁️ الاستضافة (اختياري)

لتشغيل البوت 24/7 بدون إيقاف:

**Railway.app (مجاني)**
```bash
# 1. ارفع الملفات على GitHub
# 2. اربط المستودع بـ Railway
# 3. أضف متغير بيئة: BOT_TOKEN=توكنك
```

**VPS (Ubuntu)**
```bash
nohup python bot.py &
```

---

## 🔧 إضافة مواضيع جديدة

في `bot.py`، ابحث عن قاموس `TOPICS` وأضف موضوعك:
```python
"general": {
    "ar": [
        "موضوعك الجديد هنا...",
        # ...
    ]
}
```

# 🎤 Speech Topic Bot - بوت مواضيع الخطابة

## 📋 أوامر Git التي تعلمتها (Git Cheat Sheet)

### تهيئة المشروع
```bash
git init                    # إنشاء مستودع محلي جديد
git add .                   # إضافة جميع الملفات للمنطقة المؤقتة
git commit -m "الرسالة"     # حفظ التغييرات مع وصف
```

### ربط المستودع المحلي بالبعيد (GitHub)
```bash
git remote add origin https://github.com/costa-dev-dz/Speech_Topic_Bot.git
git branch -M main          # تغيير اسم الفرع إلى main
git push -u origin main     # رفع الكود لأول مرة
```

### بعد تعديل الكود (الروتين اليومي)
```bash
git add .                   # أو git add bot.py إذا أردت ملفاً واحداً
git commit -m "وصف التعديل"
git push                    # رفع التغييرات إلى GitHub
```

### أوامر مفيدة أخرى
```bash
git status                  # معرفة حالة الملفات
git log --oneline           # عرض تاريخ commits باختصار
git pull                    # جلب آخر التحديثات من GitHub
```