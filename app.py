# -*- coding:utf-8 -*-
from flask import Flask, g
from flask import request, Response
from werkzeug.contrib.fixers import ProxyFix
import config
from zhousf_lib.util import log, string_util
from info import response_info as res
import time
import random
from flask_sqlalchemy import SQLAlchemy


def config_app(flask_app):
    flask_app.jinja_env.auto_reload = True
    flask_app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    flask_app.secret_key = config.CONFIG_SERVER.secret_key
    flask_app.config['JSON_AS_ASCII'] = False
    flask_app.wsgi_app = ProxyFix(app.wsgi_app)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.CONFIG_SERVER.database_url
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

    @flask_app.before_request
    def before_request():
        request_id = str(time.time()) + '_' + str(random.randint(10000, 99999))
        real_ip = request.headers.get('X-Real-Ip', request.remote_addr)
        g.request_id = request_id
        g.real_ip = real_ip
        g.request_path = str(request.path)
        msg = 'request =[request_id:%s, ip:%s, url:%s, method:%s]' \
              % (request_id, real_ip, g.request_path, str(request.method))
        log.API.info(msg)
        # abort(400)

    @flask_app.after_request
    def after_request(environ):
        # if isinstance(environ, Response):
            # if string_util.not_contain(environ.data, '<html>'):
            #     log.API.info(
            #         'response=[request_id:%s, ip:%s, %s]' % (g.request_id, g.real_ip, environ.data))
        return environ

    @flask_app.errorhandler(405)
    def method_illegal(e):
        return res.package(405, 'Method Not Allowed.')

    @flask_app.errorhandler(404)
    def url_not_found(e):
        return res.package(404, 'Not Found: ' + g.request_path)

    @flask_app.errorhandler(400)
    def internal_server_error(e):
        return res.package(400, 'The request was refused.')

    @flask_app.errorhandler(Exception)
    def exception_error(e):
        return res.package(500, 'Exception:%s' % str(e.message))

    @flask_app.errorhandler(500)
    def internal_server_error(e):
        return res.package(500, 'Server internal error.')


def register_blueprint(flask_app):
    from business.model_user import userModel
    flask_app.register_blueprint(userModel, url_prefix='/user')


app = Flask(__name__)


@app.route('/')
def hello():
    real_ip = request.headers.get('X-Real-Ip', request.remote_addr)
    return 'Hello %s' % real_ip


config_app(app)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    age = db.Column(db.Integer)
    sex = db.Column(db.String(10))
    department = db.Column(db.String(100))
    identifyId = db.Column(db.String(100))
    faceId = db.Column(db.Text)


if __name__ == "__main__":
    register_blueprint(app)
    if config.CONFIG_SERVER.use_ssl:
        ssl_context = (config.CONFIG_SERVER.ssl_crt, config.CONFIG_SERVER.ssl_key)
    else:
        ssl_context = None
    app.run(host=config.CONFIG_SERVER.host,
            port=config.CONFIG_SERVER.port,
            debug=config.CONFIG_SERVER.debug,
            ssl_context=ssl_context,
            threaded=True)
    db.create_all()



