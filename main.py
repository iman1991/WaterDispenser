import socket
import json
import time
sock = socket.socket()

devInfo = {
    "idv": 1,
    "state": "NO_WATER",
    "input10Counter ": 0,
    "out10Counter": 0,
    "milLitlose": 0,
    "milLitWentOut": 0,
    "milLitContIn": 0,
    "waterPrice": 0,
    "containerMinVolume": 0,
    "contVolume": 0,
    "totalPaid": 0,
    "sessionPaid": 0,
    "leftFromPaid": 0,
    "container": "TOO_LOW",
    "currentContainerVolume": 0,
    "consumerPump": False,
    "mainPump": False,
    "magistralPressure": False,
    "mainValve": False,
    "filterValve": False,
    "washFilValve": False,
    "tumperMoney": False,
    "tumperDoor": False,
    "serviceButton": False,
    "freeBattom": False,
    "Voltage": 0
}

def connect():
    sock.connect(("192.168.10.32", 9090))


def send(info, method="status"):

    d = {"method": method, "param": info}
    d = json.dumps(d)
    sock.send(d.encode("utf-8"))


def seans(info):
    connect()
    print("Running")
    send(info, method="connect")
    while True:
        data = sock.recv(2048).decode()

        if not data:
            raise IOError
        if data != {"method": "status", "param": "saved"}:
            print("response '%s'" % data)
        response = json.loads(data)
        method = response["method"]
        param = response["param"]
        # time.sleep(1)
        if method == "GetWater":
            if param["idv"] == info["idv"] and param["balance"] > 0.1:
                send(info)
        elif method == "ToUpBalans":
            if param["idv"] == info["idv"] and param["balance"] > 0.1:
                send(info)
        elif method == "GetInfo":
            send(info)
        else:
            send(info)



seans(devInfo)

