# -*- coding: utf-8 -*-
from mongo_flask.extflask import ExtBlueprint
from flask import g
from mongo_flask.utils import get_db, is_auth


url_prefix = '/bonus_transact'
bp = ExtBlueprint('bonus_transact', __name__)
# строк на странице
ROWS_IN_PAGE = 20


@bp.route('/get_bonus_transact', methods=['GET'], endpoint='get_bonus_transact')
@is_auth
@bp.dec_parse_input_param
def get_bonus_transact(num_page, date_fly, c_bonus, from_place, to_place):
    db = get_db()
    bonus_transact = db.bonus_transact
    filters = {}
    filters.update({'id_user': g.user['_id']})
    num_page = 1 if not num_page else int(num_page)
    if date_fly: filters.update({'date_fly': date_fly})
    if c_bonus: filters.update({'c_bonus': int(c_bonus)})
    if from_place: filters.update({'from_place': from_place})
    if to_place: filters.update({'to_place': to_place})
    from_row = (num_page - 1) * ROWS_IN_PAGE
    bonus_tr = bonus_transact.find(filters).skip(from_row).limit(ROWS_IN_PAGE)
    return bp.resp_json({'error': None, 'result': list(bonus_tr)})
