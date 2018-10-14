#!/usr/bin/env python3
import connexion
import logging
import html2text
import time

from commands import cmd_take_photo
from commands import cmd_generic, cmd_Write_Article
from flask import request, make_response, jsonify
from flask_cors import CORS
from flask_cors import cross_origin
#  CORS(app, resources=r'/hw_proxy/*')


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


def g32_cmd(data):
    """Prints fiscal receipt and returns confirmation or error"""
    if g32DataCheck(data) != True:
        return g32DataCheck(data)

    dataArray = data.split("/")
    output = cmd_generic(48, "1;1,1")
    suma = 0
    try:
        if output["recv_pck_Data"][4] != 44:
            return "Error Command 48"
    except:
        return "Error Command 48"
    for i in range(0, len(dataArray)):
        dataPurchase = dataArray[i].split(",")
        suma += float(dataPurchase[1]) * float(dataPurchase[2])
        output = cmd_generic(52, "S+"+dataPurchase[0]+"*"+dataPurchase[1]+"#"+dataPurchase[2])
        time.sleep(.300)
        if output["recv_pck_Data"][0] != 80:
            return "Error Print Article " + str(i)
    output = cmd_generic(53, "P"+str(suma))
    output = cmd_generic(56, "")
    return "Printed successfully"


def g32DataCheck(data):
    """Checks formatting and product existence for g32_cmd(). Returns True or error message"""
    dataArray = data.split("/")
    for ln in dataArray:
        lnArray = ln.split(",")
        if len(lnArray) != 3:
            return "Bad formatting"
        try:
            pluInt = int(lnArray[0])
            if not isinstance(pluInt, int):
                return "Bad formatting"

            if "." in lnArray[1]:
                qtyFloat = lnArray[1].split(".")
                if len(qtyFloat) != 2:
                    return "Bad formatting"
                else:
                    qty1Int = int(qtyFloat[0])
                    qty2Int = int(qtyFloat[1])
                    if not isinstance(qty1Int, int) and not isinstance(qty2Int, int) and len(qtyFloat[1]) == 2:
                        return "Bad formatting"
            else:
                qtyInt = int(lnArray[1])
                if not isinstance(qtyInt, int):
                    return "Bad formatting"

            if "." in lnArray[2]:
                priceFloat = lnArray[2].split(".")
                if len(priceFloat) != 2:
                    return "Bad formatting"
                else:
                    price1Int = int(priceFloat[0])
                    price2Int = int(priceFloat[1])
                    if not isinstance(price1Int, int) and not isinstance(price2Int, int) and len(priceFloat[1]) == 2:
                        return "Bad formatting"
            else:
                priceInt = int(lnArray[2])
                if not isinstance(priceInt, int):
                    return "Bad formatting"
        except:
            return "Bad formatting"
        output = cmd_generic(107, "R" + str(lnArray[0]))
        if output["recv_pck_Data"][0] != 80:
            return "Article not in database. PLU: " + lnArray[0]
    return True


def g33_cmd(plu, price, name):
    data = "P" + chr(128) + str(plu) + "," + str(price) + "," + str(name)
    #data="P"+"\x80"+"00034,55,ROBA-AB"
    print(data)
    output = cmd_generic(107, data)
    # output = cmd_Write_Article()
    return output


def g34_cmd():
    output = cmd_generic(107, "F")
    articles = ""
    count = 0
    while True:
        for ch in output["recv_pck_Data"]:
            if ch == 4:
                output = cmd_generic(107, "N")
                count = 0
            elif ch == 70 and count == 0:
                return articles
            elif count == 0:
                articles += "/" + chr(ch)
                count += 1
            else:
                articles += chr(ch)
                count += 1


def hello():
    # return PING
    png = 'ping'
    return make_response('ping')
def handshake_json():

    return jsonify(jsonrpc='2.0', result=True)
def status_json():
    statuses = {}
    '''
    for driver in drivers:
        statuses[driver] = drivers[driver].get_status()
        print (statuses)
    '''
    statuses = {
 'escpos': {'status': 'connected', 'messages': []
            }
}

    return jsonify(jsonrpc='2.0', result=statuses)

def print_xml_receipt_json():

    #print(request.json)

    receipt = request.json['params']['receipt']
    print(receipt)
    s = html2text.html2text(receipt)
    start=s.find('-AAA-')
    end = s.find('-ZZZ-')
    articles = s[start:end]
    print (articles)
    ar_lines = articles.split(';',20)
    print (ar_lines[0], ar_lines[1], ar_lines[2])
    data=""
    for lin in ar_lines:


        ar_lin= lin.split('|',8)
        print (ar_lin)
        if len(ar_lin) >= 5:
            data=data + ar_lin[2]  +',' + ar_lin[4] + ',' + ar_lin[6] +'/'
            print (ar_lin[3])
    data=data.replace(' ','')
    data=data[:-1]
    print (data)
    output = g32_cmd(data)
    return jsonify(jsonrpc='2.0', result=True)



logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__)
app.add_api('swagger.yaml')
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app
# add CORS support
CORS(app.app)

if __name__ == '__main__':
    app.run(port=8090)
