import ircbot
import logging, time, random
import utils
import storage

#data=channeldata['quote']
def quote(nick, msg, data):
    try:
        if len(msg) == 1:
            q=data.keys()
            q.pop('lastid')
            id = random.choice(q)
            choosequote(nick, data[id], id)
        elif msg[1].lower() == 'add':
            addquote(nick, ' '.join(msg[2:]), data)
        elif msg[1].lower() == 'edit':
            editquote(nick, ' '.join(msg[3:]), data[msg[2]], msg[2])
        elif msg[1].lower() == 'remove':
            removequote(nick, msg[2], data,)
        elif msg[1] in data.keys():
            choosequote(nick, data[msg[1]], msg[1])
    except Exception:
        return
    
#!quote add text of quote
@utils.throttle()
def addquote(nick, msg, data):
    data.setdefault('lastid',0)
    data['lastid'] += 1
    id = data['lastid']
    date = time.strftime("%m/%d/%Y")
    data[str(id)] = {'quote':msg,'date': date}
    action = ' added:'
    postquote(nick, id, msg, date, action)

#!quote edit # new text of quote    
def editquote(nick, msg, data, id):
    data['quote'] = msg
    action = ' edited:'
    postquote(nick, id, msg, data['date'], action)

#!quote remove #
def removequote(nick, id, data):
    msg = data[id]['quote']
    date = data[id]['date']
    del data[id]
    action = ' removed:'
    postquote(nick, id, msg, date, action)

#!quote
#!quote #
@utils.throttle(3)
def choosequote(nick, data, id):
    action = ':'
    msg = data['quote']
    date = data['date']
    postquote(nick, id, msg, date, action)

def postquote(nick, id, msg, date, action):
    logging.info('Quote #%s%s "%s" -%s by %s' % (id, action, msg, date, nick))
    ircbot.bot.sendmsg('Quote #%s%s "%s" -%s' % (id, action, msg, date))
    storage.save('Quote%s' % action)
