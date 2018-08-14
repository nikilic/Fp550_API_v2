#!/usr/bin/env python3
import connexion
import datetime
import logging
import json
import config

from connexion import NoContent
from commands import cmd_Get_Date_Time, cmd_Get_PIB, cmd_Paper_Move, cmd_Get_Status, cmd_Get_Tax, cmd_Get_Diag,cmd_report_ART_All
from commands import cmd_take_photo, cmd_Get_Set_Tax
from flask import Flask, request
import orm
import flask
if config.sim:
    """
    pck_Data = "\x80\x80\x80\x85\x80\xba"  # hex(ord("a"))
    pck_Len = hex(ord("b"))
    pck_Cmd = hex(ord("c"))
    pck_Seq = hex(ord("d"))
    pck_Sts = hex(ord("e"))
    """

db_session = None
def foo_get(cmd,DataF):
    # do something
    return 'You send the message: {}'.format(chr(cmd) + DataF), 200
def go_home():
    # return flask.send_from_directory('static', 'index.html')
    return ("<html><body><h2>  FP560 home </h2><p>For the Rest Api commands doc go to:</p><p><a href='/ui/#/'>Swagger GUI page!</a></p></body></html>")
def g11_cmd():
    output = cmd_Get_Date_Time()
    return output
def g12_cmd():
    output = cmd_Get_PIB()
    return output
def g13_cmd(n_lines):
    output = cmd_Paper_Move(n_lines)
    return output

def g14_cmd():
    output = cmd_Get_Status()
    return output
def g15_cmd():
    output = cmd_Get_Tax()
    return output
def g16_cmd():
    output = cmd_Get_Diag()
    return output
def g17_cmd():
    output = cmd_report_ART_All()
    return output
def g18_cmd():
    output = cmd_Get_Set_Tax()
    return output
def g21_cmd():
    output = cmd_take_photo()
    b_url = request.base_url.strip("g21_cmd")
    return b_url + output

def post_greeting(name: str) -> str:
    return 'Hello {name}'.format(name=name)
def post_greeting1():
    hell = {
        "name":"Dusan",
        "author":"yes"
    }
    print(hell)
    he = json.dumps(hell)
    print(he)

    return he

def get_pets(limit, animal_type=None):
    q = db_session.query(orm.Pet)
    # w=db_session.query(orm.Pet)
    if animal_type:
        q = q.filter(orm.Pet.animal_type == animal_type)
    return [p.dump() for p in q][:limit]

def get_pet(pet_id):
    pet = db_session.query(orm.Pet).filter(orm.Pet.id == pet_id).one_or_none()
    return pet.dump() or ('Not found', 404)


def put_pet(pet_id, pet):
    p = db_session.query(orm.Pet).filter(orm.Pet.id == pet_id).one_or_none()
    pet['id'] = pet_id
    if p is not None:
        logging.info('Updating pet %s..', pet_id)
        p.update(**pet)
    else:
        logging.info('Creating pet %s..', pet_id)
        pet['created'] = datetime.datetime.utcnow()
        db_session.add(orm.Pet(**pet))
    db_session.commit()
    return NoContent, (200 if p is not None else 201)


def delete_pet(pet_id):
    pet = db_session.query(orm.Pet).filter(orm.Pet.id == pet_id).one_or_none()
    if pet is not None:
        logging.info('Deleting pet %s..', pet_id)
        db_session.query(orm.Pet).filter(orm.Pet.id == pet_id).delete()
        db_session.commit()
        return NoContent, 204
    else:
        return NoContent, 404

logging.basicConfig(level=logging.INFO)
db_session = orm.init_db('sqlite:///dv_pet.db')
app = connexion.App(__name__)
app.add_api('swagger.yaml')
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(port=8090)
