# -*- coding: utf-8 -*-
from mongo_flask.extflask import ExtBlueprint
from flask import g
from mongo_flask.utils import is_auth


url_prefix = '/users'
bp = ExtBlueprint('users', __name__)


@bp.route('/get_user', methods=['GET'], endpoint='get_user')
@is_auth
def get_user():
    return bp.resp_json({'error': None, 'result': g.user})
