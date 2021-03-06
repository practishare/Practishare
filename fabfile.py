from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd, env
from fabric.contrib.console import confirm

env.hosts = ['practishare@ssh.alwaysdata.com']

def deploy():
    with cd('practishare'):
        run("git pull origin master")
        run("git merge master")
        run("./manage.py syncdb")
        run("./manage.py collectstatic")
        run("./manage.py migrate")
