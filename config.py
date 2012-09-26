# coding: utf-8
# Valentin Novikov, 2012

__all__ = [ 'keys', 'mouse', 'groups', 'layouts', 'screens',
            'float_windows', 'should_be_floating', 'dialogs' ]

import os.path
import subprocess, shlex

from libqtile import layout, widget, bar, manager, hook
from libqtile.manager import Key, Screen, Group, Drag
from libqtile.command import lazy
from libqtile.widget import base

from lib import mod, getTerminal, getFileManager, getWebBrowser
from lib.autostart import autostart, _popen

qtile_userhome_path = os.path.dirname(__file__)
qtile_share = os.path.join(qtile_userhome_path, 'share')
qtile_default_feh_bg = os.path.join(qtile_share, 'background', 'default')

_applications = [
    "setxkbmap -layout 'us,ru' -option 'grp:alt_shift_toggle' 2>/dev/null",
    "feh --bg-scale {0!r}".format(qtile_default_feh_bg),
    "dropbox start",
]

_fp_distr = _popen('lsb_release -d').stdout
if _fp_distr.read().find('Ubuntu'):
    _applications.insert(0, "pacmd set-sink-mute 0 true")
_fp_distr.close()
del _fp_distr

autostart(check_proc=True, apps=_applications)
del _applications, qtile_default_feh_bg

keys = [
    Key([mod], "Return", lazy.spawn('gmrun')),
    Key([mod], "F1", lazy.spawn(getFileManager(''))),

    Key([mod], "F2", lazy.spawn('lxterminal')),
    Key([mod, "shift"], "F2", lazy.spawn(getTerminal(''))),

    Key([mod], "F3", lazy.spawn(getWebBrowser(''))),

    Key([mod, "shift"], "F4", lazy.restart()),

    Key([mod], "F9", lazy.spawn("mpg123 http://pub2.di.fm:80/di_techhouse 2>~/.mpg123.log")),
    Key([mod, "shift"], "F9", lazy.spawn("killall mpg123")),

    Key([mod], "k", lazy.layout.down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_down()),

    Key([mod], "j", lazy.layout.up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_up()),

    Key([mod], "Tab", lazy.layout.next()),
    Key([mod, "shift"], "Tab", lazy.layout.client_to_next()),

    Key([mod, "shift"], "space", lazy.layout.rotate()),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),

    Key([mod], "space", lazy.nextlayout()),
    Key([mod], "f", lazy.window.toggle_floating()),

    Key([mod, "shift"], "x", lazy.window.kill()),

    Key([mod, "shift"], "m", lazy.spawn("pacmd set-sink-mute 0 false")),

    Key([mod, "shift"], "d", lazy.spawn('rdesktop 192.168.1.100:9000')),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
]

_groups = [
    ("Terminal", {}),
    ("Local", {}),
    ("Web", {'layout': 'max'}),
    ("Debug", {}),
]

groups = [ Group(name, **kwargs) for name, kwargs in _groups ]

for i, (name, kwargs) in enumerate(_groups, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))

layouts = [
    layout.Max(),
    layout.Stack(stacks=2, border_normal="#222222"),
    layout.MonadTall(border_normal="#222222"),
    layout.Tile()
]

font = 'DejaVu Sans Mono'
fg = '#BBBBBB'
alert = "#FFFF00"

bar_main = bar.Bar([
    widget.CurrentLayout(font=font, foreground=fg),
    widget.Spacer(),
    widget.Systray(icon_size=15),
    widget.Battery(font=font, foreground=fg, update_delay=5),
    widget.Sep(),
    widget.Clock(font=font, foreground=fg),
], 15)

bar_main1 = bar.Bar([
    widget.WindowName(font=font, foreground=fg),
    widget.GroupBox(font=font, fontsize=12, ctive=fg,
                    urgent_border=alert, padding=1, borderwidth=3,
                    margin_x=3, margin_y=-2),

], 15)

screens = [
    Screen(top=bar_main, bottom=bar_main1)
]

del bar_main, bar_main1

float_windows = set([
    "feh",
    "x11-ssh-askpass",
    "gmrun"
])

def should_be_floating(w):
    wm_class = w.get_wm_class()
    if isinstance(wm_class, tuple):
        for cls in wm_class:
            if cls.lower() in float_windows:
                return True
    else:
        if wm_class.lower() in float_windows:
            return True
    return w.get_wm_type() == 'dialog' or bool(w.get_wm_transient_for())

@hook.subscribe.client_new
def dialogs(window):
    if should_be_floating(window.window):
        window.floating = True
