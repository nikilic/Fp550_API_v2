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
    return "<html><body><h2>  FP560 home </h2><p>For the Rest Api commands doc go to:</p>" \
           "<p><a href='/ui/#/'>Swagger GUI page!</a></p></body></html>"


def g21_cmd():
    output = cmd_take_photo()
    b_url = request.base_url.strip("g21_cmd")
    return b_url + output


def g31_cmd(data):
    i = 0
    n = 0
    line = ""
    linearray = []
    for char in data:
        print(ord(char))
        if ord(char) == 10:
            i = 0
            linearray.append(line)
            line = ""
            print("ENTER")
        elif i == 31:
            i = 0
            line = line + char
            linearray.append(line)
            line = ""
            print("LINE END")
        elif n + 1 == len(data):
            line = line + char
            linearray.append(line)
        elif char == " ":
            if i == 0:
                i += 1
            else:
                line = line + char
        else:
            i += 1
            line = line + char
        n += 1

    output = cmd_generic(38, "")
    for lines in linearray:
        output = cmd_generic(42, lines)
    output = cmd_generic(39, "")
    return "Printed successfully"


logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__)
app.add_api('swagger.yaml')
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app


if __name__ == '__main__':
    app.run(port=8090)
