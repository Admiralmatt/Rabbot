# Import some necessary libraries.
import socket
import threading

import stats
import storage
from sendemail import send_email, load
import twitch
import commands
import utils


class ircbot():

   def __init__(self):
      # Some basic variables used to configure the bot
      self.password = load('twitch')

      self.threadquit = False

      self.currentgame = None
      self.game_override = None
      self.show_override = None

   def startup(self, channel='admiralmatt',botnick='Rab_bot',server='irc.twitch.tv'):
      self.channel = '#' + str(channel)
      self.server = server
      self.botnick = botnick
      self.show = str(channel)
      self.modlist = None

      self.makesock()
      self.connect()
      self.startthread()
      self.sendmsg('/mods')

   def makesock(self):
      self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   def joinchan(self): # Join channel.
      self.ircsock.send('JOIN ' + self.channel +'\r\n')

   #connect to the irc server.
   def connect(self):
      try:
          self.ircsock.connect((self.server, 6667)) # Connect to the server using the port 6667
      except Exception as e:
          print 'Can Not Connect To Server!'
          print e
          self.makesock()

         #connecting to twitch requires a password
      if self.server == 'irc.twitch.tv':
         self.ircsock.send('PASS ' + self.password + '\r\n')

      self.ircsock.send('USER ' + self.botnick + ' 0 * :' + self.botnick + '\r\n')
      self.ircsock.send('NICK '+ self.botnick +'\r\n') # Assign the nick to the bot
      self.joinchan() # Join the channel

   #start to read the chat commands
   def start(self):
      while 1: # Stay connected to the server and find commands
         try:
            ircmsg = self.ircsock.recv(4096) # Receive data from the server
            print(ircmsg) # Print what's coming from the server
            if ircmsg.find(' PRIVMSG ') != -1:
               nick = ircmsg.split('!')[0][1:]
               channel = ircmsg.split(' PRIVMSG ')[-1].split(' :')[0]
               self.command(nick, channel, ircmsg.lower()) #ircmsg.lower = makes all commands lowercase

            if ircmsg.find('PING :') != -1: # Responds to server ping
               self.ircsock.send('PONG :pingis\n')

            elif ircmsg.find(':jtv MODE ' + self.channel) != -1:
               self.modcheck(ircmsg.split(self.channel + ' ')[-1].split(' '))


         #To end thread without error
         except Exception as e:
            if self.threadquit == True:
               break
            '''
            print 'Out Of Loop' #in case of error
            print e
            send_email(str(e)) #send error report to bot email
            break
            '''

#MUST CATCH USERNAME TAKEN ERROR


   def startthread(self):
      try:
         global thread
         thread = threading.Thread(target=self.start, name="chatlog")
         thread.daemon = True
         thread.start()
      except Exception as e:
            print "Error: unable to start thread"
            print e

   def sendmsg(self, msg, nick = None): # Send messages to the channel.
      if nick is None:
         self.ircsock.send('PRIVMSG '+ self.channel +' :' + msg +'\n')
      else:
         self.ircsock.send('PRIVMSG '+ self.channel +' :' + nick + ': ' + msg +'\n')


   def get_current_game(self, nick):
      #Returns the game currently being played, with caching to avoid hammering the Twitch server

      channel = self.show_override or self.show
      if self.game_override is not None:
         game_obj = {'_id': self.game_override, 'name': self.game_override, 'is_override': True}
         return storage.findgame(game_obj)
      else:
         return storage.findgame(twitch.get_live_game(nick))

   # Search for correct command to use
   def is_command(self, nick, msg):
      data = storage.data

      if msg[0] == 'bot_close':
         commands.bot_close(nick)
      try:
         if msg[1] == 'new' and msg[0] not in data['allstats']:
            print 'New Stat'
            stats.change(nick, msg[0], msg[1])
            return
      except IndexError:
         pass

      if msg[0] in data['allstats']:
         if len(msg) is not 3:
            msg.extend([None] * 3)
         print 'Change Stats %s' % msg
         stats.change(nick, msg[0], msg[1], msg[2])

      elif msg[0] == 'game':
         commands.gamecheck(nick, msg)

      elif msg[0] in data['responses']:
         commands.send_response(nick, msg[0], data['responses'][msg[0]])


   # Decide if a command has been entered
   def command(self, nick, channel, message):
      if message.find(':!') != -1:
         self.is_command(nick, message.split(':!')[-1].split())

      elif message.find(':jtv!jtv@jtv.tmi.twitch.tv privmsg rab_bot :the moderators of this room are:') != -1:
         modlist = storage.getmodlist()
         self.modlist = message.strip('\r\n').split('are: ')[-1].split(', ') + ['admiralmatt']
         modlist['mods'] = self.modlist
         self.sendmsg('Mod list updated')
         storage.save()




bot = ircbot()







