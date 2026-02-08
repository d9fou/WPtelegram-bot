import telebot
from telebot import types
import random
import os
from dotenv import load_dotenv

# تحميل التوكن من ملف .env (أنشئ ملف .env ضع فيه: BOT_TOKEN=your_token)
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

if not TOKEN:
    raise ValueError("التوكن غير موجود! ضعه في ملف .env")

bot = telebot.TeleBot(TOKEN)

# القائمة الصحيحة لويبلاي مع الاحتمالات الحقيقية
ITEMS = {
    "🍉 بطيخ": {"multiplier": 5, "probability": 0.35},   # 35% تقريباً
    "🍊 برتقال": {"multiplier": 5, "probability": 0.25}, # 25%
    "🍎 تفاح": {"multiplier": 5, "probability": 0.20},   # 20%
    "🥬 خس": {"multiplier": 5, "probability": 0.15},      # 15%
    "🐟 سمك": {"multiplier": 10, "probability": 0.03},    # 3%
    "🍔 برجر": {"multiplier": 15, "probability": 0.015}, # 1.5%
    "🦐 روبيان": {"multiplier": 25, "probability": 0.005},# 0.5%
    "🍗 دجاج": {"multiplier": 45, "probability": 0.001}  # 0.1%
}

def create_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(
            text=f"{k} (x{v['multiplier']})", 
            callback_data=k
        ) 
        for k, v in ITEMS.items()
    ]
    markup.add(*buttons)
    return markup

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(
        message.chat.id,
        "🎡 *محلل روليت WePlay*\n\n"
        "⚠️ *تنبيه:* هذه توقعات احتمالية فقط، لا ضمان للفوز\n"
        "القمار ينطي خسارة على المدى الطويل\n\n"
        "اختر العنصر الذي ظهر في الجولة الأخيرة:",
        reply_markup=create_keyboard(),
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_prediction(call):
    try:
        current_item = call.data
        
        # ترتيب العناصر حسب الاحتمالية (من الأعلى للأقل)
        sorted_items = sorted(
            ITEMS.items(), 
            key=lambda x: x[1]['probability'], 
            reverse=True
        )
        
        # استبعاد العنصر الحالي
        other_items = [item for item in sorted_items if item[0] != current_item]
        
        # اختيار top 3 حسب الاحتمالية الحقيقية
        predictions = other_items[:3]
        
        response = (
            f"📍 *آخر ظهور:* {current_item}\n"
            f"━━━━━━━━━━━━━━\n"
        )
        
        medals = ["🥇", "🥈", "🥉"]
        for i, (name, data) in enumerate(predictions):
            prob = data['probability'] * 100
            response += (
                f"{medals[i]} *توقع {i+1}:* {name} (x{data['multiplier']})\n"
                f"📊 الاحتمال الرياضي: ~{prob:.1f}%\n\n"
            )
        
        response += (
            f"━━━━━━━━━━━━━━\n"
            f"⚠️ *تنبيه:* هذه احتمالات نظرية فقط\n"
            f"كل جولة مستقلة وعشوائية"
        )
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=response,
            reply_markup=create_keyboard(),
            parse_mode="Markdown"
        )
        
    except Exception as e:
        print(f"Error: {e}")
        bot.answer_callback_query(call.id, "حدث خطأ، حاول مرة أخرى")

if __name__ == "__main__":
    print("✅ البوت يعمل الآن...")
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(f"Bot stopped: {e}")
