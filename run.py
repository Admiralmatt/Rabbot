from ircbot import bot
from sendemail import send_email
import commands
import storage

#args = Channel, Nickname, Server
def connect(*args):
    bot.startup(*args)
connect('seabats')

#'only_scrubs_skip_leg_day'
