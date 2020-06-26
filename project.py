import telebot

token = '1018761895:AAE9zGMHZxYZlC_6kyRLAmTBC0Oubpp-QUQ'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def running(message):
    bot.send_message(message.chat.id, 'Please send me some kind of file')

@bot.message_handler(content_types=['photo'])
def pho(message):
    a = []
    # ass = message.text.get_id
    for i in message.photo:
        a.append(i)
    bot.send_message(message.chat.id, a[2].file_id)


@bot.message_handler(content_types=['video'])
def pho(message):
    # a = []
    # for i in message.photo:
    #     a.append(i)
    a = message.video
    print(a)
    bot.send_video(message.chat.id, 'BAACAgIAAxkBAAIB6V72M7Q6uDSUL4J-R2ADsjq8Xb6BAALVCAAC5lEoS5Uq6-79GVU6GgQ')

@bot.message_handler(content_types=['document', 'audio', 'sticker', 'video', 'voice', 'location'])
def doc_id(message):
    id = "I don't understand"
    ids = [message.document, message.audio, message.sticker, message.video, message.voice, message.location]

    for code in ids:
        try:
            code.file_id
        except AttributeError:
            pass
        else:
            id = code

    bot.send_message(message.chat.id, id.file_id)

if __name__ == '__main__':
    bot.polling()