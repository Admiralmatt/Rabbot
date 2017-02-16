#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import ircbot
from ircbot.ircbot import bot
from ircbot.storage import save,load
import ircbot.commands as commands

#Starts the program in ircbot.py
#args = Channel, Nickname, Server

def connect(*args):
    bot.version = '2.0.2'
    bot.mute = True
    bot.startup(*args)
    ircbot.ircbot.thread.join()

#Default connection is #admiralmatt
 
connect('loadingreadyrun')
#'ÃƒÂ©'=\xc3\xa9

def update():
    load()
    save('Manual Update')

def kill():
    commands.bot_shutdown('admiralmatt', 'Command line shutdown')
