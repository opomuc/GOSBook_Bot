#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from functools import wraps
from telegram.ext import CommandHandler
from telegram.error import TelegramError

import users
import time


def send_file(bot, filename, chat_id, _type, caption, **kwargs):
    def upload():
        v_var = bot.sendDocument(bot, open(filename, 'r'), chat_id, caption)
        return v_var
    try:
        return upload()
    except TelegramError as e_error:
        if "file_id" in e_error.message:
            return upload()
        else:
            raise e_error


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args):
        user_id = update.message.chat_id
        if user_id not in users.admins():
            return print("Unauthorized access denied for {}.".format(user_id)) 
        return func(bot, update, *args)
    return wrapped


class Commands(list):
    def add(self, name, func):
        self.append((name, func))

    def pprint(self):
        for cmd in self:
            print(cmd)


COMMANDS = Commands()


def init_dispatcher(dispatcher):
    for cmd in COMMANDS:
        dispatcher.add_handler(CommandHandler(cmd[0], cmd[1]))


@restricted
def get_suspectusers(bot, update):
    id_all = update.message.chat_id
    sub_list = []
    for sub in users.get_suspects():
        chat = bot.getChat(sub)
        badtimes = sum(1 for i in users.get_suspects() if i == sub)
        if chat.type == 'private':
            sub_list.append(chat.first_name + ' ' +
                            chat.last_name + ' ' + str(badtimes))
        else:
            sub_list.append("Группа: " + chat.title + ' ' + str(badtimes))
    sub_list = list(set(sub_list))
    message = '\n'.join(sub_list)
    bot.sendMessage(chat_id=id_all, text='Список подозреваемых:\n' + message)


COMMANDS.add('show_suspects', get_suspectusers)


@restricted
def saytopeople(bot, update):
    id_all = update.message.chat_id
    try:
        message = update.message.text
        message = message.split("\n", 2)[2]
    except:
        bot.sendMessage(
            chat_id=id_all, text='Сообщение не отправлено. Неправильный формат сообщения.')
        return None

    with open('mode_list', 'r') as file:
        mode_list = int(file.read())   # 0 - test; 1 -- true work.

    if mode_list == 1:
        audience = users.get_subscribers()
    if mode_list == 0:
        audience = users.get_testsubs()

    for ids in audience:
        try:
            bot.sendMessage(chat_id=ids, text=message)
        except TelegramError as err:
            users.check_suspect(ids)
        time.sleep(1)


COMMANDS.add('saytopeople', saytopeople)


@restricted
def changemode(bot, update):
    id = update.message.chat_id

    with open('mode_list', 'r') as db:
        mode = int(db.read())

    with open('mode_list', 'w') as db:
        mode = 1 - mode
        db.write(str(mode))

    bot.sendMessage(chat_id=id, text='теперь включен режим ' +
                    str(mode) + '.\n 0 -- тест, 1 -- норма.')


COMMANDS.add('changemode', changemode)


@restricted
def secretinfo(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, 
		    text='''**Список секретных команд данного бота:**\n
/howmuch -- узнать количество подписчиков данного бота
/show_subs -- показать список подписчиков
/howmanystar -- узнать количество стартеров
/show_starters -- вывести список стартеров
/show_suspects -- вывести список подозреваемых

/testsubscribe -- стать БЕТА-тестером
/testunsubscribe -- перестать быть БЕТА-тестером
/howmanytest -- узнать количество БЕТА-тестеров
/show_testsubs -- показать БЕТА-тестеров
/changemode -- смени режим работы бота. 
	Тестовый режим -- для тестовой аудитории, и нормальный режим для вещания на реальную аудиторию
"/saytopeople \\n\\n + <<сообщение>>" --  начни сообщение после двух переходов 
			на новую строку, и оно будет бродкастено на аудиторию''')


COMMANDS.add('secretinfo', secretinfo)


@restricted
def get_numberoftestsubs(bot, update):
    id = update.message.chat_id
    bot.sendMessage(chat_id=id, text="Количество БЕТА-тестеров у этого бота: " +
                    str(len(users.get_testsubs())))


COMMANDS.add('howmanytest', get_numberoftestsubs)


@restricted
def get_testusers(bot, update):
    id = update.message.chat_id
    sub_list = []
    for sub in users.get_testsubs():
        chat = bot.getChat(sub)
        if chat.type == 'private':
            sub_list.append(chat.first_name + ' ' + chat.last_name)
        else:
            sub_list.append("Группа: " + chat.title)
    message = '\n'.join(sub_list)
    bot.sendMessage(chat_id=id, text='Список БЕТА-тестеров:\n' + message)


COMMANDS.add('show_testsubs', get_testusers)


@restricted
def get_numberofsubs(bot, update):
    id = update.message.chat_id
    bot.sendMessage(chat_id=id, text="Количество подписчиков у этого бота: " +
                    str(len(users.get_subscribers())))


COMMANDS.add('howmuch', get_numberofsubs)


@restricted
def get_users(bot, update):
    id = update.message.chat_id
    sub_list = []
    for sub in users.get_subscribers():
        chat = bot.getChat(sub)
        if chat.type == 'private':
            sub_list.append(chat.first_name + ' ' + chat.last_name)
        else:
            sub_list.append("Группа: " + chat.title)
    message = '\n'.join(sub_list)
    bot.sendMessage(chat_id=id, text='Список подписчиков:\n' + message)


COMMANDS.add('show_subs', get_users)


@restricted
def get_numberofstarters(bot, update):
    id = update.message.chat_id
    bot.sendMessage(chat_id=id, text="Количество стартеров у этого бота: " +
                    str(len(users.get_starters())))


COMMANDS.add('howmanystar', get_numberofstarters)


@restricted
def get_users_starters(bot, update):
    id = update.message.chat_id
    sub_list = []
    for sub in users.get_starters():
        chat = bot.getChat(sub)
        if chat.type == 'private':
            sub_list.append(chat.first_name + ' ' + chat.last_name)
        else:
            sub_list.append("Группа: " + chat.title)
    message = '\n'.join(sub_list)
    bot.sendMessage(chat_id=id, text='Список стартеров:\n' + message)


COMMANDS.add('show_starters', get_users_starters)


def start(bot, update):
    id = update.message.chat_id
    if id not in get_starters():
        add_starter(id)
    bot.sendMessage(chat_id=update.message.chat_id, text="Я бот, вижу, вы хотите поботать ГОС?\n\
	Для ознакомления со списком возможных команд, запросите /help")


COMMANDS.add('start', start)


def help_bot(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='''**Список команд данного бота:**\n
	/book -- получить последнюю версию ГОСБука в pdf-формате\n
	/subscribe -- подписаться на рассылку об обновлениях ГОСБука, чтобы автоматически получать новые версии ГОСБука, а также читать новости, касающиеся ГОСа\n
	/unsubscribe -- отписаться от выше указанной новостной рассылки\n
	/help -- вывести список команд данного бота\n\n
	PS. Если я как-то неправильно работаю или у тебя есть интересные предложения по улучшению меня, то напиши, пожалуйста, моему создателю @didenko_andre''')


COMMANDS.add('help', help_bot)


def getbook(bot, update):
    id = update.message.chat_id
    if id not in get_starters():
        add_starter(id)
    send_file(bot, "/home/ec2-user/GOS_book/GOSBook_Matan.pdf", id, None,
              caption="Вот последняя версия ГОСбука")


COMMANDS.add('book', getbook)


def subscribe(bot, update):
    id = update.message.chat_id
    if id in users.get_subscribers():
        bot.sendMessage(chat_id=id, text="Вы уже являетесь подписчиком!")
        return None
    users.add_subscriber(id)
    bot.sendMessage(
        chat_id=id, text="Вы успешно подписались на рассылку об обновлениях ГОСбука!")


COMMANDS.add('subscribe', subscribe)


def unsubscribe(bot, update):
    id = update.message.chat_id
    if id not in users.get_subscribers():
        bot.sendMessage(chat_id=id, text="Вы не являетесь подписчиком!")
        return None
    users.del_subscriber(id)
    bot.sendMessage(
        chat_id=id, text="Вы прекратили свою подписку на рассылку об обновлениях ГОСбука!")


COMMANDS.add('unsubscribe', unsubscribe)


def testsubscribe(bot, update):
    id = update.message.chat_id
    if id in users.get_testsubs():
        bot.sendMessage(chat_id=id, text="Вы уже являетесь БЕТА-тестером!")
        return None
    users.add_testsub(id)
    bot.sendMessage(
        chat_id=id, text="Вы успешно подписались на ТЕСТОВУЮ рассылку!")


COMMANDS.add('testsubscribe', testsubscribe)


def testunsubscribe(bot, update):
    id = update.message.chat_id
    if id not in users.get_testsubs():
        bot.sendMessage(chat_id=id, text="Вы не являетесь БЕТА-тестером!")
        return None
    users.del_testsub(id)
    bot.sendMessage(
        chat_id=id, text="Вы прекратили свою подписку на ТЕСТОВУЮ рассылку!")


COMMANDS.add('testunsubscribe', testunsubscribe)
