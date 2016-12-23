import json, urllib, urllib2, logging
from ircbot import bot
import utils

GAME_CHECK_INTERVAL = 5*60 # Only check the current game at most once every five minutes

def url_open(url, data = None):
    if isinstance(data, dict):
        data['query']=urllib.quote(data['query'].encode('utf-8'), safe='/:')
        data = urllib.urlencode(data)
        data=urllib.unquote(data)
    header = 'client_id=nigr9qrlruvvbymiitss8t7ozl4ejip'
    url = '%s?%s&%s' % (url, data, header)
    response = urllib2.urlopen(url)
    html = response.read()
    return html
#Test String: https://api.twitch.tv/kraken/streams/loadingreadyrun?client_id=nigr9qrlruvvbymiitss8t7ozl4ejip

def get_info(username = None, use_fallback = False):
    # Attempt to get the channel data from /streams/channelname
    # If this succeeds, it means the channel is currently live
    if username is None:
        username = bot.show
    print "https://api.twitch.tv/kraken/streams/%s" % username
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
        username = bot.show
    
    channel_data = get_info(username, use_fallback=False)
    if not channel_data or not channel_data['live']:
        channel_data = get_info(username, use_fallback=True)
    
#might want to return None here
    if not channel_data['live']:
        return None
    if channel_data['game'] is not None:
        return get_game(name=channel_data['game'])
    return None

@utils.throttle(GAME_CHECK_INTERVAL)
def get_live_game(nick, channel):
    return get_game_playing()

