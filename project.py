import telebot
import time

bot = telebot.TeleBot('1018761895:AAE9zGMHZxYZlC_6kyRLAmTBC0Oubpp-QUQ')
key_yn = telebot.types.ReplyKeyboardMarkup(True, True)
key_yn.row('Yes', 'No')

key_loop = telebot.types.ReplyKeyboardMarkup(True, True, True)
key_loop.row("Yes ofcourse", 'No no')

@bot.message_handler(commands=['start'])
def com_start(message):
    bot.send_message(message.chat.id, 'Are you happy?', reply_markup=key_yn)


@bot.message_handler(commands=['loop'])
def loop(message):
    bot.send_message(message.chat.id, 'Do you want sex?', reply_markup=key_loop)


@bot.message_handler(commands=['inline'])
def inline(message):
    inline_keyboard = telebot.types.InlineKeyboardMarkup()
    inline_keyboard.add(telebot.types.InlineKeyboardButton('Sex', callback_data='sex_id'))
    inline_keyboard.add(telebot.types.InlineKeyboardButton('Drugs', callback_data='drug_id'))
    inline_keyboard.add(telebot.types.InlineKeyboardButton('Hacking', callback_data='hack_id'))

    bot.send_message(message.chat.id, 'What do you want?', reply_markup=inline_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    bot.answer_callback_query(callback_query_id=call.id, )

    if call.data == 'sex_id':
        answer =




@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text == 'Yes':
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAL5IV70q_zT7PexzhgRZQ7FlE45maLjAAKLVAACns4LAAGK48iBX6K11xoE')
    elif message.text == 'No':
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAL5F170ikq3SsPNjqA4Y4eIyIyYIxgoAAJwVAACns4LAAEK62yG_OKNQxoE')
    elif message.text == 'Yes ofcourse':
        bot.send_sticker(message.chat.id, 'CAACAgQAAxkBAAL5rV71vND7-NPqzB-IUQMe9srSHGujAALyBAAC8yghBN2xztTxPWqOGgQ')
    elif message.text == 'No no':
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAL5sV71vSz6UdfzNrRgbCQI8OlC9s4jAAJBAANEDc8XctX78YrX-ZQaBA')



if __name__ == '__main__':
    bot.polling()