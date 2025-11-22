import telebot

TOKEN = "8305996554:AAFdxT26nySDOwD8-ZIDD8WazSekZmPEle0"
ADMIN_ID = 822343514

bot = telebot.TeleBot(TOKEN)

user_state = {}  # хранит стадию заявки


@bot.message_handler(commands=['start'])
def start(message):
    user_state[message.chat.id] = "waiting_info"

    bot.send_message(
        message.chat.id,
        "Привет! 👋\n\n"
        "Отправь *в одном сообщении* информацию о себе И ОБЯЗАТЕЛЬНО СВОЙ ТЕГ ТГ@ иначе мы не сможем связаться.\n"
        "После этого можешь прислать треки / аудио отдельными сообщениями.\n\n"
        "Когда закончишь — просто напиши: «готово»."
    )


@bot.message_handler(func=lambda m: user_state.get(m.chat.id) == "waiting_info" and m.text.lower() != "готово")
def get_info(message):
    # Пользователь отправил описание
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    user_state[message.chat.id] = "waiting_tracks"

    bot.send_message(
        message.chat.id,
        "Описание получил! Теперь можешь присылать треки, файлы, демки и т.д.\n"
        "Когда закончишь — напиши: «готово»."
    )


@bot.message_handler(func=lambda m: user_state.get(m.chat.id) == "waiting_tracks", content_types=['audio', 'voice', 'document', 'photo', 'video'])
def get_tracks(message):
    # Пересылаем все медиа
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)


@bot.message_handler(func=lambda m: user_state.get(m.chat.id) == "waiting_tracks" and m.text.lower() == "готово")
def finish(message):
    bot.send_message(message.chat.id, "Спасибо за заявку! 🙌 Если что — мы вам напишем.")
    user_state.pop(message.chat.id, None)


bot.polling(none_stop=True)
