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
            addquote(nick, ' '.join(msg[2:]), data)
        elif msg[1] == 'edit':
            editquote(nick, ' '.join(msg[3:]), data[int(msg[2])])
        elif msg[1] == 'remove':
            removequote(nick, msg[2], data)
        elif msg
            postquote
            
            pass
            
    except KeyError:
        return

def addquote(nick,msg,data):
    data.setdefault('lastid',0)
    data['lastid'] += 1
    id = data['lastid']
    date = time.strftime("%m/%d/%Y")
    data[id] = {'quote':msg,'time': date}
    action = ' added:'
    postquote(nick,msg,date,action)
    
def editquote(nick,msg,data):
    data['quote'] = msg
    action = ' edited:'
    postquote(nick,msg,data['time'],action)

def removequote(nick, msg, data):
    del data[msg]    
    action = ' removed:'
    postquote(nick,msg,date,action)

def postquote(nick,msg,date,action):
    logging.info('Quote #%i%s %s -%s by %s' % (id, action, msg, date, nick))
    bot.sendmsg('Quote #%i%s %s -%s' % (id, action, msg, date))
    save('Quote %s' % action)





