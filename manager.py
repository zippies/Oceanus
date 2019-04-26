# -*- encoding:utf-8 -*-
from werkzeug.contrib.fixers import ProxyFix
from mock_server import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app)

app.debug = False

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def dbinit():
    db.create_all()
    print 'dbinit ok'


@manager.command
def dbdrop():
    db.drop_all()
    print 'ok'


if __name__ == '__main__':
    manager.run()
