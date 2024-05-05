#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers

execute: fab -f 3-deploy_web_static.py deploy -i ~/.ssh/id_rsa -u ubuntu
"""
import os.path
from datetime import datetime
from fabric.api import env, local, put, run

env.hosts = ["52.86.171.42", "54.90.41.188"]


def do_pack():
    """
    Creates a compressed archive of the web_static
    folder in the versions directory.
    Returns:
        str: The filename of the created archive
             if successful, None otherwise.
    """
    dt = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                         dt.month,
                                                         dt.day,
                                                         dt.hour,
                                                         dt.minute,
                                                         dt.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file


def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if os.path.isfile(archive_path) is False:
    return False

    file_n = archive_path.split("/")[-1]
    no_ext = file_n.split(".")[0]
    path = "/data/web_static/releases/"
    put(archive_path, '/tmp/')
    run('mkdir -p {}{}/'.format(path, no_ext))
    run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
    run('rm /tmp/{}'.format(file_n))
    run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
    run('rm -rf {}{}/web_static'.format(path, no_ext))
    run('rm -rf /data/web_static/current')
    run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
    return True


def deploy():
    """
    Creates and distributes an archive to the web servers
    """
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
