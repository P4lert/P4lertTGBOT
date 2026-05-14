import telebot
import time
import threading

TOKEN = "8847474252:AAG2h4bHXt6x2Jbe21SRDOpIRnZUOESQ38Q"
bot = telebot.TeleBot(TOKEN)


# --- перевод времени ---
def parse_time(text):
    if text.endswith("м"):
        return int(text[:-1]) * 60
    elif text.endswith("ч"):
        return int(text[:-1]) * 3600
    elif text.endswith("д"):
        return int(text[:-1]) * 86400
    else:
        return None


# --- разбан ---
def unban_later(chat_id, user_id, seconds):
    time.sleep(seconds)
    try:
        bot.unban_chat_member(chat_id, user_id)
    except:
        pass


# --- размут ---
def unmute_later(chat_id, user_id, seconds):
    time.sleep(seconds)
    try:
        bot.restrict_chat_member(
            chat_id,
            user_id,
            can_send_messages=True
        )
    except:
        pass


# --- БАН ---
@bot.message_handler(func=lambda m: m.text and m.text.startswith("бан"))
def ban_user(message):
    if not message.reply_to_message:
        bot.reply_to(message, "Ответь на пользователя")
        return

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Формат: бан 1д / 2ч / 10м")
        return

    seconds = parse_time(args[1])
    if not seconds:
        bot.reply_to(message, "Неверный формат времени")
        return

    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id

    bot.kick_chat_member(chat_id, user_id)
    bot.reply_to(message, f"🚫 Забанен на {args[1]}")

    threading.Thread(target=unban_later, args=(chat_id, user_id, seconds)).start()


# --- МУТ ---
@bot.message_handler(func=lambda m: m.text and m.text.startswith("мут"))
def mute_user(message):
    if not message.reply_to_message:
        bot.reply_to(message, "Ответь на пользователя")
        return

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Формат: мут 1д / 2ч / 10м")
        return

    seconds = parse_time(args[1])
    if not seconds:
        bot.reply_to(message, "Неверный формат времени")
        return

    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id

    bot.restrict_chat_member(
        chat_id,
        user_id,
        can_send_messages=False
    )

    bot.reply_to(message, f"🔇 Замучен на {args[1]}")

    threading.Thread(target=unmute_later, args=(chat_id, user_id, seconds)).start()


bot.infinity_polling()