#!/usr/bin/python3
"""
This module deploys web_static to my servers
"""

from fabric.api import env

env.hosts = ['54.242.98.93', '35.168.3.68']
# store .tgz path
paths = []


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static
    """
    from fabric.api import local
    from datetime import datetime

    local("mkdir -p versions")

    date = datetime.now().strftime('%Y%m%d%H%M%S')
    path = 'versions/web_static_{}.tgz'.format(date)
    ret = local('tar -cvzf {} web_static'.format(path))
    if ret.succeeded:
        return path
    else:
        return None


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


def deploy():
    """
    Genrates .tgz archive, upload it to servers &
    uncompress it (full deployement)
    """
    if not paths:
        archive = do_pack()
        if not archive:
            return False
        paths.append(archive)
    else:
        archive = paths[0]

    return do_deploy(archive)
