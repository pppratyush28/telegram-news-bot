
import logging
from flask import Flask, request
from telegram.ext import CommandHandler, MessageHandler, filters, ApplicationBuilder, ContextTypes
from telegram import Bot, Update
from NewsBotUtils import get_reply, fetch_news
import asyncio
from dotenv import load_dotenv
load_dotenv()

import os
TOKEN = os.getenv("TELEGRAM_TOKEN")

# logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

WEBHOOK_URL = f"https://1e72c8890564.ngrok-free.app/{TOKEN}"

dp = ApplicationBuilder().token(TOKEN).build()
initialized = False

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    try:
        global initialized
        update = Update.de_json(request.get_json(force=True), dp.bot)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        if not initialized:
            loop.run_until_complete(dp.initialize())
            initialized = True

        loop.run_until_complete(dp.process_update(update))
        return "OK"
    except Exception as e:
        logging.error(f"Error processing update: {e}")
        return "500 INTERNAL SERVER ERROR", 500

# === Handler functions ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    author = update.message.from_user.first_name
    reply = f"Hi! {author}"
    await context.bot.send_message(chat_id=update.message.chat_id, text=reply)

async def _help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_txt = "Hey! This is a help text."
    await context.bot.send_message(chat_id=update.message.chat_id, text=help_txt)


async def reply_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message:
            intent, reply = get_reply(update.message.text, update.message.chat_id)
            print(f"[DEBUG] Intent: {intent}, Reply: {reply}")

            if intent == "get_news":
                news_items = fetch_news(reply)
                if not news_items:
                    await context.bot.send_message(
                        chat_id=update.message.chat_id,
                        text="Sorry, I couldn't find any news for that."
                    )
                else:
                    for item in news_items:
                        await context.bot.send_message(
                            chat_id=update.message.chat_id,
                            text=f"{item['title']}\n{item['link']}"
                        )
            else:
                await context.bot.send_message(chat_id=update.message.chat_id, text=reply)
    except Exception as e:
        logger.error(f"Error in reply_text: {e}")
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Oops! Something went wrong."
        )


async def echo_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_sticker(chat_id=update.message.chat_id, sticker=update.message.sticker.file_id)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Update '%s' caused error '%s'", update, context.error)

# === Main setup ===
def main():
    asyncio.run(dp.bot.set_webhook(WEBHOOK_URL))

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", _help))
    dp.add_handler(MessageHandler(filters.TEXT, reply_text))
    dp.add_handler(MessageHandler(filters.Sticker, echo_sticker))
    dp.add_error_handler(error_handler)

if __name__ == "__main__":
    main()
    app.run(port=8443)


