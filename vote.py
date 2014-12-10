import ircbot
import utils

import time
from collections import Counter

@utils.mod_only
def newpoll(nick, msg):
    """
       <Mod only command>
 
       Command: !vote open <QUESTION;CHOICE1;CHOICE2;...>
 
       Open a new poll. Question and all choices must be seporated by ;
    """
    ircbot.bot.voting = True
    # Create new poll. Will erase old one
    # Poll results will be available until new one is made
    global poll
    poll = {}
    
    msg = msg.split(';')
    ircbot.bot.pollchoices = msg
    print 'Open poll'
    ircbot.bot.sendmsg('Poll Open!')
    if ircbot.bot.ismod == False:
        time.sleep(2)
    reminder(nick)

# Post question, options and instructions in chat one after the other
@utils.throttle(30)
def reminder(nick):
    """
       Command: !vote view
 
       Post the question and choices of the current open poll.
    """
    if ircbot.bot.voting == True:
        msg = ircbot.bot.pollchoices[:]
        ircbot.bot.sendmsg(msg[0])
        msg.remove(msg[0])
        for x in range(len(msg)):
            if ircbot.bot.ismod == False:
                time.sleep(2)
            ircbot.bot.sendmsg('%d) %s' % (x+1, msg[x]))

        if ircbot.bot.ismod == False:
            time.sleep(2)
        ircbot.bot.sendmsg('Use !vote # to cast your vote')
        
    elif ircbot.bot.voting == False: novote(nick)
        
@utils.mod_only
def voteclose(nick):
    """
       <Mod only command>
 
       Command: !vote close
 
       Close the current open poll.
    """
    # Close Poll and post results
    print 'Poll Closed'
    ircbot.bot.voting = False
    ircbot.bot.sendmsg('Polls Are Closed!')
    results(nick)

# Regester votes
def vote(nick, msg):
    """
       Command: !vote <#>
  
       Vote on choice #.
    """
    if ircbot.bot.voting == False: novote(nick)
    else:
        poll[nick] = int(msg)
        print 'Vote Registered'

@utils.throttle(10)
def results(nick):
    """
       Command: !vote result
 
       Check what choice is currently winning in an opoen poll or what choice won in the last open poll.
    """
    count = Counter(poll.values())
    total = sum(count.values())
    winner = dict(count.most_common(1))
    winchoice = winner.keys()
    winamt = winner.get(winchoice[0])
    question = ircbot.bot.pollchoices[0]
    # winmsg EX. = 2) Go Left (75%, 3/4 Votes)
    winmsg = '%d) %s (%.0f%%, %d/%d Votes)' %(int(winchoice[0]), ircbot.bot.pollchoices[int(winchoice[0])], 100*winamt/total, winamt, total)
    

    # Set up Response for winner or currently winning
    if ircbot.bot.voting == True:
        response = 'Current Leader is: %s' % (winmsg)
    elif ircbot.bot.voting == False:
        response = 'Winner is: %s' % (winmsg)

    if ircbot.bot.ismod == False:
        time.sleep(2)
    ircbot.bot.sendmsg(question)
    if ircbot.bot.ismod == False:
        time.sleep(2)
    ircbot.bot.sendmsg(response)

@utils.throttle()
def novote(nick):
    ircbot.bot.sendmsg('No Poll Currently Open')
