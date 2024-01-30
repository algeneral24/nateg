# pylint:disable=E0633
import telebot
from telebot import types
import requests
import json
from bs4 import BeautifulSoup

admin_chat_id = 1792449471

dev = types.InlineKeyboardButton(text="𝑴𝒊𝒏𝒊𝒂 𝑨𝒈𝒓𝒊𝒄𝒖𝒍𝒕𝒖𝒓𝒆🌸🌾 ", url='https://t.me/+rbphVRSaWD9mNjg8')
btn = types.InlineKeyboardMarkup()
btn.row_width = 1
btn.add(dev)

token = "6410467729:AAE35oFq2b1ogyxZMIlA_VbYC60DKJB9neY"
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, 'typing')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton('𓆩⋆ ׅᎯL ׅG̸E🅽ᎬRᎪⱠ ׅ⋆𓆪', url='https://t.me/BO_R0'),
                  types.InlineKeyboardButton('𝑴𝒊𝒏𝒊𝒂 𝑨𝒈𝒓𝒊𝒄𝒖𝒍𝒕𝒖𝒓𝒆☘️', url='https://t.me/+rbphVRSaWD9mNjg8'))

    bot.reply_to(message, f"- أهلاً بك عزيزي [{message.from_user.first_name}](tg://user?id={message.from_user.id}) 👋.\n"
                      f"- في بوت [{bot.get_me().first_name}](https://t.me/{bot.get_me().username}) للحصول على النتيجة.\n"
                      f"- يمكنك استخدام البوت للحصول على نتيجة كلية الزراعة جامعة المنيا.\n"
                      , parse_mode='Markdown', reply_markup=keyboard)
    bot.reply_to(message, "البوت تحت الصيانة برجاء المحاولة لاحقا")

bot.polling()
