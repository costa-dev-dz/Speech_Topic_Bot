"""
app.py — نقطة الدخول لـ Render (Web Service)
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
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Speech Topic Bot is running!"

@app.route('/health')
def health():
    return "OK", 200

# ─── Bot Runner ─────────────────────────────────────────────────────────────────
def run_bot():
    from telegram.ext import Application, CommandHandler, CallbackQueryHandler
    import bot as bot_module

    # إنشاء event loop مستقل لهذا الـ thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    application = Application.builder().token(bot_module.BOT_TOKEN).build()

    application.add_handler(CommandHandler("start",     bot_module.start))
    application.add_handler(CommandHandler("topic",     bot_module.cmd_topic))
    application.add_handler(CommandHandler("framework", bot_module.cmd_framework))
    application.add_handler(CommandHandler("help",      bot_module.cmd_help))
    application.add_handler(CallbackQueryHandler(bot_module.callback_handler))

    logger.info("🤖 Bot is running!")
    application.run_polling(drop_pending_updates=True)

# ─── Entry Point ────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    logger.info("✅ Bot thread started")

    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
