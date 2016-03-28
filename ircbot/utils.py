import time
import ircbot
import storage


DEFAULT_THROTTLE = 15

class throttle(object):
    """Prevent a function from being called more often than once per period
    Usage:
    @throttle([period])
    def func(...):
            ...
            
    @throttle([period], notify=True)
    def func(nick, ...):
            ...

    When called within the throttle period, the last return value is returned,
    for memoization. period can be set to None to never expire, allowing this to
    be used as a basic memoization decorator.
    
    params is a list of parameters to consider as distinct, so calls where the
    watched parameters are the same are throttled together, but calls where they
    are different are throttled separately. Should be a list of ints (for positional
    parameters) and strings (for keyword parameters).
    """
    def __init__(self, period=DEFAULT_THROTTLE, notify=False, params=[]):
        self.period = period
        self.notify = notify
        self.watchparams = params
        self.lastrun = {}
        self.lastreturn = {}

    def watchedparams(self, args, kwargs):
        params = []
        for i in self.watchparams:
            if isinstance(i, int):
                param = args[i]
            else:
                param = kwargs[i]
                if isinstance(param, str):
                    param = param.lower()
            params.append(param)
        return tuple(params)
                        
    def __call__(self, func):
        def wrapper(nick, *args, **kwargs):
            params = self.watchedparams(args, kwargs)
            if params not in self.lastrun or (self.period and time.time() - self.lastrun[params] >= self.period):
                self.lastreturn[params] = func(nick, *args, **kwargs)
                self.lastrun[params] = time.time()
                return self.lastreturn[params]
            else:
                if self.notify:
                    ircbot.bot.sendmsg('A similar command has been registered recently', nick)
                return self.lastreturn[params]
        # Copy this method across so it can be accessed on the wrapped function
        wrapper.reset_throttle = self.reset_throttle
        return wrapper
    
    def reset_throttle(self):
        self.lastrun = {}
        self.lastreturn = {}


def mod_only(func):
    """
    Prevent an event-handler function from being called by non-moderators
    Usage:
    @mod_only
    def func(nick):
    ...
    """

    # Only complain about non-mods with throttle
    # but allow the command itself to be run without throttling
    @throttle()
    def response(nick):
        #Will not send message if in lockdown
        if ircbot.bot.lockdown != True:
            ircbot.bot.sendmsg('That is a mod-only command', nick)
            
    # Only complain about non-mods with throttle
    # but allow the command itself to be run without throttling
    def wrapper(nick, *args, **kwargs):
        if nick in ircbot.bot.modlist:
            return func(nick, *args, **kwargs)
        else:
            response(nick)
            return
    return wrapper

def admin_only(func):
    """Prevent an event-handler function from being called by anyone other then the streamer or admin.
    Usage:
    @admin_only
    def func(nick):
    ...
    """

    # Only complain about non-mods with throttle
    # but allow the command itself to be run without throttling
    @throttle()
    def response(nick):
        if ircbot.bot.lockdown != True:
            ircbot.bot.sendmsg('That is an admin-only command', nick)
            
    # Only complain about non-mods with throttle
    # but allow the command itself to be run without throttling
    def wrapper(nick, *args, **kwargs):
        if nick in (ircbot.bot.show, 'admiralmatt'):
            return func(nick, *args, **kwargs)
        else:
            response(nick)
            return
    return wrapper

