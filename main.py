import telebot
from telebot import types
import google_table
import buttons
bot = telebot.TeleBot('')
dict_update ={}
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_job = types.KeyboardButton('Начать заполнение')
    markup.add(start_job)
    mesg = bot.send_message(message.chat.id, 'Начало работы', reply_markup=markup)
@bot.message_handler(commands=['сбросить'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_job = types.KeyboardButton('Начать заполнение')
    markup.add(start_job)
    mesg = bot.send_message(message.chat.id, 'Начало работы', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "Начать заполнение"):
        mesg = bot.send_message(message.chat.id, 'Выберите РП объекта',reply_markup=buttons.new_markup_RP(google_table.get_value_RP()))
        bot.register_next_step_handler(mesg, set_ID)
    # if (message.text == "ГВВ"):
    #     google_table.set_RP('ГВВ')
    #     mesg = bot.send_message(message.chat.id, 'Введите дату (год-месяц-число)\nПример: 2023-06-20')
    #     bot.register_next_step_handler(mesg, set_date)
    # if (message.text == "КРВ"):
    #     google_table.set_RP('КРВ')
    #     mesg = bot.send_message(message.chat.id, 'Введите дату (год-месяц-число)\nПример: 2023-06-20')
    #     bot.register_next_step_handler(mesg, set_date)
    # if (message.text == "ПДА"):
    #     google_table.set_RP('ПДА')
    #     mesg = bot.send_message(message.chat.id, 'Введите дату (год-месяц-число)\nПример: 2023-06-20')
    #     bot.register_next_step_handler(mesg, set_date)

@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback(callback):
    if callback.data == "yes_sum":
        date = callback.message.text
        date = date.split(' ')
        date = date[1]
        dict_update.update({'Сумма': date})
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        num1 = types.KeyboardButton('Строительные работы')
        num2 = types.KeyboardButton('Материалы')
        num3 = types.KeyboardButton('Материалы наценка')
        num4 = types.KeyboardButton('Материалы механизация')
        num5 = types.KeyboardButton('Спецмонтаж')
        num6 = types.KeyboardButton('Мотивационный расход')

        sbros = types.KeyboardButton('/сбросить')

        markup.add(num1, num2)
        markup.add(num3,num4)
        markup.add(num5,num6)
        markup.add(sbros)
        mesg = bot.send_message(callback.message.chat.id, 'Выберите направление деятельности', reply_markup=markup)
        bot.register_next_step_handler(mesg, set_direction_of_activity)
    if callback.data == "wrong_choicec":
        mesg = bot.send_message(callback.message.chat.id, 'Введите сумму')
        bot.register_next_step_handler(mesg, set_sum)


# def set_date(message):
#     if message.text == '/сбросить':
#         return bot.send_message(message.chat.id, 'Сбрасываю')
#     if google_table.valid(message.text) == 'valid':
#         print(123)
#         dict_update.update({'Дата':message.text})
#         mesg = bot.send_message(message.chat.id, 'Выберите РП объекта',reply_markup=buttons.new_markup_RP(google_table.get_value_RP()))
#         bot.register_next_step_handler(mesg, set_ID)
#     else:
#         mesg = bot.send_message(message.chat.id, 'Вы ввели не правильную дату\nПример: 2023-06-20')
#         bot.register_next_step_handler(mesg, set_date)


def set_ID(message):
    if message.text == '/сбросить':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start_job = types.KeyboardButton('Начать заполнение')
        markup.add(start_job)
        return bot.send_message(message.chat.id, 'Сбрасываю',reply_markup=markup)
    dict_update.update({'РП': message.text})
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    sbros = types.KeyboardButton('/сбросить')
    markup.add(sbros)
    mesg = bot.send_message(message.chat.id, 'Введите ИД объекта', reply_markup=markup)
    bot.register_next_step_handler(mesg, set_sum_2)

def set_sum_2(message):
    if message.text == '/сбросить':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start_job = types.KeyboardButton('Начать заполнение')
        markup.add(start_job)
        return bot.send_message(message.chat.id, 'Сбрасываю',reply_markup=markup)
    if google_table.get_RP_for_ID(message.text) == dict_update['РП']:
        dict_update.update({'ИД': message.text})
        mesg = bot.send_message(message.chat.id, 'Введите сумму')
        bot.register_next_step_handler(mesg, set_sum)
    else:
        mesg = bot.send_message(message.chat.id, 'У РП нет такого ИД\nВведите ИД')
        bot.register_next_step_handler(mesg, set_sum_2)



def set_sum(message):
    if message.text == '/сбросить':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start_job = types.KeyboardButton('Начать заполнение')
        markup.add(start_job)
        return bot.send_message(message.chat.id, 'Сбрасываю',reply_markup=markup)
    markup = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text='Да', callback_data=f"{'yes_sum'}")
    no = types.InlineKeyboardButton(text='Нет', callback_data=f"{'wrong_choicec'}")
    markup.add(yes, no)
    msg = f"Сумма {message.text}, верно ?"
    bot.send_message(message.chat.id, msg, reply_markup=markup)

def set_direction_of_activity(message):
    if message.text == '/сбросить':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start_job = types.KeyboardButton('Начать заполнение')
        markup.add(start_job)
        return bot.send_message(message.chat.id, 'Сбрасываю',reply_markup=markup)
    dict_update.update({'Направление':message.text})
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    num1 = types.KeyboardButton('Доп.расходы на объект')
    num2 = types.KeyboardButton('ФОТ мастера')
    num3 = types.KeyboardButton('Расходы черновой')
    num4 = types.KeyboardButton('Расходы спецмонтаж/подрядчики')
    num5 = types.KeyboardButton('Выручка')
    num6 = types.KeyboardButton('Скидка/доп.расход/гарантия')
    sbros = types.KeyboardButton('/сбросить')
    markup.add(num1, num2)
    markup.add(num3, num4)
    markup.add(num5, num6)
    markup.add(sbros)
    mesg = bot.send_message(message.chat.id, 'Выберите статью', reply_markup=markup)
    bot.register_next_step_handler(mesg, set_article)

def set_article(message):
    if message.text == '/сбросить':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start_job = types.KeyboardButton('Начать заполнение')
        markup.add(start_job)
        return bot.send_message(message.chat.id, 'Сбрасываю',reply_markup=markup)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    sbros = types.KeyboardButton('/сбросить')
    markup.add(sbros)
    dict_update.update({'Статья': message.text})
    mesg = bot.send_message(message.chat.id, 'Введите коментарий(N акта и тд)', reply_markup=markup)
    bot.register_next_step_handler(mesg, set_comment)

def set_comment(message):
    if message.text == '/сбросить':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start_job = types.KeyboardButton('Начать заполнение')
        markup.add(start_job)
        return bot.send_message(message.chat.id, 'Сбрасываю',reply_markup=markup)
    dict_update.update({'Комментарий': message.text})
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    num1 = types.KeyboardButton('Начать заполнение')
    markup.add(num1)
    bot.send_message(message.chat.id, 'Таблица заполнена',reply_markup=markup)
    print(dict_update)
    google_table.update_table(dict_update)


print('Run Bot')
bot.polling(none_stop=True)