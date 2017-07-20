#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import socket
import json
import time
from uartcontrol import dev
import agent

sock = socket.socket()


def connect():
    try:
        sock.connect(("194.67.217.180", 8080))
    except:
        sock.connect(("194.67.217.180", 9090))


def send(info, method="status"):
    d = {"method": method, "param": info}
    d = json.dumps(d)
    if method == "connect":
        print("connect")
    elif method != "status":
        print(d)
    sock.send(d.encode("utf-8"))


def seans(info):
    data = sock.recv(2048).decode()
    if not data:
        return
    try:
        response = json.loads(data)
        method = response["method"]
        if method != "got":
            print("response %s" % response)
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
    if method == "Activate":
        if int(param["idv"]) == info["idv"]:
            if dev.devInfo["state"] == "WAIT":
                dev.payment(param["score"])
        send(info)
    elif method == "Stop":
        if int(param["idv"]) == info["idv"]:
            param["score"] = dev.getPutting()
        param["status"] = dev.devInfo
        send(param, method="AnswerUP")
    elif method == "error":
        send(param, method="error")
    else:
        send(info)


if __name__ == "__main__":
    try:
        connect()
    except:
        print("exit: not connect")
        exit(0)
    else:
        thread = threading.Thread(target=dev.startUart)
        thread.start()
        zabagent = threading.Thread(target=agent.startAgent)
        zabagent.start()
        send(dev.devInfo, method="connect")
        while True:
            seans(dev.devInfo)
