from storage import save, getchanneldata
from ircbot import bot
import utils
import logging

#update stats
def stat_update(nick, stat, n, set_=False):
    game = bot.get_current_game(nick)
    if game is None:
        return None
    game.setdefault("stats", {}).setdefault(stat, 0)
    if set_:
        game["stats"][stat] = n
    else:
        game["stats"][stat] += n
        
    logging.info('Stat %s Updated by %s' %(stat, nick))
    stat_print(nick, stat)
    storage.save('Stat Update')
    return game


#request to add one to a counter, or create a new counter

@utils.throttle(notify = True, params = [0])
def add(nick, stat, n = None, set_ = False):
    """
        Command: !<STAT>
        
        Add 1 to <STAT> counter.

        --command
        <Mod only command>
        
        Command: !<STAT> add #

        Adds # amount to <STAT>
    """
    n = 1 if n is None else int(n)
    game = stat_update(nick, stat, n, set_)
    if game is None:
        bot.sendmsg("Not currently playing any game")
        return

@utils.throttle(notify = True, params = [0])
def remove(nick, stat, n = None):
    """
        Command: !<STAT> remove
        
        Removes 1 from <STAT> counter.
    """
    n = -1 if n is None else int(-n)
    game = stat_update(nick, stat, n)
    if game is None:
        bot.sendmsg("Not currently playing any game")
        return
    
@utils.mod_only
def multiremove(nick, stat, n = None):
    """
        <Mod only command>
        
        Command: !<STAT> remove #
        
        Removes # from <STAT> counter.
    """
    n = -1 if n is None else int(-n)
    game = stat_update(nick, stat, n)
    if game is None:
        bot.sendmsg("Not currently playing any game")
        return
    
@utils.mod_only
def newstat(nick, stat, amt = 1):
    """
        <Mod only command>
        
        Command: !<STAT> new
        
        Creates a new <STAT> counter that has not been used in any game so far.
    """
    channeldata = storage.getchanneldata()
    if stat not in channeldata['showstats']:
        channeldata['showstats'].append(stat)
    add(nick, stat, amt)

@utils.mod_only
#Creates Mod Only Command
def addstat(nick, stat, amt):
    add(nick, stat, amt)

@utils.mod_only
def setstat(nick, stat, amt):

    """
        <Mod only command>
        
        Command: !<STAT> set (#)
        
        Sets <STAT> to #
    """    
    stat_update(nick, stat, amt, True)


def stat_print(nick, stat):
    """
        Command: !<STAT> count
        
        Posts the current <STAT> count for current game.

        Auto called after stat update.
    """
    game = bot.get_current_game(nick)
    if game is None:
        bot.sendmsg("Not currently playing any game")
        return
    try:
        count = game['stats'][stat]
        if count > 1:
            stat += 's'
        bot.sendmsg('%d %s for %s' % (count, stat, game['name']))
    except KeyError:
        pass

def statcheck(nick, channeldata):
    msg = ', '.join(channeldata['showstats'])
    bot.sendmsg('Stats currently being tracked are: ' + msg)
    

def change(nick, stat, command = None, amt = None):
    amt = 1 if amt is None else int(amt)

    if command == None:
        logging.info('Stat %s increased by %i Triggered by %s' %(stat, amt, nick))
        add(nick, stat)

    elif command == 'add': #mod only
        logging.info('Stat %s increased by %i Triggered by %s' %(stat, amt, nick))
        addstat(nick, stat, amt)
        
    
    elif command == 'new': #mod only
        logging.info('New Stat %s Created by %s' %(stat, nick))
        newstat(nick, stat)
            
    elif command == 'remove' and amt != 1: #mod only
        logging.info('Stat %s reduced by %i Triggered by %s' %(stat, amt, nick))
        multiremove(nick, stat, amt)

    elif command == 'remove':
        logging.info('Stat %s reduced by %i Triggered by %s' %(stat, amt, nick))
        remove(nick, stat)
        
    elif command == 'set': #mod only
        logging.info('Stat %s set to %i Triggered by %s' %(stat, amt, nick))
        setstat(nick, stat, amt)

    elif command == 'count':
        stat_print(nick, stat)
