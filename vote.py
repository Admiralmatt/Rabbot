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
        ircbot.bot.sendmsg('%d) %s' % (x, msg[x]))

    ircbot.bot.sendmsg('Use <vote #> to cast your vote')

def voteclose(nick):
    print 'Poll Closed'
    ircbot.bot.voting = False
    ircbot.bot.sendmsg('Poll Closed!')
    pass

# Regester votes
def vote(nick, msg):
    if msg in (range(len(ircbot.bot.pollchoices))):
        poll[nick] = msg

def results(nick, msg):
    count = Counter(poll.values())
    total = sum(count.values())
    winner = dict(count.mostcommon(1))
    winchoice = winner.keys()
    winamt = winner.get(winchoice[0])
    question = ircbot.bot.pollchoices[0]
    winmsg = '%d) %s (%.0f%%)' %(winchoice[0], ircbot.bot.pollchoices[winchoice[0]], 100*winamt/total)

    # Set up Responces for winner or currently winning
    if ircbot.bot.voting == True:
        response = 'Current Leader is %s' % (winmsg)
    elif ircbot.bot.voting == False:
        response = 'Winner Is: %s' % (winmsg)

    ircbot.bot.sendmsg(question)
    ircbot.bot.sendmsg(responce)
    
    
    pass

#http://stackoverflow.com/a/13462417

a = {'ee': 'a', 'qgw': 'b', 'fee': 'a', 'qw': 'a'}

c = Counter(a.values())
