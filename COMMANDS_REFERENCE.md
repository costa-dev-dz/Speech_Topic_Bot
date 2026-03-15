# 📖 مرجع الأوامر الكامل — Speech Topic Bot

---

## 1️⃣ Python & pip

```powershell
# تثبيت المتطلبات من ملف
python -m pip install -r requirements.txt

# تثبيت مكتبة واحدة
python -m pip install python-telegram-bot
python -m pip install flask
python -m pip install python-dotenv
python -m pip install apscheduler
python -m pip install google-genai
python -m pip install httpx==0.27.0

# تشغيل ملف Python
python bot.py
python app.py
python topic_generator.py

# استيراد مواضيع من ملف
python import_topics.py topics.csv
python import_topics.py topics.json

# التحقق من نسخة Python
python --version

# تشغيل سطر Python سريع
python -c "print('hello')"
```

---

## 2️⃣ متغيرات البيئة في PowerShell

```powershell
# تعيين متغير مؤقت (يختفي عند إغلاق PowerShell)
$env:BOT_TOKEN = "توكنك"
$env:WEBHOOK_URL = "https://speech-topic-bot.onrender.com"
$env:GROQ_API_KEY = "مفتاحك"
$env:SUPABASE_URL = "https://xxxx.supabase.co"
$env:SUPABASE_KEY = "مفتاحك"

# تعيين عدة متغيرات في سطر واحد
$env:GROQ_API_KEY = "..."; $env:SUPABASE_URL = "..."; $env:SUPABASE_KEY = "..."

# التحقق من قيمة متغير
$env:BOT_TOKEN

# التحقق من طول متغير (للتأكد من عدم وجود أحرف زيادة)
$env:BOT_TOKEN.Length
```

---

## 3️⃣ Git — الأساسيات

```powershell
# تهيئة مستودع جديد
git init

# ربط المستودع بـ GitHub
git remote add origin https://github.com/username/repo.git
git branch -M main
git push -u origin main

# الروتين اليومي
git add .
git commit -m "وصف التعديل"
git push

# أو بالـ shortcut
gcp "وصف التعديل"
```

---

## 4️⃣ Git — أوامر مفيدة

```powershell
# معرفة حالة الملفات
git status
# أو بالـ shortcut
gs

# عرض آخر 5 commits
git log --oneline -5
# أو بالـ shortcut
gl

# جلب آخر التحديثات من GitHub
git pull

# عرض تاريخ كامل
git log --oneline

# إضافة استثناء للمجلد الآمن
git config --global --add safe.directory 'Z:/Telegram bots/Speech_Topic_Bot'
```

---

## 5️⃣ Git — حل المشاكل

```powershell
# حل مشكلة رفض الـ push
git pull origin main --allow-unrelated-histories
git push

# إنشاء ملف profile.ps1 إذا لم يكن موجوداً
New-Item -Path $PROFILE -Force
notepad $PROFILE
```

---

## 6️⃣ PowerShell — الملف الشخصي (Aliases)

```powershell
# فتح ملف الإعدادات
notepad $PROFILE

# معرفة مسار الملف
echo $PROFILE

# تفعيل الملف في الجلسة الحالية
. $PROFILE

# تفعيل تشغيل السكريبتات (مرة واحدة فقط)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# تفعيل shortcuts من ملف المشروع
. .\shortcuts.ps1
```

---

## 7️⃣ محتوى shortcuts.ps1

```powershell
function gcp {
    param($msg)
    git add .
    git commit -m $msg
    git push
}
function gs { git status }
function gl { git log --oneline -5 }
```

---

## 8️⃣ التنقل بين المجلدات

```powershell
# الانتقال للمشروع (المسار بين علامتي اقتباس لأن فيه مسافات)
cd "Z:\Telegram bots\Speech_Topic_Bot"

# الرجوع للمجلد السابق
cd ..

# عرض محتوى المجلد الحالي
ls
# أو
dir
```

---

## 9️⃣ الاختبار المحلي

```powershell
# تشغيل البوت مباشرة (للاختبار المحلي)
python bot.py

# تشغيل الكامل مع Flask
python app.py

# توليد مواضيع جديدة يدوياً
python topic_generator.py

# اختبار نموذج AI سريع
python -c "from google import genai; c = genai.Client(api_key='KEY'); r = c.models.generate_content(model='gemini-2.0-flash-lite', contents='say hello'); print(r.text)"
```

---

## 🔟 Render — النشر

```
Build Command: pip install -r requirements.txt
Start Command: python app.py
```

**متغيرات البيئة على Render:**
```
BOT_TOKEN         = توكن البوت
WEBHOOK_URL       = https://speech-topic-bot.onrender.com
GROQ_API_KEY      = مفتاح Groq
SUPABASE_URL      = https://xxxx.supabase.co
SUPABASE_KEY      = مفتاح Supabase
```

---

## 1️⃣1️⃣ مشاكل شائعة وحلولها

```powershell
# مشكلة: pip غير معروف
python -m pip install ...

# مشكلة: المجلد ليس git repository
git config --global --add safe.directory 'المسار'

# مشكلة: scripts disabled
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# مشكلة: BOT_TOKEN اختفى بعد إغلاق PowerShell
# الحل: استخدم ملف .env بدلاً من المتغيرات المؤقتة
```

---

## 1️⃣2️⃣ ملفات المشروع ووظيفة كل منها

| الملف | الوظيفة |
|-------|---------|
| `bot.py` | منطق البوت والأوامر والأزرار |
| `app.py` | Flask + Webhook + Scheduler |
| `topic_generator.py` | توليد مواضيع أسبوعياً بـ Groq |
| `db_topics.py` | قراءة المواضيع من Supabase |
| `import_topics.py` | استيراد مواضيع من CSV/JSON |
| `requirements.txt` | المكتبات المطلوبة |
| `shortcuts.ps1` | اختصارات Git |
| `.env` | المفاتيح السرية (لا يُرفع على GitHub) |
| `.env.example` | قالب لملف .env |
| `.gitignore` | ملفات يتجاهلها Git |
| `TOPICS_GUIDE.md` | دليل إضافة المواضيع والبرومبت |
| `COMMANDS_REFERENCE.md` | هذا الملف |

---

## 1️⃣3️⃣ روابط مهمة

| الخدمة | الرابط |
|--------|--------|
| BotFather | https://t.me/BotFather |
| GitHub | https://github.com |
| Render | https://render.com |
| UptimeRobot | https://uptimerobot.com |
| Supabase | https://supabase.com |
| Groq Console | https://console.groq.com |
| Bitwarden | https://bitwarden.com |

