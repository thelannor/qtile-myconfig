# coding: utf-8

__all__ = [ 'autostart', '_popen', 'check_process' ]

import os
import shlex
import subprocess

def _write(msg, prefix=''):
    with open("/tmp/qtile-autorun.txt", "w") as fp:
        fp.write("Autorun: {0!r}: {1!r}\n".format(prefix, msg))

def _popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE):
    return subprocess.Popen(shlex.split(command), stdin=stdin,
                            stdout=stdout, stderr=subprocess.PIPE)

def check_process(name):
    pids = []

    try:
        r_ps = _popen("ps lU {}".format(os.getuid()))
        r_grep = _popen("grep {0!r}".format(name), stdin=r_ps.stdout)
        r_ps.stdin.close()

        result = r_grep.communicate()[0]

        for line in filter(lambda l: l, result.split("\n")):
            uid, pid, ppid, pri = line.split()[1:5]

            if int(pid) not in (r_ps.pid, r_grep.pid):
                pids.append(int(pid))

    except Exception as err:
        _write(err, "check_process")
        pids = []

    return (False, set()) if len(pids) < 1 else (True, pids)

def autostart(apps, check_proc=False):
    assert isinstance(apps, (list, tuple, set)), "Bad type: not list"

    if len(apps) < 1:
        return

    try:
        for app in filter(lambda s: s and isinstance(s, (str, unicode)), apps):
            # import pdb; pdb.set_trace()
            if check_proc and check_process(app.split()[0])[0]:
                continue
            p = subprocess.Popen(shlex.split(app))

    except Exception as err:
        _write(err, "autostart")
        return
