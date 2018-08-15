#!/usr/bin/env python3
import connexion
import logging

from commands import cmd_take_photo
from commands import cmd_generic
from flask import request


def g1_cmd(cmd, data):
    output = cmd_generic(cmd, data)
    return output


def go_home():
    # return flask.send_from_directory('static', 'index.html')
    return "<html><body><h2>  FP560 home </h2><p>For the Rest Api commands doc go to:</p><p><a href='/ui/#/'>Swagger GUI page!</a></p></body></html>"


def g21_cmd():
    output = cmd_take_photo()
    b_url = request.base_url.strip("g21_cmd")
    return b_url + output


logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__)
app.add_api('swagger.yaml')
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app


if __name__ == '__main__':
    app.run(port=8090)
