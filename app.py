"""
app.py — نقطة الدخول لـ Render
يشغّل Flask لاستقبال health checks + البوت في خيط منفصل
"""

import os
import logging
import asyncio
import threading
from flask import Flask

# ─── Flask App ──────────────────────────────────────────────────────────────────
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Speech Topic Bot is running!"

@app.route('/health')
def health():
    return "OK", 200

# ─── Bot Runner ─────────────────────────────────────────────────────────────────
def run_bot():
    """تشغيل البوت في event loop مستقل داخل thread منفصل"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    from bot import main as bot_main
    bot_main()

# ─── Entry Point ────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    # تشغيل البوت في خيط منفصل مع event loop خاص به
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    logging.info("✅ Bot thread started")

    # تشغيل Flask على المنفذ المطلوب
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
