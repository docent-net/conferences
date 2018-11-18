from flask import Flask
from flask import Response
from flask import request
import logging

application = Flask(__name__)

application.logger.addHandler(logging.StreamHandler())
application.logger.setLevel(logging.INFO)

@application.route("/")
def hello():
    return open('index.html', 'r').read()

@application.route("/auth")
def authenticate_user():
    if request.remote_addr == '192.168.122.12':
        application.logger.info('authenticated')
        txt = open('index.html', 'r').read()
        resp = Response(txt, status=200, mimetype='text/html')
    else:
        application.logger.info('auth-error, wrong client-IP: %s' % format(request.remote_addr))
        resp = Response('no', status=401, mimetype='text/html')
    return resp

if __name__ == "__main__":
    application.run(host='127.0.0.1', port=8000)