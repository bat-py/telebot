import telebot
import time
from sql import MemberInfo
from template import template

#token
token = '1018761895:AAE9zGMHZxYZlC_6kyRLAmTBC0Oubpp-QUQ'
bot = telebot.TeleBot(token)


#Reply_Keyboard_Creator
def reply_keyboard_creator(message, *args: list, one_type_keyboard: bool = None,):   # каждый элемент args это одна строка: [], [], [] - создается 3 строки и каждые элементы этих трех массивов станут как кнопка
    keyboard = telebot.types.ReplyKeyboardMarkup(True, one_type_keyboard)            # каждый массив должен содержать ключи из template
    for arg in args:
        row_bottons = []
        for a in arg:
                row_bottons.append(leng[a])
        keyboard.row(*row_bottons)

    return keyboard

#Inline_keyboard_Creator
def inline_keyboard_creator(message, *args):
    pass


@bot.message_handler(commands=['start'])
def after_start(message):
    mem = MemberInfo(message.chat.id, first_name=message.chat.first_name, username=message.chat.username)
    try:
        mem.add_id()
    except:
        pass
    mem.add_first_name()
    mem.add_username()

    # #language buttons:
    lang_buttons = telebot.types.InlineKeyboardMarkup()
    lang_buttons_1 = telebot.types.InlineKeyboardButton('Русский 🇷🇺', callback_data='rus1')
    lang_buttons_2 = telebot.types.InlineKeyboardButton('O\'zbekcha 🇺🇿', callback_data='uz1')
    lang_buttons.row(lang_buttons_1, lang_buttons_2)
    msg = bot.send_message(message.chat.id, 'Пожалуйста выберите язык', reply_markup=lang_buttons)

@bot.callback_query_handler(func=lambda call: True)
def choice(call):
    # bot.send_message(call.message.chat.id, call)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data == 'rus1':
        MemberInfo(id=call.message.chat.id, lang='rus').add_language()
        main_keyboard(call.message)
    elif call.data == 'uz1':
        MemberInfo(id=call.message.chat.id, lang='uz').add_language()
        main_keyboard(call.message)


def main_keyboard(message):
    global leng                # после leng просто выберишь какой-то ключ из template: leng.mgs
    leng = template[MemberInfo(message.chat.id).get_lang()]
    keyboard = reply_keyboard_creator(message, ['uzcard to qiwi'], ['qiwi to uzcard' ], ['requisites' , 'rate'])
    bot.send_message(message.chat.id, leng['msg'], reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    if message.text == lang['uzcard to qiwi']:
        uzcard_to_qiwi(message)
    elif message.text == lang:
        pass



def uzcard_to_qiwi(message):
    pass






if __name__ == "__main__":
    bot.polling()