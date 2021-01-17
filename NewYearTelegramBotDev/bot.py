import telebot
import config

from telebot import types

bot = telebot.TeleBot(config.TOKEN);


# Функция обработки команды /start
@bot.message_handler(commands=['start'])
def welcome(message):
    sticker = open('resources/stickerGreetingsSanta.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)

    # Добавление клавиатуры
    # resize_keyboard=True означает, что клавиатура у нас будет масштабироваться
    # в зависимости от размера экрана устройства, на котором будет запущен бот
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Создание двух кнопок клавиатуры для управления ботом
    item1 = types.KeyboardButton("Поздравить с Новым Годом 🎄")
    item2 = types.KeyboardButton("Поднять настроение 😊")

    # добавление кнопок в клавиатуру
    markup.add(item1, item2)
    bot.send_message(message.chat.id,
                     "Добро пожаловать, <b>{0.first_name}!</b>\nЯ - <b>{1.first_name}</b> - новогодний чат-бот, "
                     "который будет поздравлять тебя.".format(message.from_user, bot.get_me()), parse_mode='html',
                     reply_markup=markup)


# Функция отправки сообщения ботом
# В аннотации @bot.message_handler мы указываем какой тип сообщений боту нужно обрабатывать:
# В нашем случае - это текстовые сообщения
@bot.message_handler(content_types=['text'])
def send_message(message):
    # Обработчик реакции бота
    # Если получено личное сообщение
    if message.chat.type == 'private':
        if message.text == 'Поздравить с Новым Годом 🎄':
            sticker = open('resources/stickerMerryChristmas.webp', 'rb')
            bot.send_sticker(message.chat.id, sticker)
            bot.send_message(message.chat.id,
                             "Уважаемый <b>{0.first_name}</b>\nЯ - <b>{1.first_name}</b> - новогодний чат-бот, "
                             "Поздравляю тебя с <b>Наступающим Новым Годом и Рождеством!!!</b>"
                             .format(message.from_user, bot.get_me()), parse_mode='html')
        elif message.text == 'Поднять настроение 😊':
            # отображение inline-клавиатуры для показа кнопок в сообщении
            markup = types.InlineKeyboardMarkup(row_width=2)
            # добавление кнопок клавиатуры
            item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')
            markup.add(item1, item2)
            bot.send_message(message.chat.id, "Как настроение?", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Я не знаю, что тебе ответить :(')


# Обработчик нажатий кнопок клавиатуры в сообщении
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                sticker = open('resources/AnimatedSnowManSticker.tgs', 'rb')
                bot.send_sticker(call.message.chat.id, sticker)
                bot.send_message(call.message.chat.id, '<b>C Новым Годом! Ура!!!</b>', parse_mode='html')
            elif call.data == 'bad':
                sticker = open('resources/AnimatedSantaSticker.tgs', 'rb')
                christmas_song = open('resources/ChristmasSong.mp3', 'rb')
                bot.send_sticker(call.message.chat.id, sticker)
                bot.send_message(call.message.chat.id, '<b>C Новым Годом! Ура!!!</b>', parse_mode='html')
                bot.send_audio(call.message.chat.id, christmas_song)

    except Exception as e:
        print(repr(e))


# Запуск бота
bot.polling(none_stop=True)
