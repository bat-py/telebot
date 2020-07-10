# -*- coding: utf-8 -*-
import telebot
import json
from sql import MemberInfo
import random
import time

#token
token = '1018761895:AAE9zGMHZxYZlC_6kyRLAmTBC0Oubpp-QUQ'
bot = telebot.TeleBot(token)

### KEYBOARDS ###
#Reply_Keyboard_Creator
def reply_keyboard_creator(message, *args: list, one_type_keyboard: bool = None,):   # каждый элемент args это одна строка: [], [], [] - создается 3 строки и каждые элементы этих трех массивов станут как кнопка
    lang = template[MemberInfo(message.chat.id).get_lang()]
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_type_keyboard)            # каждый массив должен содержать ключи из template
    for arg in args:
        row_bottons = []
        for a in arg:
                row_bottons.append(lang[a])
        keyboard.row(*row_bottons)

    return keyboard
#Inline_keyboard_Creator
def inline_keyboard_creator(message, *args):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    keyboard = telebot.types.InlineKeyboardMarkup()
    for arg in args:
        row_buttons = []
        for a in arg:
            row_buttons.append(telebot.types.InlineKeyboardButton(lang[a], callback_data=a))
        keyboard.row(*row_buttons)
    return keyboard


### КНОПКИ ГЛАВНОГО МЕНЮ ###
#Main_menu keyboard
def main_keyboard(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    keyboard = reply_keyboard_creator(message, ['uzcard to qiwi'], ['qiwi to uzcard'], ['requisites' , 'rate'], one_type_keyboard=True)
    bot.send_message(message.chat.id, lang['main_menu'], reply_markup=keyboard, parse_mode='html')
#Кнопка: Отдать с Uzcard и получать на Qiwi
def uzcard_to_qiwi(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    data = MemberInfo(message.chat.id)
    if check_exist_uzcard_qiwi(message):
        check_id_application(message)
        msg = f"{lang['application']}\n🆔: <i>{data.get_id_working_application()[0]}</i>\n\n{lang['from']}  UzCard\n{lang['to']}  Qiwi RUB\n\nUzCard:  <i>{data.get_nice_uzcard()}</i>\nQiwi:  <i>+{data.get_nice_qiwi()}</i>"
        key = inline_keyboard_creator(message, ['uzcard_to_qiwi_from_uzcard'], ['uzcard_to_qiwi_from_qiwi'], ['cancel'])
        bot.send_message(message.chat.id, msg, reply_markup=key, parse_mode='html')
#Кнопка: Отдать с Qiwi и получать на Uzcard
def qiwi_to_uzcard(message):

    lang = template[MemberInfo(message.chat.id).get_lang()]
    data = MemberInfo(message.chat.id)
    if check_exist_uzcard_qiwi(message):
        check_id_application(message)
        msg = f"{lang['application']}\n🆔: <i>{data.get_id_working_application()[0]}</i>\n\n{lang['from']} Qiwi RUB\n{lang['to']} UzCard\n\nQiwi:  <i>+{data.get_nice_qiwi()}</i>\nUZCard:  <i>{data.get_nice_uzcard()}</i>"
        key = inline_keyboard_creator(message, ['qiwi_to_uzcard_from_qiwi'],['qiwi_to_uzcard_from_uzcard'], ['cancel'])
        bot.send_message(message.chat.id, msg, reply_markup=key, parse_mode='html')
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

    uzcard = MemberInfo(message.chat.id).get_nice_uzcard() if MemberInfo(message.chat.id).get_nice_uzcard() != None  else lang['empty']
    qiwi = MemberInfo(message.chat.id).get_nice_qiwi() if MemberInfo(message.chat.id).get_qiwi() != None  else lang['empty']

    msg = f'UzCard:<i>\n{uzcard}</i>\n\nQiwi:\n<i>{plus}{qiwi}</i>'
    bot.send_message(message.chat.id, lang['msg_into_requisites'], reply_markup=reply_key, parse_mode='html')
    bot.send_message(message.chat.id, msg, reply_markup=inline_key, parse_mode='html')
#Кнопка: Курс
def rate(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    key = inline_keyboard_creator(message, ['main_menu'])
    msg = f"{lang['selling_rate']}\n1 Qiwi RUB = <u>{rates[0]} UZS</u>\n\n{lang['buying_rate']}\n1 Qiwi RUB = <u>{rates[1]} UZS</u>"
    bot.send_message(message.chat.id, msg, reply_markup=key, parse_mode='html')


### Other functions ###
def after_plus_uzcard(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    key = inline_keyboard_creator(message, ['cancel'])
    if message.text.strip().isdigit() and len(message.text.strip()) == 16:
        MemberInfo(message.chat.id, uzcard=message.text.strip()).add_uzcard()
        key = inline_keyboard_creator(message, ['main_menu', 'add_more'])
        bot.send_message(message.chat.id, lang['succes_uzcard'], reply_markup=key)
    elif  message.text.strip().isdigit() and len(message.text.strip()) != 16:
        msg = bot.send_message(message.chat.id, lang['error_uzcard_count_num'], reply_markup=key, parse_mode='html')
        bot.register_next_step_handler(msg, after_plus_uzcard)
    else:
        msg = bot.send_message(message.chat.id, lang['error_num_uzcard'], reply_markup=key, parse_mode='html')
        bot.register_next_step_handler(msg, after_plus_uzcard)
def after_plus_qiwi(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    key = inline_keyboard_creator(message, ['cancel'])
    if message.text.strip().isdigit() and len(message.text.strip()) == 12:
        MemberInfo(message.chat.id, qiwi=message.text.strip()).add_qiwi()
        key = inline_keyboard_creator(message, ['main_menu', 'add_more'])
        bot.send_message(message.chat.id, lang['succes_qiwi'], reply_markup=key)
    elif message.text.startswith('+') and message.text[1:].strip().isdigit() and len(message.text[1:].strip()) == 12:
        MemberInfo(message.chat.id, qiwi=message.text.strip()[1:]).add_qiwi()
        key = inline_keyboard_creator(message, ['main_menu'])
        bot.send_message(message.chat.id, lang['succes_qiwi'], reply_markup=key)
    elif message.text.strip().isdigit() and len(message.text.strip()) != 12:
        msg = bot.send_message(message.chat.id, lang['error_qiwi_count_num'], reply_markup=key, parse_mode='html')
        bot.register_next_step_handler(msg, after_plus_qiwi)
    elif message.text.startswith('+') and message.text[1:].strip().isdigit() and len(message.text[1:].strip()) != 12:
        msg = bot.send_message(message.chat.id, lang['error_qiwi_count_num'], reply_markup=key, parse_mode='html')
        bot.register_next_step_handler(msg, after_plus_qiwi)
    else:
        msg = bot.send_message(message.chat.id, lang['error_num_qiwi'], reply_markup=key, parse_mode='html')
        bot.register_next_step_handler(msg, after_plus_qiwi)
def check_exist_uzcard_qiwi(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    if MemberInfo(message.chat.id).get_uzcard() and MemberInfo(message.chat.id).get_qiwi():
        return True
    elif MemberInfo(message.chat.id).get_uzcard() and not MemberInfo(message.chat.id).get_qiwi():
        key = inline_keyboard_creator(message, ['add_qiwi'])
        bot.send_message(message.chat.id, lang['doesnt_exist_qiwi'], reply_markup=key)
        return False
    elif not MemberInfo(message.chat.id).get_uzcard() and MemberInfo(message.chat.id).get_qiwi():
        key = inline_keyboard_creator(message, ['add_uzcard'])
        bot.send_message(message.chat.id, lang['doesnt_exist_uzcard'], reply_markup=key)
        return False
    else:
        key = inline_keyboard_creator(message, ['add_all'])
        bot.send_message(message.chat.id, lang['doesnt_exist_all'], reply_markup=key)
        return False
def check_id_application(message):
    id_working_application = MemberInfo(message.chat.id).get_id_working_application()
    if not id_working_application:
        id_application = random.randint(100000, 999999)
        check_exist = MemberInfo(message.chat.id, id_application=id_application).get_id_application()
        if not check_exist:
            MemberInfo(message.chat.id, id_application=id_application).add_working_application()
        else:
            check_id_application(message)
def uzcard_to_qiwi_check_sum(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    key = inline_keyboard_creator(message, ['pay_cancel'])
    if message.text.strip().isdigit() and 15000 <= int(message.text.strip()) and int(message.text.strip()) <= 1000000:
        sum = int(message.text)
        rubl = round(sum/float(rates[0]), 1)
        data = MemberInfo(message.chat.id, rubl=rubl, sum=sum)
        data.add_summa_rubl_uzs()
        return True
    elif message.text.strip().isdigit() and int(message.text.strip()) < 15000:
        msg = bot.send_message(message.chat.id, lang['min_sum_error'], reply_markup=key, parse_mode='html')
        bot.register_next_step_handler(msg, after_uzcard_to_qiwi_from_uzcard)
    elif message.text.strip().isdigit() and int(message.text.strip()) > 1000000:
        msg =bot.send_message(message.chat.id, lang['max_sum_error'], reply_markup=key, parse_mode='html')
        bot.register_next_step_handler(msg, after_uzcard_to_qiwi_from_uzcard)
    else:
        msg = bot.send_message(message.chat.id, lang['sum_error'], reply_markup=key, parse_mode='html')
        bot.register_next_step_handler(msg, after_uzcard_to_qiwi_from_uzcard)
def uzcard_to_qiwi_check_rubl(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    key = inline_keyboard_creator(message, ['pay_cancel'])
    if message.text.strip().isdigit() and 100 <= float(message.text.strip()) and  float(message.text.strip())  <= 7000:
        rubl = float(message.text)
        sum = round(rubl*float(rates[0]), 1)
        data = MemberInfo(message.chat.id, rubl=rubl, sum=sum)
        data.add_summa_rubl_uzs()
        return True
    elif message.text.strip().isdigit() and float(message.text.strip()) < 100:
        msg = bot.send_message(message.chat.id, lang['min_rubl_error'], reply_markup=key, parse_mode='html')
        bot.register_next_step_handler(msg, after_uzcard_to_qiwi_from_qiwi)
    elif message.text.strip().isdigit() and float(message.text.strip()) > 7000:
        msg =bot.send_message(message.chat.id, lang['max_rubl_error'], reply_markup=key, parse_mode='html')
        bot.register_next_step_handler(msg, after_uzcard_to_qiwi_from_qiwi)
    else:
        msg = bot.send_message(message.chat.id, lang['rubl_error'], reply_markup=key, parse_mode='html')
        bot.register_next_step_handler(msg, after_uzcard_to_qiwi_from_qiwi)
def qiwi_to_uzcard_check_sum(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    key = inline_keyboard_creator(message, ['pay_cancel'])
    if message.text.strip().isdigit() and 15000 <= int(message.text.strip()) and int(message.text.strip()) <= 1000000:
        sum = int(message.text)
        rubl = round(sum/float(rates[1]), 1)
        data = MemberInfo(message.chat.id, rubl=rubl, sum=sum)
        data.add_summa_rubl_uzs()
        return True
    elif message.text.strip().isdigit() and int(message.text.strip()) < 15000:
        msg = bot.send_message(message.chat.id, lang['min_sum_error'], reply_markup=key, parse_mode='html')
        bot.register_next_step_handler(msg, after_qiwi_to_uzcard_from_uzcard)
    elif message.text.strip().isdigit() and int(message.text.strip()) > 1000000:
        msg =bot.send_message(message.chat.id, lang['max_sum_error'], reply_markup=key, parse_mode='html')
        bot.register_next_step_handler(msg, after_qiwi_to_uzcard_from_qiwi_uzcard)
    else:
        msg = bot.send_message(message.chat.id, lang['sum_error'], reply_markup=key, parse_mode='html')
        bot.register_next_step_handler(msg, after_qiwi_to_uzcard_from_qiwi_uzcard)
def qiwi_to_uzcard_check_rubl(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    key = inline_keyboard_creator(message, ['pay_cancel'])
    if message.text.strip().isdigit() and 100 <= float(message.text.strip()) and  float(message.text.strip())  <= 7000:
        rubl = float(message.text)
        sum = round(rubl*float(rates[1]), 1)
        data = MemberInfo(message.chat.id, rubl=rubl, sum=sum)
        data.add_summa_rubl_uzs()
        return True
    elif message.text.strip().isdigit() and float(message.text.strip()) < 100:
        msg = bot.send_message(message.chat.id, lang['min_rubl_error'], reply_markup=key, parse_mode='html')
        bot.register_next_step_handler(msg, after_qiwi_to_uzcard_from_qiwi)
    elif message.text.strip().isdigit() and float(message.text.strip()) > 7000:
        msg =bot.send_message(message.chat.id, lang['max_rubl_error'], reply_markup=key, parse_mode='html')
        bot.register_next_step_handler(msg, after_qiwi_to_uzcard_from_qiwi)
    else:
        msg = bot.send_message(message.chat.id, lang['rubl_error'], reply_markup=key, parse_mode='html')
        bot.register_next_step_handler(msg, after_qiwi_to_uzcard_from_qiwi)

### Money-Change functions ###
#Отдать с Uzcard и получать на Qiwi ->  Отдать * сум с UzCard
def uzcard_to_qiwi_from_uzcard(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    key = inline_keyboard_creator(message, ['pay_cancel'])
    msg = f"{lang['after_uzcard_to_qiwi_from_uzcard']}\n{lang['min']}  <u>15.000 UZS</u>\n{lang['max']}  <u>1.000.000 UZS</u>"
    ms = bot.send_message(message.chat.id, msg, reply_markup=key, parse_mode='html')
    bot.register_next_step_handler(ms, after_uzcard_to_qiwi_from_uzcard)
def after_uzcard_to_qiwi_from_uzcard(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    if uzcard_to_qiwi_check_sum(message):
        data = MemberInfo(message.chat.id, type='uzcard_to_qiwi')
        data.add_type_change()
        msg = f"{lang['application']}\n🆔: <i>{data.get_id_working_application()[0]}</i>\n\n{lang['from']}  <u>{int(data.get_summa_uzs_rubl()[0])} UZS</u>\n{lang['to']}  <u>{data.get_summa_uzs_rubl()[1]} RUB</u>\n\nUzCard: <i>{data.get_nice_uzcard()}</i>\nQiwi: <i>+{data.get_nice_qiwi()}</i>"
        key = inline_keyboard_creator(message, ['pay'], ['pay_cancel'])
        bot.send_message(message.chat.id, msg, reply_markup=key, parse_mode='html')

#Отдать с Uzcard и получать на Qiwi ->  Получить * рублей на Qiwi
def uzcard_to_qiwi_from_qiwi(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    key = inline_keyboard_creator(message, ['pay_cancel'])
    msg = f"{lang['after_uzcard_to_qiwi_from_qiwi']}\n{lang['min']}  <u>100 RUB</u>\n{lang['max']}  <u>7.000 RUB</u>"
    ms = bot.send_message(message.chat.id, msg, reply_markup=key, parse_mode='html')
    bot.register_next_step_handler(ms, after_uzcard_to_qiwi_from_qiwi)
def after_uzcard_to_qiwi_from_qiwi(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    if uzcard_to_qiwi_check_rubl(message):
        data = MemberInfo(message.chat.id, type='uzcard_to_qiwi')
        data.add_type_change()
        msg = f"{lang['application']}\n🆔: <i>{data.get_id_working_application()[0]}</i>\n\n{lang['from']}  <u>{data.get_summa_uzs_rubl()[0]} UZS</u>\n{lang['to']}  <u>{data.get_summa_uzs_rubl()[1]} RUB</u>\n\nUzCard: <i>{data.get_nice_uzcard()}</i>\nQiwi: <i>+{data.get_nice_qiwi()}</i>"
        key = inline_keyboard_creator(message, ['pay'], ['pay_cancel'])
        bot.send_message(message.chat.id, msg, reply_markup=key, parse_mode='html')
#Отдать с Qiwi и получать на Uzcard -> Отдать * рублей с Qiwi
def qiwi_to_uzcard_from_qiwi(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    key = inline_keyboard_creator(message, ['pay_cancel'])
    msg = f"{lang['after_qiwi_to_uzcard_from_qiwi']}\n{lang['min']}  <u>100 RUB</u>\n{lang['max']}  <u>7.000 RUB</u>"
    ms = bot.send_message(message.chat.id, msg, reply_markup=key, parse_mode='html')
    bot.register_next_step_handler(ms, after_qiwi_to_uzcard_from_qiwi)
def after_qiwi_to_uzcard_from_qiwi(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    if qiwi_to_uzcard_check_rubl(message):
        data = MemberInfo(message.chat.id, type='qiwi_to_uzcard')
        data.add_type_change()
        msg = f"{lang['application']}\n🆔: <i>{data.get_id_working_application()[0]}</i>\n\n{lang['from']} <u>{data.get_summa_uzs_rubl()[1]} RUB</u>\n{lang['to']} <u>{data.get_summa_uzs_rubl()[0]} UZS</u>\n\nUzCard: <i>{data.get_nice_uzcard()}</i>\nQiwi: <i>+{data.get_nice_qiwi()}</i>"
        key = inline_keyboard_creator(message, ['pay'], ['pay_cancel'])
        bot.send_message(message.chat.id, msg, reply_markup=key, parse_mode='html')
#Отдать с Qiwi и получать на Uzcard -> Получить * рублей на Qiwi
def qiwi_to_uzcard_from_uzcard(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    key = inline_keyboard_creator(message, ['pay_cancel'])
    msg = f"{lang['after_qiwi_to_uzcard_from_uzcard']}\n{lang['min']}  <u>15.000 UZS</u>\n{lang['max']}  <u>1.000.000 UZS</u>"
    ms = bot.send_message(message.chat.id, msg, reply_markup=key, parse_mode='html')
    bot.register_next_step_handler(ms, after_qiwi_to_uzcard_from_uzcard)
def after_qiwi_to_uzcard_from_uzcard(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    if qiwi_to_uzcard_check_sum(message):
        data = MemberInfo(message.chat.id, type='qiwi_to_uzcard')
        data.add_type_change()
        msg = f"{lang['application']}\n🆔: <i>{data.get_id_working_application()[0]}</i>\n\n{lang['from']} <u>{data.get_summa_uzs_rubl()[1]} RUB</u>\n{lang['to']} <u>{data.get_summa_uzs_rubl()[0]} UZS</u>\n\nUzCard: <i>{data.get_nice_uzcard()}</i>\nQiwi: <i>+{data.get_nice_qiwi()}</i>"
        key = inline_keyboard_creator(message, ['pay'], ['pay_cancel'])
        bot.send_message(message.chat.id, msg, reply_markup=key, parse_mode='html')

#PAY
def pay(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    data = MemberInfo(message.chat.id)
    type = data.get_type_change()
    summa = data.get_summa_uzs_rubl()
    key = inline_keyboard_creator(message, ['payed'])

    if type == 'uzcard_to_qiwi':
        msg = lang['uzcard_to_qiwi_pay'].replace('&sum', f"<u>{str(summa[0])}</u>").replace('&uzcard', f"<code> {lang['my_uzcard']}</code>")
        bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=key)
    elif type == 'qiwi_to_uzcard':
        msg = lang['qiwi_to_uzcard_pay'].replace('&rub', f"<u>{str(summa[1])}</u>").replace('&qiwi', f"<code> {lang['my_qiwi']}</code>")
        bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=key)

#PAYED
def payed(message):
    lang = template[MemberInfo(message.chat.id).get_lang()]
    data = MemberInfo(message.chat.id)
    key = reply_keyboard_creator(message, ['main_menu'])
    bot.send_message(message.chat.id, f"🆔: {data.get_id_working_application()[0]}\n\n{lang['after_payed']}", reply_markup=key)


    data = MemberInfo(message.chat.id).get_working_applications()
    MemberInfo(message.chat.id).del_working_applications()
    times = time.asctime()
    if  data[4] == "uzcard_to_qiwi":
        kurs = float(rates[0])
    elif data[4] == "qiwi_to_uzcard":
        kurs = float(rates[1])
    else:
        kurs = "Error"

    datas = MemberInfo(message.chat.id, id_application=data[0], rubl=data[2], sum=data[3], type=data[4], time=times, kurs=kurs)
    datas.close_application()
#Отправка заявка на админ:
    keya = inline_keyboard_creator(message, ['del_working_application_on_admin'])
    if data[4] == "uzcard_to_qiwi":
        msg = f"🆔: {data[0]}\n\nКлиент отправил деньги с UzCard карты:\n<i>{datas.get_nice_uzcard()}</i>\nСумма отправки:  <u>{data[3]} UZS</u>\n\nТы должен отправить на кошелек:\n<code>{datas.get_qiwi()}</code>\nСумма отправки:\n<code>{data[2]}</code> RUB"
    elif data[4] == "qiwi_to_uzcard":
        msg = f"🆔: {data[0]}\n\nКлинет отравил деньги с Qiwi кошелька:\n<i>{datas.get_qiwi()}</i>\nСумма отправки:\n{data[2]} RUB\n\nТы должен отправить на карту:\n<code>{datas.get_uzcard()}</code>\nСумма отправки:\n<code>{data[3]}</code> UZS"

    bot.send_message(lang['my_chat_id'], msg, reply_markup=keya, parse_mode='html')



#START
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

#CALLBACK HANDLER
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
    elif call.data == 'add_all' or call.data == 'add_uzcard' or call.data == 'add_qiwi':
        requisites(call.message)
    elif call.data == 'add_more':
        requisites(call.message)
    elif call.data == 'cancel':
        bot.clear_step_handler_by_chat_id(call.message.chat.id)
        main_keyboard(call.message)
    elif call.data == "pay_cancel":
        bot.clear_step_handler_by_chat_id(call.message.chat.id)
        main_keyboard(call.message)
    elif call.data == "uzcard_to_qiwi_from_uzcard":
        uzcard_to_qiwi_from_uzcard(call.message)
    elif call.data == "uzcard_to_qiwi_from_qiwi":
        uzcard_to_qiwi_from_qiwi(call.message)
    elif call.data == "qiwi_to_uzcard_from_qiwi":
        qiwi_to_uzcard_from_qiwi(call.message)
    elif call.data == "qiwi_to_uzcard_from_uzcard":
        qiwi_to_uzcard_from_uzcard(call.message)
    elif call.data == "pay":
        pay(call.message)
    elif call.data == "payed":
        payed(call.message)

#TEXT handler
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
        key = inline_keyboard_creator(message, ['cancel'])
        msg = bot.send_message(message.chat.id,  lang['after_plus_uzcard'], reply_markup=key, parse_mode='html')
        bot.register_next_step_handler(msg, after_plus_uzcard)
    elif message.text == lang['plus_qiwi'] or message.text == lang['edit_qiwi']:
        key = inline_keyboard_creator(message, ['cancel'])
        msg = bot.send_message(message.chat.id, lang['after_plus_qiwi'], reply_markup=key, parse_mode='html')
        bot.register_next_step_handler(msg, after_plus_qiwi)

if __name__ == "__main__":
    with open('/home/batpy/telebot/template.json', 'r', encoding='utf-8') as w:
        template = json.load(w)
    with open('/home/batpy/PycharmProjects/telebot/rate.json', 'r', encoding='utf-8') as w:
        rates = json.load(w)
    bot.polling()
