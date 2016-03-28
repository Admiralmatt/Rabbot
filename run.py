#!/usr/bin/env python 2.7
import ircbot
import ircbot.storage
from ircbot.storage import save,load
from ircbot.ircbot import bot
from ircbot.sendemail import send_email
import ircbot.commands


#args = Channel, Nickname, Server
def connect(*args):
    bot.startup(*args)

#Default connection is #admiralmatt

connect('sageofsong')
#'Ã©'=\xc3\xa9

def update():
    load()
    save('Manual Update')
