import telebot

#token
API_TOKEN = '1018761895:AAE9zGMHZxYZlC_6kyRLAmTBC0Oubpp-QUQ'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(content_types=['text'])
def after_start(message):
    if message.text == 'sex':
        bot.send_message(message.chat.id, message)

if __name__ == "__main__":
    bot.polling()
