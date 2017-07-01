import serial
import argparse
import json
import time


devInfo = {
    "ID": 1,
    "state": "NO_WATER",
    "input10Counter ": 0,
    "out10Counter": 0,
    "milLitlose": 0,
    "milLitWentOut": 0,
    "milLitContIn": 0,
    "waterPrice": 0,
    "waterContThreshold": 0,
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

ID = -1

input10Counter = 0
out10Counter = 1
milLitlose = 2
milLitWentOut = 3
milLitContIn = 4
waterPrice = 5
waterContThreshold = 6
maxContainerVolume = 7
totalPaid = 8
sessionPaid = 9
leftFromPaid = 10
state = 11
container = 12
currentContainerVolume = 13
consumerPump = 14
mainPump= 15
magistralPressure = 16
mainValve = 17
filterValve = 18
washFilValve = 19
tumperMoney = 20
tumperDoor = 21
serviceButton = 22
freeBattom = 23
# Voltage = 24

GET_INFO = b'g\n'

NOT_ERROR = b'0\n'
ERROR_ASCII = b'1\n'
ERROR_SHORT = b'2\n'
ERROR_LONG = b'3\n'

stateList =["NO_WATER",
            "WASH_FILTER",
            "WAIT",
            "SETTING",
            "JUST_PAID",
            "WORK",
            "SERVICE",
            "FREE",
            "NONE"
            ]

containerList = ["TOO_LOW", "NOT_FULL", "FULL"]

def read(com):
    code = com.readline()
    if code == NOT_ERROR:
        return com.readline()

    elif code ==ERROR_ASCII:
        raise IOError("Неверный ASCII Символ")

    elif code ==ERROR_SHORT:
        raise IOError("Слишкм короткая строка")

    elif code ==ERROR_LONG:
        raise IOError("Слишкм длинная строка")

    else:
        raise IOError(code)


def readinfo(com):
    com.write(GET_INFO)
    return read(com)


def raw2list(raw):
    date = json.loads(raw.decode())
    dev = {}
    dev["input10Counter"] = date[input10Counter]
    dev["out10Counter"] = date[out10Counter]
    dev["milLitlose"] = date[milLitlose]
    dev["milLitWentOut"] = date[milLitWentOut]
    dev["milLitContIn"] = date[milLitContIn]
    dev["waterPrice"] = date[waterPrice]
    dev["waterContThreshold"] = date[waterContThreshold]
    dev["maxContainerVolume"] = date[maxContainerVolume]
    dev["totalPaid"] = date[totalPaid]
    dev["sessionPaid"] = date[sessionPaid]
    dev["leftFromPaid"] = date[leftFromPaid]
    dev["state"] = stateList[date[state]]
    dev["container"] = date[container]
    dev["currentContainerVolume"] = date[currentContainerVolume]
    dev["consumerPump"] = date[consumerPump] == 1
    dev["mainPump"] = date[mainPump] == 1
    dev["magistralPressure"] = date[magistralPressure] == 1
    dev["mainValve"] = date[mainValve] == 1
    dev["filterValve"] = date[filterValve] == 1
    dev["washFilValve"] = date[washFilValve] == 1
    dev["tumperMoney"] = date[tumperMoney] == 1
    dev["tumperDoor"] = date[tumperDoor] == 1
    dev["serviceButton"] = date[serviceButton] == 1
    dev["freeBattom"] = date[freeBattom]
    # dev["Voltage"] = date[Voltage]
    return dev


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--baud", nargs="?", type=int, default=38400,
                        help="скорость передачи данных, по умолчанию равно 38400")
    parser.add_argument("-p", "--port", nargs="?", default="/dev/ttyUSB0",
                        help="порт по которому опрашивается устройство")
    return parser

def main():
    parser = createParser()
    namespace = parser.parse_args()
    port = serial.Serial(namespace.port, namespace.baud)
    raw = readinfo(port)
    devInfo = raw2list(raw)
    print(json.dumps(devInfo))
    # while True:
    #
    #     # raw = readinfo(port)
    #     # devInfo = raw2list(raw)
    #     # print(devInfo)
    #     time.sleep(1)



if __name__ == "__main__":
    main()


