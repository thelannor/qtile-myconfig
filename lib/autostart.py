# coding: utf-8

__all__ = [ 'autostart' ]

import os
import shlex
import subprocess

def autostart(apps):
    assert isinstance(apps, (list, tuple, set)), "Bad type: not list"

    for app in filter(lambda s: s and isinstance(s, (str, unicode)), apps):
        try:
            p = subprocess.Popen(shlex.split(app))
        except Exception as err:
            continue
