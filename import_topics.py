"""
import_topics.py — استيراد مواضيع من CSV إلى Supabase
الاستخدام: python import_topics.py topics.csv
"""

import os
from dotenv import load_dotenv
load_dotenv()

import sys
import csv
import json
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def supabase_headers():
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

def import_from_csv(filepath: str, batch_size: int = 50):
    """استيراد من CSV — كل صف: category, lang, topic"""
    rows = []
    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "category": row["category"].strip(),
                "lang":     row["lang"].strip(),
                "topic":    row["topic"].strip(),
            })

    logger.info(f"📂 Found {len(rows)} topics in CSV")
    _upload_batches(rows, batch_size)

def import_from_json(filepath: str, batch_size: int = 50):
    """
    استيراد من JSON — الصيغة:
    [
      {"category": "general", "lang": "ar", "topic": "..."},
      ...
    ]
    """
    with open(filepath, encoding="utf-8") as f:
        rows = json.load(f)

    logger.info(f"📂 Found {len(rows)} topics in JSON")
    _upload_batches(rows, batch_size)

def _upload_batches(rows: list, batch_size: int):
    """رفع البيانات على دفعات لتجنب timeout"""
    total = 0
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i + batch_size]
        try:
            resp = httpx.post(
                f"{SUPABASE_URL}/rest/v1/topics",
                headers=supabase_headers(),
                json=batch,
                timeout=30
            )
            resp.raise_for_status()
            total += len(batch)
            logger.info(f"✅ Uploaded {total}/{len(rows)} topics")
        except Exception as e:
            logger.error(f"❌ Error at batch {i}: {e}")

    logger.info(f"🎉 Done — {total} topics imported to Supabase")

if __name__ == "__main__":
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Set SUPABASE_URL and SUPABASE_KEY first")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: python import_topics.py <file.csv or file.json>")
        sys.exit(1)

    filepath = sys.argv[1]

    if filepath.endswith(".csv"):
        import_from_csv(filepath)
    elif filepath.endswith(".json"):
        import_from_json(filepath)
    else:
        print("❌ Only .csv and .json files are supported")
        sys.exit(1)
