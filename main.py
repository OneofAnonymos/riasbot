import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from openai import OpenAI

# تنظیمات توکن‌ها
TELEGRAM_BOT_TOKEN = "7772214943:AAGXbULvJzWzYoGd4-mMac9ppIhckB8T_XU"
OPENAI_API_KEY = "aa-lBU8qQMHlVTawjRet4GAZesnA2KUCpNzbY8ZhFaNYlYwRvBw"
MASTER_ID = 6864140483  # آیدی ارباب

# اتصال به AvalAI
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.avalai.ir/v1"
)

# تنظیم لاگ
logging.basicConfig(level=logging.INFO)

# حافظه موقتی برای مکالمات
user_memory = {}

async def handle_rias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    message_text = update.message.text
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    bot_username = context.bot.username.lower()
    is_group = update.effective_chat.type in ["group", "supergroup"]

    # فقط جواب بده اگر در گروه، بهش ریپلای شده یا منشن شده
    should_respond = False
    if is_group:
        if bot_username in message_text.lower() or \
           (update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id):
            should_respond = True
    else:
        should_respond = True

    # اگر "ریاس" توی پیام نیست، بی‌خیال شو
    if "ریاس" not in message_text.lower() or not should_respond:
        return

    is_master = user_id == MASTER_ID
    display_name = "اربابم" if is_master else user_name

    # لحن و شخصیت ریاس
    prompt = f"""
تو یه دختر خوشگل، باهوش، مغرور و شیطون به اسم "ریاس گریموری" هستی.
وقتی کسی اسمت رو صدا می‌زنه، با لحن دخترونه‌ی شیطون و مغرور جواب می‌دی.
اگه اون شخص "ارباب"ت باشه ({display_name})، یه کم مهربون‌تر و وسوسه‌انگیزتر حرف می‌زنی، ولی هنوز غرور و نازتو داری.

مثال‌هایی از سبک حرف زدنت:
- هووم؟ تو با من کاری داشتی؟ جالبه... ولی شاید دلم بخواد جواب بدم.
- فقط چون اربابمی، اینو بهت می‌گم... وگرنه اهمیتی نمی‌دادم.
- آخی، چه سوال ساده‌ای... انتظار بیشتری ازت داشتم!

حالا اینو بهم گفت:
{message_text}

جواب بده با همین لحن دخترونه و مغرور و شیطون:
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        reply_text = response.choices[0].message.content.strip()

        # فقط یک‌بار ریپلای کن
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=reply_text,
            reply_to_message_id=update.message.message_id
        )

    except Exception as e:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="ریاس الان حال نداره، بعداً بیا بازی کنیم... 😒",
            reply_to_message_id=update.message.message_id
        )
        logging.error(f"خطا: {e}")

# اجرای برنامه
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_rias))
    print("ریاس گریموری آماده‌ی شیطنت شد! 😈")
    app.run_polling()
