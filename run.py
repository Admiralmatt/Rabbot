#!/usr/bin/env python 2.7

import storage
from ircbot import bot
from sendemail import send_email
import commands


#args = Channel, Nickname, Server
def connect(*args):
    bot.startup(*args)

#Default connection is #admiralmatt

connect()
#'Ã©'