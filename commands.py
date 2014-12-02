import random

import ircbot
from sendemail import send_email
import utils
import twitch
import vote
from storage import save

@utils.admin_only
def bot_close(nick): #Disconnect from server
   """
      <Mod only command>

      Command: !bot_close

      Preforms safe shutdown of bot.
   """
   ircbot.bot.threadquit = True
   ircbot.bot.sendmsg('Shutting Down')
   ircbot.bot.ircsock.close()
   # Send safe shut down report to bot email
   send_email('Bot has safley shut down from user command', 'Safe Shut Down')


def game_anounce(nick):
   """
      Command: !game

      Post the game currently being played.
   """
   game = ircbot.bot.get_current_game(nick)
   if game is None:
      msg = 'Not currently playing any game'
   else:
      msg = 'Currently playing: %s' % game['name']
      # If there are any ratings for the game it will be displayed
      if game.get('rating'):
         good = sum(game['rating'].values())
         msg += " (rating %.0f%%)" % (100*good/len(game['rating']))

   if ircbot.bot.game_override is not None:
      msg += ' (Overridden)'

   ircbot.bot.sendmsg(msg)


#assume msg[0] = 'game'
def gamecheck(nick, msg, msgcap):
   try:
      if msg[1] == 'override':
         msg[2] = ' '.join(msgcap[2:])
         game_override(nick, msg[2])

      elif msg[1] == 'refresh':
         refresh(nick)

      elif msg[1] in ('good', 'bad'):
         rategame(nick, msg[1])

   except IndexError:
      pass
      game_anounce(nick)

@utils.mod_only
def game_override(nick, msg):
   '''
      <Mod only command>
      
      Command: !game override <NAME>

      eg: !game override Prayer Warriors: A.O.F.G.

      Override what game is being played (eg. when the current game isn't in the Twitch database)

      <Mod only command>
      --command
      Command: !game override off

      Disable override, go back to getting current game from Twitch stream settings.
   '''
   if msg == 'off':
      twitch.get_live_game.reset_throttle()
      ircbot.bot.game_override = None
   else:
      ircbot.bot.game_override = msg
   game_anounce(nick)

#checks storage file for correct responses
@utils.throttle(5)
def send_response(nick, msg, data):
   """
      Command: !<Depends>

      Posts a static response to a command. Or random response from list
      All commands and responces are listed in data file

      Each command can have different access levels.
   """
   
   if data['access'] == 'admin' and nick not in (ircbot.bot.show, 'admiralmatt'):
      return
   elif data['access'] == 'mod' and nick not in (ircbot.bot.modlist, ircbot.bot.show):
      return
   else:
      response = data['response']
      if isinstance(response, (tuple, list)):
         response = random.choice(response)
      ircbot.bot.sendmsg(response)

def refresh(nick):
   """
      Command: !game refresh

      Force a refresh of the current Twitch game (normally this is updated at most once every 15 minutes)
   """
   twitch.get_live_game.reset_throttle()
   game_anounce(nick)

@utils.mod_only
def lockdown(nick, msg):
   """
      Command: !lockdown
      Command: !lockdown off
      
      Prevent anyone other then mods to use bot
   """
   msg.extend([None])

   if msg[1] == 'off':
      ircbot.bot.lockdown = False
      print "Mod Only Mode Over"
   else:
      ircbot.bot.lockdown = True
      print "Mod Only Mode"


# Only mods can use bot
@utils.mod_only
def lockdown_mode(nick, msg, msgcap):
   ircbot.bot.is_command(nick, msg, msgcap)


def rategame(nick, msg):
   """
      Command: !game good
      Command: !game bad
      
      Declare whether you believe this game is entertaining to watch on-stream.
      Voting a second time replaces your existing vote.
   """
   game = ircbot.bot.get_current_game(nick)
   if game is None:
      msg = 'Not currently playing any game'
      return
   
   game.setdefault("rating", {})

   if msg in ('good'):
      game['rating'][nick] = True
      save()
      rate_respond(nick, game)

   elif msg in ('bad'):
      game['rating'][nick] = False
      save()
      rate_respond(nick, game)

@utils.throttle(10)
def rate_respond(nick, game):
   if game and game.get('rating'):
      good = sum(game['rating'].values())
      count = len(game['rating'])
      ircbot.bot.sendmsg ('Rating for %s is now %.0f%% (%d/%d)' % (game['name'], 100*good/count, good, count))

def vote(nick, msg, msgcap):
   try:
      if msg[1] == 'open':
         msg[2] = ' '.join(msgcap[2:])
         ircbot.bot.voting = True
         vote.newpoll(nick, msg[2])

      elif msg[1] == 'close':
         ircbot.bot.voting = False

      elif msg[1] in (range(len(ircbot.bot.pollchoices))):
         vote.vote(nick, msg[1])
         

   except IndexError:
      pass


















