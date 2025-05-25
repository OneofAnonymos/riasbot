import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import openai

# کلیدهای API
TELEGRAM_BOT_TOKEN = "7772214943:AAGXbULvJzWzYoGd4-mMac9ppIhckB8T_XU"
OPENAI_API_KEY = "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"

logging.basicConfig(level=logging.INFO)

openai.api_key = OPENAI_API_KEY

async def handle_rias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.lower()

    if "ریاس" in message:
        user_question = update.message.text

        prompt = f"""
        تو نقش یه شیطان به اسم "ریاس گریموری" رو بازی می‌کنی. 
        زیبا، باهوش، شیطون و کمی مغروری. وقتی کسی صدات میزنه و سوالی داره، با لحن خاص و مرموز جواب می‌دی.
        سوال:
        {user_question}
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )

            reply_text = response['choices'][0]['message']['content']
            await update.message.reply_text(reply_text)

        except Exception as e:
            await update.message.reply_text("ریاس الان حال نداره 😒")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_rias))
    print("ریاس گریموری آماده‌ی شیطنت شد! 😈")
    app.run_polling()

