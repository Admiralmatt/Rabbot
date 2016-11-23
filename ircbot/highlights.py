from twitch import url_open
import json

def get_current_video_id(nick, channel):
    url='https://api.twitch.tv/kraken/channels/%s/videos' %channel
    options='broadcasts=true'
    res = url_open(url,options)
    res = jason.loads(res)
    video_id = res['videos'][0]['_id']
    return 'https://www.twitch.tv/%s/v/%s' %(channel, video_id)

def test():
    # Get time and generate link to VOD
    pass
#z=datetime.strptime(a, "%Y-%m-%dT%H:%M:%SZ")
#http://stackoverflow.com/questions/21378977/compare-two-timestamps-in-python
'''
>>> z=datetime.datetime.strptime(a, "%Y-%m-%dT%H:%M:%SZ")
>>> z
datetime.datetime(2016, 11, 23, 13, 15, 46)
>>> a
u'2016-11-23T13:15:46Z'
'''
