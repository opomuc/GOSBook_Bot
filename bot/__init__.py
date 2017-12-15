#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from telegram import Bot
from telegram.ext import Updater
from telegram.error import TelegramError

from .commands import COMMANDS, init_dispatcher


def start(token):
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    init_dispatcher(dispatcher)

    COMMANDS.pprint()

    updater.start_polling()
    updater.idle()
