#!/usr/bin/env python3
# -*- coding: utf-8 -*-ls

import threading
import socket
import json
import time
from uartcontrol import dev
import agent
from  config import server




def connect():
    try:
        sock.connect((server["ip"], server["port_main"]))
    except:
        sock.connect((server["ip"], server["port_reserv]"]))


def send(info, method="status"):
    d = {"method": method, "param": info}
    d = json.dumps(d)
    sock.send(d.encode("utf-8"))


def seans(info):
    data = sock.recv(2048).decode()
    if not data:
        return
    try:
        response = json.loads(data)
        method = response["method"]
        if method == "got":
            print("got")
        else:
            print("#!response # %s}" % response)
        param = response["param"]
    except ValueError as e:
        method = "error"
        print("error JSON {%s}" % data)
        param = {"types": "json", "msg": e.args}
    except KeyError as e:
        method = "error"
        param = {"types": "notKey", "msg": e.args}
    except Exception as e:
        method = "error"
        param = {"types": "error fotall", "msg": e.args}


    time.sleep(1)
    if method == "got":
        dev.readinfo()
        send(info)
    elif method == "Start":
        if int(param["idv"]) == info["idv"]:
            if dev.devInfo["state"] == "WAIT":
                dev.payment(param["score"])
        send(info)
        print("payment")
    elif method == "Stop":
        param["score"] = dev.getPutting()
        param["Status"] = dev.devInfo
        print(param["score"])
        send(param, method="Answer")
        print("get Putting")
    elif method == "error":
        print("error %s" % param)
        send(param, method="error")
    else:
        dev.readinfo()
        send(info)

sock = socket.socket()
if __name__ == "__main__":
    try:
        connect()
    except:
        print("exit: not connect")
        exit(0)
    else:
        zabagent = threading.Thread(target=agent.startAgent)
        zabagent.start()
        send(dev.devInfo, method="connect")
        while True:
            seans(dev.devInfo)