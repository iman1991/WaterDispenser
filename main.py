#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import socket
import json
import time
import uartcontrol


sock = socket.socket()
dev = uartcontrol.Vodomat("/dev/ttyAMA0", 38400)



def connect():
    try:
        sock.connect(("194.67.217.180", 8080))
    except:
        sock.connect(("194.67.217.180", 9090))

def send(info, method="status"):
    d = {"method": method, "param": info}
    d = json.dumps(d)
    if method != "status":
        print(d)
    sock.send(d.encode("utf-8"))


def seans(info):
    data = sock.recv(2048).decode()
    if not data:
        raise IOError
    try:
        response = json.loads(data)
        method = response["method"]
        if method != "got":
            print(response)
        param = response["param"]

    except ValueError as e:
        method = "error"
        print(data)
        param = {"types": "json", "msg": e.args}
    except KeyError as e:
        method = "error"
        param = {"types": "notKey", "msg": e.args}
    except Exception as e:
        method = "error"
        param = {"types": "error fotall", "msg": e.args}


    time.sleep(1)
    if method == "GetWater":
        # if int(param["idv"]) == info["idv"]:
        #     if dev.devInfo["state"] == "WAIT":
        #         dev.payment(param["score"])
        send(info)
    elif method == "ToUpBalance":
        # if int(param["idv"]) == info["idv"]:
        #     param["score"] += dev.getPutting()
        param["score"] = 10000
        send(param, method="AnswerUP")
    elif method == "error":
        send(param, method="error")
    else:
        send(info)


if __name__ == "__main__":
    thread = threading.Thread(target=dev.startUart)
    thread.start()
    connect()
    send(dev.devInfo, method="connect")
    while True:
        seans(dev.devInfo)
