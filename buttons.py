import telebot
from telebot import types
import google_table

def new_markup_RP(list_button):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in list_button['РП']:

        markup.add(types.KeyboardButton(f"{i}"))

    sbros = types.KeyboardButton('/сбросить')
    markup.add(sbros)
    return markup
