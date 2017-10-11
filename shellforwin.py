#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import zabbixactivechecks.zabbix_agent as zbx
from zabbixactivechecks import ItemList
import json
import socket
import struct
import time

devInfo = {
    "idv": 0,
    "input10Counter ": 0,
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
    "State": "WAIT",
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
    "freeButtom": 0,
    "Voltage": 0,
    "billAccept": 0,
    "containerGraph": 0,
    "stateGraph": 0

}


hostname = "vodomat0"
server = "194.67.217.17"
port = 10051

def getkey():
    itemList = ItemList(host=hostname)
    response = itemList.get(server=server, port=port)
    return response.data


def addData(host, key, clock, value):
    print("key: {}; value: {}".format(key, value))
    return {"host": host, "key": key, "value": value, "clock": clock}




def startAgent():
    print("Start agent")
    while True:
        keys = [item["key"] for item in getkey()]
        clock = int(time.time())
        request = {
            "request": "agent data",
            "data": [],
            "clock": clock
        }
        for key in keys:
            try:
                if key == "ping":
                    request["data"].append(addData(hostname, key, clock, 1))
                else:
                    request["data"].append(addData(hostname, key, clock, devInfo[key]))

            except:
                pass
        raw = zbx.get_data_to_send(json.dumps(request))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server, port))
        sock.send(raw)
        data = sock.recv(5)
        if data == zbx.ZABBIX_HEADER:
            data = sock.recv(8)
            l = struct.unpack("i", data[:4])[0]
            sock.recv(l)
            sock.close()
        time.sleep(30)

if __name__ == "__main__":
    startAgent()