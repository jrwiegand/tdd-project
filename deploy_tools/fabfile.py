from fabric.contrib.files import append, exists, sed, contains
from fabric.api import env, local, run
from fabric.context_managers import prefix
import random

REPO_URL = 'https://github.com/jrwiegand/tdd-project.git'

def deploy(db_name='', db_user='', db_pass='', db_host='', db_port=''):
    site_folder = '/home/%s/sites/%s' % (env.user, env.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host,
                     env.user, db_name,
                     db_user, db_pass,
                     db_host, db_port)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))

def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' % (source_folder,))
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))

def _update_settings(source_folder, site_name,
                     user, db_name,
                     db_user, db_pass,
                     db_host, db_port):
    virtualenv_folder = '/home/%s/.virtualenvs/tdd/bin/' % (user,)
    postactivate = virtualenv_folder + 'postactivate'
    predeactivate = virtualenv_folder + 'predeactivate'

    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))

    if not contains(postactivate, "DJANGO_SECRET_KEY"):
        append(postactivate, "export DJANGO_SECRET_KEY='%s'" % (key,))
        append(postactivate, "export DJANGO_DEBUG=False")
        append(postactivate, "export DB_NAME=%s" % (db_name,))
        append(postactivate, "export DB_USER=%s" % (db_user,))
        append(postactivate, "export DB_PASSWORD=%s" % (db_pass,))
        append(postactivate, "export DB_HOST=%s" % (db_host,))
        append(postactivate, "export DB_PORT=%s" % (db_port,))

    if not contains(predeactivate, "DJANGO_SECRET_KEY"):
        append(predeactivate, "unset DJANGO_SECRET_KEY")
        append(predeactivate, "unset DJANGO_DEBUG")
        append(predeactivate, "unset DB_NAME")
        append(predeactivate, "unset DB_USER")
        append(predeactivate, "unset DB_PASSWORD")
        append(predeactivate, "unset DB_HOST")
        append(predeactivate, "unset DB_PORT")

    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, 'DOMAIN = "localhost"', 'DOMAIN = "%s"' % (site_name,))


def _update_virtualenv(source_folder):
    with prefix('export WORKON_HOME=$HOME/.virtualenvs'):
        with prefix('export PROJECT_HOME=$HOME/sites'):
            with prefix('export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3'):
                with prefix('source /usr/local/bin/virtualenvwrapper.sh'):
                    with prefix('workon tdd'):
                        run('pip install -r %s/requirements.txt' % (source_folder,))


def _update_static_files(source_folder):
    with prefix('export WORKON_HOME=$HOME/.virtualenvs'):
        with prefix('export PROJECT_HOME=$HOME/sites'):
            with prefix('export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3'):
                with prefix('source /usr/local/bin/virtualenvwrapper.sh'):
                    with prefix('workon tdd'):
                        run('cd %s && python3 manage.py collectstatic --noinput' % (source_folder,))


def _update_database(source_folder):
    with prefix('export WORKON_HOME=$HOME/.virtualenvs'):
        with prefix('export PROJECT_HOME=$HOME/sites'):
            with prefix('export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3'):
                with prefix('source /usr/local/bin/virtualenvwrapper.sh'):
                    with prefix('workon tdd'):
                        run('cd %s && python3 manage.py migrate --noinput' % (source_folder,))
