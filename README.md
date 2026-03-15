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

### 2. أنشئ ملف `.env`
انسخ `.env.example` وسمّه `.env` وأدخل مفاتيحك:
```env
BOT_TOKEN=توكن_البوت
WEBHOOK_URL=https://speech-topic-bot.onrender.com
GROQ_API_KEY=مفتاح_groq
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_KEY=مفتاح_supabase
```

### 3. ثبّت المتطلبات
```bash
python -m pip install -r requirements.txt
```

> المتطلبات تشمل: `python-telegram-bot`, `flask`, `APScheduler`, `python-dotenv`

### 4. شغّل البوت محلياً
```powershell
python bot.py
```

---

## ☁️ النشر على Render

1. ارفع الملفات على GitHub
2. أنشئ **Web Service** على [render.com](https://render.com)
3. اضبط الإعدادات:

| الحقل | القيمة |
|-------|--------|
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python app.py` |

4. أضف متغيرات البيئة:

| Key | Value |
|-----|-------|
| `BOT_TOKEN` | توكن البوت |
| `WEBHOOK_URL` | `https://اسم-مشروعك.onrender.com` |
| `GROQ_API_KEY` | مفتاح Groq |
| `SUPABASE_URL` | رابط Supabase |
| `SUPABASE_KEY` | مفتاح Supabase |

---

## 🔄 منع النوم مع UptimeRobot

أنشئ monitor على [uptimerobot.com](https://uptimerobot.com):
- **Monitor Type:** HTTP(s)
- **URL:** `https://اسم-مشروعك.onrender.com/health`
- **Interval:** Every 5 minutes

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
- 🏥 صحة / Health
- ⚽ رياضة / Sports
- 📜 تاريخ / History
- 🧐 فلسفة / Philosophy
- 🎭 ثقافة / Culture
- 📚 تعليم / Education
- ❤️ علاقات / Relationships
- 🧠 عقلية / Mindset

## 🧱 الأطر الخطابية

- ⭐ **STAR** — مثالي للمقابلات
- 📝 **PREP** — مثالي للإقناع
- ⏳ **PPF** — ماضي / حاضر / مستقبل
- 🧠 **MECE** — مثالي لحل المشكلات

---

## 🤖 إضافة مواضيع جديدة

راجع ملف `TOPICS_GUIDE.md` للتفاصيل الكاملة حول:
- توليد مواضيع بالذكاء الاصطناعي
- استيراد من CSV أو JSON
- البرومبت الاحترافي الجاهز

---

## 📋 Git Cheat Sheet

### الروتين اليومي (باستخدام الـ shortcut)
```powershell
gcp "وصف التعديل"   # يرفع كل شيء بأمر واحد
```

### أو يدوياً
```bash
git add .
git commit -m "وصف التعديل"
git push
```

### أوامر مفيدة
```bash
gs                      # git status
gl                      # آخر 5 commits
git pull                # جلب آخر التحديثات
git log --oneline       # تاريخ كامل
```

---

## ⚡ Git Shortcuts (shortcuts.ps1)

لتفعيل الاختصارات على أي جهاز جديد، شغّل هذا مرة واحدة:
```powershell
. .\shortcuts.ps1
```

أو لتفعيلها بشكل دائم على جهازك:
```powershell
notepad $PROFILE
```
والصق محتوى `shortcuts.ps1` فيه.

### الاختصارات المتاحة

| الأمر | يعادل |
|-------|-------|
| `gcp "رسالة"` | `git add . && git commit -m "رسالة" && git push` |
| `gs` | `git status` |
| `gl` | `git log --oneline -5` |
