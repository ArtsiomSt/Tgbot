import telebot
from telebot import types

botsite = telebot.TeleBot('5337259262:AAGgF5IkIBs9_g8af-9WeTS7-xg')
categories = ['Видеотехника', 'Аудиотехника', 'Вычислительная']
@botsite.message_handler(commands=['start'])
def start(message):
    mess = f'Hello there, <b>{message.from_user.username}</b>\n Type /help to get the list of commands'
    botsite.send_message(message.chat.id, mess, parse_mode= 'html')

@botsite.message_handler(commands=['help'])
def start(message):
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    site = types.KeyboardButton('/site')
    photo = types.KeyboardButton('Photo')
    get_category_list = types.KeyboardButton('Categories')
    buttons.add(site, photo, get_category_list)
    botsite.send_message(message.chat.id, 'Choose from those variants', reply_markup=buttons)

@botsite.message_handler(commands=['site'])
def website(message):
    button = types.InlineKeyboardMarkup()
    button.add(types.InlineKeyboardButton('Go to web', url='http://127.0.0.1:8000/'))
    botsite.send_message(message.chat.id, 'There is our site', reply_markup=button)


@botsite.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == 'Categories':
        mess = 'Choose from those categories'
        for item in categories:
            mess += '\n'+item
        buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        for item in categories:
            buttons.add(types.KeyboardButton(item))
        botsite.send_message(message.chat.id, mess, reply_markup=buttons)
    elif message.text in categories:
        for item in categories:
            if message.text == item:
                get_buttons_for_cat(message, item)
    # elif message.text == categories[0]:
    #     get_buttons_for_cat(message, categories[0])
    # elif message.text == categories[1]:
    #     get_buttons_for_cat(message, categories[1])
    # elif message.text == categories[2]:
    #     get_buttons_for_cat(message, categories[2])
    elif message.text == 'Photo':
        photo = open('photos/cat_for_bot.png', 'rb')
        botsite.send_photo(message.chat.id, photo, 'Here is you good cat')
    else:
        botsite.send_message(message.chat.id, '<b>There is no such command</b>', parse_mode='html')



def get_buttons_for_cat(message, category):
        buttons = types.InlineKeyboardMarkup()
        counter = 0
        for item in categories:
            if category == item:
                break
            else:
                counter+=1
        buttons.add(types.InlineKeyboardButton(f'Get some info about the {category}', url=f'http://127.0.0.1:8000/category/{counter+1}/'))
        botsite.send_message(message.chat.id, 'Here you are', reply_markup=buttons)

botsite.polling(none_stop=True)
