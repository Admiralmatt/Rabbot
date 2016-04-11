'''
from ircbot import bot
import utils
import logging
import time
from storage import save
'''

['quote', 'add', 'this', 'is', 'a', 'test']

#data=channeldata['quote']
def quote(nick,msg,data):
    try:
        if msg[1] == 'add':
            addquote(nick,' '.join(msg[2:]),data)
        elif msg[1] == 'edit':
            editquote(nick, ' '.join(msg[3:]),data[int(msg[2])])
            
    except KeyError:
        return

def addquote(nick,msg,data):
    data.setdefault('lastid',0)
    data['lastid'] += 1
    id = data['lastid']
    date = time.strftime("%m/%d/%Y")
    data[id] = {'quote':msg,'time': date}
    postquote(nick,msg,date,action)
    logging.info('Quote #%i added: %s -%s by nick' % (id, msg,date,nick))
    bot.sendmsg('Quote #%i added: %s -%s' % (id, msg,date))
    save('Quote added')
    
def editquote(nick,msg,data):
    data['quote'] = msg
    
    pass

def removequote(nick,msg):
    pass

def postquote(nick,msg,date,action):
    bot.sendmsg('Quote #%i%s %s -%s' % (id, action, msg, date))
    pass





