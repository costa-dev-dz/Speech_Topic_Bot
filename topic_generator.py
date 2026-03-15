"""
topic_generator.py — توليد مواضيع أسبوعياً بـ Groq API (مجاني)
"""

import os
from dotenv import load_dotenv
load_dotenv()

import json
import logging
import time
import httpx

logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

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
    "education":  {"ar": "تعليم",        "en": "Education"},
    "relationship":{"ar": "علاقات",      "en": "Relationships"},
    "mindset":    {"ar": "عقلية",        "en": "Mindset"},
}

def supabase_headers():
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }

def generate_topics(category: str, lang: str, count: int = 5) -> list[str]:
    cat_name = CATEGORIES[category][lang]

    if lang == "ar":
        prompt = f"""أنت خبير في فن الخطابة والتحدث أمام الجمهور.
اقترح {count} مواضيع جديدة ومثيرة للنقاش لفئة "{cat_name}" باللغة العربية.
المواضيع يجب أن تكون قصيرة ومثيرة للتفكير ومناسبة للتحدث عنها لمدة دقيقة.

أجب فقط بـ JSON بهذا الشكل بدون أي نص إضافي:
{{"topics": ["الموضوع 1", "الموضوع 2", "الموضوع 3", "الموضوع 4", "الموضوع 5"]}}"""
    else:
        prompt = f"""You are a public speaking expert.
Suggest {count} new thought-provoking topics for the "{cat_name}" category in English.
Topics should be short, debatable, suitable for 1-minute speeches.

Reply ONLY with JSON, no extra text:
{{"topics": ["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"]}}"""

    response = httpx.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.8,
        },
        timeout=30
    )
    response.raise_for_status()
    text = response.json()["choices"][0]["message"]["content"].strip()

    if "```" in text:
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]

    data = json.loads(text.strip())
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
                time.sleep(3)  # تأخير بسيط بين الطلبات
            except Exception as e:
                logger.error(f"❌ Error {category}/{lang}: {e}")
                time.sleep(5)
    logger.info(f"✅ Done — {total} topics added")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    weekly_topic_generation()
