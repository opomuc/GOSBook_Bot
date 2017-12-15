#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import bot

with open('GOSBook_Bot_token', 'r') as file1:
    TOKEN = file1.read().strip()

bot.start(TOKEN)
