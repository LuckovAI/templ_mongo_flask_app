# -*- coding: utf-8 -*-
import flask
import json
from inspect import getargspec
from functools import wraps
from bson import json_util


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
                    values = flask.request.values
                    vparam = []
                    for p in aparam:
                        val = values.get(p)
                        val = str(val) if str(val).isdigit() or val is None else '"' + val + '"'
                        vparam.append(val)
                    return eval('f(' + ', '.join([v for v in vparam]) + ')')
                return f()
            except Exception, exc:
                msg = u'Ошибка сервиса %s' % str(exc)
                print msg
                raise Exception(msg)

        return parse_input_param
