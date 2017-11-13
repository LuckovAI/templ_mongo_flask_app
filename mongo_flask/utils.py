# -*- coding: utf-8 -*-
# encoding: utf-8

import os
import sys
from flask import _app_ctx_stack, current_app, g, Response, request
import ConfigParser
import syslog
import codecs
import logging
import logging.handlers
from werkzeug.utils import find_modules, import_string
from pymongo import MongoClient
import json
from functools import wraps
from base64 import b64decode


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'db'):
        host = current_app.config.get('base_conf').get('host')
        port = int(current_app.config.get('base_conf').get('port'))
        dbname = current_app.config.get('base_conf').get('dbname')
        client = MongoClient(host, port)
        top.db = client[dbname]
    return top.db


def load_config():
    """  Load configuration  """
    conf = dict()
    conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'baseconfig.conf')

    cfg = ConfigParser.RawConfigParser()

    try:
        cfg.readfp(codecs.open(conf_file, "r", "utf-8"))

    except ConfigParser.Error, ce:
        msg = u'Ошибка чтения файла конфигурации. %s.'
        msg = msg % conf_file
        sys.stderr.write(msg.encode('utf8'))
        syslog.syslog(msg.encode('utf8'))
        raise ce

    if not cfg.has_section('log') or \
            not cfg.has_section('db') or \
            not cfg.has_section('base_authenticate'):
        msg = u'Ошибка чтения секций файла конфигурации. %s.'
        msg = msg % conf_file
        sys.stderr.write(msg.encode('utf8'))
        syslog.syslog(msg.encode('utf8'))
        raise RuntimeError(msg)

    try:

        # Настройки логирования
        conf['log_file'] = cfg.get('log', 'log_file')
        conf['format'] = cfg.get('log', 'format')
        conf['log_level'] = cfg.get('log', 'level')
        conf['dateformat'] = cfg.get('log', 'dateformat')
        conf['maxBytes'] = cfg.getint('log', 'maxBytes')
        conf['backupCount'] = cfg.getint('log', 'backupCount')

        # База
        conf['dbname'] = cfg.get('db', 'dbname')
        conf['host'] = cfg.get('db', 'host')
        conf['port'] = cfg.get('db', 'port')
        conf['user'] = cfg.get('db', 'user')
        conf['password'] = cfg.get('db', 'password')
        # Базовая аутентификация
        conf['ba_username'] = cfg.get('base_authenticate', 'username')
        conf['ba_password'] = cfg.get('base_authenticate', 'password')
        # Почтовый сервер
        conf['mail'] = cfg.get('mail_account', 'mail')
        conf['mpass'] = cfg.get('mail_account', 'pass')
        conf['server'] = cfg.get('mail_account', 'server')

    except (ConfigParser.Error, TypeError), cpex:
        msg = u'Некорректные настройки %s. %s' % (conf_file, cpex)
        sys.stderr.write(msg.encode('utf8'))
        syslog.syslog(msg.encode('utf8'))
        raise cpex

    return {'base_conf': conf, 'SECRET_TYPE': bytes(cfg.get('session', 'session_type')),
            'SECRET_KEY': bytes(cfg.get('session', 'secret_key'))}


def init_log(app):
    """
    Init log file
    """
    base_conf = app.config.get('base_conf')
    logging_level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    app.logger.setLevel(logging_level_map[base_conf['log_level']])
    log_form = logging.Formatter(base_conf['format'], base_conf['dateformat'])
    rotation_handler = logging.handlers.RotatingFileHandler(
        base_conf['log_file'] + '.log', 'ab', maxBytes=base_conf['maxBytes'],
        backupCount=base_conf['backupCount'], encoding='utf8')
    rotation_handler.setFormatter(log_form)
    app.logger.addHandler(rotation_handler)
    app.logger.debug('TaskImpl::__init_log')
    return


def register_blueprints(app):
    "register blueprints"
    for name in find_modules('mongo_flask.blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp') and hasattr(mod, 'url_prefix'):
            app.register_blueprint(mod.bp, url_prefix=mod.url_prefix)
    return


def is_auth(f):
    @wraps(f)
    def is_authorization(*a):
        # return f()
        if not g.user:
            return Response(
                status=401,
                mimetype="application/json",
                response=json.dumps({'error': None, 'result': 'need_login'})
            )
        return f()

    return is_authorization


def clear_bonus_transact():
    "clear bonus transactions"
    db = get_db()
    bonus_transact = db.bonus_transact
    bonus_transact.delete_many({})


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    ba_password = current_app.config.get('base_conf').get('ba_password')
    ba_username = current_app.config.get('base_conf').get('ba_username')
    return username == ba_username and password == ba_password


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        status=401,
        mimetype="application/json",
        response=json.dumps({'WWW-Authenticate': 'Basic realm="Login Required"'}))


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization')
        try:
            user_pass = b64decode(auth.split(' ')[1]).split(':')
            if not check_auth(user_pass[0], user_pass[1]):
                return authenticate()
        except Exception, exc:
            err = u'Ошибка базовой авторизации. ' + str(exc)
            current_app.logger.debug(err)
            print err
            return authenticate()
        return f(*args, **kwargs)

    return decorated
