"""
app.py — نقطة الدخول لـ Render (Web Service)
Flask في thread منفصل، البوت في main thread
"""

import os
import asyncio
import logging
import threading
from flask import Flask

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ─── Flask App ──────────────────────────────────────────────────────────────────
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "🤖 Speech Topic Bot is running!"

@flask_app.route('/health')
def health():
    return "OK", 200

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    flask_app.run(host='0.0.0.0', port=port)

# ─── Entry Point ────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    # Flask في thread منفصل
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("✅ Flask thread started")

    # البوت في main thread (ضروري لأن run_polling يحتاج main thread)
    from telegram.ext import Application, CommandHandler, CallbackQueryHandler
    import bot as bot_module

    application = Application.builder().token(bot_module.BOT_TOKEN).build()
    application.add_handler(CommandHandler("start",     bot_module.start))
    application.add_handler(CommandHandler("topic",     bot_module.cmd_topic))
    application.add_handler(CommandHandler("framework", bot_module.cmd_framework))
    application.add_handler(CommandHandler("help",      bot_module.cmd_help))
    application.add_handler(CallbackQueryHandler(bot_module.callback_handler))

    logger.info("🤖 Bot is running!")
    application.run_polling(drop_pending_updates=True)
