# Import some necessary libraries.
import socket, threading, re, linecache, sys
import stats, commands, storage, twitch,utils
from sendemail import send_email, load
from quote import quote

import logging
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S',
                    filename='botlogs.log',level=logging.DEBUG)
class ircbot():
   def __init__(self):
      # Some basic variables used to configure the bot
      self.version = 2.00
      self.password = load('twitch')

      self.currentgame = None
      self.game_override = None
      self.show_override = None
      self.pollchoices = None
      self.lockdown = False
      self.voting = False
      self.norespond = True
      self.startupcheck = True
      self.spam_rules = []
      self.spammers = {}
      self.ismod = False
      self.ircmsg=None
      self.channeldata = None

   def startup(self, channel='admiralmatt',botnick='Rab_bot',server='irc.twitch.tv'):
      #can't be done in __init__ so compiled here
      logging.info('\n\nBot Startup\nVersion: %s' %self.version)
      logging.info('Connecting to channel: %s' %str(channel))
      self.spam_rules = [(re.compile(i['re']), i['message']) for i in storage.data['spam_rules']]
      
      self.channel = '#' + str(channel.lower())
      self.server = server
      self.botnick = botnick
      self.show = str(channel.lower())
      self.modlist = ['admiralmatt']

      self.makesock()
      self.connect()
      self.channeldata = storage.getchanneldata()
      self.startthread()
      self.sendmsg('/mods')
      self.get_current_game(botnick)
      self.startupcheck = False
      print 'Connected to channel: %s' %str(channel)

   def makesock(self):
      self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   def joinchan(self, channel): # Join channel.
      self.ircsock.send('CAP REQ :twitch.tv/commands\r\n')
      self.ircsock.send('JOIN ' + channel +'\r\n')

   #connect to the irc server.
   def connect(self):
      try:
          self.ircsock.connect((self.server, 6667)) # Connect to the server using the port 6667
      except Exception as e:
          logging.error('Can Not Connect To Server!\n' + e)
          print 'Can Not Connect To Server!'
          print e

         #connecting to twitch requires a password
      if self.server == 'irc.twitch.tv':
         self.ircsock.send('PASS ' + self.password + '\r\n')

      self.ircsock.send('USER ' + self.botnick + ' 0 * :' + self.botnick + '\r\n')
      self.ircsock.send('NICK '+ self.botnick +'\r\n') # Assign the nick to the bot
      self.joinchan(self.channel) # Join the channel

   #start to read the chat commands
   def start(self):
      while 1:# Stay connected to the server and find commands
         try:
            ircmsg = self.ircsock.recv(4096) # Receive data from the server
            if len(ircmsg) == 0 or len(ircmsg) == None:
               logging.error('Socket error from twitch')
               print 'Socket error from twitch'
               send_email('No Data From Twitch') #send error report to bot email
               raise
#            print(ircmsg) # Print what's coming from the server
            if ircmsg.find(' PRIVMSG ') != -1:
               nick = ircmsg.split('!')[0][1:]
               channel = ircmsg.split(' PRIVMSG ')[-1].split(' :')[0]
               self.channel = channel
               self.command(nick, channel, ircmsg.lower(), ircmsg)
               #ircmsg.lower = makes all commands lower-case

            if ircmsg.find('PING :') != -1: # Responds to server ping
               self.ircsock.send('PONG :pingis\n')
            
            if ircmsg.find(' NOTICE ') != -1: # Responds to server ping
               self.modcheck(ircmsg)
         
         #To end thread without error

         except socket.error as error:
            print error
            self.ircsock.close()
            storage.save()
            printexception()
            quit()
            
         except Exception as e:
            print type(e)
            printexception()
            logging.error('Thread Error\n%s\nLast message sent:%s' %(e,ircmsg))
            send_email(str(e), ircmsg) #send error report to bot email

         
   def startthread(self):
      try:
         global thread
         thread = threading.Thread(target=self.start, name='chatlog')
         thread.daemon = True
         thread.start()
      except Exception as e:
         logging.error('Error: unable to start thread\n' + e)
         print 'Error: unable to start thread'
         print e

   def sendmsg(self, msg, nick = None): # Send messages to the channel.
      if self.norespond != True:
         if nick is None:
            self.ircsock.send('PRIVMSG '+ self.channel +' :' + msg +'\n')
            logging.info('Message: %s sent' % msg)
         else:
            self.ircsock.send('PRIVMSG '+ self.channel +' :' + nick + ': ' + msg +'\n')
            logging.info('Message: %s sent' % msg)
      else:
         logging.info('Message: %s not sent, bot is muted.' % msg)

   def get_current_game(self, nick):
      #Returns the game currently being played, with caching to avoid hammering the Twitch server
      try:
         channel = self.show_override or self.show
         if self.game_override is not None:
            game_obj = {'_id': self.game_override, 'name': self.game_override, 'is_override': True}
            return storage.findgame(game_obj)
         else:
            return storage.findgame(twitch.get_live_game(nick, self.channel))
      except UnicodeError as e:
         logging.error('Unicode error in game title\n%s' %e)

   #get a list of current mods on the stream
   def modcheck(self, message):
      if message.find(':The moderators of this room are:') != -1:
         modlist = storage.getmodlist()
         self.modlist = message.strip('\r\n').split('are: ')[-1].split(', ') + ['admiralmatt',self.show]
         modlist['mods'] = self.modlist
         logging.info('Mod list updated')
         if self.botnick.lower() in self.modlist:
            self.ismod = True
         storage.save('Mod Update')


   # Search for correct command to use
   def is_command(self, nick, msg, msgcap):
      try:
         data = storage.data
         if msg[0] == 'shutdown':
            commands.bot_shutdown(nick, msg)
            
         try:
            if nick in bot.channeldata['banlist']:
               return

            if msg[1] == 'new' and msg[0] not in bot.channeldata['showstats']:
               stats.change(nick, msg[0], msg[1])
               return
         except IndexError:
            pass
         except KeyError:
            pass

         if msg[0] in bot.channeldata['showstats']:
            if len(msg) is not 3:
               msg.extend([None] * 3)
            stats.change(nick, msg[0], msg[1], msg[2])

         elif msg[0] == 'game':
            commands.gamecheck(nick, msg, msgcap.split(':!')[-1].split())
            
         elif msg[0] == 'stats':
            stats.statcheck(nick, bot.channeldata)

         elif msg[0] == 'quote':
            quote(nick, msgcap.split(':!')[-1].split(), bot.channeldata['quotes'])

         elif msg[0] == 'vote':
            commands.comm_vote(nick, msg, msgcap.split(':!')[-1].split())

         elif msg[0] in ['request','gamerequest']:
            commands.game_request(nick,' '.join(msg[1:]))

         elif msg[0] == 'response':
            commands.edit_response(nick, msg, msgcap.split(':!')[-1].split(), bot.channeldata['showresponse'])

         elif msg[0] in ['ban','unban']:
            commands.botban(nick, msg, bot.channeldata)

         elif msg[0] == 'uptime':
            commands.uptime()

         elif msg[0] == 'highlight':
            commands.make_highlight(nick, msgcap.split(':!')[-1].split())
            
         elif msg[0] == 'lockdown':
            commands.lockdown(nick, msg, bot.channeldata)

         #Mods only
         elif msg[0] == 'norespond':
            if nick in self.modlist:
               try:
                  if msg[1] == 'off':
                     self.norespond = False
                     logging.info('Bot unmuted by %s' %nick)
               except IndexError:
                  self.norespond = True
                  logging.info('Bot muted by %s' %nick)
                  
         elif msg[0] in bot.channeldata['showresponse']:
            commands.send_response(nick, msg[0], bot.channeldata['showresponse'][msg[0]])
         
         elif msg[0] in data['responses']:
            commands.send_response(nick, msg[0], data['responses'][msg[0]])

      except IndexError:
         pass
            
   # Decide if a command has been entered
   def command(self, nick, channel, message, msgcap):
      self.get_current_game(self.botnick)
      if message.find(':!') != -1 and self.lockdown == False:
         self.is_command(nick, message.split(':!')[-1].split(), msgcap)

      elif message.find(':!') != -1 and self.lockdown == True:
         commands.lockdown_mode(nick, message.split(':!')[-1].split(), msgcap)

      elif self.ismod == True:
         self.spam_check(nick, message)
         
   def spam_check(self, nick, msg):
      for re, desc in self.spam_rules:
         matches = re.search(msg)
         if matches:
            logging.info('Spam detected, username:%s,Message:%s' %(nick, msg))
            groups = {str(i+1):v for i,v in enumerate(matches.groups())}
            desc = desc % groups
            self.spammers.setdefault(nick, 0)
            self.spammers[nick] += 1
            level = self.spammers[nick]
            if level <= 1:
               self.sendmsg('/timeout %s 1' % nick)
               self.sendmsg('%s: Message deleted (first warning) for auto-detected spam (%s). Please contact Admiralmatt if this is incorrect.' % (nick, desc))
            elif level <= 2:
               self.sendmsg('/timeout %s' % nick)
               self.sendmsg('%s: Timeout (second warning) for auto-detected spam (%s). Please contact Admiralmatt if this is incorrect.' % (nick, desc))
            else:
               self.sendmsg('/ban %s' % nick)
               self.sendmsg('%s: Banned for persistent spam (%s). Please contact Admiralmatt if this is incorrect.' % (nick, desc))
               level = 3
            return True

def printexception():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
    logging.error('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
            
bot = ircbot()
