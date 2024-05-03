#!/usr/bin/python3
# Fabric script to genereate tgz archive
"""
Fabfile to generates a .tgz archive from the contents of web_static.
execute: fab -f 1-pack_web_static.py do_pack
"""

from datetime import datetime
from fabric.api import *


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""

    time = datetime.now()
    archive = 'web_static_' + time.strftime("%Y%m%d%H%M%S") + '.' + 'tgz'
    local('mkdir -p versions')
    create = local('tar -cvzf versions/{} web_static'.format(archive))

    if create is not None:
        return archive
    else:
        return None
