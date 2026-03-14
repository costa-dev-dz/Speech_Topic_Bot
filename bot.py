"""
🎤 Speech Topic Bot - بوت مواضيع الخطابة
Supports Arabic & English | يدعم العربية والإنجليزية
"""

import logging
import random
import os
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

# ─── User Language Storage (in-memory) ─────────────────────────────────────────
user_languages: dict[int, str] = {}

def get_lang(user_id: int) -> str:
    return user_languages.get(user_id, "ar")

# ─── Content Data ───────────────────────────────────────────────────────────────
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
        "general":   "💬 عام",
        "tech":      "💻 تقنية",
        "finance":   "💰 مالية",
        "interview": "🎯 مقابلات عمل",
        "hot_takes": "🌶️ آراء جريئة",
    },
    "en": {
        "general":   "💬 General",
        "tech":      "💻 Tech",
        "finance":   "💰 Finance",
        "interview": "🎯 Interview Prep",
        "hot_takes": "🌶️ Hot Takes",
    },
}

DIFFICULTY_LABELS = {
    "ar": {"easy": "🟢 سهل", "medium": "🟡 متوسط", "hard": "🔴 صعب"},
    "en": {"easy": "🟢 Easy", "medium": "🟡 Medium", "hard": "🔴 Hard"},
}

# ─── Helpers ────────────────────────────────────────────────────────────────────
def get_random_topic(category: str, lang: str) -> str:
    pool = TOPICS.get(category, TOPICS["general"]).get(lang, [])
    return random.choice(pool) if pool else "—"

def difficulty_tag(topic: str, lang: str) -> str:
    words = len(topic.split())
    if words < 8:
        return DIFFICULTY_LABELS[lang]["easy"]
    elif words < 14:
        return DIFFICULTY_LABELS[lang]["medium"]
    else:
        return DIFFICULTY_LABELS[lang]["hard"]

def topic_message(topic: str, category: str, lang: str) -> str:
    cat_label = CATEGORIES_META[lang].get(category, "")
    diff = difficulty_tag(topic, lang)
    if lang == "ar":
        return (
            f"🎤 *موضوعك للخطابة*\n\n"
            f"_{topic}_\n\n"
            f"📂 الفئة: {cat_label}  |  {diff}\n\n"
            f"⏱ اضبط مؤقتًا لمدة دقيقة وابدأ الكلام!"
        )
    else:
        return (
            f"🎤 *Your Speech Topic*\n\n"
            f"_{topic}_\n\n"
            f"📂 Category: {cat_label}  |  {diff}\n\n"
            f"⏱ Set a 1-minute timer and start speaking!"
        )

# ─── Keyboards ──────────────────────────────────────────────────────────────────
def main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    if lang == "ar":
        buttons = [
            [InlineKeyboardButton("🎲 موضوع عشوائي", callback_data="topic_random")],
            [InlineKeyboardButton("📂 اختر الفئة", callback_data="menu_category"),
             InlineKeyboardButton("🧱 الأطر الخطابية", callback_data="menu_framework")],
            [InlineKeyboardButton("🌐 English", callback_data="lang_en")],
        ]
    else:
        buttons = [
            [InlineKeyboardButton("🎲 Random Topic", callback_data="topic_random")],
            [InlineKeyboardButton("📂 Pick Category", callback_data="menu_category"),
             InlineKeyboardButton("🧱 Frameworks", callback_data="menu_framework")],
            [InlineKeyboardButton("🌐 العربية", callback_data="lang_ar")],
        ]
    return InlineKeyboardMarkup(buttons)

def category_keyboard(lang: str) -> InlineKeyboardMarkup:
    cats = CATEGORIES_META[lang]
    buttons = [
        [InlineKeyboardButton(label, callback_data=f"topic_cat_{key}")]
        for key, label in cats.items()
    ]
    back_label = "🔙 رجوع" if lang == "ar" else "🔙 Back"
    buttons.append([InlineKeyboardButton(back_label, callback_data="menu_main")])
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
            [InlineKeyboardButton("🔄 موضوع جديد", callback_data=f"topic_cat_{category}"),
             InlineKeyboardButton("🧱 إطار خطابي", callback_data="menu_framework")],
            [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="menu_main")],
        ]
    else:
        buttons = [
            [InlineKeyboardButton("🔄 New Topic", callback_data=f"topic_cat_{category}"),
             InlineKeyboardButton("🧱 Framework", callback_data="menu_framework")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="menu_main")],
        ]
    return InlineKeyboardMarkup(buttons)

# ─── Handlers ───────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    name = update.effective_user.first_name or "صديقي"

    if lang == "ar":
        text = (
            f"👋 أهلًا *{name}*!\n\n"
            f"🎤 أنا بوت *مواضيع الخطابة الارتجالية*\n\n"
            f"سأعطيك موضوعًا عشوائيًا، اضبط مؤقت دقيقة، وابدأ الحديث!\n"
            f"ممارسة يومية = خطيب بارع 💪\n\n"
            f"اختر من القائمة:"
        )
    else:
        text = (
            f"👋 Hey *{name}*!\n\n"
            f"🎤 I'm your *Impromptu Speaking Bot*\n\n"
            f"I'll give you a random topic, set a 1-minute timer and speak!\n"
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

    if data.startswith("lang_"):
        lang = data.split("_")[1]
        user_languages[user_id] = lang
        label = "تم تغيير اللغة إلى العربية 🇸🇦" if lang == "ar" else "Language changed to English 🇺🇸"
        await query.edit_message_text(label, reply_markup=main_menu_keyboard(lang))

    elif data == "menu_main":
        title = "اختر من القائمة:" if lang == "ar" else "Choose from the menu:"
        await query.edit_message_text(title, reply_markup=main_menu_keyboard(lang))

    elif data == "menu_category":
        title = "📂 اختر الفئة:" if lang == "ar" else "📂 Choose a category:"
        await query.edit_message_text(title, reply_markup=category_keyboard(lang))

    elif data == "menu_framework":
        title = "🧱 اختر الإطار الخطابي:" if lang == "ar" else "🧱 Choose a speaking framework:"
        await query.edit_message_text(title, reply_markup=framework_keyboard(lang))

    elif data.startswith("fw_"):
        fw_key = data.split("_")[1]
        fw = FRAMEWORKS.get(fw_key, {}).get(lang, {})
        title = fw.get("title", fw_key)
        desc = fw.get("desc", "")
        back_label = "🔙 رجوع" if lang == "ar" else "🔙 Back"
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(back_label, callback_data="menu_framework")]
        ])
        await query.edit_message_text(
            f"*{title}*\n\n{desc}", parse_mode="Markdown", reply_markup=kb
        )

    elif data == "topic_random":
        category = random.choice(list(TOPICS.keys()))
        topic = get_random_topic(category, lang)
        msg = topic_message(topic, category, lang)
        await query.edit_message_text(
            msg, parse_mode="Markdown",
            reply_markup=after_topic_keyboard(lang, category)
        )

    elif data.startswith("topic_cat_"):
        category = data.replace("topic_cat_", "")
        topic = get_random_topic(category, lang)
        msg = topic_message(topic, category, lang)
        await query.edit_message_text(
            msg, parse_mode="Markdown",
            reply_markup=after_topic_keyboard(lang, category)
        )

# ─── Quick Commands ─────────────────────────────────────────────────────────────
async def cmd_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    category = random.choice(list(TOPICS.keys()))
    topic = get_random_topic(category, lang)
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

# ─── Main ───────────────────────────────────────────────────────────────────────
def main():
    # ✅ إصلاح لـ Python 3.12+ الذي لا ينشئ event loop تلقائيًا
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
