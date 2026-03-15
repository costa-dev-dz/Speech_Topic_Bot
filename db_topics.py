"""
db_topics.py — قراءة مواضيع من Supabase عبر REST API
"""

import os
from dotenv import load_dotenv
load_dotenv()

import random
import logging
import httpx

logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_topic_from_db(category: str, lang: str) -> str | None:
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    try:
        resp = httpx.get(
            f"{SUPABASE_URL}/rest/v1/topics",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
            },
            params={
                "category": f"eq.{category}",
                "lang": f"eq.{lang}",
                "select": "topic"
            }
        )
        resp.raise_for_status()
        data = resp.json()
        if data:
            return random.choice(data)["topic"]
    except Exception as e:
        logger.warning(f"⚠️ Supabase read failed: {e}")
    return None
