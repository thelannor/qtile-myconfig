# coding: utf-8

__all__ = [ 'mod', 'getTerminal', 'getFileManager' ]

from decorator import finder

mod = 'mod4'

@finder(['urxvt', 'terminator', 'gnome-terminal', 'lxterminal', 'xterm'])
def getTerminal(app):
    return app

@finder(['thunar', 'pcmanfm'])
def getFileManager(app):
    return app

@finder(['chromium-browser', 'chromium', 'firefox'])
def getWebBrowser(app):
    return app + " 2>/dev/null"
