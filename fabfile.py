import os
import time
import yaml

from fabric.api import env, execute, get, hide, lcd, local, require, run, settings, shell_env, sudo, task
from fabric.colors import red
from fabric.contrib import files, project
from fabric.contrib.console import confirm
from fabric.utils import abort

# Directory structure
PROJECT_ROOT = os.path.dirname(__file__)
CONF_ROOT = os.path.join(PROJECT_ROOT, 'conf')
SALT_ROOT = os.path.join(CONF_ROOT, 'roots')
env.shell = '/bin/bash -c'
env.disable_known_hosts = True
env.forward_agent = True
servers = yaml.load(file(os.path.join(CONF_ROOT, 'servers.yaml'), 'r'))


@task
def vagrant():
    env.environment = 'vagrant'
    setup()


@task
def staging():
    env.environment = 'staging'
    setup()


@task
def production():
    env.environment = 'production'
    setup()


def setup():
    env.nodes = servers[env.environment]['nodes']
    if 'salt' in env.nodes:
        env.standalone = False
        env.master = env.nodes['salt']
    else:
        # standalone minion, there is no master
        env.standalone = True
        env.master = {'address': 'localhost'}


@task
def master():
    """Communicate with master"""
    env.hosts = [env.master['address']]


@task
def minion(id_):
    """Communicate with specified minion"""
    if not id_ in env.nodes:
        abort("No such minion: %s" % id_)
    env.minion = env.nodes[id_]
    if id_ == 'salt':
        env.minion['id'] = id_
    elif env.environment == 'vagrant':
        env.minion['id'] = "{}-{}-{}".format(id_, env.environment, env.local_user)
    else:
        env.minion['id'] = "{}-{}".format(id_, env.environment)
    env.hosts = [env.minion['address']]


@task
def setup_host():
    """Set server hostname on minion"""
    require('environment')
    id_ = env.minion['id']
    setup_hosts = env.minion.get('setup-hosts', True)
    if not setup_hosts:
        print('hostname and /etc/hosts setup is disabled for {}, skipping...'.format(id_))
        return
    # resolve hostname locally
    files.append("/etc/hosts", '127.0.0.1 {}'.format(id_), use_sudo=True)
    # point salt hostname to master address
    files.append("/etc/hosts", '{} salt'.format(env.master['address']),
                 use_sudo=True)
    # set hostname
    sudo('echo "{}" > /etc/hostname'.format(id_))
    sudo('hostname {}'.format(id_))


@task
def setup_minion():
    """Setup with salt-minion and point to designated master"""
    # install salt minion if it's not there already
    require('environment', 'minion')
    with settings(warn_only=True):
        with hide('running', 'stdout', 'stderr'):
            installed = run('which salt-call')
    if not installed:
        # install stable version of salt-minion
        run('wget -O /tmp/bootstrap-salt.sh http://bootstrap.saltstack.org')
        sudo('sh /tmp/bootstrap-salt.sh -P stable')
    config = {}
    if 'minion' in servers and 'base-config' in servers['minion']:
        # load common minion config first if present
        config.update(servers['minion']['base-config'])
    config['id'] = env.minion['id']
    config.update(env.minion['config'])
    if 'grains' in config:
        config['grains']['environment'] = env.environment
        if env.standalone:
            config['grains']['minion-type'] = 'standalone'
    context = {'config': yaml.dump(config)}
    files.upload_template(filename='minion.yaml',
                          destination="/etc/salt/minion",
                          context=context,
                          template_dir=CONF_ROOT,
                          use_jinja=True, use_sudo=True)
    sudo('service salt-minion restart')


@task
def highstate(target='*', loglevel='warning'):
    """Run highstate command on master"""
    require('environment', 'minion')
    setup_minion()
    if env.standalone:
        sync()
    salt('saltutil.sync_all')
    print("This can take a long time without output, be patient")
    salt('state.highstate', target, loglevel)


@task
def state(name, target='*', loglevel='warning'):
    """Run explicit state on host"""
    require('environment')
    setup_minion()
    if env.standalone:
        sync()
    salt('saltutil.sync_all')
    salt('state.sls {}'.format(name), target, loglevel)


@task
def salt(cmd, target='*', loglevel='warning'):
    """Run arbitrary salt commands on host"""
    call = []
    if env.standalone:
        call.extend(['salt-call', '--local'])
    else:
        call.extend(["salt", "'{}'".format(target)])
    call.append('-l{}'.format(loglevel))
    call.append(cmd)
    with settings(warn_only=True):
        sudo(' '.join(call))


@task
def sync():
    """Upload local states"""
    require('environment')
    # Rsync local states and pillars
    salt_root = SALT_ROOT if SALT_ROOT.endswith('/') else SALT_ROOT + '/'
    environments = ['vagrant', 'staging', 'testing', 'production', 'proxy']
    exclude = [os.path.join('pillar', e) for e in environments if e != env.environment]
    # Reconcile any problems with secrets file
    local_secrets_dir = os.path.join(SALT_ROOT, 'pillar', env.environment)
    remote_secrets_dir = os.path.join('/srv', 'pillar', env.environment)
    local_exists = os.path.exists(os.path.join(local_secrets_dir, "secrets.sls"))
    remote_exists = files.exists(os.path.join(remote_secrets_dir, "secrets.sls"))
    with lcd(local_secrets_dir):
        if local_exists:
            # backup local file
            local("cp secrets.sls secrets.sls.local")
            if remote_exists:
                get_secrets("secrets.sls.remote")
            else:
                # no remote file, so create an empty one for the diff below
                local("touch %s" % "secrets.sls.remote")
            with settings(warn_only=True):
                result = local('diff -u secrets.sls.remote secrets.sls.local')
                if result.failed and not confirm(red("Above changes will be made to secrets.sls. Continue?")):
                    abort("Aborted. Files have been copied to secrets.sls.local and secrets.sls.remote. " +
                          "Resolve conflicts, then retry.")
                else:
                    local("rm secrets.sls.local")
                    local("rm secrets.sls.remote")
        else:
            # no local secrets file.
            if not confirm(red("No local secrets.sls. Get one from the remote server?")):
                abort("Aborted. You need a secrets.sls file. Get one from a colleague.")
            else:
                get_secrets()
    project.rsync_project(local_dir=salt_root, remote_dir='/tmp/salt', delete=True, exclude=exclude)
    sudo('rm -rf /srv/salt /srv/pillar')
    sudo('mv /tmp/salt/* /srv/')
    sudo('rm -rf /tmp/salt/')


@task
def setup_master(name='salt'):
    """Provision master with salt-master"""
    require('environment')
    with settings(warn_only=True):
        with hide('running', 'stdout', 'stderr'):
            installed = run('which salt')
    if not installed:
        sudo('apt-get update -qq -y')
        sudo('apt-get install python-software-properties -qq -y')
        sudo('add-apt-repository ppa:saltstack/salt -y')
        sudo('apt-get update -qq')
        sudo('apt-get install salt-master -qq -y')
    # make sure git is installed for gitfs
    with settings(warn_only=True):
        with hide('running', 'stdout', 'stderr'):
            installed = run('which git')
    if not installed:
        sudo('apt-get install python-pip git-core -qq -y')
        sudo('pip install -q -U GitPython')
    context = {}
    files.upload_template(filename='master.yaml',
                          destination="/etc/salt/master",
                          context=context,
                          template_dir=CONF_ROOT,
                          use_jinja=True, use_sudo=True)
    sudo('service salt-master restart')


@task
def overstate():
    """Run ordered states - Multi-server only"""
    require('environment')
    # need to sync_states so our custom _states modules are sync'd
    salt('saltutil.sync_states')
    sudo('salt-run state.over')


@task
def ping():
    """Ping minions - Multi-server only"""
    salt('test.ping')


@task
def accept_key():
    """Accept minion key on master - Multi-server only"""
    require('environment')
    found = False
    while not found:
        result = sudo('salt-key -L')
        found = env.minion['id'] in result
        if not found:
            print(red("Didn't see {} key, sleeping...".format(env.minion['id'])))
            time.sleep(2)
    sudo('salt-key --accept={} -y'.format(env.minion['id']))
    sudo('salt-key -L')


@task
def delete_key(name):
    """Accept specific key on master - Multi-server only"""
    require('environment')
    sudo('salt-key -L')
    sudo('salt-key --delete={} -y'.format(name))
    sudo('salt-key -L')


@task
def get_secrets(local_file=None):
    require('environment')
    if not local_file:
        local_file = os.path.join(SALT_ROOT, 'pillar', env.environment, "%(basename)s")
    secrets_file = os.path.join('/srv/pillar/%(environment)s/secrets.sls' % env)
    get(secrets_file, local_file)


@task
def setup_server(servername, user, key_filename=None):
    """
    Sets up the given servername (e.g., 'vumi' or 'app1') from scratch.
    ``user`` is the initial username, and ``key_filename`` is the initial
    key filename to use (if other than your default SSH key). If the user
    is ``'vagrant'``, the ``key_filename`` will be discovered automatically.
    """
    require('environment')
    key_filename_bak = env.key_filename
    user_bak = env.user
    if user == 'vagrant' and key_filename is None:
        vagrant_version = local('vagrant -v', capture=True).split()[1]
        key_filename = '/opt/vagrant/embedded/gems/gems/vagrant-%s/keys/vagrant' % vagrant_version
    env.key_filename = key_filename
    env.user = user
    execute(minion, servername)
    execute(setup_host)
    execute(setup_minion)
    execute(state, 'margarita')
    execute(highstate)
    env.user = user_bak
    env.key_filename = key_filename_bak
    execute(minion, servername)
    execute(highstate)


@task
def setup_all(user, key_filename=None):
    """
    Sets up all the servers in the given environment.
    """
    require('environment')
    for servername in env.nodes.keys():
        setup_server(servername, user, key_filename)


@task
def ssh():
    """
    Convenience task to ssh to whatever host has been selected.

    E.g. ``fab production minion:app1 ssh``
    """
    require('environment', 'minion')
    local("ssh %s" % env.hosts[0])


@task
def manage_run(command):
    """
    Run a Django management command on the remote server.
    """
    require('environment', 'minion')
    PILLAR_ROOT = os.path.join(SALT_ROOT, 'pillar')
    # Get the project name (which is also the project user)
    env.project = yaml.load(open(os.path.join(PILLAR_ROOT, 'project.sls'))).get('project_name')
    # Get all the environment variables
    ENV_ROOT = os.path.join(PILLAR_ROOT, env.environment)
    env_vars = yaml.load(open(os.path.join(ENV_ROOT, 'env.sls'))).get('environment_variables')
    env_vars.update(yaml.load(open(os.path.join(ENV_ROOT, 'secrets.sls'))).get('secrets'))
    # Setup the call
    django_admin = u"/var/www/{project}-{environment}/env/bin/django-admin.py ".format(**env)
    settings = u" --settings={project}.settings.{environment}".format(**env)
    with shell_env(**env_vars):
        sudo(django_admin + command + settings, user=env.project)
