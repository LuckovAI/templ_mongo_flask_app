# -*- coding: utf-8 -*-
import unittest
from mongo_flask.main import app, get_db
import json
from base64 import b64encode
import random
from datetime import datetime
from os import urandom
import StringIO


# from mongo_flask.utils import clear_bonus_transact

# @unittest.skip("игнорирование")
class LoginTestClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # контекст исключительно для инициализации конфига для БД
        with app.app_context():
            db = get_db()
            users = db.users
            user1 = {'_id': 1, 'FIO': 'FIO1', 'email': 'mail1@mail.ru', 'num_cart': 'num_cart1',
                     'pw_hash': 'pbkdf2:sha256:50000$ENYCDQgG$2a5019de2d69c8b2b23b580d5402e770a6c4a15c8f2c4f7741f25f45ae195ef9'}  # pw_hash1
            user2 = {'_id': 2, 'FIO': 'FIO2', 'email': 'mail2@mail.ru', 'num_cart': 'num_cart2',
                     'pw_hash': 'pbkdf2:sha256:50000$6JOR49LN$0381cfd335f1abc13cc05fe78d78dcd8a561ba9742b15d2c5204f5fa52ca2570'}  # pw_hash2
            user3 = {'_id': 3, 'FIO': 'FIO3', 'email': 'mail3@mail.ru', 'num_cart': 'num_cart3',
                     'pw_hash': 'pbkdf2:sha256:50000$IiG5fCla$dce5dfea9c1a0e61f6f987aaac7f579d0f5ee68ffdd830e3b399f21fa4947c76'}  # pw_hash3
            user4 = {'_id': 4, 'FIO': 'FIO4', 'email': 'mail4@mail.ru', 'num_cart': 'num_cart4',
                     'pw_hash': 'pbkdf2:sha256:50000$IiG5fCla$dce5dfea9c1a0e61f6f987aaac7f579d0f5ee68ffdd830e3b399f21fa4947c76'}  # pw_hash3
            user5 = {'_id': 5, 'FIO': 'FIO5', 'email': 'mail5@mail.ru', 'num_cart': 'num_cart5',
                     'pw_hash': 'pbkdf2:sha256:50000$IiG5fCla$dce5dfea9c1a0e61f6f987aaac7f579d0f5ee68ffdd830e3b399f21fa4947c76'}  # pw_hash3
            user6 = {'_id': 6, 'FIO': 'FIO6', 'email': 'mail6@mail.ru', 'num_cart': 'num_cart6',
                     'pw_hash': 'pbkdf2:sha256:50000$IiG5fCla$dce5dfea9c1a0e61f6f987aaac7f579d0f5ee68ffdd830e3b399f21fa4947c76'}  # pw_hash3
            user7 = {'_id': 7, 'FIO': 'FIO7', 'email': 'mail7@mail.ru', 'num_cart': 'num_cart7',
                     'pw_hash': 'pbkdf2:sha256:50000$IiG5fCla$dce5dfea9c1a0e61f6f987aaac7f579d0f5ee68ffdd830e3b399f21fa4947c76'}  # pw_hash3
            user8 = {'_id': 8, 'FIO': 'FIO8', 'email': 'mail8@mail.ru', 'num_cart': 'num_cart8',
                     'pw_hash': 'pbkdf2:sha256:50000$IiG5fCla$dce5dfea9c1a0e61f6f987aaac7f579d0f5ee68ffdd830e3b399f21fa4947c76'}  # pw_hash3
            user9 = {'_id': 9, 'FIO': 'FIO9', 'email': 'mail9@mail.ru', 'num_cart': 'num_cart9',
                     'pw_hash': 'pbkdf2:sha256:50000$IiG5fCla$dce5dfea9c1a0e61f6f987aaac7f579d0f5ee68ffdd830e3b399f21fa4947c76'}  # pw_hash3
            user10 = {'_id': 10, 'FIO': 'FIO10', 'email': 'mail10@mail.ru', 'num_cart': 'num_cart10',
                      'pw_hash': 'pbkdf2:sha256:50000$IiG5fCla$dce5dfea9c1a0e61f6f987aaac7f579d0f5ee68ffdd830e3b399f21fa4947c76'}  # pw_hash3

            users.replace_one({'_id': 1}, user1, True)
            users.replace_one({'_id': 2}, user2, True)
            users.replace_one({'_id': 3}, user3, True)
            users.replace_one({'_id': 4}, user4, True)
            users.replace_one({'_id': 5}, user5, True)
            users.replace_one({'_id': 6}, user6, True)
            users.replace_one({'_id': 7}, user7, True)
            users.replace_one({'_id': 8}, user8, True)
            users.replace_one({'_id': 9}, user9, True)
            users.replace_one({'_id': 10}, user10, True)

    def setUp(self):
        self.client = app.test_client()

    # @unittest.skip("игнорирование")
    def test_login_post(self):
        resp = self.client.post('/login', data=dict(
            email='mail1@mail.ru',
            password='pw_hash1'
        ), follow_redirects=True)
        # print resp.get_data()
        data = json.loads(resp.get_data())
        # print data
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(data['error'], None)
        self.assertEquals(data['result'], 'ok')

    # @unittest.skip("игнорирование")
    def test_login_post_bad_pass(self):
        resp = self.client.post('/login', data=dict(
            email='mail1@mail.ru',
            password='pw_hash5'
        ), follow_redirects=True)
        data = json.loads(resp.get_data())
        # print data
        self.assertEquals(resp.status_code, 401)
        self.assertEquals(data['error'], 'email or password are wrong')

    # @unittest.skip("игнорирование")
    def test_login_post_bad_login(self):
        resp = self.client.post('/login', data=dict(
            email='mail5@mail.ru',
            password='pw_hash1'
        ), follow_redirects=True)
        data = json.loads(resp.get_data())
        # print data
        self.assertEquals(resp.status_code, 401)
        self.assertEquals(data['error'], 'email or password are wrong')

    # @unittest.skip("игнорирование")
    def test_logout(self):
        resp = self.client.get('/logout', follow_redirects=True)
        self.assertEquals(resp.status_code, 401)

    # @unittest.skip("игнорирование")
    def test_forget_mail_post_bad_mail(self):
        resp = self.client.post('/forget_mail', data=dict(
            email='mail500@mail.ru'
        ), follow_redirects=True)
        data = json.loads(resp.get_data())
        # print data
        self.assertEquals(resp.status_code, 401)
        self.assertEquals(data['error'], 'Invalid email')

    @unittest.skip("игнорирование")
    def test_forget_mail_post_mail(self):
        resp = self.client.post('/forget_mail', data=dict(
            email='mail1@mail.ru',
        ), follow_redirects=True)

        data = json.loads(resp.get_data())
        print data
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(data['error'], None)
        self.assertEquals(data['result'], 'ok')

    def forget_mail_post_prep_mail(self):
        self.client.post('/forget_mail', data=dict(
            email='mail1@mail.ru',
        ), follow_redirects=True)

    # @unittest.skip("игнорирование")
    def test_forget_pass_post_bad_pass(self):
        self.forget_mail_post_prep_mail()
        resp = self.client.post('/forget_pass', data=dict(
            password='pw_hash5'
        ), follow_redirects=True)
        data = json.loads(resp.get_data())
        # print data
        self.assertEquals(resp.status_code, 401)
        self.assertEquals(data['error'], 'Invalid password')

    @unittest.skip("игнорирование")
    # необходимо прочитать пароль из письма на сервере
    def test_forget_pass_post_pass(self):
        self.forget_mail_post_prep_mail()
        resp = self.client.post('/forget_pass', data=dict(
            password='pw_hash123'
        ), follow_redirects=True)
        data = json.loads(resp.get_data())
        print data
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(data['error'], None)


# @unittest.skip("игнорирование")
class UserTestClass(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def login_post(self):
        self.client.post('/login', data=dict(
            email='mail1@mail.ru',
            password='pw_hash1'
        ), follow_redirects=False)

    # @unittest.skip("игнорирование")
    def test_get_user(self):
        self.login_post()
        resp = self.client.get('/users/get_user', follow_redirects=True)
        data = json.loads(resp.get_data())
        # print data
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(data['error'], None)


# @unittest.skip("игнорирование")
class BonusTrTestClass(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    # генератор бонусных транзакций
    def gen_bonus_tr(self):
        with app.app_context():
            db = get_db()
            users = db.users
            for r in xrange(30):
                id_user = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
                places = [u'Абакан', u'Анадырь (Угольный)', u'Анапа (Витязево)', u'Архангельск (Талаги)',
                          u'Астрахань (Нариманово)', u'Барнаул (Михайловка)', u'Белгород', u'Благовещенск (Игнатьево)',
                          u'Братск', u'Брянск', u'Владивосток (Кневичи)', u'Владикавказ (Беслан)',
                          u'Волгоград (Гумрак)', u'Вологда', u'Воронеж (Чертовицкое)', u'Горно-Алтайск',
                          u'Грозный (Северный)', u'Екатеринбург (Кольцово)', u'Иваново (Южный)', u'Ижевск']
                from_place = random.choice(places)
                to_place = random.choice(places)
                user = users.find_one({'_id': id_user})
                bonus_tr = {'num_tr': b64encode(urandom(20)), 'c_bonus': random.randint(1, 100),
                            'date_fly': datetime(2017, 10, random.randint(1, 30)).strftime("%Y.%m.%d"),
                            'from_place': from_place, 'to_place': to_place}
                bonus_tr.update(user)
                yield bonus_tr

    # @unittest.skip("игнорирование")
    def test_post_bonus_tr(self):
        with app.app_context():
            gen_tr = self.gen_bonus_tr()
            list_bonus_tr = []
            for bonus_tr in gen_tr:
                list_bonus_tr.append(bonus_tr)

            strIO = StringIO.StringIO()
            strIO.write(json.dumps(list_bonus_tr, ensure_ascii=False))
            strIO.seek(0)
            hauth = {'Authorization': 'Basic ' + b64encode('admin:secret')}
            resp = self.client.post('/import_bonus_transact/set_bonus_transact', data=strIO, headers=hauth)
            self.assertEquals(resp.status_code, 200)

    # @unittest.skip("игнорирование")
    def test_post_bonus_tr_failed(self):
        with app.app_context():
            gen_tr = self.gen_bonus_tr()
            list_bonus_tr = []
            for bonus_tr in gen_tr:
                list_bonus_tr.append(bonus_tr)
            strIO = StringIO.StringIO()
            strIO.write(json.dumps(list_bonus_tr, ensure_ascii=False))
            strIO.seek(0)
            resp = self.client.post('/import_bonus_transact/set_bonus_transact', data=strIO)
            # print resp.data
            self.assertEquals(resp.status_code, 401)

    def login_post(self):
        self.client.post('/login', data=dict(
            email='mail1@mail.ru',
            password='pw_hash1'
        ), follow_redirects=True)

    # @unittest.skip("игнорирование")
    def test_get_bonus_tr(self):
        self.login_post()
        resp = self.client.get('/bonus_transact/get_bonus_transact?num_page=1', follow_redirects=True)
        # print resp.data
        self.assertEquals(resp.status_code, 200)

    # @unittest.skip("игнорирование")
    def test_get_bonus_tr_filter(self):
        self.login_post()
        resp = self.client.get('/bonus_transact/get_bonus_transact?num_page=1&c_bonus=50', follow_redirects=True)
        # print resp.data
        self.assertEquals(resp.status_code, 200)


if __name__ == '__main__':
    # with app.app_context():
    # clear_bonus_transact()
    # unittest.main(verbosity=2)
    unittest.main()
