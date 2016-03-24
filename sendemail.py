import base64,zlib
import json

from drive import drivelogin
import storage
import logging
from datetime import datetime


def load(twitch = None):
    drive = drivelogin()
    login = json.loads(drive)
    if twitch is 'twitch':
        return login['twitchlogin']
    return login

def send_email(msg, last= 'No Msg Found', sub= 'Bot Error'):
    from ircbot import bot
    time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    import smtplib
    zd_b64d = lambda s: zlib.decompress(base64.decodestring(s))
    gmail_user = zd_b64d(login['email'])#enter email address to send from
    gmail_pwd = zd_b64d(login['emailpassword'])#enter email password

    savedata = storage.data    
    FROM = gmail_user
    TO = [gmail_user] #Enter destination email
    SUBJECT = sub #Enter text of email
    TEXT = 'Bot Version: %s \n\n%s \n\n%s \n\nConnected to channel %s \n\nLast message sent: %s \n\nSave Data:\n%s' %(bot.version, msg, time, bot.channel, last, str(savedata))
           # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        #server = smtplib.SMTP(SERVER)
        server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        logging.info('successfully sent the mail')
        print 'successfully sent the mail'
    except Exception as e:
        logging.error('failed to send mail')
        print "failed to send mail"
        print e
            
login = load()



