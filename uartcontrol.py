import serial
import json
import time

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
freeBattom = 23
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
# vodoList = ["input10Counter", "out10Counter", "milLitlose", "milLitWentOut", "milLitContIn", "waterPrice",
#             "containerMinVolume", "maxContainerVolume", "totalPaid", "sessionPaid", "leftFromPaid", "state",
#             "container", "currentContainerVolume", "consumerPump", "magistralPressure", "mainValve",
#             "filterValve", "washFilValve", "tumperMoney", "tumperDoor", "serviceButton", "freeBattom", "Voltage"]


class Vodomat(object):

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
        "state":"WAIT",
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
        "Voltage": 0,
        "billAccept": False
    }


    def __init__(self, port, baud):
        self.uart = serial.Serial(port, baud)
        self.locked = False


    def lock(self):
        # while self.locked:
        #     pass
        self.locked = True


    def unlock(self):
        self.locked = False

    def read(self):
        return self.uart.readline()


    def write(self, data):
        if type(data) == str:
            data = data.encode("ascii")
        return self.uart.write(data)


    def checkCode(self, code, types="code"):
        if code == NOT_ERROR:
            return True
        elif code ==ERROR_ASCII:
            raise IOError("Неверный ASCII Символ")
        elif code ==ERROR_SHORT:
            raise IOError("Слишкм короткая строка")
        elif code ==ERROR_LONG:
            raise IOError("Слишкм длинная строка")
        elif code == ERROR_TEST:
            return False
        else:
            if types == "code":
                raise IOError(code)
            elif types == "int":
                return int(code)


    def readinfo(self):
        self.write(GET_INFO)
        if self.checkCode(self.read()):
            raw = self.read()
            self.raw2list(raw)



    def raw2list(self, raw):
        date = json.loads(raw.decode())
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
        self.devInfo["leftFromPaid"] = date[leftFromPaid]
        self.devInfo["state"] = stateList[date[state]]
        self.devInfo["container"] = containerList[date[container]]
        self.devInfo["currentContainerVolume"] = date[currentContainerVolume]
        self.devInfo["consumerPump"] = date[consumerPump] == 1
        self.devInfo["mainPump"] = date[mainPump] == 1
        self.devInfo["magistralPressure"] = date[magistralPressure] == 1
        self.devInfo["mainValve"] = date[mainValve] == 1
        self.devInfo["filterValve"] = date[filterValve] == 1
        self.devInfo["washFilValve"] = date[washFilValve] == 1
        self.devInfo["tumperMoney"] = date[tumperMoney] == 1
        self.devInfo["tumperDoor"] = date[tumperDoor] == 1
        self.devInfo["serviceButton"] = date[serviceButton] == 1
        self.devInfo["freeBattom"] = date[freeBattom] == 1
        self.devInfo["Voltage"] = date[Voltage]
        self.devInfo["billAccept"] = date[billAccept] == 1


    def startUart(self):
        print("start UART")
        while True:
            self.readinfo()
            time.sleep(1)


    def setting(self, _waterPrice, containerMinVolume,_maxContainerVolume):
        msg = "{}{},{},{}\n".format(SETTING, _waterPrice, containerMinVolume, _maxContainerVolume).encode("ascii")
        self.write(msg)
        raw = self.read()

        self.checkCode(raw)
        self.locked = False




    def getPutting(self):
        self.write(PUTTING)
        raw = self.read()
        print(raw)
        code = self.checkCode(raw, types="int")
        if code == True:
            return 0
        elif code > 0:
            return code
        else:
            raise IOError(raw)


    def payment(self,score):
        self.lock()
        msg = "%s%i\n" % (PAYMENT, score)
        self.write(msg.encode("ascii"))
        raw = self.read()
        if self.checkCode(raw):
            return True


    def textOUT(self, text, line):
        self.lock()
        msg = "%s%s,%i\n" % (PAYMENT, text, line)
        self.write(msg.encode("ascii"))
        raw = self.read()
        self.unlock()
        if self.checkCode(raw):
            return True


    def enablePayment(self):
        self.write(ENABLE)
        return self.checkCode(self.read())


    def disablePayment(self):
        self.write(DISABLE)
        return self.checkCode(self.read())