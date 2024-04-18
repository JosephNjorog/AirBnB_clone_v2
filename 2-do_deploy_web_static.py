#!/usr/bin/python3
"""
This script distributes archive of web_static to web servers
"""

from fabric.api import env

env.hosts = ['100.26.49.104', '18.204.6.37']


def do_deploy(archive_path):
    """
    Upload archive to env.hosts & uncompress it
    """
    from fabric.api import run, put
    import re

    if not archive_path:
        return False

    # get folder name where to uncompress archive
    match = re.compile(r'.*/(\w+).tgz$').search(archive_path)
    if not match:
        return False
    folder = match.group(1)

    # upload archive to server
    ret = put(archive_path, '/tmp/')
    if not ret.succeeded:
        return False

    # uncompress archive
    ret = run("mkdir -p /data/web_static/releases/{}".format(folder))
    if not ret.succeeded:
        return False
    ret = run("tar -xzf /tmp/{}.tgz -C \
               /data/web_static/releases/{}".format(folder, folder))
    if not ret.succeeded:
        return False

    # delete archive from server & move files
    ret = run("rm /tmp/{}.tgz".format(folder))
    if not ret.succeeded:
        return False
    ret = run("mv /data/web_static/releases/{}/web_static/* \
               /data/web_static/releases/{}/".format(folder, folder))
    if not ret.succeeded:
        return False
    ret = run("rm -rf /data/web_static/releases/{}/web_static/".format(folder))
    if not ret.succeeded:
        return False

    # delete symlink and create new one
    ret = run("rm -rf /data/web_static/current")
    if not ret.succeeded:
        return False
    ret = run("ln -fs /data/web_static/releases/{}/ \
               /data/web_static/current".format(folder))
    if not ret.succeeded:
        return False

    return True
