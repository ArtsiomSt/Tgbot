import telebot
import sqlite3
from telebot import types

class answerforuser:
    def __init__(self, username='NULL', question='', answer='', is_answered=0):
        self.username = username
        self.question = question
        self.answer = answer
        self.is_answered = is_answered

conn = sqlite3.connect('db.sqlite3', check_same_thread=False)
cursor = conn.cursor()

def get_data_category():
    cursor.execute('SELECT title from glpage_category')
    data = cursor.fetchall()
    return data

# cursor.execute('INSERT INTO tgQA_telegramqa (tguser, question, is_answered) VALUES (?,?, ?)', ('aboba','test', 0))
# conn.commit()

categories = []

for item in get_data_category():
    for item_1 in item:
        categories.append(item_1)

def push_question_into_db(tguser, text_of_q):
    cursor.execute('INSERT INTO tgQA_telegramqa (tguser, question, is_answered) VALUES (?,?,?)', (tguser,text_of_q, 0))
    conn.commit()



botsite = telebot.TeleBot('5337259262:AAGgF5IkIBs91MU3lvPw_g8af-9WeTS7-xg')


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

@botsite.message_handler(commands=['Question'])
def get_question(message):
    msg = botsite.send_message(message.chat.id, 'Ask your qustion here ^_^')
    botsite.register_next_step_handler(msg, process_asking)

def process_asking(message):
    text_of_q = message.text
    user = message.from_user.username
    push_question_into_db(user, text_of_q)
    botsite.send_message(message.chat.id, 'Your QA has been added, you will be answered soon (:')

@botsite.message_handler(commands=['MyAnswers'])
def get_answers(message):
    user = message.from_user.username
    print(user)
    answer_for_user =''
    cursor.execute(f"SELECT tguser,question,answer,is_answered FROM tgQA_telegramqa where tguser='{message.from_user.username}'")
    conn.commit()
    row_data = cursor.fetchall()
    print(row_data)
    for item in row_data:
        userQA=answerforuser
        userQA.username = item[0]
        userQA.question = item[1]
        userQA.answer = item[2]
        userQA.is_answered = item[3]
        answer_for_user += 'Your question: '+userQA.question + '\n'
        answer_for_user += 'Your answer: '
        if userQA.is_answered:
            answer_for_user += userQA.answer+'\n'
        else:
            answer_for_user += 'There is no answer yet'+'\n'
        botsite.send_message(message.chat.id, answer_for_user)
        answer_for_user = ''







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

