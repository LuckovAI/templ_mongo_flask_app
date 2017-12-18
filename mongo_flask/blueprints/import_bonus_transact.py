# -*- coding: utf-8 -*-
from mongo_flask.extflask import ExtBlueprint
from flask import request
from mongo_flask.utils import get_db, requires_auth
import json


url_prefix = '/import_bonus_transact'
bp = ExtBlueprint('import_bonus_transact', __name__)


@bp.route('/set_bonus_transact', methods=['POST'], endpoint='set_bonus_transact')
@requires_auth
def set_bonus_transact():
    data = request.data
    if data:
        obj = json.loads(data)
        db = get_db()
        bonus_transact = db.bonus_transact
        users = db.users
        for r in obj:
            user = users.find_one({'FIO': r['FIO'], 'num_cart': r['num_cart'],
                                   'email': r['email']})
            if user:
                bonus_tr = {'id_user': user['_id'], 'num_tr': r['num_tr'],
                            'c_bonus': r['c_bonus'], 'date_fly': r['date_fly'],
                            'from_place': r['from_place'], 'to_place': r['to_place']}
                bonus_transact.insert(bonus_tr)
        return bp.resp_json({'error': None, 'result': 'ok'})
