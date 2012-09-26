# coding: utf-8

__all__ = [ 'finder' ]

import os.path

def finder(names, paths=["/usr/bin", "/usr/local/bin"], default="echo"):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            for path in paths:
                for name in names:
                    fpath = os.path.join(path, name)
                    if os.path.isfile(fpath):
                        return func(fpath)
            return func(default)
        return wrapper
    return decorator
    
