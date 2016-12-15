from twitch import url_open, get_info
import json, datetime
import logging

def get_current_video_id(channel, nick = None):
    url='https://api.twitch.tv/kraken/channels/%s/videos' %channel
    options='broadcasts=true'
    res = url_open(url,options)
    res = json.loads(res)
    video_id = res['videos'][0]['_id']
    return 'https://www.twitch.tv/%s/v/%s' %(channel, video_id)

def get_uptime():
    # Get uptime and generate link to VOD
    current_time = datetime.datetime.utcnow()
    channel_data = get_info()
    start_time = channel_data['stream_created_at']
    # u'2016-11-23T13:15:46Z'
    start_time = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")
    
    difference = current_time - start_time
    minutes, seconds = divmod(difference.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return {'hours':hours, 'minutes':minutes, 'seconds':seconds}
    

def highlight():
    try:
        channel_data = get_info()
        uptime = get_uptime()
        VOD_link = get_current_video_id(channel = channel_data['display_name'])
        #https://www.twitch.tv/loadingreadyrun/v/98781251?t=1h3m15s
        highlight = VOD_link + '?t=%sh%sm%ss' %(uptime['hours'], uptime['minutes'], uptime['seconds'])
        return highlight
    except TypeError as e:
        bot.sendmsg('Stream is not live')
    
        
#z=datetime.strptime(a, "%Y-%m-%dT%H:%M:%SZ")
#http://stackoverflow.com/questions/21378977/compare-two-timestamps-in-python
'''
>>> z=datetime.datetime.strptime(a, "%Y-%m-%dT%H:%M:%SZ")
>>> z
datetime.datetime(2016, 11, 23, 13, 15, 46)
>>> a
u'2016-11-23T13:15:46Z'
'''
