# -*- coding: utf-8 -*-

class TenhouBotSingleton(object):
    instance = None

    def __init__(self):
        if not TenhouBotSingleton.instance:
            TenhouBotSingleton.instance = TenhouBot()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, key, value):
        return setattr(self.instance, key, value)


class TenhouBot(object):
    def __init__(self):
        # Game not start at all, bot may be angry
        self.qbot = None

bot_tracker = TenhouBotSingleton()
