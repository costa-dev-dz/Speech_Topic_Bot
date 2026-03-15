"""
🎤 Speech Topic Bot - بوت مواضيع الخطابة
Supports Arabic & English | يدعم العربية والإنجليزية
v2.0 - إضافة فئات جديدة + مؤقت + فلتر الصعوبة
"""

from __future__ import annotations
import logging
import random

import os
from dotenv import load_dotenv
load_dotenv()

import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

# ─── Configuration ─────────────────────────────────────────────────────────────
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ لم يتم تعيين BOT_TOKEN في متغيرات البيئة!")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ─── User Storage ──────────────────────────────────────────────────────────────
user_languages: dict[int, str] = {}
user_difficulty: dict[int, str] = {}  # easy / medium / hard / any

def get_lang(user_id: int) -> str:
    return user_languages.get(user_id, "ar")

def get_difficulty(user_id: int) -> str:
    return user_difficulty.get(user_id, "any")

# ─── Content Data ──────────────────────────────────────────────────────────────
TOPICS = {
    "general": {
        "ar": [
            "هل وسائل التواصل الاجتماعي تؤثر سلبًا على العلاقات الإنسانية؟",
            "ما هو أهم اختراع في القرن الحادي والعشرين؟",
            "هل الذكاء الاصطناعي يشكّل تهديدًا أم فرصة للبشرية؟",
            "تحدث عن شخص أثّر في حياتك بشكل كبير.",
            "هل السعادة تكمن في المال أم في التجارب؟",
            "ما هو أهم شيء تعلمته من فشلك؟",
            "هل التعليم التقليدي لا يزال مناسبًا لعصرنا؟",
            "تحدث عن هواية تريد تعلمها ولم تبدأ بعد.",
            "ما الذي يجعل مدينة مثالية للسكن؟",
            "هل العمل عن بُعد مستقبل العمل؟",
        ],
        "en": [
            "Is social media doing more harm than good?",
            "What's the most important invention of the 21st century?",
            "Is AI a threat or an opportunity for humanity?",
            "Talk about a person who greatly influenced your life.",
            "Does happiness lie in money or experiences?",
            "What's the most important thing you've learned from failure?",
            "Is traditional education still relevant today?",
            "Talk about a hobby you want to learn but haven't started.",
            "What makes a city ideal to live in?",
            "Is remote work the future of employment?",
        ],
    },
    "tech": {
        "ar": [
            "هل يجب تنظيم الذكاء الاصطناعي حكوميًا؟",
            "ما هو تأثير الميتافيرس على حياتنا اليومية؟",
            "هل الخصوصية الرقمية أصبحت وهمًا في عصر التكنولوجيا؟",
            "تحدث عن مستقبل العملات الرقمية.",
            "هل التكنولوجيا تجعلنا أكثر عزلة أم تواصلًا؟",
            "ما هي أخطر التهديدات الأمنية الإلكترونية اليوم؟",
            "هل يمكن للروبوتات أن تحل محل البشر في سوق العمل؟",
            "تحدث عن التطبيق الذي غيّر حياتك اليومية.",
        ],
        "en": [
            "Should governments regulate AI?",
            "What impact will the Metaverse have on daily life?",
            "Has digital privacy become an illusion?",
            "Talk about the future of cryptocurrency.",
            "Does technology make us more isolated or connected?",
            "What are the most dangerous cybersecurity threats today?",
            "Can robots replace humans in the job market?",
            "Talk about the app that changed your daily life.",
        ],
    },
    "finance": {
        "ar": [
            "هل الاستثمار في الأسهم أفضل من العقارات؟",
            "كيف يمكن لشخص عادي تحقيق الاستقلال المالي؟",
            "هل التضخم يؤثر على الطبقة المتوسطة أكثر من الأغنياء؟",
            "تحدث عن أهمية بناء صندوق طوارئ.",
            "هل يجب تعليم مبادئ المال في المدارس؟",
            "ما هو الفرق بين الثروة الحقيقية والمظهر الكاذب للثروة؟",
        ],
        "en": [
            "Is investing in stocks better than real estate?",
            "How can an average person achieve financial independence?",
            "Does inflation affect the middle class more than the wealthy?",
            "Talk about the importance of building an emergency fund.",
            "Should financial literacy be taught in schools?",
            "What's the difference between true wealth and the appearance of wealth?",
        ],
    },
    "interview": {
        "ar": [
            "أخبرني عن نفسك.",
            "ما هو أكبر تحدٍّ مررت به في العمل؟",
            "أين ترى نفسك بعد خمس سنوات؟",
            "تحدث عن موقف كنت مخطئًا فيه وكيف تعاملت معه.",
            "ما هي نقاط قوتك وضعفك؟",
            "كيف تتعامل مع ضغط العمل؟",
            "أخبرني عن إنجاز تفخر به.",
            "لماذا تريد العمل في هذه الشركة؟",
        ],
        "en": [
            "Tell me about yourself.",
            "What's the biggest challenge you've faced at work?",
            "Where do you see yourself in five years?",
            "Talk about a situation where you were wrong and how you handled it.",
            "What are your strengths and weaknesses?",
            "How do you handle work pressure?",
            "Tell me about an achievement you're proud of.",
            "Why do you want to work at this company?",
        ],
    },
    "hot_takes": {
        "ar": [
            "الجامعة مضيعة للوقت لمعظم الناس.",
            "الكسل هو أصل الابتكار.",
            "التواضع المفرط هو نوع من الأنانية.",
            "العمل الجماعي يُبطئ الإنجاز في معظم الأحيان.",
            "الصداقة الحقيقية أندر من الحب الحقيقي.",
            "التخطيط المفرط يقتل الإبداع.",
        ],
        "en": [
            "College is a waste of time for most people.",
            "Laziness is the root of innovation.",
            "Excessive humility is a form of selfishness.",
            "Teamwork slows down achievement most of the time.",
            "True friendship is rarer than true love.",
            "Over-planning kills creativity.",
        ],
    },
    # ─── فئات جديدة ───────────────────────────────────────────────────────────
    "health": {
        "ar": [
            "هل النوم الكافي أهم من ممارسة الرياضة؟",
            "كيف تؤثر الصحة النفسية على الإنتاجية اليومية؟",
            "هل الأنظمة الغذائية الشائعة فعّالة حقاً؟",
            "تحدث عن عادة صحية غيّرت حياتك.",
            "هل يجب أن يكون الوصول للرعاية الصحية حقاً مجانياً للجميع؟",
            "ما هو تأثير الهاتف على صحتنا الجسدية والنفسية؟",
            "هل التأمل والاسترخاء ضرورة أم رفاهية؟",
            "كيف نحافظ على صحتنا في عالم مليء بالضغوط؟",
        ],
        "en": [
            "Is getting enough sleep more important than exercising?",
            "How does mental health affect daily productivity?",
            "Are popular diet trends actually effective?",
            "Talk about a healthy habit that changed your life.",
            "Should healthcare be a free right for everyone?",
            "What is the impact of smartphones on our physical and mental health?",
            "Is meditation a necessity or a luxury?",
            "How do we stay healthy in a world full of stress?",
        ],
    },
    "sports": {
        "ar": [
            "هل الرياضة تبني الشخصية أم تعكسها فقط؟",
            "ما هو الرياضي الذي ألهمك وما الذي تعلمته منه؟",
            "هل رواتب لاعبي كرة القدم مبررة؟",
            "تحدث عن أصعب تحدٍّ رياضي واجهته.",
            "هل الرياضات الإلكترونية رياضة حقيقية؟",
            "ما هو دور الرياضة في تحقيق السلام بين الشعوب؟",
            "هل المنافسة في الرياضة تعلّم الأطفال قيماً جيدة؟",
        ],
        "en": [
            "Does sports build character or just reveal it?",
            "Which athlete inspired you and what did you learn from them?",
            "Are professional footballers' salaries justified?",
            "Talk about the toughest sports challenge you've faced.",
            "Are esports a real sport?",
            "What role does sports play in achieving peace between nations?",
            "Does competition in sports teach children good values?",
        ],
    },
    "history": {
        "ar": [
            "ما هو الحدث التاريخي الذي تتمنى لو حدث بشكل مختلف؟",
            "ماذا يمكننا أن نتعلم من سقوط الحضارات القديمة؟",
            "هل التاريخ يعيد نفسه فعلاً؟",
            "تحدث عن شخصية تاريخية تلهمك ولماذا.",
            "ما هو اختراع في التاريخ غيّر مسار البشرية؟",
            "هل يجب تدريس التاريخ المؤلم بصدق في المدارس؟",
            "كيف شكّلت الحروب العالم الذي نعيش فيه اليوم؟",
        ],
        "en": [
            "What historical event do you wish had gone differently?",
            "What can we learn from the fall of ancient civilizations?",
            "Does history truly repeat itself?",
            "Talk about a historical figure who inspires you and why.",
            "What invention in history most changed the course of humanity?",
            "Should painful history be taught honestly in schools?",
            "How did wars shape the world we live in today?",
        ],
    },
    "philosophy": {
        "ar": [
            "هل الإنسان طيّب بطبعه أم شرير؟",
            "ما معنى حياة ناجحة بالنسبة لك؟",
            "هل الحرية الكاملة ممكنة؟",
            "تحدث عن قيمة تؤمن بها وكيف تطبّقها في حياتك.",
            "هل الأخلاق مطلقة أم نسبية؟",
            "ما الذي يجعل الإنسان سعيداً حقاً؟",
            "هل التقدم التكنولوجي يجعلنا أكثر إنسانية أم أقل؟",
        ],
        "en": [
            "Is human nature inherently good or evil?",
            "What does a successful life mean to you?",
            "Is complete freedom possible?",
            "Talk about a value you believe in and how you apply it.",
            "Are morals absolute or relative?",
            "What truly makes a person happy?",
            "Does technological progress make us more or less human?",
        ],
    },
    "education": {
        "ar": [
            "هل نظام التعليم الحالي يُعدّ الطلاب للحياة الحقيقية؟",
            "هل يجب إلغاء الامتحانات النهائية؟",
            "ما الفرق بين التعليم والتثقيف الذاتي؟",
            "هل الشهادة الجامعية ضرورة في عصر الإنترنت؟",
            "تحدث عن مادة دراسية غيّرت طريقة تفكيرك.",
            "هل الذكاء العاطفي أهم من الذكاء الأكاديمي؟",
            "هل يجب تعليم مهارات الحياة في المدارس؟",
        ],
        "en": [
            "Is the current education system preparing students for real life?",
            "Should final exams be abolished?",
            "What's the difference between education and self-learning?",
            "Is a university degree necessary in the age of the internet?",
            "Talk about a subject that changed the way you think.",
            "Is emotional intelligence more important than academic intelligence?",
            "Should life skills be taught in schools?",
        ],
    },
    "relationship": {
        "ar": [
            "هل الصداقة الحقيقية ممكنة بين الجنسين؟",
            "ما الذي يجعل العلاقة ناجحة على المدى الطويل؟",
            "هل وسائل التواصل الاجتماعي أضرّت بالعلاقات الإنسانية؟",
            "تحدث عن شخص علّمك درسًا مهمًا في الحياة.",
            "هل من الضروري أن تتشابه اهتمامات الشريكين؟",
            "كيف تتعامل مع الخلافات في العلاقات؟",
            "هل العلاقات عن بُعد قابلة للنجاح؟",
        ],
        "en": [
            "Is true friendship between genders possible?",
            "What makes a relationship successful long-term?",
            "Has social media damaged human relationships?",
            "Talk about someone who taught you an important life lesson.",
            "Do partners need to share the same interests?",
            "How do you handle conflicts in relationships?",
            "Can long-distance relationships truly work?",
        ],
    },
    "mindset": {
        "ar": [
            "هل الإنسان يمكنه تغيير شخصيته بإرادته؟",
            "ما الفرق بين العقلية الثابتة والعقلية النامية؟",
            "هل التفاؤل المفرط خطير؟",
            "تحدث عن عادة غيّرت حياتك للأفضل.",
            "هل الفشل ضروري للنجاح؟",
            "كيف تتعامل مع الخوف من المجهول؟",
            "هل الانضباط أهم من الموهبة؟",
        ],
        "en": [
            "Can a person truly change their personality by willpower?",
            "What's the difference between a fixed and growth mindset?",
            "Is excessive optimism dangerous?",
            "Talk about a habit that changed your life for the better.",
            "Is failure necessary for success?",
            "How do you deal with fear of the unknown?",
            "Is discipline more important than talent?",
        ],
    },
}
    "culture": {
        "ar": [
            "كيف تؤثر ثقافتك على طريقة تفكيرك؟",
            "هل العولمة تُثري الثقافات أم تمحوها؟",
            "تحدث عن عادة من ثقافتك تفخر بها.",
            "ما هو الكتاب أو الفيلم الذي غيّر نظرتك للحياة؟",
            "هل اللغة تشكّل طريقة تفكيرنا؟",
            "كيف نحافظ على الموروث الثقافي في عصر التكنولوجيا؟",
            "هل السياحة تقرّب الشعوب من بعضها؟",
        ],
        "en": [
            "How does your culture influence the way you think?",
            "Does globalization enrich cultures or erase them?",
            "Talk about a tradition from your culture you're proud of.",
            "What book or film changed your outlook on life?",
            "Does language shape the way we think?",
            "How do we preserve cultural heritage in the age of technology?",
            "Does tourism bring people closer together?",
        ],
    },
}

FRAMEWORKS = {
    "STAR": {
        "ar": {
            "title": "⭐ إطار STAR",
            "desc": (
                "*S* — الموقف: صِف السياق والخلفية\n"
                "*T* — المهمة: وضّح مسؤوليتك\n"
                "*A* — الإجراء: اشرح ما فعلته بالضبط\n"
                "*R* — النتيجة: شارك ما حققته\n\n"
                "💡 _مثالي لأسئلة مقابلات العمل_"
            ),
        },
        "en": {
            "title": "⭐ STAR Framework",
            "desc": (
                "*S* — Situation: Set the scene & context\n"
                "*T* — Task: Describe your responsibility\n"
                "*A* — Action: Explain exactly what you did\n"
                "*R* — Result: Share what you achieved\n\n"
                "💡 _Ideal for job interview questions_"
            ),
        },
    },
    "PREP": {
        "ar": {
            "title": "📝 إطار PREP",
            "desc": (
                "*P* — النقطة: اذكر رأيك الرئيسي\n"
                "*R* — السبب: وضّح لماذا تعتقد ذلك\n"
                "*E* — المثال: أعطِ مثالًا ملموسًا\n"
                "*P* — النقطة: أعِد تأكيد رأيك\n\n"
                "💡 _مثالي للمواضيع الرأي والإقناع_"
            ),
        },
        "en": {
            "title": "📝 PREP Framework",
            "desc": (
                "*P* — Point: State your main argument\n"
                "*R* — Reason: Explain why you believe it\n"
                "*E* — Example: Give a concrete example\n"
                "*P* — Point: Restate your argument\n\n"
                "💡 _Ideal for opinion & persuasion topics_"
            ),
        },
    },
    "PPF": {
        "ar": {
            "title": "⏳ إطار PPF",
            "desc": (
                "*P* — الماضي: من أين بدأنا؟\n"
                "*P* — الحاضر: أين نحن الآن؟\n"
                "*F* — المستقبل: إلى أين نتجه؟\n\n"
                "💡 _مثالي للمواضيع التحليلية والاتجاهات_"
            ),
        },
        "en": {
            "title": "⏳ PPF Framework",
            "desc": (
                "*P* — Past: Where did we come from?\n"
                "*P* — Present: Where are we now?\n"
                "*F* — Future: Where are we headed?\n\n"
                "💡 _Ideal for analytical & trend topics_"
            ),
        },
    },
    "MECE": {
        "ar": {
            "title": "🧠 إطار MECE",
            "desc": (
                "*M* — متبادل الاستبعاد: لا تداخل بين النقاط\n"
                "*E* — شامل مجتمعًا: لا يُترك شيء خارج\n\n"
                "الطريقة:\n"
                "1️⃣ قسّم المشكلة إلى فئات مستقلة\n"
                "2️⃣ تأكد أن الفئات تغطي كل شيء\n"
                "3️⃣ حلّل كل فئة بعمق\n\n"
                "💡 _مثالي لأسئلة الاستشارات وحل المشكلات_"
            ),
        },
        "en": {
            "title": "🧠 MECE Framework",
            "desc": (
                "*M*utually *E*xclusive: No overlapping buckets\n"
                "*C*ollectively *E*xhaustive: Nothing left out\n\n"
                "Method:\n"
                "1️⃣ Break the problem into distinct categories\n"
                "2️⃣ Ensure categories cover everything\n"
                "3️⃣ Drill into each category deeply\n\n"
                "💡 _Ideal for consulting & problem-solving questions_"
            ),
        },
    },
}

CATEGORIES_META = {
    "ar": {
        "general":    "💬 عام",
        "tech":       "💻 تقنية",
        "finance":    "💰 مالية",
        "interview":  "🎯 مقابلات عمل",
        "hot_takes":  "🌶️ آراء جريئة",
        "education": "📚 تعليم",
        "relationship": "❤️ علاقات",
        "mindset": "🧠 عقلية",
        "health":     "🏥 صحة",
        "sports":     "⚽ رياضة",
        "history":    "📜 تاريخ",
        "philosophy": "🧐 فلسفة",
        "culture":    "🎭 ثقافة",
    },
    "en": {
        "general":    "💬 General",
        "tech":       "💻 Tech",
        "finance":    "💰 Finance",
        "interview":  "🎯 Interview Prep",
        "hot_takes":  "🌶️ Hot Takes",
        "education": "📚 Education",
        "relationship": "❤️ Relationships",
        "mindset": "🧠 Mindset",
        "health":     "🏥 Health",
        "sports":     "⚽ Sports",
        "history":    "📜 History",
        "philosophy": "🧐 Philosophy",
        "culture":    "🎭 Culture",
    },
}

DIFFICULTY_LABELS = {
    "ar": {"easy": "🟢 سهل", "medium": "🟡 متوسط", "hard": "🔴 صعب"},
    "en": {"easy": "🟢 Easy", "medium": "🟡 Medium", "hard": "🔴 Hard"},
}

# ─── Helpers ───────────────────────────────────────────────────────────────────
def difficulty_level(topic: str) -> str:
    words = len(topic.split())
    if words < 8:
        return "easy"
    elif words < 14:
        return "medium"
    else:
        return "hard"

def get_random_topic(category: str, lang: str, difficulty: str = "any") -> str:
    # أولاً: حاول جلب موضوع من Supabase
    try:
        from db_topics import get_topic_from_db
        db_topic = get_topic_from_db(category, lang)
        if db_topic:
            return db_topic
    except Exception:
        pass

    # احتياطاً: استخدم القائمة الثابتة
    pool = TOPICS.get(category, TOPICS["general"]).get(lang, [])
    if difficulty != "any":
        filtered = [t for t in pool if difficulty_level(t) == difficulty]
        pool = filtered if filtered else pool
    return random.choice(pool) if pool else "—"

def topic_message(topic: str, category: str, lang: str) -> str:
    cat_label = CATEGORIES_META[lang].get(category, "")
    diff_key = difficulty_level(topic)
    diff_label = DIFFICULTY_LABELS[lang][diff_key]
    if lang == "ar":
        return (
            f"🎤 *موضوعك للخطابة*\n\n"
            f"_{topic}_\n\n"
            f"📂 الفئة: {cat_label}  |  {diff_label}\n\n"
            f"⏱ اضغط *ابدأ المؤقت* وتحدث لمدة دقيقة!"
        )
    else:
        return (
            f"🎤 *Your Speech Topic*\n\n"
            f"_{topic}_\n\n"
            f"📂 Category: {cat_label}  |  {diff_label}\n\n"
            f"⏱ Press *Start Timer* and speak for one minute!"
        )

# ─── Keyboards ─────────────────────────────────────────────────────────────────
def main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    diff = user_difficulty.get(0, "any")
    if lang == "ar":
        buttons = [
            [InlineKeyboardButton("🎲 موضوع عشوائي", callback_data="topic_random")],
            [InlineKeyboardButton("📂 اختر الفئة", callback_data="menu_category"),
             InlineKeyboardButton("🧱 الأطر الخطابية", callback_data="menu_framework")],
            [InlineKeyboardButton("🎯 مستوى الصعوبة", callback_data="menu_difficulty")],
            [InlineKeyboardButton("🌐 English", callback_data="lang_en")],
        ]
    else:
        buttons = [
            [InlineKeyboardButton("🎲 Random Topic", callback_data="topic_random")],
            [InlineKeyboardButton("📂 Pick Category", callback_data="menu_category"),
             InlineKeyboardButton("🧱 Frameworks", callback_data="menu_framework")],
            [InlineKeyboardButton("🎯 Difficulty Level", callback_data="menu_difficulty")],
            [InlineKeyboardButton("🌐 العربية", callback_data="lang_ar")],
        ]
    return InlineKeyboardMarkup(buttons)

def category_keyboard(lang: str) -> InlineKeyboardMarkup:
    cats = CATEGORIES_META[lang]
    items = list(cats.items())
    # صفّين في كل صف
    buttons = []
    for i in range(0, len(items), 2):
        row = [InlineKeyboardButton(items[i][1], callback_data=f"topic_cat_{items[i][0]}")]
        if i + 1 < len(items):
            row.append(InlineKeyboardButton(items[i+1][1], callback_data=f"topic_cat_{items[i+1][0]}"))
        buttons.append(row)
    back_label = "🔙 رجوع" if lang == "ar" else "🔙 Back"
    buttons.append([InlineKeyboardButton(back_label, callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)

def difficulty_keyboard(lang: str, current: str) -> InlineKeyboardMarkup:
    def mark(key):
        return "✅ " if current == key else ""
    if lang == "ar":
        buttons = [
            [InlineKeyboardButton(f"{mark('any')}🎲 عشوائي", callback_data="diff_any"),
             InlineKeyboardButton(f"{mark('easy')}🟢 سهل", callback_data="diff_easy")],
            [InlineKeyboardButton(f"{mark('medium')}🟡 متوسط", callback_data="diff_medium"),
             InlineKeyboardButton(f"{mark('hard')}🔴 صعب", callback_data="diff_hard")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="menu_main")],
        ]
    else:
        buttons = [
            [InlineKeyboardButton(f"{mark('any')}🎲 Any", callback_data="diff_any"),
             InlineKeyboardButton(f"{mark('easy')}🟢 Easy", callback_data="diff_easy")],
            [InlineKeyboardButton(f"{mark('medium')}🟡 Medium", callback_data="diff_medium"),
             InlineKeyboardButton(f"{mark('hard')}🔴 Hard", callback_data="diff_hard")],
            [InlineKeyboardButton("🔙 Back", callback_data="menu_main")],
        ]
    return InlineKeyboardMarkup(buttons)

def framework_keyboard(lang: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("⭐ STAR", callback_data="fw_STAR"),
         InlineKeyboardButton("📝 PREP", callback_data="fw_PREP")],
        [InlineKeyboardButton("⏳ PPF",  callback_data="fw_PPF"),
         InlineKeyboardButton("🧠 MECE", callback_data="fw_MECE")],
    ]
    back_label = "🔙 رجوع" if lang == "ar" else "🔙 Back"
    buttons.append([InlineKeyboardButton(back_label, callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)

def after_topic_keyboard(lang: str, category: str) -> InlineKeyboardMarkup:
    if lang == "ar":
        buttons = [
            [InlineKeyboardButton("⏱ ابدأ المؤقت 60 ث", callback_data=f"timer_{category}")],
            [InlineKeyboardButton("🔄 موضوع جديد", callback_data=f"topic_cat_{category}"),
             InlineKeyboardButton("🧱 إطار خطابي", callback_data="menu_framework")],
            [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="menu_main")],
        ]
    else:
        buttons = [
            [InlineKeyboardButton("⏱ Start 60s Timer", callback_data=f"timer_{category}")],
            [InlineKeyboardButton("🔄 New Topic", callback_data=f"topic_cat_{category}"),
             InlineKeyboardButton("🧱 Framework", callback_data="menu_framework")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="menu_main")],
        ]
    return InlineKeyboardMarkup(buttons)

# ─── Timer ─────────────────────────────────────────────────────────────────────
async def run_timer(context, chat_id: int, lang: str):
    """مؤقت 60 ثانية يرسل تنبيهات"""
    checkpoints = {
        45: ("⏱ 45 ثانية..." if lang == "ar" else "⏱ 45 seconds..."),
        30: ("⏱ نصف الوقت — 30 ثانية!" if lang == "ar" else "⏱ Halfway — 30 seconds!"),
        15: ("⚡ 15 ثانية فقط!" if lang == "ar" else "⚡ Only 15 seconds left!"),
    }
    await asyncio.sleep(15)
    await context.bot.send_message(chat_id=chat_id, text=checkpoints[45])
    await asyncio.sleep(15)
    await context.bot.send_message(chat_id=chat_id, text=checkpoints[30])
    await asyncio.sleep(15)
    await context.bot.send_message(chat_id=chat_id, text=checkpoints[15])
    await asyncio.sleep(15)
    done_msg = "⏰ *انتهى الوقت!* أحسنت 💪\n\nهل تريد موضوعاً جديداً؟" if lang == "ar" else "⏰ *Time's up!* Well done 💪\n\nWant a new topic?"
    await context.bot.send_message(chat_id=chat_id, text=done_msg, parse_mode="Markdown")

# ─── Handlers ──────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    name = update.effective_user.first_name or ("صديقي" if lang == "ar" else "there")
    if lang == "ar":
        text = (
            f"👋 أهلًا *{name}*!\n\n"
            f"🎤 أنا بوت *مواضيع الخطابة الارتجالية*\n\n"
            f"سأعطيك موضوعًا عشوائيًا، اضغط المؤقت، وابدأ الحديث!\n"
            f"ممارسة يومية = خطيب بارع 💪\n\n"
            f"اختر من القائمة:"
        )
    else:
        text = (
            f"👋 Hey *{name}*!\n\n"
            f"🎤 I'm your *Impromptu Speaking Bot*\n\n"
            f"I'll give you a random topic, press the timer and speak!\n"
            f"Daily practice = confident speaker 💪\n\n"
            f"Choose from the menu:"
        )
    await update.message.reply_text(
        text, parse_mode="Markdown", reply_markup=main_menu_keyboard(lang)
    )

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data
    lang = get_lang(user_id)
    difficulty = get_difficulty(user_id)

    # ── Language toggle ────────────────────────────────────────────
    if data.startswith("lang_"):
        lang = data.split("_")[1]
        user_languages[user_id] = lang
        label = "تم تغيير اللغة إلى العربية 🇸🇦" if lang == "ar" else "Language changed to English 🇺🇸"
        await query.edit_message_text(label, reply_markup=main_menu_keyboard(lang))

    # ── Main menu ──────────────────────────────────────────────────
    elif data == "menu_main":
        title = "اختر من القائمة:" if lang == "ar" else "Choose from the menu:"
        await query.edit_message_text(title, reply_markup=main_menu_keyboard(lang))

    # ── Category menu ──────────────────────────────────────────────
    elif data == "menu_category":
        title = "📂 اختر الفئة:" if lang == "ar" else "📂 Choose a category:"
        await query.edit_message_text(title, reply_markup=category_keyboard(lang))

    # ── Difficulty menu ────────────────────────────────────────────
    elif data == "menu_difficulty":
        title = "🎯 اختر مستوى الصعوبة:" if lang == "ar" else "🎯 Choose difficulty level:"
        await query.edit_message_text(title, reply_markup=difficulty_keyboard(lang, difficulty))

    elif data.startswith("diff_"):
        level = data.split("_")[1]
        user_difficulty[user_id] = level
        labels = {
            "ar": {"any": "🎲 عشوائي", "easy": "🟢 سهل", "medium": "🟡 متوسط", "hard": "🔴 صعب"},
            "en": {"any": "🎲 Any", "easy": "🟢 Easy", "medium": "🟡 Medium", "hard": "🔴 Hard"},
        }
        label = labels[lang][level]
        msg = f"✅ تم اختيار: {label}" if lang == "ar" else f"✅ Selected: {label}"
        await query.edit_message_text(msg, reply_markup=difficulty_keyboard(lang, level))

    # ── Framework menu ─────────────────────────────────────────────
    elif data == "menu_framework":
        title = "🧱 اختر الإطار الخطابي:" if lang == "ar" else "🧱 Choose a speaking framework:"
        await query.edit_message_text(title, reply_markup=framework_keyboard(lang))

    elif data.startswith("fw_"):
        fw_key = data.split("_")[1]
        fw = FRAMEWORKS.get(fw_key, {}).get(lang, {})
        title = fw.get("title", fw_key)
        desc = fw.get("desc", "")
        back_label = "🔙 رجوع" if lang == "ar" else "🔙 Back"
        kb = InlineKeyboardMarkup([[InlineKeyboardButton(back_label, callback_data="menu_framework")]])
        await query.edit_message_text(
            f"*{title}*\n\n{desc}", parse_mode="Markdown", reply_markup=kb
        )

    # ── Timer ──────────────────────────────────────────────────────
    elif data.startswith("timer_"):
        category = data.replace("timer_", "")
        chat_id = query.message.chat_id
        start_msg = "🟢 *بدأ المؤقت! تحدث الآن...*" if lang == "ar" else "🟢 *Timer started! Speak now...*"
        await query.edit_message_text(start_msg, parse_mode="Markdown")
        asyncio.create_task(run_timer(context, chat_id, lang))

    # ── Random topic ───────────────────────────────────────────────
    elif data == "topic_random":
        category = random.choice(list(TOPICS.keys()))
        topic = get_random_topic(category, lang, difficulty)
        msg = topic_message(topic, category, lang)
        await query.edit_message_text(
            msg, parse_mode="Markdown",
            reply_markup=after_topic_keyboard(lang, category)
        )

    # ── Topic from category ────────────────────────────────────────
    elif data.startswith("topic_cat_"):
        category = data.replace("topic_cat_", "")
        topic = get_random_topic(category, lang, difficulty)
        msg = topic_message(topic, category, lang)
        await query.edit_message_text(
            msg, parse_mode="Markdown",
            reply_markup=after_topic_keyboard(lang, category)
        )

# ─── Quick Commands ────────────────────────────────────────────────────────────
async def cmd_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    difficulty = get_difficulty(user_id)
    category = random.choice(list(TOPICS.keys()))
    topic = get_random_topic(category, lang, difficulty)
    msg = topic_message(topic, category, lang)
    await update.message.reply_text(
        msg, parse_mode="Markdown",
        reply_markup=after_topic_keyboard(lang, category)
    )

async def cmd_framework(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    title = "🧱 اختر الإطار الخطابي:" if lang == "ar" else "🧱 Choose a speaking framework:"
    await update.message.reply_text(title, reply_markup=framework_keyboard(lang))

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    if lang == "ar":
        text = (
            "📖 *الأوامر المتاحة:*\n\n"
            "/start — القائمة الرئيسية\n"
            "/topic — موضوع عشوائي فوري\n"
            "/framework — اختر إطارًا خطابيًا\n"
            "/help — عرض هذه الرسالة\n\n"
            "*نصيحة:* استخدم /topic يوميًا وتمرن لمدة دقيقة كاملة 🎯"
        )
    else:
        text = (
            "📖 *Available Commands:*\n\n"
            "/start — Main menu\n"
            "/topic — Get a random topic instantly\n"
            "/framework — Choose a speaking framework\n"
            "/help — Show this message\n\n"
            "*Tip:* Use /topic daily and practice for a full minute 🎯"
        )
    await update.message.reply_text(text, parse_mode="Markdown")

# ─── Main ──────────────────────────────────────────────────────────────────────
def main():
    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("topic", cmd_topic))
    app.add_handler(CommandHandler("framework", cmd_framework))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CallbackQueryHandler(callback_handler))

    logger.info("🤖 Bot is running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
