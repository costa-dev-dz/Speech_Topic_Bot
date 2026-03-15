"""
topic_generator.py — توليد مواضيع أسبوعياً بالذكاء الاصطناعي
Claude API + Supabase REST API (بدون مكتبة supabase)
"""

import os
import json
import logging
import httpx
import anthropic

logger = logging.getLogger(__name__)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
SUPABASE_URL      = os.getenv("SUPABASE_URL")
SUPABASE_KEY      = os.getenv("SUPABASE_KEY")

CATEGORIES = {
    "general":    {"ar": "عام",          "en": "General"},
    "tech":       {"ar": "تقنية",        "en": "Tech"},
    "finance":    {"ar": "مالية",        "en": "Finance"},
    "interview":  {"ar": "مقابلات عمل", "en": "Interview Prep"},
    "hot_takes":  {"ar": "آراء جريئة",  "en": "Hot Takes"},
    "health":     {"ar": "صحة",          "en": "Health"},
    "sports":     {"ar": "رياضة",        "en": "Sports"},
    "history":    {"ar": "تاريخ",        "en": "History"},
    "philosophy": {"ar": "فلسفة",        "en": "Philosophy"},
    "culture":    {"ar": "ثقافة",        "en": "Culture"},
}

def supabase_headers():
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }

def generate_topics(category: str, lang: str, count: int = 5) -> list[str]:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    cat_name = CATEGORIES[category][lang]

    if lang == "ar":
        prompt = f"""أنت خبير في فن الخطابة والتحدث أمام الجمهور.
اقترح {count} مواضيع جديدة ومثيرة للنقاش لفئة "{cat_name}" باللغة العربية.
المواضيع يجب أن تكون:
- قصيرة وواضحة (جملة واحدة أو سؤال)
- مثيرة للتفكير والنقاش
- مناسبة للتحدث عنها لمدة دقيقة
- مختلفة عن المواضيع الشائعة

أجب فقط بـ JSON بهذا الشكل بدون أي نص إضافي:
{{"topics": ["الموضوع 1", "الموضوع 2", "الموضوع 3", "الموضوع 4", "الموضوع 5"]}}"""
    else:
        prompt = f"""You are an expert in public speaking and rhetoric.
Suggest {count} new and thought-provoking topics for the "{cat_name}" category in English.
Topics should be short, debatable, and suitable for 1-minute speeches.

Reply ONLY with JSON, no extra text:
{{"topics": ["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"]}}"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    data = json.loads(message.content[0].text.strip())
    return data["topics"]

def save_topics_to_db(topics: list[str], category: str, lang: str):
    rows = [{"category": category, "lang": lang, "topic": t} for t in topics]
    resp = httpx.post(
        f"{SUPABASE_URL}/rest/v1/topics",
        headers=supabase_headers(),
        json=rows
    )
    resp.raise_for_status()
    logger.info(f"✅ Saved {len(rows)} topics — {category}/{lang}")

def get_topics_from_db(category: str, lang: str) -> list[str]:
    resp = httpx.get(
        f"{SUPABASE_URL}/rest/v1/topics",
        headers=supabase_headers(),
        params={"category": f"eq.{category}", "lang": f"eq.{lang}", "select": "topic"}
    )
    resp.raise_for_status()
    return [row["topic"] for row in resp.json()]

def weekly_topic_generation():
    logger.info("🔄 Starting weekly topic generation...")
    total = 0
    for category in CATEGORIES:
        for lang in ["ar", "en"]:
            try:
                topics = generate_topics(category, lang, count=5)
                save_topics_to_db(topics, category, lang)
                total += len(topics)
            except Exception as e:
                logger.error(f"❌ Error {category}/{lang}: {e}")
    logger.info(f"✅ Done — {total} topics added")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    weekly_topic_generation()
