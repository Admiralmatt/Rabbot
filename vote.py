import ircbot

from collections import Counter


def newpoll(nick,msg):
    global poll
    poll = {}
    
    msg = msg.split(';')

    ircbot.bot.pollchoices = msg

    print 'Open poll'
    ircbot.bot.sendmsg('Poll Open!')
    for x in range(len(msg)):
        ircbot.bot.sendmsg('%d) %s' % (x + 1, msg[x]))

    ircbot.bot.sendmsg('Use <vote #> to cast your vote')

def voteclose():
    print 'Poll Closed'
    ircbot.bot.sendmsg('Poll Closed!')
    pass

def vote(nick, msg):
    if msg in (range(len(ircbot.bot.pollchoices))):
        poll[nick] = msg

def results(nick, msg):
    count = Counter(poll.values())
    total = sum(count.values())

    winner = dict(count.mostcommon(1))
    winchoice = winner.keys()
    winamt = winner.get(winchoice[0])
    
    pass

#http://stackoverflow.com/a/13462417

a = {'ee': 'a', 'qgw': 'b', 'fee': 'a', 'qw': 'a'}

c = Counter(a.values())
