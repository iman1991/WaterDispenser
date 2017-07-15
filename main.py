import threading
import socket
import json
import time
import argparse
import uartcontrol


sock = socket.socket()
dev = uartcontrol.Vodomat("/dev/ttyAMA0", 38400)


def connect():
    sock.connect(("192.168.10.32", 9090))


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
            if dev.devInfo["state"] == "WAIT":
                dev.payment(param["score"])
            send(info)
    elif method == "ToUpBalance":
        if int(param["idv"]) == info["idv"]:
            param["score"] = dev.getPutting()
            send(param, method="Answer")
    elif method == "error":
        send(param, method="error")
    else:
        send(info)


if __name__ == "__main__":
    thread = threading.Thread(target=dev.startUart)
    thread.start()
    time.sleep(1)
    while True:
        c = input("0 - payment\n1 - get money\n2 - enable\n3 - disable\n -->")
        if c == "0":
            g = int(input("score \n"))
            print(dev.payment(g))
        elif c == "1":
            print(dev.getPutting())
        elif c == "2":
            print(dev.enablePayment())
        elif c == "3":
            print(dev.disablePayment())
        elif c == "4":
            print(dev.readinfo())
        elif c == 'q':
            exit()
