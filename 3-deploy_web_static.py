#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
from datetime import datetime
from fabric.api import env, local, put, run

env.hosts = ["52.86.171.42", "54.90.41.188"]


def do_pack():
    """
    Creates a compressed archive of the web_static folder in the versions directory.

    Returns:
        str: The filename of the created archive if successful, None otherwise.
    """
    time = datetime.now()
    archive = 'web_static_' + time.strftime("%Y%m%d%H%M%S") + '.' + 'tgz'
    local('mkdir -p versions')
    try:
        local('tar -cvzf versions/{} web_static'.format(archive))
        return archive
    except Exception as e:
        print(f"Failed to create archive: {e}")
        return None


def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        if not os.path.isfile(archive_path):
            return False
        file = archive_path.split("/")[-1]
        name = file.split(".")[0]

        put(archive_path, "/tmp/{}".format(file))
        run("rm -rf /data/web_static/releases/{}/".format(name))
        run("mkdir -p /data/web_static/releases/{}/".format(name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name))
        run("rm /tmp/{}".format(file))
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name))
        run("rm -rf /data/web_static/releases/{}/web_static".format(name))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name))
        return True
    except Exception as e:
        print(f"Failed to deploy: {e}")
        return False


def deploy():
    """Creates and distributes an archive to the web servers"""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
