import random

import ircbot
from sendemail import send_email
import utils
import twitch

@utils.mod_only
def hello_comm(nick):
   ircbot.bot.sendmsg('Hello!')

@utils.throttle(60)
def help_comm(nick = None):
   ircbot.bot.sendmsg('My other command is !test and !hello.', nick)

def test_comm(nick = None):
   ircbot.bot.sendmsg('test', nick)

@utils.mod_only
def bot_close(nick): #Disconnect from server
   """
      <Mod only command>

      Command: !bot_close

      Preforms safe shutdown of bot.
   """
   ircbot.bot.threadquit = True
   ircbot.bot.ircsock.close()
   #send safe shut down report to bot email
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
      print 'got game'
   if ircbot.bot.game_override is not None:
      msg += ' (Overridden)'
   ircbot.bot.sendmsg(msg)


#assume msg[0] = 'game'
def gamecheck(nick, msg):
   try:
      if msg[1] == 'override':
         msg[2] = ' '.join(msg[2:])
         game_override(nick, msg[2])

      elif msg[1] == 'refresh':
         refresh(nick)
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
   
   if data['access'] != 'any' and nick not in mods:
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
