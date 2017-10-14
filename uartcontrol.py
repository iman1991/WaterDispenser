#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
import json
import config

ID = -1
input10Counter = 0
out10Counter = 1
milLitlose = 2
milLitWentOut = 3
milLitContIn = 4
waterPrice = 5
containerMinVolume = 6
maxContainerVolume = 7
totalPaid = 8
sessionPaid = 9
leftFromPaid = 10
state = 11
container = 12
currentContainerVolume = 13
consumerPump = 14
mainPump = 15
magistralPressure = 16
mainValve = 17
filterValve = 18
washFilValve = 19
tumperMoney = 20
tumperDoor = 21
serviceButton = 22
freeButtom = 23
Voltage = 24
billAccept = 25


GET_INFO = b'g\n'
ENABLE = b'cj\n'
DISABLE = b'ci\n'
PUTTING = b'cm\n'

SETTING = 'cs'
PAYMENT = 'm'
TEXTOUT = 'ct'
FILLTERSET = 'cf'

NOT_ERROR = b'0\n'
ERROR_ASCII = b'-1\n'
ERROR_SHORT = b'-2\n'
ERROR_LONG = b'-3\n'
ERROR_TEST = b'-4\n'


stateList = ["NO_WATER", "WASH_FILTER", "WAIT", "SETTING", "JUST_PAID", "WORK", "SERVICE", "FREE", "NONE"]
containerList = ["TOO_LOW", "NOT_FULL", "FULL"]

class Vodomat(object):
    devInfo = {
        "idv": 1,
        "input10Counter": 0,
        "out10Counter": 0,
        "milLitlose": 0,
        "milLitWentOut": 0,
        "milLitContIn": 0,
        "waterPrice": 0,
        "containerMinVolume": 0,
        "maxContainerVolume": 0,
        "contVolume": 0,
        "totalPaid": 0,
        "sessionPaid": 0,
        "leftFromPaid": 0,
        "state": "WAIT",
        "container": "TOO_LOW",
        "currentContainerVolume": 0,
        "consumerPump": 0,
        "mainPump": 0,
        "magistralPressure": 0,
        "mainValve": 0,
        "filterValve": 0,
        "washFilValve": 0,
        "tumperMoney": 0,
        "tumperDoor": 0,
        "serviceButton": 0,
        "freeButton": 0,
        "Voltage": 0,
        "billAccept": 0,
        "containerGraph": 0,
        "stateGraph": 0

    }


    def __init__(self, port, baud, id):
        self.uart = serial.Serial(port, baud, timeout=1)
        self.devInfo["idv"] = id


    def read(self):
        return self.uart.readline()


    def write(self, data):
        try:
            if type(data) == str:
                data = data.encode("ascii")
            self.uart.write(data)
        except:
            pass


    def checkCode(self, code, types="code"):
        if types == "code":
            if code == NOT_ERROR:
                return True
            else:
                return False
        elif types == "int":
            return int(code)


    def raw2list(self, raw):
        date = json.loads(raw.decode())
        if type(date) != list:
            return
        self.devInfo["input10Counter"] = date[input10Counter]
        self.devInfo["out10Counter"] = date[out10Counter]
        self.devInfo["milLitlose"] = date[milLitlose]
        self.devInfo["milLitWentOut"] = date[milLitWentOut]
        self.devInfo["milLitContIn"] = date[milLitContIn]
        self.devInfo["waterPrice"] = date[waterPrice]
        self.devInfo["containerMinVolume"] = date[containerMinVolume]
        self.devInfo["maxContainerVolume"] = date[maxContainerVolume]
        self.devInfo["totalPaid"] = date[totalPaid]
        self.devInfo["sessionPaid"] = date[sessionPaid]
        self.devInfo["leftFromPaid"] = date[leftFromPaid] // 100
        self.devInfo["state"] = stateList[date[state]]
        self.devInfo["stateGraph"] = date[state]
        self.devInfo["container"] = containerList[date[container]]
        self.devInfo["containerGraph"] = date[container]
        self.devInfo["currentContainerVolume"] = date[currentContainerVolume]
        self.devInfo["consumerPump"] = date[consumerPump]
        self.devInfo["mainPump"] = date[mainPump]
        self.devInfo["magistralPressure"] = date[magistralPressure]
        self.devInfo["mainValve"] = date[mainValve]
        self.devInfo["filterValve"] = date[filterValve]
        self.devInfo["washFilValve"] = date[washFilValve]
        self.devInfo["tumperMoney"] = date[tumperMoney]
        self.devInfo["tumperDoor"] = date[tumperDoor]
        self.devInfo["serviceButton"] = date[serviceButton]
        self.devInfo["freeButton"] = date[freeButtom]
        self.devInfo["Voltage"] = date[Voltage]
        self.devInfo["billAccept"] = date[billAccept]


    def readinfo(self):
        # print("Command readinfo, the lock %s" % self.locked)
        self.write(GET_INFO)
        if self.checkCode(self.read()):
            raw = self.read()
            print(raw)
            try:
                self.raw2list(raw)
            except:
                pass


    def setting(self, _waterPrice, containerMinVolume,_maxContainerVolume):
        msg = "{}{},{},{}\n".format(SETTING, _waterPrice, containerMinVolume, _maxContainerVolume).encode("ascii")
        self.write(msg)
        raw = self.read()
        self.checkCode(raw)


    def getPutting(self):
        print("Command getPutting")
        self.write(PUTTING)
        raw = self.read()
        code = self.checkCode(raw, types="int")
        if code >= 0:
            return code // 10000
        else:
            return False



    def payment(self,score):
        print("Command playment")
        msg = "%s%i\n" % (PAYMENT, score * 100)
        self.write(msg.encode("ascii"))
        raw = self.read()
        if self.checkCode(raw):
            return True


    def textOUT(self, text, line):
        msg = "%s%s,%i\n" % (PAYMENT, text, line)
        self.write(msg.encode("ascii"))
        raw = self.read()
        if self.checkCode(raw):
            return True


    def enablePayment(self):
        self.write(ENABLE)
        result = self.checkCode(self.read())
        return result


    def disablePayment(self):
        self.write(DISABLE)
        result = self.checkCode(self.read())
        return result


nameserial = config.uart["port"]
baud = config.uart["baud"]
mashineId = config.mashine["id"]
dev = Vodomat(nameserial, baud, mashineId)
