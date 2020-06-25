import telebot
import time

bot = telebot.TeleBot(token='1018761895:AAE9zGMHZxYZlC_6kyRLAmTBC0Oubpp-QUQ')
keyword = telebot.types.ReplyKeyboardMarkup(True, True, True)
keyword.row('Yes', 'No')

@bot.message_handler(commands=['start'])
def send_welome(message):
    bot.send_message(message.chat.id, 'Are you happy?', reply_markup=keyword)


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text == 'Yes':
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAL5IV70q_zT7PexzhgRZQ7FlE45maLjAAKLVAACns4LAAGK48iBX6K11xoE')
    elif message.text == 'No':
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAL5F170ikq3SsPNjqA4Y4eIyIyYIxgoAAJwVAACns4LAAEK62yG_OKNQxoE")
    else:
        bot.send_message(message.chat.id, "I don't understant you ser! 🥺")


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text == 'Yes':
        bot.send_message(message.chat.id, 'Suka blyad')
    elif message.text == 'No':
        bot.send_message(message.chat.id, "Pidr")



@bot.message_handler(commands=['clear'])
def clear(message):
    pass

if __name__ == '__main__':
    bot.polling()
