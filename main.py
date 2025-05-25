import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# اطلاعات ربات و ارباب
TELEGRAM_BOT_TOKEN = "7772214943:AAGXbULvJzWzYoGd4-mMac9ppIhckB8T_XU"
FREE_API_EMAIL = "AmirzAli121990@gmail.com"
MASTER_ID = 6864140483  # << این تویی!

# حافظه کوتاه‌مدت برای هر کاربر
user_memory = {}

logging.basicConfig(level=logging.INFO)

async def handle_rias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    message = update.message.text.lower()
    is_group = update.effective_chat.type in ["group", "supergroup"]

    should_respond = False

    if is_group:
        if context.bot.username.lower() in message or \
           (update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id):
            should_respond = True
    else:
        should_respond = True

    if "ریاس" in message and should_respond:
        user_question = update.message.text

        is_master = user_id == MASTER_ID
        display_name = "اربابم" if is_master else user_name
        tone = "با لحن عاشقانه و مطیع" if is_master else "با لحن محترمانه ولی سرد"

        previous_messages = user_memory.get(user_id, [])
        if len(previous_messages) > 5:
            previous_messages = previous_messages[-5:]

        user_memory[user_id] = previous_messages + [f"{display_name}: {user_question}"]

        prompt = f"""
تو نقش شیطان مونث زیبایی به اسم "ریاس گریموری" هستی.
تو فقط عاشق و مطیع {display_name} هستی.
وقتی او صحبت می‌کند، تو {tone} پاسخ می‌دهی.
با بقیه مؤدب ولی جدی هستی.

مکالمات قبلی:
{chr(10).join(previous_messages)}

الان {display_name} گفت:
{user_question}

ریاس پاسخ می‌دهد:
        """

        try:
            model = 'gpt-3.5-turbo'
            url = f"http://195.179.229.119/gpt/api.php?prompt={requests.utils.quote(prompt)}&api_key={requests.utils.quote(FREE_API_EMAIL)}&model={model}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            reply_text = data.get("response", "ریاس حرفی برای گفتن نداره...")

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

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_rias))
    print("ریاس آماده‌ی اطاعت از اربابشه... در همه جا!")
    app.run_polling()
