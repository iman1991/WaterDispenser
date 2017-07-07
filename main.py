import threading
import socket
import json
import time
import argparse
import uartcontrol


sock = socket.socket()






# devInfo = {
#     "idv": 1,
#     "state": "NO_WATER",
#     "input10Counter ": 0,
#     "out10Counter": 0,
#     "milLitlose": 0,
#     "milLitWentOut": 0,
#     "milLitContIn": 0,
#     "waterPrice": 0,
#     "containerMinVolume": 0,
#     "contVolume": 0,
#     "totalPaid": 0,
#     "sessionPaid": 0,
#     "leftFromPaid": 0,
#     "container": "TOO_LOW",
#     "currentContainerVolume": 0,
#     "consumerPump": False,
#     "mainPump": False,
#     "magistralPressure": False,
#     "mainValve": False,
#     "filterValve": False,
#     "washFilValve": False,
#     "tumperMoney": False,
#     "tumperDoor": False,
#     "serviceButton": False,
#     "freeBattom": False,
#     "Voltage": 0
# }



def connect():
    sock.connect(("192.168.10.32", 8080))


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--baud", nargs="?", type=int, default=38400,
                        help="скорость передачи данных, по умолчанию равно 38400")
    parser.add_argument("-p", "--port", nargs="?", default="/dev/ttyUSB0",
                        help="порт по которому опрашивается устройство")
    return parser


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
        response = json.loads(data)
        method = response["method"]
        param = response["param"]
        print("response %s" % data)
        time.sleep(1)
        if method == "GetWater":
            if int(param["idv"]) == info["idv"]:
                pass
        elif method == "ToUpBalans":
            if int(param["idv"]) == info["idv"]:
                pass
        send(info)



if __name__ == "__main__":

    seans(uartcontrol.devInfo)

