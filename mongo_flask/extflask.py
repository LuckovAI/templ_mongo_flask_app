# -*- coding: utf-8 -*-
import flask
import json
from inspect import getargspec
from functools import wraps
from bson import json_util
import ast


class ExtBlueprint(flask.Blueprint):
    def resp_json(self, data={}, code=200):
        return flask.Response(
            status=code,
            mimetype="application/json",
            response=json.dumps(data, default=json_util.default))

    def dec_parse_input_param(self, f):
        """"создание соответствия для параметров функции и сервиса"""
        @wraps(f)
        def parse_input_param(*a):
            try:
                # т.к. нам параметры в функцию напрямую не передаются, то получаем их из запроса хттп
                aparam = getargspec(f).args
                if len(aparam) > 0:
                    values = []
                    #проверяем зловред код во входящих параметрах
                    [values.append(ast.literal_eval(val)) for val in flask.request.values.values()]
                    return f(*values)
                return f()
            except Exception, exc:
                msg = u'Ошибка сервиса %s' % str(exc)
                print msg
                raise Exception(msg)
        return parse_input_param
