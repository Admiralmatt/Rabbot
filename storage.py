import json

import drive
import ircbot

def save(): #Save Data to File
    print 'Saving'
    with open('data.json', 'w') as fp:
        json.dump(data, fp, indent=2, sort_keys=True)
    drive.drivesave()

def load(): #Load Data From File
    global data
    with open('data.json', 'r') as fp:
        data = json.load(fp)

#returns (path) that navigates to games portion of records
def getgamepath():
    path = data.setdefault('shows', {}).setdefault(ircbot.bot.show, {"name": ircbot.bot.show}).setdefault('games', {})
    return path

#returns (path) that navigates to list of mods for channel
def getmodlist():
    modlist = data.setdefault('shows', {}).setdefault(ircbot.bot.show, {"name": ircbot.bot.show})
    return modlist

#returns (path) that navigates to games portion of records
def getchanneldata():
    channeldata = data['shows'][ircbot.bot.show]
    channeldata.setdefault("showstats", ["death"])
    channeldata.setdefault("showresponse", {})
    return channeldata

#Search records to see if game allready exists.
#if not, will add new game to records
def findgame(game = None):
    if game is None:
        return None

    if isinstance(game, str):
        game = {'_id': game, 'name': game, 'is_override': True}
        
    path = getgamepath()

    # First try to find the game using the Twitch ID
    if str(game['_id']) in path:
        gamedata = path[str(game['_id'])]
        # Check if the name has changed
        if gamedata['name'] != game['name']:
            gamedata['name'] = game['name']
            save()
        gamedata['id'] = str(game['_id'])
        return (gamedata)
    
    # Next try to find the game using the name
    for gameid, gamedata in path.items():
        if gamedata['name'] == game['name']:
            # If this is from Twitch, fix the ID
            if not game.get('is_override'):
                del path[gameid]
                path[str(game['_id'])] = gamedata
                gamedata['id'] = str(game['_id'])
                save()
            else:
                gamedata['id'] = gameid
            return (gamedata)
        
            # Look up the game by display name as a fallback
            for gamedata in path.items():
                if 'display' in gamedata and gamedata['display'] == game['name']:
                    # Don't try to keep things aligned here...
                    gamedata['id'] = gameid
                    return (gamedata)

    #in the event of a new game                
    gamedata = {
        'id': str(game['_id']),
        'name': game['name'],
        'stats': {},
        }
    #Add to records
    path[str(game['_id'])] = gamedata
    save()
    return gamedata

drive.driveload()
load()
        
'''
data = {
            'stats':
                    {
                            'stats': {
                'death': {'plural': "deaths"},
                },
                            '''
'''
Data structure:

data = {
        'stats': { # Different statistics that are tracked
                '<stat-name>': { # the name as used in commands
                        'singular': '<stat-name>', # For display - defaults to the same as the command
                        'plural': '<stat-names>', # For display
                },
        },
        'shows': { # Shows we have tracked stats for
                '<id>': { # Show ID or '' for unknown show
                        'name': '<name>', # Name of this show
                        'games': { # Games we have tracked stats for
                                <id>: { # id is the Twitch game ID, or the game name for non-Twitch override games
                                'name': '<name>', # Official game name as Twitch recognises it - to aid matching
                                'display': '<display name>' # Display name, defaults to the same as name. For games with LRL nicknames
                                'stats': {
                                        '<stat-name>': <count>,
                                },
                        },
                },
        },
        'spam_rules': [
                {
                        're': '<regular expression>',
                        'message': '<ban description>',
                },
        ],
}
For example:
data = {
        'stats': {
                'death': {'plural': "deaths"},
        },
        'shows': {
                '': {
                        'name': "Unknown",
                        'games': {
                                12345: {
                                        'name': "Example game",
                                        'display': "Funny name for example game",
                                        'stats': {
                                                'death': 17,
                                        },
                                },
                        },
                },
        },
        'spam_rules': [
                {
                        're': '^I am a spambot!$',
                        'message': "claims to be a spambot",
                },
        ],
}
'''
