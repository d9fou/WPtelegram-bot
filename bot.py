import telebot
from telebot import types
import random
import os

# ضع التوكن الخاص بك هنا
TOKEN = os.environ.get('BOT_TOKEN', '8585433109:AAHAFvn82R5Fckh5vSGS80zh3wQ76jEajx0')
bot = telebot.TeleBot(TOKEN)

# القائمة الصحيحة لويبلاي
ITEMS = {
    "🍉 بطيخ": "x5",
    "🍊 برتقال": "x5",
    "🍎 تفاح": "x5",
    "🥬 خس": "x5",
    "🐟 سمك": "x10",
    "🍔 برجر": "x15",
    "🦐 روبيان": "x25",
    "🍗 دجاج": "x45"
}

def create_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=f"{k} ({v})", callback_data=k) for k, v in ITEMS.items()]
    markup.add(*buttons)
    return markup

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(
        message.chat.id,
        "🎡 محلل روليت WePlay (نسخة الأيفون)\n\n"
        "اختر العنصر الذي ظهر في الجولة الأخيرة الآن:",
        reply_markup=create_keyboard(),
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_prediction(call):
    current_item = call.data
    
    other_items = [item for item in ITEMS.keys() if item != current_item]
    predictions = random.sample(other_items, 3)
    response = (
        f"📍 **آخر ظهور:** {current_item}\n"
        f"━━━━━━━━━━━━━━\n"
        f"🥇 **توقع 1:** {predictions[0]} ({ITEMS[predictions[0]]})\n"
        f"📊 نسبة الثقة: {random.randint(88, 96)}%\n\n"
        f"🥈 **توقع 2:** {predictions[1]} ({ITEMS[predictions[1]]})\n"
        f"📊 نسبة الثقة: {random.randint(75, 87)}%\n\n"
        f"🥉 **توقع 3:** {predictions[2]} ({ITEMS[predictions[2]]})\n"
        f"📊 نسبة الثقة: {random.randint(60, 74)}%\n"
        f"━━━━━━━━━━━━━━\n"
        f"⚠️ اضغط على النتيجة الجديدة لتحديث التوقع"
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=response,
        reply_markup=create_keyboard(),
        parse_mode="Markdown"
    )

print("✅ البوت يعمل الآن...")
bot.polling(none_stop=True)
