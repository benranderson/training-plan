#!/usr/bin/env python
import os

from app import create_app, db
from app.models import User
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(PROJECT_ROOT, 'tests')

# TODO: REST API


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='0.0.0.0', port=8080))


@manager.command
def test(cov=False):
    """Run the unit tests."""
    import pytest
    if cov:
        pytest.main(['--cov-report', 'term', '--cov-report',
                     'html:tmp/cov/', '--cov=app', TEST_PATH])
    else:
        pytest.main([TEST_PATH])


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade
    # migrate database to latest revision
    upgrade()


@manager.command
def clean():
    """Remove *.pyc and *.pyo files recursively starting at current directory.
    """
    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                full_pathname = os.path.join(dirpath, filename)
                print('Removing {}'.format(full_pathname))
                os.remove(full_pathname)


if __name__ == '__main__':
    manager.run()
