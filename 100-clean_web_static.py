#!/usr/bin/python3
"""
This script deletes out-of-date archives
"""

from fabric.api import env

env.hosts = ['100.26.49.104', '18.204.6.37']


def do_clean(number=0):
    """
    Delete all unnecessary archives in /version locally &
    in /data/web_static/releases remotely
    """
    from fabric.api import local, run, env

    number = int(number)
    if number == 0:
        number = 1

    # remove local archives
    if env.host_string == env.hosts[0]:  # execute once
        archives = local("ls -tr versions/ | tr ' ' '\\n' |\
                          head -n -{}".format(number), capture=True)
        if archives != '':
            for archive in archives.split('\n'):
                ret = local("rm versions/{}".format(archive))
                if ret.failed:
                    return False

    # remove remote archives
    archives = run("ls -tr --hide=test /data/web_static/releases/ \
                    | tr ' ' '\\n' | head -n -{}".format(number))
    if archives != '':
        for archive in archives.split('\n'):
            ret = run("rm -rf /data/web_static/releases/\
                       {}".format(archive.strip('\r')))
            if ret.failed:
                return False

    return True
