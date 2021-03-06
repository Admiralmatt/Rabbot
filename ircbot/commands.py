import random, logging, time
from ircbot import bot
from sendemail import send_email
import twitch, vote, storage, highlights, utils

@utils.admin_only
def bot_shutdown(nick, msg): #Disconnect from server
   """
      <Mod only command>

      Command: !bot_shutdown

      Preforms safe shut-down of bot.
   """
   bot.sendmsg('Shutting Down')
   # Send safe shut down report to bot email
   logging.info('Bot safe shutdown by %s' %nick)   
   send_email('Bot has safley shut down by %s' %nick, msg, 'Safe Shut Down')
   bot.ircsock.close()
   quit()

def game_anounce(nick):
   """
      Command: !game

      Post the game currently being played.
   """
   game = bot.get_current_game(nick)
  
   if game is None:
      msg = 'Not currently playing any game'
   else:
      msg = 'Currently playing: %s' % game['name']
      # If there are any ratings for the game it will be displayed
      if game.get('rating'):
         good = sum(game['rating'].values())
         msg += " (rating %.0f%%)" % (100*good/len(game['rating']))

   if bot.game_override is not None:
      msg += ' (Overridden)'
   bot.sendmsg(msg)


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
   """
      <Mod only command>
      
      Command: !game override <NAME>

      eg: !game override Prayer Warriors: A.O.F.G.

      Override what game is being played (eg. when the current game isn't in the Twitch database)

      <Mod only command>
      --command
      Command: !game override off

      Disable override, go back to getting current game from Twitch stream settings.
   """
   if msg == 'off':
      twitch.get_live_game.reset_throttle()
      bot.game_override = None
      logging.info('Game Override disabled Triggered by %s' %nick)
   else:
      bot.game_override = msg
      logging.info('Game Overridden to %s Triggered by %s' %(msg,nick))
   game_anounce(nick)

#checks storage file for correct responses
@utils.throttle(5)
def send_response(nick, msg, data):
   """
      Command: !<Depends>

      Posts a static response to a command. Or random response from list
      All commands and responses are listed in data file

      Each command can have different access levels.
   """
   
   if data['access'] == 'admin' and nick not in (bot.show, 'admiralmatt'):
      return
   elif data['access'] == 'mod' and nick not in (bot.modlist, bot.show):
      return
   else:
      response = data['response']
      if isinstance(response, (tuple, list)):
         response = random.choice(response)
      bot.sendmsg(response)

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
      bot.lockdown = False
      logging.info('Lockdown mode disabled Triggered by %s' %nick)
      print "Mod Only Mode Over"
   else:
      bot.lockdown = True
      logging.info('Lockdown mode Triggered by %s' %nick)
      print "Mod Only Mode"

# Only mods can use bot
@utils.mod_only
def lockdown_mode(nick, msg, msgcap):
   bot.is_command(nick, msg, msgcap)

def rategame(nick, msg):
   """
      Command: !game good
      Command: !game bad
      
      Declare whether you believe this game is entertaining to watch on-stream.
      Voting a second time replaces your existing vote.
   """
   game = bot.get_current_game(nick)
   if game is None:
      msg = 'Not currently playing any game'
      return
   
   game.setdefault("rating", {})

   if msg in ('good'):
      game['rating'][nick] = True
      storage.save('good rating update')
      rate_respond(nick, game)

   elif msg in ('bad'):
      game['rating'][nick] = False
      storage.save('good rating update')
      rate_respond(nick, game)

@utils.throttle(10)
def rate_respond(nick, game):
   if game and game.get('rating'):
      good = sum(game['rating'].values())
      count = len(game['rating'])
      bot.sendmsg ('Rating for %s is now %.0f%% (%d/%d)' % (game['name'], 100*good/count, good, count))
	  
def comm_vote(nick, msg, msgcap):
   try:
      # New Poll  MOD_ONLY
      if msg[1] == 'open':
         msg[2] = ' '.join(msgcap[2:])
         vote.newpoll(nick, msg[2])
         
      # Close Poll  MOD_ONLY
      elif msg[1] == 'close':
         vote.voteclose(nick)

      # What are we voting on again?
      elif msg[1] == 'view':
         vote.reminder(nick)

      # Who is Winning/Won?
      elif msg[1] == 'result':
         vote.results(nick)

      # Vote On Poll
      try:
         if int(msg[1]) in (range(1,len(bot.pollchoices))):
            vote.vote(nick, msg[1])
            
      except TypeError:
         print 'Type Error On Vote'
         vote.novote(nick)

      except ValueError:
         pass
         
   except IndexError:
      pass

#Request a game to be played
@utils.throttle(5)
def game_request(nick, msg):
   request = bot.channeldata['request']
   if msg == 'clear':
      f=utils.mod_only(lambda nick,request: request.clear())
      f(nick,request)
      bot.sendmsg('Game request list cleared')
      logging.info('Game request list cleared by %s' %nick)
      storage.save('Game request cleared')
   elif msg == 'show':
      print 'Games requested'
      game = sorted(request, key=request.get, reverse=True)
      for name in game:
         print name
   elif msg in request:
      request[msg]+=1
      bot.sendmsg('Game request registered')
      logging.info('Game request for %s registered by %s' %(msg, nick))
      storage.save('Game request added')
   else:
      request[msg]=1
      bot.sendmsg('Game request registered')
      logging.info('Game request for %s registered by %s' %(msg, nick))
      storage.save('Game request added')

#Called by ircbot
def edit_response(nick, msg, msgcap, data):
   if msg[1] == 'add':
      msg[4] = ' '.join(msgcap[4:])
      add_response(nick, msg[2], msg[3], msg[4], data)
   elif msg[1] == 'remove':
      remove_response(nick, msg[2], data)

#Add Static response
@utils.mod_only
def add_response(nick, access, command, msg, data):
   try:
      if access not in ['admin','mod','all']:
         raise ValueError('Access Syntax Error:')
      data[command]={'access': access, 'response': msg}
      storage.save('Command Added')
      bot.sendmsg('New command added: Command: %s , Response: %s' %(command, msg))
      logging.info('New command added: Access: %s, Command: %s, Response: %s , Triggered by %s' %(access, command, msg, nick))
   except ValueError as e:
      logging.error('%s Access must be either admin, mod, or all' %e)
      print '%s Access must be either admin, mod, or all' %e
      bot.sendmsg('Syntax Must Be: !response add [admin/mod/all] [command] [Message]')

#Remove Static response
@utils.mod_only
def remove_response(nick, command, data):
   try:
      access = data[command]['access']
      msg = data[command]['response']
      del data[command]
      storage.save('Command Removed')
      bot.sendmsg('Command Removed: Command: %s , Response: %s' %(command, msg))
      logging.info('Command Removed: Access: %s, Command: %s,  Response: %s, Triggered by %s' %(access, command, msg, nick))
   except KeyError:
      logging.error('Delete attempt failed: %s command not found. Triggered by %s' %(command, nick))

#Add to ban list
@utils.mod_only
def botban(nick, msg, data):
   if msg[0] == 'ban':
      data.setdefault('banlist',[])
      data['banlist'].append(' '.join(msg[1:]))
      logging.info('%s Banned from bot usage by %s' %(' '.join(msg[1:]),nick))
      bot.sendmsg('%s Banned from bot usage by %s' %(' '.join(msg[1:]),nick))
   elif msg[0] == 'unban':
      data['banlist'].remove(' '.join(msg[1:]))
      logging.info('%s removed from ban list by %s' %(' '.join(msg[1:]),nick))
      bot.sendmsg('%s removed from ban list by %s' %(' '.join(msg[1:]),nick))

@utils.throttle(5)
def make_highlight(nick, msg):
   try:
      msg = ' '.join(msg[1:])
      highlight = highlights.highlight()
      #Get path to game in data
      game = bot.get_current_game(nick)
      date = time.strftime("%m/%d/%Y")
      #Confirms location to save highlight and set up if missing
      game.setdefault('highlights', {}).setdefault(date, [])
      #Save Highlight
      game['highlights'][date].append({'link':highlight, 'tag':msg})

      #send confirmation
      logging.info('Highlight Created by %s, tagged: %s' %(nick, msg))
      bot.sendmsg('Highlight Created')
      print 'Highlight: %s - %s' %(msg, highlight)
      storage.save('Highlight')
   except TypeError as e:
      print e
      bot.sendmsg('Stream is not live')
      
def uptime():
   try:
      uptime = highlights.get_uptime()
      bot.sendmsg('The stream has been live for %i:%i:%i' %(uptime['hours'], uptime['minutes'], uptime['seconds']))
   except TypeError as e:
      bot.sendmsg('Stream is not live')
