import threading
import socket
import json
import time
import uartcontrol
import os

print(os.name)

sock = socket.socket()
dev = uartcontrol.Vodomat()


def connect():
    sock.connect(("192.168.10.32", 8080))


def send(info, method="status"):
    d = {"method": method, "param": info}
    d = json.dumps(d)
    sock.send(d.encode("utf-8"))


def seans(info):
    data = sock.recv(2048).decode()
    if not data:
        raise IOError
    print("response %s" % data)
    response = json.loads(data)
    try:
        method = response["method"]
        param = response["param"]
    except json.JSONDecodeError as e:
        method = "error"
        param = {"types": "json", "msg": e.msg}
    except KeyError as e:
        method = "error"
        param = {"types": "notKey", "msg": e.args}
    time.sleep(1)
    if method == "GetWater":
        if int(param["idv"]) == info["idv"]:
            if dev.devInfo["state"] == uartcontrol.stateList[uartcontrol.state]:
                pass
                # dev.payment(param["score"])
            send(info)
    elif method == "ToUpBalance":
        if int(param["idv"]) == info["idv"]:
            # w = dev.getPutting()
            param["score"] = 10000
            send(param, method="Answer")
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

