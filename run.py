#!/usr/bin/env python 2.7
import ircbot
from ircbot.ircbot import bot

import ircbot.storage
from ircbot.storage import save,load

from ircbot.sendemail import send_email
from ircbot.highlights import highlight
import ircbot.commands


#args = Channel, Nickname, Server
def connect(*args):
    bot.startup(*args)

#Default connection is #admiralmatt

connect('sacriel')
#'Ã©'=\xc3\xa9

def update():
    load()
    save('Manual Update')
