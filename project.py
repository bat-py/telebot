import telebot
import time
from sql import MemberInfo
from template import template

#token
token = '1018761895:AAE9zGMHZxYZlC_6kyRLAmTBC0Oubpp-QUQ'
bot = telebot.TeleBot(token)


#Reply_Keyboard_Creator
def reply_keyboard_creator(message, *args: list, one_type_keyboard: bool = None,):   # каждый элемент args это одна строка: [], [], [] - создается 3 строки и каждые элементы этих трех массивов станут как кнопка
    lang = template[MemberInfo(message.chat.id).get_lang()]
    keyboard = telebot.types.ReplyKeyboardMarkup(True, one_type_keyboard)            # каждый массив должен содержать ключи из template
    for arg in args:
        row_bottons = []
        for a in arg:
                row_bottons.append(lang[a])
        keyboard.row(*row_bottons)

    return keyboard

#Inline_keyboard_Creator                       (вместо args должен передовать только ключи из template. Например: ['main_menu'],['del_uzcard', 'del_qiwi']
def inline_keyboard_creator(message, *args):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    keyboard = telebot.types.InlineKeyboardMarkup()
    for arg in args:
        row_buttons = []
        for a in arg:
            row_buttons.append(telebot.types.InlineKeyboardButton(lang[a], callback_data=a))
        keyboard.row(*row_buttons)
    return keyboard



#Main_menu keyboard
def main_keyboard(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    keyboard = reply_keyboard_creator(message, ['uzcard to qiwi'], ['qiwi to uzcard'], ['requisites' , 'rate'])
    bot.send_message(message.chat.id, lang['main_menu'], reply_markup=keyboard)

#Кнопка:
def uzcard_to_qiwi(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    pass

#Кнопка:
def qiwi_to_uzcard(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    pass

#Кнопка: адреса моих кошельков
def requisites(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    if not MemberInfo(message.chat.id).get_uzcard():
        uzcard = 'plus_uzcard'
    else:
        uzcard = 'edit_uzcard'

    plus = ''
    if not MemberInfo(message.chat.id).get_qiwi():
        qiwi = 'plus_qiwi'
    else:
        qiwi = 'edit_qiwi'
        plus = '+'

    reply_key = reply_keyboard_creator(message, [uzcard, qiwi], ['main_menu'], one_type_keyboard=True )
    inline_key = inline_keyboard_creator(message, ['del_data'])

    uzcard = MemberInfo(message.chat.id).get_uzcard() if MemberInfo(message.chat.id).get_uzcard() != None  else lang['empty']
    qiwi = MemberInfo(message.chat.id).get_qiwi() if MemberInfo(message.chat.id).get_qiwi() != None  else lang['empty']

    msg = f'UzCard:\n{uzcard}\n\nQiwi:\n{plus}{qiwi}'
    bot.send_message(message.chat.id, lang['msg_into_requisites'], reply_markup=reply_key)
    bot.send_message(message.chat.id, msg, reply_markup=inline_key)

#Кнопка: Курс
def rate(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    pass



#Other functions
def after_plus_uzcard(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    if message.text.strip().isdigit() and len(message.text.strip()) == 16:
        MemberInfo(message.chat.id, uzcard=message.text.strip()).add_uzcard()
        key = inline_keyboard_creator(message, ['main_menu'])
        bot.send_message(message.chat.id, lang['succes_uzcard'], reply_markup=key)

    elif  message.text.strip().isdigit() and len(message.text.strip()) != 16:
        msg = bot.send_message(message.chat.id, lang['error_uzcard_count_num'])
        bot.register_next_step_handler(msg, after_plus_uzcard)
    else:
        msg = bot.send_message(message.chat.id, lang['error_num'])
        bot.register_next_step_handler(msg, after_plus_uzcard)

def after_plus_qiwi(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    if message.text.strip().isdigit() and len(message.text.strip()) == 12:
        MemberInfo(message.chat.id, qiwi=message.text.strip()).add_qiwi()
        key = inline_keyboard_creator(message, ['main_menu'])
        bot.send_message(message.chat.id, lang['succes_qiwi'], reply_markup=key)
    elif message.text.startswith('+') and message.text[1:].strip().isdigit() and len(message.text[1:].strip()) == 12:
        MemberInfo(message.chat.id, qiwi=message.text.strip()[1:]).add_qiwi()
        key = inline_keyboard_creator(message, ['main_menu'])
        bot.send_message(message.chat.id, lang['succes_qiwi'], reply_markup=key)
    else:
        msg = bot.send_message(message.chat.id, lang['error_num'])
        bot.register_next_step_handler(msg, after_plus_qiwi)





#Handler start
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


#handler callback
@bot.callback_query_handler(func=lambda call: True)
def choice(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data == 'rus1':
        MemberInfo(id=call.message.chat.id, lang='rus').add_language()
        bot.answer_callback_query(call.id, 'Вы выбрали русский язык')
        main_keyboard(call.message)
    elif call.data == 'uz1':
        MemberInfo(id=call.message.chat.id, lang='uz').add_language()
        bot.answer_callback_query(call.id, "Siz o'zbek tilini tanladingiz")
        main_keyboard(call.message)
    elif call.data == 'main_menu':
        main_keyboard(call.message)
    elif call.data == 'del_data':
        lang = template[MemberInfo(call.message.chat.id).get_lang()]
        MemberInfo(call.message.chat.id).del_uzcard_qiwi()
        bot.answer_callback_query(call.id, lang['after_del'])
        requisites(call.message)




#Handler text
@bot.message_handler(content_types=['text'])
def text_handler(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    if message.text == lang['uzcard to qiwi']:
        uzcard_to_qiwi(message)
    elif message.text == lang['qiwi to uzcard']:
        qiwi_to_uzcard(message)
    elif message.text == lang['requisites']:
        requisites(message)
    elif message.text == lang['rate']:
        rate(message)
    elif message.text == lang['main_menu']:
        main_keyboard(message)
    elif message.text == lang['plus_uzcard'] or message.text == lang['edit_uzcard']:
        msg = bot.send_message(message.chat.id,  lang['after_plus_uzcard'])
        bot.register_next_step_handler(msg, after_plus_uzcard)
    elif message.text == lang['plus_qiwi'] or message.text == lang['edit_uzcard']:
        msg = bot.send_message(message.chat.id, lang['after_plus_qiwi'])
        bot.register_next_step_handler(msg, after_plus_qiwi)






if __name__ == "__main__":
    bot.polling()
