import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from openai import OpenAI

# توکن و API
TELEGRAM_BOT_TOKEN = "7772214943:AAGXbULvJzWzYoGd4-mMac9ppIhckB8T_XU"
OPENAI_API_KEY = "aa-lBU8qQMHlVTawjRet4GAZesnA2KUCpNzbY8ZhFaNYlYwRvBw"
MASTER_ID = 6864140483

# تنظیم کلاینت AvalAI
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.avalai.ir/v1"
)

# لاگ
logging.basicConfig(level=logging.INFO)

# حافظه مکالمه برای هر کاربر
memory = {}

# لیست استیکرهای رندوم دخترونه
sticker_list = [
    "CAACAgUAAxkBAAEBb4tgZK7JmHYAAY_KfCS5dy3V0zDJi9IAAr8KAAKxEclWi7Wxwx4kmn4wBA",
    "CAACAgUAAxkBAAEBlc9mZkECWn5TnRRT7JcsU0v2OTTC9QACGwADwZxgDPz_hcP0lmcZMAQ",
    "CAACAgUAAxkBAAEBlc1mZkD3Wq0mRvbfAEJh1A6HZDssvQAC9g8AArxfyFY7FJ5I4Gx3aTAE",
    "CAACAgUAAxkBAAEBlc5mZkEfFtGPaS8Iueu7Uq0Er3c1qAACnAcAAtBxyFXuJPVIfY35wzAE"
]

async def handle_rias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text
    user = update.message.from_user
    user_id = user.id
    user_name = user.first_name
    chat_id = update.effective_chat.id
    bot_username = context.bot.username.lower()

    is_group = update.effective_chat.type in ["group", "supergroup"]
    should_respond = False

    if is_group:
        if bot_username in text.lower() or "ریاس" in text.lower() or (
            update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id
        ):
            should_respond = True
    else:
        should_respond = True

    if not should_respond:
        return

    display_name = "اربابم" if user_id == MASTER_ID else user_name

    # دریافت تاریخچه مکالمه
    if user_id not in memory:
        memory[user_id] = []

    memory[user_id].append({"role": "user", "content": text})

    # محدود کردن حافظه به 6 پیام آخر
    conversation_history = memory[user_id][-6:]

    # اضافه کردن نقش ریاس
    system_prompt = f"""
تو ریاس گریموری هستی، یه دختر خوشگل، مغرور، باهوش و شیطون.
با همه مغرور و تیکه‌دار حرف می‌زنی، ولی با {display_name} چون اربابت هست، یه کم مهربونی و ناز می‌کنی.
از شکلک‌های دخترونه استفاده کن، ولی جمله‌هات کوتاه و باحال باشه. حرفاتو شیرین و جذاب بزن.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                *conversation_history
            ]
        )

        reply = response.choices[0].message.content.strip()

        await context.bot.send_message(
            chat_id=chat_id,
            text=reply,
            reply_to_message_id=update.message.message_id
        )

        # انتخاب استیکر رندوم
        random_sticker = random.choice(sticker_list)
        await context.bot.send_sticker(chat_id=chat_id, sticker=random_sticker)

        # ذخیره جواب ریاس
        memory[user_id].append({"role": "assistant", "content": reply})

    except Exception as e:
        logging.error(f"خطا در پاسخ: {e}")
        await context.bot.send_message(
            chat_id=chat_id,
            text="ریاس الان حس حرف زدن نداره... ولی بعداً شاید بخواد شیطونی کنه 😏",
            reply_to_message_id=update.message.message_id
        )

# اجرای برنامه
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_rias))
    print("ریاس گریموری آماده‌ی شیطنت شد! 😈")
    app.run_polling()
