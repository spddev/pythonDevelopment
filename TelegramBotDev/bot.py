import telebot
import config
import random

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

# Функция обработки команды /start
@bot.message_handler(commands=['start'])
def welcome(message):
    sticker = open('Resources/sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)

    # Добавление клавиатуры
    # resize_keyboard=True означает, что клавиатура у нас будет маленькой
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Создание двух кнопок на клавиатуре
    item1 = types.KeyboardButton("🎲Случайное число")
    item2 = types.KeyboardButton("😊Как дела?")

    # Добавление кнопок в клавиатуру
    markup.add(item1, item2)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы быть подопытным кроликом.".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)

# Функция отправки сообщения ботом
# В аннотации @bot.message_handler мы указываем какой тип сообщений боту нужно обрабатывать:
# В нашем случае - это текстовые сообщения
@bot.message_handler(content_types=['text'])
def send_message(message):
    # Обработка реакции бота
    # Если получено личное сообщение
    if message.chat.type == 'private':
        if message.text == '🎲Случайное число':
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
        elif message.text == '😊Как дела?':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Отлично, сам как ?', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Я не знаю, что тебе ответить :((')

# Обработчик нажатий кнопок клавиатуры в сообщении
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает...')

            # удаление кнопок клавиатуры в сообщении
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😊Как дела?",
                                  reply_markup=None)

            # показ уведомлений пользователю
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Это тестовое уведомление!!!1111")
    except Exception as e:
        print(repr(e))


# ЗАПУСК БОТА
bot.polling(none_stop=True)