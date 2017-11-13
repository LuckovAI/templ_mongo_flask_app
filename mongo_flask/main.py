# -*- coding: utf-8 -*-

from flask import Flask, Response, g, session, request, url_for, redirect
from mongo_flask.utils import load_config, get_db, register_blueprints, init_log, is_auth
from werkzeug import check_password_hash, generate_password_hash
from gevent import monkey, sleep
from gevent.pywsgi import WSGIServer
from os import urandom
import json
from base64 import b64encode
import smtplib
from email.MIMEText import MIMEText

# защита от перебора
SLEEP = 2

monkey.patch_all()

app = Flask(__name__)
conf = load_config()
app.config.update(conf)
register_blueprints(app)
init_log(app)
http_server = WSGIServer(('', 5000), app.wsgi_app)


@app.route('/', methods=['GET'], endpoint='index')
@is_auth
def index():
    return redirect(url_for('users.get_user'))


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        db = get_db()
        g.user = db.users.find_one({"_id": session['user_id']})


@app.route('/login', methods=['POST'])
def login():
    if g.user:
        return Response(
            status=200,
            mimetype="application/json",
            response=json.dumps({'error': None, 'result': 'ok'})
        )
    error = None
    db = get_db()
    user = db.users.find_one({"email": request.values['email']})
    if user is None:
        sleep(SLEEP)
        error = 'email or password are wrong'
    elif not check_password_hash(user['pw_hash'], request.values['password']):
        sleep(SLEEP)
        error = 'email or password are wrong'
    else:
        session['user_id'] = user['_id']
        return Response(
            status=200,
            mimetype="application/json",
            response=json.dumps({'error': None, 'result': 'ok'})
        )

    return Response(
        status=401,
        mimetype="application/json",
        response=json.dumps({'error': error, 'result': None})
    )


# для формы "введите почту"
@app.route('/forget_mail', methods=['POST'])
def forget_mail():
    error = None
    db = get_db()
    user = db.users.find_one({"email": request.values['email']})
    if user is None:
        sleep(SLEEP)
        error = 'Invalid email'
    else:
        forget_pass = b64encode(urandom(10))
        session['forget_pass'] = forget_pass
        session['email'] = request.values['email']
        res = sent_to_mail(request.values['email'], forget_pass)
        return Response(
            status=res[0],
            mimetype="application/json",
            response=json.dumps({'result': res[1], 'error': res[2]})
        )

    return Response(
        status=401,
        mimetype="application/json",
        response=json.dumps({'result': None, 'error': error})
    )


# для формы "введите пароль полученный с почты"
@app.route('/forget_pass', methods=['POST'])
def forget_pass():
    error = None
    if not request.values['password'] == session.get('forget_pass'):
        sleep(SLEEP)
        error = 'Invalid password'
    else:
        db = get_db()
        user = db.users.find_one({"email": session['email']})
        session['user_id'] = user['_id']
        session.pop('forget_pass', None)
        session.pop('email', None)
        return Response(
            status=200,
            mimetype="application/json",
            response=json.dumps({'error': None, 'result': 'ok'})
        )
    return Response(
        status=401,
        mimetype="application/json",
        response=json.dumps({'error': error, 'result': None})
    )


def sent_to_mail(email, forget_pass):
    fromaddr = app.config.get('base_conf').get('mail')
    password = app.config.get('base_conf').get('mpass')
    mserver = app.config.get('base_conf').get('server')
    msg = MIMEText("Temporary password: " + forget_pass, "", "utf-8")
    msg['Subject'] = "Temporary password"
    msg['From'] = fromaddr
    msg['To'] = email

    try:
        server = smtplib.SMTP_SSL(mserver)
        server.login(fromaddr.split('@')[0], password)
    except Exception, exc:
        app.logger.debug(str(exc))
        print str(exc)
        return (500, None, str(exc))

    try:
        server.sendmail(fromaddr, email, msg.as_string())
        server.quit()
    except Exception, exc:
        print str(exc)
        return (401, None, str(exc))

    return (200, 'ok', None)

#
# if __name__ == '__main__':
# Псевдомногопоточность
# http_server.serve_forever()
# app.run(debug=True)
