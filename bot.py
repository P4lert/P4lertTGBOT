import os
import telebot
import time
import threading
import sys

print("🚀 Starting bot...")

TOKEN = os.getenv("BOT_TOKEN")

# --- ЖЁСТКАЯ ПРОВЕРКА ---
if not TOKEN:
    print("❌ ERROR: BOT_TOKEN is None")
    print("👉 Railway Variables не передали токен")
    sys.exit(1)

print("✅ TOKEN loaded:", TOKEN[:10] + "...")

bot = telebot.TeleBot(TOKEN)


# --- парсер времени ---
def parse_time(text):
    try:
        if text.endswith("m"):
            return int(text[:-1]) * 60
        if text.endswith("h"):
            return int(text[:-1]) * 3600
        if text.endswith("d"):
            return int(text[:-1]) * 86400
    except:
        return None


# --- размут ---
def unmute(chat_id, user_id, seconds):
    time.sleep(seconds)
    try:
        bot.restrict_chat_member(chat_id, user_id, can_send_messages=True)
    except Exception as e:
        print("Unmute error:", e)


# --- разбан ---
def unban(chat_id, user_id, seconds):
    time.sleep(seconds)
    try:
        bot.unban_chat_member(chat_id, user_id)
    except Exception as e:
        print("Unban error:", e)


# --- МУТ ---
@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith("мут"))
def mute(message):
    if not message.reply_to_message:
        bot.reply_to(message, "Ответь на пользователя")
        return

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Формат: мут 10m / 1h / 1d")
        return

    seconds = parse_time(args[1])
    if not seconds:
        bot.reply_to(message, "Ошибка времени")
        return

    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id

    bot.restrict_chat_member(chat_id, user_id, can_send_messages=False)
    bot.reply_to(message, f"🔇 мут на {args[1]}")

    threading.Thread(target=unmute, args=(chat_id, user_id, seconds)).start()


# --- БАН ---
@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith("бан"))
def ban(message):
    if not message.reply_to_message:
        bot.reply_to(message, "Ответь на пользователя")
        return

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Формат: бан 10m / 1h / 1d")
        return

    seconds = parse_time(args[1])
    if not seconds:
        bot.reply_to(message, "Ошибка времени")
        return

    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id

    bot.kick_chat_member(chat_id, user_id)
    bot.reply_to(message, f"🚫 бан на {args[1]}")

    threading.Thread(target=unban, args=(chat_id, user_id, seconds)).start()
print("🚀 BEFORE POLLING START")

while True:
    try:
        bot.infinity_polling()
    except Exception as e:
        print("❌ POLLING ERROR:", e)
        time.sleep(5)
        bot.infinity_polling(skip_pending=True, timeout=20, long_polling_timeout=10)
