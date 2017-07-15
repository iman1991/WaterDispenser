import threading
import socket
import json
import time
import uartcontrol


sock = socket.socket()
dev = uartcontrol.Vodomat("/dev/ttyAMA0", 38400)


def connect():
    sock.connect(("194.67.217.180", 8080))


def send(info, method="status"):
    d = {"method": method, "param": info}
    d = json.dumps(d)
    sock.send(d.encode("utf-8"))


def seans(info):
    data = sock.recv(2048).decode()
    if not data:
        raise IOError
    response = json.loads(data)
    print(response)
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
            if dev.devInfo["state"] == "WAIT":
                dev.payment(param["score"])
            send(info)
    elif method == "ToUpBalance":
        if int(param["idv"]) == info["idv"]:
            param["score"] += dev.getPutting()
            print(param["score"])
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
