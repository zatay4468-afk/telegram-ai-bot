import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

# Environment Variables မှ Keys များ ရယူခြင်း
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini Client သတ်မှတ်ခြင်း
client = genai.Client(api_key=GEMINI_API_KEY)

# Bot သို့ ပေးမည့် System Prompt (မိမိ Bot သိစေချင်သည်များကို ဒီနေရာတွင် ကြိုရေးထားနိုင်ပါသည်)
SYSTEM_INSTRUCTION = (
    "သင်သည် ကူညီပေးသူ AI Assistant ဖြစ်သည်။ "
    "အသုံးပြုသူ (User) မေးမြန်းသည့် ဘာသာစကားအတိုင်း အတိအကျ ပြန်လည်ဖြေကြားပေးပါ "
    "(မြန်မာလိုမေးပါက မြန်မာလို ပြန်ဖြေပါ၊ အင်္ဂလိပ်လိုမေးပါက အင်္ဂလိပ်လို ပြန်ဖြေပါ)။ "
    "သဘာဝကျကျနှင့် ယဉ်ကျေးစွာ အဖြေပေးပါ။"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ! ကျွန်တော်က Gemini AI သုံးထားတဲ့ Telegram Bot ဖြစ်ပါတယ်။ ဘာများကူညီပေးရမလဲခင်ဗျာ။")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    try:
        # Gemini 2.5 Flash Model ကို သုံး၍ အဖြေထုတ်ခြင်း
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
            config={'system_instruction': SYSTEM_INSTRUCTION}
        )
        ai_reply = response.text
        await update.message.reply_text(ai_reply)
    except Exception as e:
        await update.message.reply_text("တောင်းပန်းပါတယ်၊ အဖြေထုတ်ပေးရာတွင် အမှားတစ်ခု ရှိနေပါတယ်။")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is running...")
    app.run_polling()
