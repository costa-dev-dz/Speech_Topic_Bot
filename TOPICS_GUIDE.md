# 📚 دليل إضافة المواضيع — Speech Topic Bot

---

## 🚀 الطريقة 1: استيراد من ملف (CSV أو JSON)

### الخطوة 1 — توليد الملف بالذكاء الاصطناعي
انسخ البرومبت أدناه والصقه في أي نموذج AI (ChatGPT, Claude, Gemini, إلخ)
ثم احفظ الناتج كملف `topics.csv`

### الخطوة 2 — استيراد الملف إلى Supabase
```powershell
# تأكد أن ملف .env موجود ومعبّأ بالمفاتيح أولاً

# من CSV
python import_topics.py topics.csv

# من JSON
python import_topics.py topics.json
```

---

## 🤖 الطريقة 2: توليد تلقائي بـ Groq (أسبوعياً)
```powershell
python topic_generator.py
```

---

## 📋 البرومبت الاحترافي لتوليد قاعدة البيانات

انسخ هذا البرومبت كاملاً والصقه في أي نموذج AI:

```
أنت خبير في فن الخطابة والتحدث أمام الجمهور.

مهمتك: توليد قاعدة بيانات شاملة من مواضيع الخطابة الارتجالية.
المطلوب: 10 مواضيع لكل فئة، لكل لغة (عربي وإنجليزي).

الفئات المطلوبة:
- general (عام)
- tech (تقنية)
- finance (مالية)
- interview (مقابلات عمل)
- hot_takes (آراء جريئة)
- health (صحة)
- sports (رياضة)
- history (تاريخ)
- philosophy (فلسفة)
- culture (ثقافة)
- education (تعليم)
- relationship (علاقات)
- mindset (عقلية)

قواعد صارمة لكل موضوع:
1. جملة واحدة أو سؤال (بحد أقصى 15 كلمة)
2. قابل للنقاش — يمكن للناس الاختلاف فيه
3. مناسب للتحدث عنه لمدة دقيقة كاملة
4. حديث ويعكس اهتمامات 2024-2026
5. تجنب المواضيع المبتذلة والمكررة جداً
6. المواضيع العربية تكون بالعربية الفصحى المبسطة
7. المواضيع الإنجليزية تكون بإنجليزية واضحة
8. لا تكرر مواضيع موجودة مسبقاً

صيغة الإخراج المطلوبة (CSV فقط، بدون أي نص إضافي):
category,lang,topic
general,ar,موضوع عربي هنا
general,en,English topic here
tech,ar,موضوع تقني عربي
tech,en,English tech topic
education,ar,موضوع تعليمي عربي
education,en,English education topic
relationship,ar,موضوع عن العلاقات بالعربية
relationship,en,English relationship topic
mindset,ar,موضوع عن العقلية بالعربية
mindset,en,English mindset topic
...

ابدأ مباشرة بالـ CSV بدون أي مقدمة أو شرح.
```

---

## 📁 صيغة ملف CSV

```csv
category,lang,topic
general,ar,هل الإنسان بطبعه اجتماعي أم انعزالي؟
general,en,Is ambition a blessing or a curse?
tech,ar,هل سيصبح الذكاء الاصطناعي أذكى من البشر قبل 2030؟
tech,en,Should social media platforms be liable for user content?
education,ar,هل نظام التعليم الحالي يُعدّ الطلاب للحياة الحقيقية؟
education,en,Is a university degree still worth it in 2026?
relationship,ar,هل الصداقة الحقيقية ممكنة بين الجنسين؟
relationship,en,Can long-distance relationships truly work?
mindset,ar,هل الفشل ضروري للنجاح؟
mindset,en,Is discipline more important than talent?
```

---

## 📁 صيغة ملف JSON

```json
[
  {"category": "general", "lang": "ar", "topic": "هل الإنسان بطبعه اجتماعي؟"},
  {"category": "general", "lang": "en", "topic": "Is ambition a blessing or a curse?"},
  {"category": "education", "lang": "ar", "topic": "هل الشهادة الجامعية ضرورة في 2026؟"},
  {"category": "education", "lang": "en", "topic": "Should life skills be taught in schools?"}
]
```

---

## ✅ قائمة الفئات المتاحة

| الكود | العربية | الإنجليزية |
|-------|---------|------------|
| `general` | 💬 عام | 💬 General |
| `tech` | 💻 تقنية | 💻 Tech |
| `finance` | 💰 مالية | 💰 Finance |
| `interview` | 🎯 مقابلات عمل | 🎯 Interview Prep |
| `hot_takes` | 🌶️ آراء جريئة | 🌶️ Hot Takes |
| `health` | 🏥 صحة | 🏥 Health |
| `sports` | ⚽ رياضة | ⚽ Sports |
| `history` | 📜 تاريخ | 📜 History |
| `philosophy` | 🧐 فلسفة | 🧐 Philosophy |
| `culture` | 🎭 ثقافة | 🎭 Culture |
| `education` | 📚 تعليم | 📚 Education |
| `relationship` | ❤️ علاقات | ❤️ Relationships |
| `mindset` | 🧠 عقلية | 🧠 Mindset |

---

## ⚠️ تذكير مهم

- تأكد أن ملف `.env` موجود ومعبّأ قبل تشغيل أي أمر
- أسماء الفئات في CSV يجب أن تكون بالإنجليزية بالضبط كما في الجدول أعلاه
- قيم `lang` يجب أن تكون `ar` أو `en` فقط
