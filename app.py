"""
app.py — الحل النهائي
"""

import os
import asyncio
import logging
import threading
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import bot as b

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# ─── Event loop ثابت في thread خاص ─────────────────────────────────────────────
loop = asyncio.new_event_loop()

def start_event_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()

threading.Thread(target=start_event_loop, daemon=True).start()

# ─── إعداد البوت ────────────────────────────────────────────────────────────────
application = Application.builder().token(b.BOT_TOKEN).build()
application.add_handler(CommandHandler("start",     b.start))
application.add_handler(CommandHandler("topic",     b.cmd_topic))
application.add_handler(CommandHandler("framework", b.cmd_framework))
application.add_handler(CommandHandler("help",      b.cmd_help))
application.add_handler(CallbackQueryHandler(b.callback_handler))

# ─── Flask ──────────────────────────────────────────────────────────────────────
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "🤖 Bot is running!"

@flask_app.route('/health')
def health():
    return "OK", 200

@flask_app.route(f'/webhook/{b.BOT_TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    # أرسل للـ loop بدون انتظار — Flask يرد لتيليجرام فوراً
    asyncio.run_coroutine_threadsafe(
        application.process_update(update), loop
    )
    return "OK", 200  # رد فوري قبل معالجة الـ update

# ─── تسجيل الـ Webhook ──────────────────────────────────────────────────────────
async def setup():
    await application.initialize()
    await application.start()
    webhook_url = f"{WEBHOOK_URL}/webhook/{b.BOT_TOKEN}"
    await application.bot.set_webhook(url=webhook_url)
    logger.info(f"✅ Webhook set: {webhook_url}")

# ─── Main ────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    if not WEBHOOK_URL:
        raise ValueError("❌ يجب تعيين WEBHOOK_URL في متغيرات البيئة!")

    asyncio.run_coroutine_threadsafe(setup(), loop).result()

    logger.info("🚀 Starting Flask...")
    port = int(os.environ.get('PORT', 10000))
    flask_app.run(host='0.0.0.0', port=port)
