"""
app.py — Webhook mode للـ Render (الحل النهائي الصحيح)
لا polling = لا conflict أبداً
"""

import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import asyncio
import bot as b

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ─── إعداد البوت ────────────────────────────────────────────────────────────────
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # مثال: https://speech-topic-bot.onrender.com

# بناء الـ application مرة واحدة عند البدء
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
    return "🤖 Bot is running via Webhook!"

@flask_app.route('/health')
def health():
    return "OK", 200

@flask_app.route(f'/webhook/{b.BOT_TOKEN}', methods=['POST'])
def webhook():
    """استقبال التحديثات من تيليجرام"""
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    asyncio.run(application.process_update(update))
    return "OK", 200

# ─── تسجيل الـ Webhook عند البدء ────────────────────────────────────────────────
async def setup_webhook():
    await application.initialize()
    webhook_url = f"{WEBHOOK_URL}/webhook/{b.BOT_TOKEN}"
    await application.bot.set_webhook(url=webhook_url)
    logger.info(f"✅ Webhook set: {webhook_url}")

# ─── Main ────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    if not WEBHOOK_URL:
        raise ValueError("❌ يجب تعيين WEBHOOK_URL في متغيرات البيئة!")
    
    # تسجيل الـ webhook
    asyncio.run(setup_webhook())
    logger.info("🚀 Starting Flask...")
    
    port = int(os.environ.get('PORT', 10000))
    flask_app.run(host='0.0.0.0', port=port)
