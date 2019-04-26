# -*- coding: utf-8 -*-
from flask import Flask
from config import Config, get_gitlab_key, cur_dir
from flask_sqlalchemy import SQLAlchemy
from werkzeug.routing import BaseConverter
from flask_oauthlib.client import OAuth
from flask_login import LoginManager
from flask_cache import Cache
from flask_redis import FlaskRedis
import logging
import os


class RegexConverter(BaseConverter):

    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app = Flask(__name__)
db = SQLAlchemy()
login_manager = LoginManager()
oauth = OAuth(app)
redis = FlaskRedis()
cache = Cache()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=os.path.join(cur_dir, 'logs', 'app.log'),
    filemode='a'
)

logger = logging.getLogger("mock-server")

gitlab = oauth.remote_app('gitlab',
    base_url='http://git.caimi-inc.com/api/v3/',
    request_token_url=None,
    access_token_url='http://git.caimi-inc.com/oauth/token',
    authorize_url='http://git.caimi-inc.com/oauth/authorize',
    access_token_method='POST',
    consumer_key=get_gitlab_key()[0],
    consumer_secret=get_gitlab_key()[1]
)

def create_app():
    app.url_map.converters['regex'] = RegexConverter
    config = Config()
    app.config.from_object(config)
    db.init_app(app)
    cache.init_app(app)
    redis.init_app(app)
    login_manager.init_app(app)
    from mock_server.views import url
    app.register_blueprint(url)

    return app