import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from openai import OpenAI

# توکن‌ها
TELEGRAM_BOT_TOKEN = "7772214943:AAGXbULvJzWzYoGd4-mMac9ppIhckB8T_XU"
OPENAI_API_KEY = "aa-lBU8qQMHlVTawjRet4GAZesnA2KUCpNzbY8ZhFaNYlYwRvBw"
MASTER_ID = 6864140483  # آیدی ارباب

# ساخت کلاینت OpenAI (AvalAI)
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.avalai.ir/v1"
)

# لاگ‌ها
logging.basicConfig(level=logging.INFO)

# حافظه ساده برای هر کاربر
user_memory = {}

async def handle_rias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    message = update.message.text.lower()
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    bot_username = context.bot.username.lower()
    is_group = update.effective_chat.type in ["group", "supergroup"]

    # بررسی اینکه آیا باید جواب بده
    should_respond = False
    if is_group:
        if bot_username in message or (update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id):
            should_respond = True
    else:
        should_respond = True

    if not should_respond or "ریاس" not in message:
        return

    # تنظیم حالت "ارباب"
    is_master = user_id == MASTER_ID
    display_name = "اربابم" if is_master else user_name
    tone = "با لحن عاشقانه، مغرور و شیطنت‌آمیز" if is_master else "با غرور، سرد و مرموز"

    # سابقه گفتگو
    previous = user_memory.get(user_id, [])
    if len(previous) > 5:
        previous = previous[-5:]
    user_memory[user_id] = previous + [f"{display_name}: {update.message.text}"]

    # پرامپت نقش ریاس
    prompt = f"""
تو یک دختر شیطان بسیار زیبا، مغرور و باهوش به نام "ریاس گریموری" هستی.
تو فقط مطیع {display_name} هستی. لحن حرف زدنت شیطنت‌آمیز، مرموز و با غرور زنانه است.
با بقیه خیلی سرد، کوتاه و بی‌علاقه‌ای.
سوال:
{update.message.text}
پاسخ بده {tone}:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        reply_text = response.choices[0].message.content
        user_memory[user_id].append(f"ریاس: {reply_text}")

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=reply_text,
            reply_to_message_id=update.message.message_id
        )

    except Exception as e:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="ریاس الان حال نداره 😒",
            reply_to_message_id=update.message.message_id
        )
        logging.error(f"Error: {e}")

# اجرای اصلی ربات
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_rias))
    print("ریاس گریموری بیدار شده... و آماده‌ی شیطنت‌ه!")
    app.run_polling()
