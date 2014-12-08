import storage
from ircbot import bot
from sendemail import send_email
import commands


#args = Channel, Nickname, Server
def connect(*args):
    bot.startup(*args)
connect('loadingreadyrun')
#Default connection is #admiralmatt
