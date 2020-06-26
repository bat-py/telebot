import telebot

token = '1018761895:AAE9zGMHZxYZlC_6kyRLAmTBC0Oubpp-QUQ'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def running(message):
    bot.send_message(message.chat.id, 'Please send me some kind of file')

@bot.message_handler(content_types=['photo'])
def pho(message):
    a = []
    for i in message.photo:
        a.append(i)

    size = str(round(float(a[2].file_size/1000), 1))
    bot.send_message(message.chat.id, 'File ID:\n'+a[2].file_id+'\n\nFile size:\n'+size+' kb')


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

    size = str(round(float(id.file_size/1000), 1))
    bot.send_message(message.chat.id, 'File ID:\n'+id.file_id+'\n\nFile size:\n'+size+' kb')

if __name__ == '__main__':
    bot.polling()