import telebot
import time
from sql import MemberInfo

#token
token = '1018761895:AAE9zGMHZxYZlC_6kyRLAmTBC0Oubpp-QUQ'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def after_start(message):
    #language buttons:
    lang_buttons = telebot.types.InlineKeyboardMarkup()
    lang_buttons_1 = telebot.types.InlineKeyboardButton('Русский 🇷🇺', callback_data='rus')
    lang_buttons_2 = telebot.types.InlineKeyboardButton('O\'zbekcha 🇺🇿', callback_data='uz')
    lang_buttons.add(lang_buttons_1, lang_buttons_2)

    bot.send_message(message.chat.id, 'Пожалуйста выберите язык', reply_markup=lang_buttons)


@bot.callback_query_handler(func=lambda call: True)
def inline(call):
    global lang
    if call.data == 'rus':
        lang = call.data
    elif call.data == 'uz':
        lang = call.data




if __name__ == "__main__":
    bot.polling()