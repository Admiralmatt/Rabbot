import json
import urllib, urllib2

import ircbot
import utils

GAME_CHECK_INTERVAL = 5*60 # Only check the current game at most once every five minutes

def url_open(url, data = None):
    if isinstance(data, dict):
        data = urllib.urlencode(data)
    url = '%s?%s' % (url, data)
    response = urllib2.urlopen(url)
    html = response.read()
    return html

def get_info(username = None, use_fallback = False):
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
    print 'Using Fallback'
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
            return res['games']
        else:
            for game in res['games']:
                if game['name'] == name:
                    return game
            return None


def get_game_playing(username = None):
    """
    Get the game information for the game the stream is currently playing
    """
    if username is None:
        username = ircbot.bot.channel.strip('#')

    
    channel_data = get_info(username, use_fallback=False)
    if not channel_data or not channel_data['live']:
        return None
        #channel_data = get_info(username, use_fallback=True)
        
#might want to return None here
    if channel_data['game'] is not None:
        return get_game(name=channel_data['game'])
    return None

@utils.throttle(GAME_CHECK_INTERVAL)
def get_live_game(nick, channel):
    print 'using server'
    return get_game_playing()
