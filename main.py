#!/usr/bin/python3
# -*- coding: utf-8 -*-ls
import threading
import socket
import json
import time
from uartcontrol import dev
import agent
from config import server


command = {"cmd": 0}

def setCmd(cmd):
    command.update({"cmd": cmd})


request = {}

def connect():
    try:
        sock.connect((server["ip"], server["port_main"]))
        print("connect to {}:{}".format(server["ip"], server["port_main"]))
    except:
        sock.connect((server["ip"], server["port_reserv]"]))
        print("connect to {}:{}".format(server["ip"], server["port_reserv"]))


def send(info, method="status"):
    d = {"method": method, "param": info}
    print("method -> {}".format(d["method"]))
    d = json.dumps(d)
    sock.send(d.encode())

def report():
    while True:
        param = request["param"]
        if command["cmd"] == 0:
            dev.readinfo()
            send(dev.devInfo)
        elif command["cmd"] == 1:
            if int(param["idv"]) == dev.devInfo["idv"]:
                if dev.devInfo["state"] == "WAIT":
                    dev.payment(param["score"])
                    send(dev.devInfo)
                    print("payment")
        elif command["cmd"] == 2:
            info = param
            info["score"] = dev.devInfo["leftFromPaid"] // 10000
            dev.getPutting()
            info["Status"] = dev.devInfo
            print(param["score"])
            print("get Putting")
            send(info, "Answer")
        setCmd(0)
        time.sleep(1)






def seans():
    get_request()
    method = request["method"]
    if method == "Start":
        setCmd(1)
    elif method == "Stop":
        setCmd(2)

def get_request():
    data = sock.recv(2048).decode()
    if not data:
        method = "error"
        param = {"types": "not data", "msg": "not data or data is null"}
        request.update({"method": method, "param": param})
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
        param = {"types": "error fatall", "msg": e.args}
    request.update({"method": method, "param": param})


sock = socket.socket()
if __name__ == "__main__":
    while True:
        try:
            connect()
        except:
            print("exit: not connect")
            time.sleep(10)
            continue
        else:
            zabagent = threading.Thread(target=agent.startAgent)
            zabagent.start()
            send(dev.devInfo, method="connect")
            get_request()
            zabagent = threading.Thread(target=report)
            zabagent.start()

            while True:
                seans()
