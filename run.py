#!/usr/bin/env python 2.7

import storage
from storage import save,load
from ircbot import bot
from sendemail import send_email
import commands


#args = Channel, Nickname, Server
def connect(*args):
    bot.startup(*args)

#Default connection is #admiralmatt

connect('sageofsong')
#'Ã©'=\xc3\xa9

def update():
    load()
    save()
