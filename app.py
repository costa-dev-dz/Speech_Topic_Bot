"""
app.py — الحل النهائي لـ Render (Web Service)
"""

import os
import asyncio
import logging
import threading

from flask import Flask
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import bot as b

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ─── Flask ──────────────────────────────────────────────────────────────────────
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "🤖 Bot is running!"

@flask_app.route('/health')
def health():
    return "OK", 200

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    flask_app.run(host='0.0.0.0', port=port)

# ─── Bot ────────────────────────────────────────────────────────────────────────
async def run_bot():
    try:
        logger.info("⚙️ Building application...")
        async with Application.builder().token(b.BOT_TOKEN).build() as app:
            app.add_handler(CommandHandler("start",     b.start))
            app.add_handler(CommandHandler("topic",     b.cmd_topic))
            app.add_handler(CommandHandler("framework", b.cmd_framework))
            app.add_handler(CommandHandler("help",      b.cmd_help))
            app.add_handler(CallbackQueryHandler(b.callback_handler))

            await app.updater.start_polling(drop_pending_updates=True)
            logger.info("🤖 Bot is running!")
            await asyncio.Event().wait()
    except Exception as e:
        logger.error(f"❌ Bot crashed: {e}", exc_info=True)
        raise

# ─── Main ────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    logger.info("🚀 Starting app...")

    threading.Thread(target=run_flask, daemon=True).start()
    logger.info("✅ Flask thread started")

    logger.info("⏳ Starting bot...")
    asyncio.run(run_bot())
