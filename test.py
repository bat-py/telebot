import sql
# import telebot
#
# #token
# token = '1018761895:AAE9zGMHZxYZlC_6kyRLAmTBC0Oubpp-QUQ'
# bot = telebot.TeleBot(token)
#
# @bot.message_handler(commands=['start'])
# def after_start(message):
#     keyboard = telebot.types.ReplyKeyboardMarkup(True, row_width=2, one_time_keyboard=True)
#     button_contact = telebot.types.KeyboardButton(text='Отправить контакт', request_location=True)
#     keyboard.add(button_contact)
#     msg = bot.send_message(message.chat.id, 'Пожалуйста отправить номер телефона', reply_markup=keyboard)
#     bot.register_next_step_handler(msg, after_contact)
#
# def after_contact(message):
#     bot.send_message(message.chat.id, message.location)
#
# @bot.message_handler(content_types=['text'])
# def msg_handler(message):
#     if message.text == 'Пожалуйста отправить номер телефона':
#         bot.send_message(message.chat.id, message)
#
#
#
# if __name__ == "__main__":
#     bot.polling()

print(sql.MemberInfo(212345, id_application=123456).get_id_application())
