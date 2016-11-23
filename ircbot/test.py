Python 2.7.12 (v2.7.12:d33e0cf91556, Jun 27 2016, 15:19:22) [MSC v.1500 32 bit (Intel)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> 
======== RESTART: C:\Users\mreed\Desktop\Rabbot\ircbot\highlights.py ========

Traceback (most recent call last):
  File "C:\Users\mreed\Desktop\Rabbot\ircbot\highlights.py", line 1, in <module>
    from twitch import url_open
  File "C:\Users\mreed\Desktop\Rabbot\ircbot\twitch.py", line 4, in <module>
    import ircbot
  File "C:\Users\mreed\Desktop\Rabbot\ircbot\ircbot.py", line 4, in <module>
    import stats
  File "C:\Users\mreed\Desktop\Rabbot\ircbot\stats.py", line 1, in <module>
    import storage
  File "C:\Users\mreed\Desktop\Rabbot\ircbot\storage.py", line 3, in <module>
    import drive
  File "C:\Users\mreed\Desktop\Rabbot\ircbot\drive.py", line 2, in <module>
    from pydrive.auth import GoogleAuth
ImportError: No module named pydrive.auth
>>> def url_open(url, data = None):
    if isinstance(data, dict):
        data['query']=urllib.quote(data['query'].encode('utf-8'), safe='/:')
        data = urllib.urlencode(data)
        data=urllib.unquote(data)
    header = 'client_id=nigr9qrlruvvbymiitss8t7ozl4ejip'
    url = '%s?%s&%s' % (url, data, header)
    response = urllib2.urlopen(url)
    html = response.read()
    return html

>>> json

Traceback (most recent call last):
  File "<pyshell#2>", line 1, in <module>
    json
NameError: name 'json' is not defined
>>> import json
>>> def get_info(username = None, use_fallback = False):
    # Attempt to get the channel data from /streams/channelname
    # If this succeeds, it means the channel is currently live
    res = url_open("https://api.twitch.tv/kraken/streams/%s" % username)
    data = json.loads(res)
    channel_data = data.get('stream') and data['stream'].get('channel')
    if channel_data:
        channel_data['live'] = True
        channel_data['viewers'] = data['stream'].get('viewers')
        channel_data['stream_created_at'] = data['stream'].get('created_at')
        return channel_data
    
    if not use_fallback:
        return None
    
    # If that failed, it means the channel is offline
    # Get the channel data from here instead
    logging.info('Using Fallback For Offline Channel')
    res = url_open("https://api.twitch.tv/kraken/channels/%s" % username)
    channel_data = json.loads(res)
    channel_data['live'] = False
    return channel_data


def get_game(name, all = False):
        """
        Get the game information for a particular game.

        For response object structure, see:
        https://github.com/justintv/Twitch-API/blob/master/v3_resources/search.md#example-response-1

        May throw exceptions on network/Twitch error.
        """
        search_opts = {
                'query': name,
                'type': 'suggest',
                'live': 'false',
        }
        res = url_open("https://api.twitch.tv/kraken/search/games", search_opts)
        res = json.loads(res)
        if all:
            res['games'][0]['name']= res['games'][0]['name'].encode('utf8') 
            return res['games']
        else:
            for game in res['games']:
                if game['name'] == name:
                    game['name']= game['name'].encode('utf8')
                    return game
            return None


def get_game_playing(username = None):
    """
    Get the game information for the game the stream is currently playing
    """
    if username is None:
        username = ircbot.bot.show

    
    channel_data = get_info(username, use_fallback=False)
    if not channel_data or not channel_data['live']:
        #return None
        channel_data = get_info(username, use_fallback=True)
        
#might want to return None here
    if channel_data['game'] is not None:
        return get_game(name=channel_data['game'])
    return None

@utils.throttle(GAME_CHECK_INTERVAL)
def get_live_game(nick, channel):
    return get_game_playing()



SyntaxError: invalid syntax
>>> def get_info(username = None, use_fallback = False):
    # Attempt to get the channel data from /streams/channelname
    # If this succeeds, it means the channel is currently live
    res = url_open("https://api.twitch.tv/kraken/streams/%s" % username)
    data = json.loads(res)
    channel_data = data.get('stream') and data['stream'].get('channel')
    if channel_data:
        channel_data['live'] = True
        channel_data['viewers'] = data['stream'].get('viewers')
        channel_data['stream_created_at'] = data['stream'].get('created_at')
        return channel_data

    if not use_fallback:
        return None

    # If that failed, it means the channel is offline
    # Get the channel data from here instead
    logging.info('Using Fallback For Offline Channel')
    res = url_open("https://api.twitch.tv/kraken/channels/%s" % username)
    channel_data = json.loads(res)
    channel_data['live'] = False
    return channel_data


def get_game(name, all = False):
        """
        Get the game information for a particular game.

        For response object structure, see:
        https://github.com/justintv/Twitch-API/blob/master/v3_resources/search.md#example-response-1

        May throw exceptions on network/Twitch error.
        """
        search_opts = {
                'query': name,
                'type': 'suggest',
                'live': 'false',
        }
        res = url_open("https://api.twitch.tv/kraken/search/games", search_opts)
        res = json.loads(res)
        if all:
            res['games'][0]['name']= res['games'][0]['name'].encode('utf8')
            return res['games']
        else:
            for game in res['games']:
                if game['name'] == name:
                    game['name']= game['name'].encode('utf8')
                    return game
            return None


def get_game_playing(username = None):
    """
    Get the game information for the game the stream is currently playing
    """
    if username is None:
        username = ircbot.bot.show


    channel_data = get_info(username, use_fallback=False)
    if not channel_data or not channel_data['live']:
        #return None
        channel_data = get_info(username, use_fallback=True)

#might want to return None here
    if channel_data['game'] is not None:
        return get_game(name=channel_data['game'])
    return None

@utils.throttle(GAME_CHECK_INTERVAL)
def get_live_game(nick, channel):
    return get_game_playing()
SyntaxError: invalid syntax
>>> @utils.throttle(GAME_CHECK_INTERVAL)
def get_live_game(nick, channel):
    return get_game_playing()


Traceback (most recent call last):
  File "<pyshell#7>", line 1, in <module>
    @utils.throttle(GAME_CHECK_INTERVAL)
NameError: name 'utils' is not defined
>>> NameError: name 'utils' is not defined
SyntaxError: invalid syntax
>>> 
>>> def get_info(username = None, use_fallback = False):
    # Attempt to get the channel data from /streams/channelname
    # If this succeeds, it means the channel is currently live
    res = url_open("https://api.twitch.tv/kraken/streams/%s" % username)
    data = json.loads(res)
    channel_data = data.get('stream') and data['stream'].get('channel')
    if channel_data:
        channel_data['live'] = True
        channel_data['viewers'] = data['stream'].get('viewers')
        channel_data['stream_created_at'] = data['stream'].get('created_at')
        return channel_data
    
    if not use_fallback:
        return None
    
    # If that failed, it means the channel is offline
    # Get the channel data from here instead
    logging.info('Using Fallback For Offline Channel')
    res = url_open("https://api.twitch.tv/kraken/channels/%s" % username)
    channel_data = json.loads(res)
    channel_data['live'] = False
    return channel_data


def get_game(name, all = False):
        """
        Get the game information for a particular game.

        For response object structure, see:
        https://github.com/justintv/Twitch-API/blob/master/v3_resources/search.md#example-response-1

        May throw exceptions on network/Twitch error.
        """
        search_opts = {
                'query': name,
                'type': 'suggest',
                'live': 'false',
        }
        res = url_open("https://api.twitch.tv/kraken/search/games", search_opts)
        res = json.loads(res)
        if all:
            res['games'][0]['name']= res['games'][0]['name'].encode('utf8') 
            return res['games']
        else:
            for game in res['games']:
                if game['name'] == name:
                    game['name']= game['name'].encode('utf8')
                    return game
            return None


def get_game_playing(username = None):
    """
    Get the game information for the game the stream is currently playing
    """
    if username is None:
        username = ircbot.bot.show
        
SyntaxError: invalid syntax
>>> search/games", search_opts)
        res = json.loads(res)
        
SyntaxError: EOL while scanning string literal
>>> 
>>> 
>>> def get_info(username = None, use_fallback = False):
    # Attempt to get the channel data from /streams/channelname
    # If this succeeds, it means the channel is currently live
    res = url_open("https://api.twitch.tv/kraken/streams/%s" % username)
    data = json.loads(res)
    channel_data = data.get('stream') and data['stream'].get('channel')
    if channel_data:
        channel_data['live'] = True
        channel_data['viewers'] = data['stream'].get('viewers')
        channel_data['stream_created_at'] = data['stream'].get('created_at')
        return channel_data
    
    if not use_fallback:
        return None

>>> def get_info(username = None, use_fallback = False):
    # Attempt to get the channel data from /streams/channelname
    # If this succeeds, it means the channel is currently live
    res = url_open("https://api.twitch.tv/kraken/streams/%s" % username)
    data = json.loads(res)
    channel_data = data.get('stream') and data['stream'].get('channel')
    if channel_data:
        channel_data['live'] = True
        channel_data['viewers'] = data['stream'].get('viewers')
        channel_data['stream_created_at'] = data['stream'].get('created_at')
        return channel_data

    if not use_fallback:
        return None

>>> 
>>>     
    # If that failed, it means the channel is offline
    # Get the channel data from here instead
    logging.info('Using Fallback For Offline Channel')
    res = url_open("https://api.twitch.tv/kraken/channels/%s" % username)
    channel_data = json.loads(res)
    channel_data['live'] = False
    return channel_data
  File "<pyshell#19>", line 5
    logging.info('Using Fallback For Offline Channel')
    ^
IndentationError: unexpected indent
>>> 
>>> # If that failed, it means the channel is offline
# Get the channel data from here instead
logging.info('Using Fallback For Offline Channel')
res = url_open("https://api.twitch.tv/kraken/channels/%s" % username)
channel_data = json.loads(res)
channel_data['live'] = False
return channel_data

Traceback (most recent call last):
  File "<pyshell#21>", line 3, in <module>
    logging.info('Using Fallback For Offline Channel')
NameError: name 'logging' is not defined
>>> l')
NameError: name 'logging' is not defined
SyntaxError: EOL while scanning string literal
>>> 
>>> def get_info(username = None, use_fallback = False):
    # Attempt to get the channel data from /streams/channelname
    # If this succeeds, it means the channel is currently live
    res = url_open("https://api.twitch.tv/kraken/streams/%s" % username)
    data = json.loads(res)
    channel_data = data.get('stream') and data['stream'].get('channel')
    if channel_data:
        channel_data['live'] = True
        channel_data['viewers'] = data['stream'].get('viewers')
        channel_data['stream_created_at'] = data['stream'].get('created_at')
        return channel_data
    
    if not use_fallback:
        return None
    
    # If that failed, it means the channel is offline
    # Get the channel data from here instead
    logging.info('Using Fallback For Offline Channel')
    res = url_open("https://api.twitch.tv/kraken/channels/%s" % username)
    channel_data = json.loads(res)
    channel_data['live'] = False
    return channel_data

>>> def get_game(name, all = False):
        """
        Get the game information for a particular game.

        For response object structure, see:
        https://github.com/justintv/Twitch-API/blob/master/v3_resources/search.md#example-response-1

        May throw exceptions on network/Twitch error.
        """
        search_opts = {
                'query': name,
                'type': 'suggest',
                'live': 'false',
        }
        res = url_open("https://api.twitch.tv/kraken/search/games", search_opts)
        res = json.loads(res)
        if all:
            res['games'][0]['name']= res['games'][0]['name'].encode('utf8') 
            return res['games']
        else:
            for game in res['games']:
                if game['name'] == name:
                    game['name']= game['name'].encode('utf8')
                    return game
            return None

        
>>> 
>>> 
>>> def get_game_playing(username = None):
    """
    Get the game information for the game the stream is currently playing
    """
    if username is None:
        username = ircbot.bot.show

    
    channel_data = get_info(username, use_fallback=False)
    if not channel_data or not channel_data['live']:
        #return None
        channel_data = get_info(username, use_fallback=True)
        
#might want to return None here
    if channel_data['game'] is not None:
        return get_game(name=channel_data['game'])
    return None


>>> 
>>> 
>>> def get_current_video_id(nick, channel):
    url='https://api.twitch.tv/kraken/channels/%s/videos' %channel
    options='broadcasts=true'
    res = url_open(url,options)
    res = jason.loads(res)
    video_id = res['videos'][0]['_id']
    return 'https://www.twitch.tv/%s/v/%s' %(channel, video_id)


>>> get_current_video_id
<function get_current_video_id at 0x02C83130>
>>> get_current_video_id()

Traceback (most recent call last):
  File "<pyshell#35>", line 1, in <module>
    get_current_video_id()
TypeError: get_current_video_id() takes exactly 2 arguments (0 given)
>>> get_game('portal')

Traceback (most recent call last):
  File "<pyshell#36>", line 1, in <module>
    get_game('portal')
  File "<pyshell#27>", line 15, in get_game
    res = url_open("https://api.twitch.tv/kraken/search/games", search_opts)
  File "<pyshell#1>", line 3, in url_open
    data['query']=urllib.quote(data['query'].encode('utf-8'), safe='/:')
NameError: global name 'urllib' is not defined
>>> import urllib,urllib2
>>> get_game('portal')
>>> q=get_game('portal')
>>> q
>>> print get_game('portal')
None
>>> q=get_info('faceittv')
>>> q
{u'updated_at': u'2016-11-23T21:30:15Z', u'video_banner': u'https://static-cdn.jtvnw.net/jtv_user_pictures/faceittv-channel_offline_image-d6d794fd189dc076-1920x1080.jpeg', u'logo': u'https://static-cdn.jtvnw.net/jtv_user_pictures/faceittv-profile_image-45e9e95c0f48f50e-300x300.jpeg', u'partner': True, u'display_name': u'FACEIT TV', 'stream_created_at': u'2016-11-23T13:15:46Z', u'delay': None, 'live': True, u'followers': 836656, u'_links': {u'videos': u'http://api.twitch.tv/kraken/channels/faceittv/videos', u'stream_key': u'http://api.twitch.tv/kraken/channels/faceittv/stream_key', u'subscriptions': u'http://api.twitch.tv/kraken/channels/faceittv/subscriptions', u'follows': u'http://api.twitch.tv/kraken/channels/faceittv/follows', u'self': u'http://api.twitch.tv/kraken/channels/faceittv', u'commercial': u'http://api.twitch.tv/kraken/channels/faceittv/commercial', u'editors': u'http://api.twitch.tv/kraken/channels/faceittv/editors', u'teams': u'http://api.twitch.tv/kraken/channels/faceittv/teams', u'chat': u'http://api.twitch.tv/kraken/chat/faceittv'}, u'broadcaster_language': u'en', u'status': u'ECS Season 2 Europe - G2 vs FaZe Clan', u'views': 128187849, u'game': u'Counter-Strike: Global Offensive', u'background': None, u'banner': None, 'viewers': 39509, u'name': u'faceittv', u'language': u'en', u'url': u'https://www.twitch.tv/faceittv', u'created_at': u'2012-02-03T20:17:51Z', u'mature': False, u'profile_banner_background_color': None, u'_id': 27942990, u'profile_banner': u'https://static-cdn.jtvnw.net/jtv_user_pictures/faceittv-profile_banner-1ef361661c41e8f3-480.png'}
>>> q.keys()
[u'updated_at', u'video_banner', u'logo', u'partner', u'display_name', 'stream_created_at', u'delay', 'live', u'followers', u'_links', u'broadcaster_language', u'status', u'views', u'game', u'background', u'banner', 'viewers', u'name', u'language', u'url', u'created_at', u'mature', u'profile_banner_background_color', u'_id', u'profile_banner']
>>> get_info('faceittv')
{u'updated_at': u'2016-11-23T21:30:15Z', u'video_banner': u'https://static-cdn.jtvnw.net/jtv_user_pictures/faceittv-channel_offline_image-d6d794fd189dc076-1920x1080.jpeg', u'logo': u'https://static-cdn.jtvnw.net/jtv_user_pictures/faceittv-profile_image-45e9e95c0f48f50e-300x300.jpeg', u'partner': True, u'display_name': u'FACEIT TV', 'stream_created_at': u'2016-11-23T13:15:46Z', u'delay': None, 'live': True, u'followers': 836656, u'_links': {u'videos': u'http://api.twitch.tv/kraken/channels/faceittv/videos', u'stream_key': u'http://api.twitch.tv/kraken/channels/faceittv/stream_key', u'subscriptions': u'http://api.twitch.tv/kraken/channels/faceittv/subscriptions', u'follows': u'http://api.twitch.tv/kraken/channels/faceittv/follows', u'self': u'http://api.twitch.tv/kraken/channels/faceittv', u'commercial': u'http://api.twitch.tv/kraken/channels/faceittv/commercial', u'editors': u'http://api.twitch.tv/kraken/channels/faceittv/editors', u'teams': u'http://api.twitch.tv/kraken/channels/faceittv/teams', u'chat': u'http://api.twitch.tv/kraken/chat/faceittv'}, u'broadcaster_language': u'en', u'status': u'ECS Season 2 Europe - G2 vs FaZe Clan', u'views': 128187849, u'game': u'Counter-Strike: Global Offensive', u'background': None, u'banner': None, 'viewers': 40037, u'name': u'faceittv', u'language': u'en', u'url': u'https://www.twitch.tv/faceittv', u'created_at': u'2012-02-03T20:17:51Z', u'mature': False, u'profile_banner_background_color': None, u'_id': 27942990, u'profile_banner': u'https://static-cdn.jtvnw.net/jtv_user_pictures/faceittv-profile_banner-1ef361661c41e8f3-480.png'}
>>> def get_info(username = None, use_fallback = False):
    # Attempt to get the channel data from /streams/channelname
    # If this succeeds, it means the channel is currently live
    res = url_open("https://api.twitch.tv/kraken/streams/%s" % username)
    data = json.loads(res)
    channel_data = data.get('stream') and data['stream'].get('channel')
    if channel_data:
        channel_data['live'] = True
        channel_data['viewers'] = data['stream'].get('viewers')
        channel_data['stream_created_at'] = data['stream'].get('created_at')
        return channel_data
    
    if not use_fallback:
        return None

>>> get_info('faceittv')
{u'updated_at': u'2016-11-23T21:30:15Z', u'video_banner': u'https://static-cdn.jtvnw.net/jtv_user_pictures/faceittv-channel_offline_image-d6d794fd189dc076-1920x1080.jpeg', u'logo': u'https://static-cdn.jtvnw.net/jtv_user_pictures/faceittv-profile_image-45e9e95c0f48f50e-300x300.jpeg', u'partner': True, u'display_name': u'FACEIT TV', 'stream_created_at': u'2016-11-23T13:15:46Z', u'delay': None, 'live': True, u'followers': 836656, u'_links': {u'videos': u'http://api.twitch.tv/kraken/channels/faceittv/videos', u'stream_key': u'http://api.twitch.tv/kraken/channels/faceittv/stream_key', u'subscriptions': u'http://api.twitch.tv/kraken/channels/faceittv/subscriptions', u'follows': u'http://api.twitch.tv/kraken/channels/faceittv/follows', u'self': u'http://api.twitch.tv/kraken/channels/faceittv', u'commercial': u'http://api.twitch.tv/kraken/channels/faceittv/commercial', u'editors': u'http://api.twitch.tv/kraken/channels/faceittv/editors', u'teams': u'http://api.twitch.tv/kraken/channels/faceittv/teams', u'chat': u'http://api.twitch.tv/kraken/chat/faceittv'}, u'broadcaster_language': u'en', u'status': u'ECS Season 2 Europe - G2 vs FaZe Clan', u'views': 128187849, u'game': u'Counter-Strike: Global Offensive', u'background': None, u'banner': None, 'viewers': 40037, u'name': u'faceittv', u'language': u'en', u'url': u'https://www.twitch.tv/faceittv', u'created_at': u'2012-02-03T20:17:51Z', u'mature': False, u'profile_banner_background_color': None, u'_id': 27942990, u'profile_banner': u'https://static-cdn.jtvnw.net/jtv_user_pictures/faceittv-profile_banner-1ef361661c41e8f3-480.png'}

>>> def get_info(username = None, use_fallback = False):
    # Attempt to get the channel data from /streams/channelname
    # If this succeeds, it means the channel is currently live
    res = url_open("https://api.twitch.tv/kraken/streams/%s" % username)
    data = json.loads(res)
    channel_data = data.get('stream') and data['stream'].get('channel')
    if channel_data:
        channel_data['live'] = True
        channel_data['viewers'] = data['stream'].get('viewers')
        channel_data['stream_created_at'] = data['stream'].get('created_at')
        print channel_data
        return channel_data

    if not use_fallback:
        return None

>>> )
SyntaxError: invalid syntax
>>> get_info('faceittv')
{u'updated_at': u'2016-11-23T21:30:15Z', u'video_banner': u'https://static-cdn.jtvnw.net/jtv_user_pictures/faceittv-channel_offline_image-d6d794fd189dc076-1920x1080.jpeg', u'logo': u'https://static-cdn.jtvnw.net/jtv_user_pictures/faceittv-profile_image-45e9e95c0f48f50e-300x300.jpeg', u'partner': True, u'display_name': u'FACEIT TV', 'stream_created_at': u'2016-11-23T13:15:46Z', u'delay': None, 'live': True, u'followers': 836656, u'_links': {u'videos': u'http://api.twitch.tv/kraken/channels/faceittv/videos', u'stream_key': u'http://api.twitch.tv/kraken/channels/faceittv/stream_key', u'subscriptions': u'http://api.twitch.tv/kraken/channels/faceittv/subscriptions', u'follows': u'http://api.twitch.tv/kraken/channels/faceittv/follows', u'self': u'http://api.twitch.tv/kraken/channels/faceittv', u'commercial': u'http://api.twitch.tv/kraken/channels/faceittv/commercial', u'editors': u'http://api.twitch.tv/kraken/channels/faceittv/editors', u'teams': u'http://api.twitch.tv/kraken/channels/faceittv/teams', u'chat': u'http://api.twitch.tv/kraken/chat/faceittv'}, u'broadcaster_language': u'en', u'status': u'ECS Season 2 Europe - G2 vs FaZe Clan', u'views': 128187849, u'game': u'Counter-Strike: Global Offensive', u'background': None, u'banner': None, 'viewers': 40741, u'name': u'faceittv', u'language': u'en', u'url': u'https://www.twitch.tv/faceittv', u'created_at': u'2012-02-03T20:17:51Z', u'mature': False, u'profile_banner_background_color': None, u'_id': 27942990, u'profile_banner': u'https://static-cdn.jtvnw.net/jtv_user_pictures/faceittv-profile_banner-1ef361661c41e8f3-480.png'}
{u'updated_at': u'2016-11-23T21:30:15Z', u'video_banner': u'https://static-cdn.jtvnw.net/jtv_user_pictures/faceittv-channel_offline_image-d6d794fd189dc076-1920x1080.jpeg', u'logo': u'https://static-cdn.jtvnw.net/jtv_user_pictures/faceittv-profile_image-45e9e95c0f48f50e-300x300.jpeg', u'partner': True, u'display_name': u'FACEIT TV', 'stream_created_at': u'2016-11-23T13:15:46Z', u'delay': None, 'live': True, u'followers': 836656, u'_links': {u'videos': u'http://api.twitch.tv/kraken/channels/faceittv/videos', u'stream_key': u'http://api.twitch.tv/kraken/channels/faceittv/stream_key', u'subscriptions': u'http://api.twitch.tv/kraken/channels/faceittv/subscriptions', u'follows': u'http://api.twitch.tv/kraken/channels/faceittv/follows', u'self': u'http://api.twitch.tv/kraken/channels/faceittv', u'commercial': u'http://api.twitch.tv/kraken/channels/faceittv/commercial', u'editors': u'http://api.twitch.tv/kraken/channels/faceittv/editors', u'teams': u'http://api.twitch.tv/kraken/channels/faceittv/teams', u'chat': u'http://api.twitch.tv/kraken/chat/faceittv'}, u'broadcaster_language': u'en', u'status': u'ECS Season 2 Europe - G2 vs FaZe Clan', u'views': 128187849, u'game': u'Counter-Strike: Global Offensive', u'background': None, u'banner': None, 'viewers': 40741, u'name': u'faceittv', u'language': u'en', u'url': u'https://www.twitch.tv/faceittv', u'created_at': u'2012-02-03T20:17:51Z', u'mature': False, u'profile_banner_background_color': None, u'_id': 27942990, u'profile_banner': u'https://static-cdn.jtvnw.net/jtv_user_pictures/faceittv-profile_banner-1ef361661c41e8f3-480.png'}
>>> get_info('faceittv')
{u'updated_at': u'2016-11-23T21:30:15Z', u'video_banner': u'https://static-cdn.jtvnw.net/jtv_user_pictures/faceittv-channel_offline_image-d6d794fd189dc076-1920x1080.jpeg', u'logo': u'https://static-cdn.jtvnw.net/jtv_user_pictures/faceittv-profile_image-45e9e95c0f48f50e-300x300.jpeg', u'partner': True, u'display_name': u'FACEIT TV', 'stream_created_at': u'2016-11-23T13:15:46Z', u'delay': None, 'live': True, u'followers': 836656, u'_links': {u'videos': u'http://api.twitch.tv/kraken/channels/faceittv/videos', u'stream_key': u'http://api.twitch.tv/kraken/channels/faceittv/stream_key', u'subscriptions': u'http://api.twitch.tv/kraken/channels/faceittv/subscriptions', u'follows': u'http://api.twitch.tv/kraken/channels/faceittv/follows', u'self': u'http://api.twitch.tv/kraken/channels/faceittv', u'commercial': u'http://api.twitch.tv/kraken/channels/faceittv/commercial', u'editors': u'http://api.twitch.tv/kraken/channels/faceittv/editors', u'teams': u'http://api.twitch.tv/kraken/channels/faceittv/teams', u'chat': u'http://api.twitch.tv/kraken/chat/faceittv'}, u'broadcaster_language': u'en', u'status': u'ECS Season 2 Europe - G2 vs FaZe Clan', u'views': 128187849, u'game': u'Counter-Strike: Global Offensive', u'background': None, u'banner': None, 'viewers': 40741, u'name': u'faceittv', u'language': u'en', u'url': u'https://www.twitch.tv/faceittv', u'created_at': u'2012-02-03T20:17:51Z', u'mature': False, u'profile_banner_background_color': None, u'_id': 27942990, u'profile_banner': u'https://static-cdn.jtvnw.net/jtv_user_pictures/faceittv-profile_banner-1ef361661c41e8f3-480.png'}
{u'updated_at': u'2016-11-23T21:30:15Z', u'video_banner': u'https://static-cdn.jtvnw.net/jtv_user_pictures/faceittv-channel_offline_image-d6d794fd189dc076-1920x1080.jpeg', u'logo': u'https://static-cdn.jtvnw.net/jtv_user_pictures/faceittv-profile_image-45e9e95c0f48f50e-300x300.jpeg', u'partner': True, u'display_name': u'FACEIT TV', 'stream_created_at': u'2016-11-23T13:15:46Z', u'delay': None, 'live': True, u'followers': 836656, u'_links': {u'videos': u'http://api.twitch.tv/kraken/channels/faceittv/videos', u'stream_key': u'http://api.twitch.tv/kraken/channels/faceittv/stream_key', u'subscriptions': u'http://api.twitch.tv/kraken/channels/faceittv/subscriptions', u'follows': u'http://api.twitch.tv/kraken/channels/faceittv/follows', u'self': u'http://api.twitch.tv/kraken/channels/faceittv', u'commercial': u'http://api.twitch.tv/kraken/channels/faceittv/commercial', u'editors': u'http://api.twitch.tv/kraken/channels/faceittv/editors', u'teams': u'http://api.twitch.tv/kraken/channels/faceittv/teams', u'chat': u'http://api.twitch.tv/kraken/chat/faceittv'}, u'broadcaster_language': u'en', u'status': u'ECS Season 2 Europe - G2 vs FaZe Clan', u'views': 128187849, u'game': u'Counter-Strike: Global Offensive', u'background': None, u'banner': None, 'viewers': 40741, u'name': u'faceittv', u'language': u'en', u'url': u'https://www.twitch.tv/faceittv', u'created_at': u'2012-02-03T20:17:51Z', u'mature': False, u'profile_banner_background_color': None, u'_id': 27942990, u'profile_banner': u'https://static-cdn.jtvnw.net/jtv_user_pictures/faceittv-profile_banner-1ef361661c41e8f3-480.png'}


>>> 
>>> q
{u'updated_at': u'2016-11-23T21:30:15Z', u'video_banner': u'https://static-cdn.jtvnw.net/jtv_user_pictures/faceittv-channel_offline_image-d6d794fd189dc076-1920x1080.jpeg', u'logo': u'https://static-cdn.jtvnw.net/jtv_user_pictures/faceittv-profile_image-45e9e95c0f48f50e-300x300.jpeg', u'partner': True, u'display_name': u'FACEIT TV', 'stream_created_at': u'2016-11-23T13:15:46Z', u'delay': None, 'live': True, u'followers': 836656, u'_links': {u'videos': u'http://api.twitch.tv/kraken/channels/faceittv/videos', u'stream_key': u'http://api.twitch.tv/kraken/channels/faceittv/stream_key', u'subscriptions': u'http://api.twitch.tv/kraken/channels/faceittv/subscriptions', u'follows': u'http://api.twitch.tv/kraken/channels/faceittv/follows', u'self': u'http://api.twitch.tv/kraken/channels/faceittv', u'commercial': u'http://api.twitch.tv/kraken/channels/faceittv/commercial', u'editors': u'http://api.twitch.tv/kraken/channels/faceittv/editors', u'teams': u'http://api.twitch.tv/kraken/channels/faceittv/teams', u'chat': u'http://api.twitch.tv/kraken/chat/faceittv'}, u'broadcaster_language': u'en', u'status': u'ECS Season 2 Europe - G2 vs FaZe Clan', u'views': 128187849, u'game': u'Counter-Strike: Global Offensive', u'background': None, u'banner': None, 'viewers': 39509, u'name': u'faceittv', u'language': u'en', u'url': u'https://www.twitch.tv/faceittv', u'created_at': u'2012-02-03T20:17:51Z', u'mature': False, u'profile_banner_background_color': None, u'_id': 27942990, u'profile_banner': u'https://static-cdn.jtvnw.net/jtv_user_pictures/faceittv-profile_banner-1ef361661c41e8f3-480.png'}
>>> q.keys()
[u'updated_at', u'video_banner', u'logo', u'partner', u'display_name', 'stream_created_at', u'delay', 'live', u'followers', u'_links', u'broadcaster_language', u'status', u'views', u'game', u'background', u'banner', 'viewers', u'name', u'language', u'url', u'created_at', u'mature', u'profile_banner_background_color', u'_id', u'profile_banner']
>>> q.keys()[1]
u'video_banner'
>>> q['live']
True
>>> q['created_at']
u'2012-02-03T20:17:51Z'
>>> q['stream_created_at']
u'2016-11-23T13:15:46Z'
>>> a=q['stream_created_at']
>>> a
u'2016-11-23T13:15:46Z'
>>> a.index('T')
10
>>> a.inde

Traceback (most recent call last):
  File "<pyshell#64>", line 1, in <module>
    a.inde
AttributeError: 'unicode' object has no attribute 'inde'

>>> a[10]
u'T'
>>> a[11:]
u'13:15:46Z'
>>> a[11:-1]
u'13:15:46'
>>> u'13:15:46'
u'13:15:46'

>>> import datetime
>>> datetime.t

Traceback (most recent call last):
  File "<pyshell#70>", line 1, in <module>
    datetime.t
AttributeError: 'module' object has no attribute 't'
>>> datetime.time()
datetime.time(0, 0)
>>> datetime.time(now)

Traceback (most recent call last):
  File "<pyshell#72>", line 1, in <module>
    datetime.time(now)
NameError: name 'now' is not defined
>>> datetime.time('now')

Traceback (most recent call last):
  File "<pyshell#73>", line 1, in <module>
    datetime.time('now')
TypeError: an integer is required
>>> datetime.time(1)
datetime.time(1, 0)
>>> datetime.datetime()

Traceback (most recent call last):
  File "<pyshell#75>", line 1, in <module>
    datetime.datetime()
TypeError: Required argument 'year' (pos 1) not found
>>> datetime.datetime(now)

Traceback (most recent call last):
  File "<pyshell#76>", line 1, in <module>
    datetime.datetime(now)
NameError: name 'now' is not defined
>>> datetime.datetime('now')

Traceback (most recent call last):
  File "<pyshell#77>", line 1, in <module>
    datetime.datetime('now')
TypeError: an integer is required
>>> datetime.datetime.now()
datetime.datetime(2016, 11, 23, 16, 51, 11, 794000)
>>> datetime.time.now()

Traceback (most recent call last):
  File "<pyshell#79>", line 1, in <module>
    datetime.time.now()
AttributeError: type object 'datetime.time' has no attribute 'now'
>>> datetime.time.hour()

Traceback (most recent call last):
  File "<pyshell#80>", line 1, in <module>
    datetime.time.hour()
TypeError: 'getset_descriptor' object is not callable
>>> datetime.time.hour
<attribute 'hour' of 'datetime.time' objects>
>>> AttributeError: type object 'datetime.time' has no attribute 'now'
SyntaxError: invalid syntax
>>> SyntaxError: invalid syntax
SyntaxError: invalid syntax
>>> 
>>> u'2016-11-23T13:15:46Z'
u'2016-11-23T13:15:46Z'
>>> a=u'2016-11-23T13:15:46Z'
>>> a
u'2016-11-23T13:15:46Z'
>>> z=datetime.strptime(a, "%Y-%m-%dT%H:%M:%SZ")

Traceback (most recent call last):
  File "<pyshell#89>", line 1, in <module>
    z=datetime.strptime(a, "%Y-%m-%dT%H:%M:%SZ")
AttributeError: 'module' object has no attribute 'strptime'
>>> datetime.strptime

Traceback (most recent call last):
  File "<pyshell#90>", line 1, in <module>
    datetime.strptime
AttributeError: 'module' object has no attribute 'strptime'
>>> import datetime
>>> datetime.strptime

Traceback (most recent call last):
  File "<pyshell#92>", line 1, in <module>
    datetime.strptime
AttributeError: 'module' object has no attribute 'strptime'
>>> datetime.strptime()

Traceback (most recent call last):
  File "<pyshell#93>", line 1, in <module>
    datetime.strptime()
AttributeError: 'module' object has no attribute 'strptime'
>>> datetime.datetime.strptime()

Traceback (most recent call last):
  File "<pyshell#94>", line 1, in <module>
    datetime.datetime.strptime()
TypeError: strptime() takes exactly 2 arguments (0 given)
>>> z=datetime.datetime.strptime(a, "%Y-%m-%dT%H:%M:%SZ")
>>> z
datetime.datetime(2016, 11, 23, 13, 15, 46)
>>> a
u'2016-11-23T13:15:46Z'
>>> 
