import socket
import json
import time
from config import server

REPORT = 0
ANSWAER = 1
PAYMENT = 2
PUTTING = 3

class Net(object):
    def __init__(self):
        self.sock = socket.socket()
        self.cmd = 0


    def getCommand(self):
        data = self.sock.recv(2048)
        method, param = self.parsing_package(data)
        if method == "Start":
            pass
        elif method == "Stop":
            param = {}
        elif method == "error":
            self.resetCmd()
        else:
            self.resetCmd()


    def parsing_package(self, data):
        if not data:
            method = "error"
            param = {"types": "not data ", "msg": "not data in request"}
            return method, param
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

        return method, param


    def setCmd(self, command):
        self.cmd = command


    def resetCmd(self):
        self.cmd = REPORT


    def report(self, row):
        if self.cmd == 0:
            self.set_data(row)
        elif self.cmd == 1:
            self.resetCmd()
            self.set_data(row, method="Answer")


    def set_data(self, row, method="status"):
        d = {"method": method, "param": row}
        d = json.dumps(d)
        self.send(d)


    def send(self, data):
        self.sock.send(data.encode("utf-8"))


    def connect(self):
        try:
            self.sock.connect((server["ip"], server["port_main"]))
        except:
            self.sock.connect((server["ip"], server["port_reserv]"]))
