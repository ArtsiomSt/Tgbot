import telebot
from telebot import types
import json
import requests

class answerforuser:
    def __init__(self, username='NULL', question='', answer='', is_answered=0):
        self.username = username
        self.question = question
        self.answer = answer
        self.is_answered = is_answered

categories = []

domen = 'http://127.0.0.1:8000/'
catAPI = 'api/v1/getcategories/'
url = domen+catAPI
resp = requests.get(url)
for item in resp.json()['category']:
    categories.append(item['title'])


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
    json_for_creation = {'tguser': user, 'question': text_of_q}
    creatqAPI = 'api/v1/questions/'
    url = domen + creatqAPI
    resp = requests.post(url, data=json_for_creation)
    botsite.send_message(message.chat.id, 'Your QA has been added, you will be answered soon (:')

@botsite.message_handler(commands=['MyAnswers'])
def get_answers(message):
    user = message.from_user.username
    print(user)
    getqAPI = 'api/v1/questions/'
    url = domen + getqAPI+user
    resp = requests.get(url)
    answer_for_user =''
    if not resp.json()['userquestions']:
        botsite.send_message(message.chat.id, 'You have no questions yet')
        return
    for item in resp.json()['userquestions']:
        answer_for_user += 'Your question: '+item['question'] + '\n'
        answer_for_user += 'Your answer: '
        if item['is_answered']:
            answer_for_user += item['answer']+'\n'
        else:
            answer_for_user += 'There is no answer yet'+'\n'
        botsite.send_message(message.chat.id, answer_for_user)
        answer_for_user = ''

@botsite.message_handler(commands=['ClearQuestions'])
def clear_questions(message):
    user = message.from_user.username
    deleteqAPI = 'api/v1/questions/'
    url = domen + deleteqAPI+user
    resp = requests.delete(url)
    botsite.send_message(message.chat.id, 'Your question history has been cleared')


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

