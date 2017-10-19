import zabbixactivechecks.zabbix_agent as zbx
from zabbixactivechecks import ItemList
from uartcontrol import dev
import json
import socket
import struct
import time
from config import zabbix


hostname = zabbix["hostname"]
server = zabbix["server"]
port = zabbix["port"]


def getkey():
    itemList = ItemList(host=hostname)
    response = itemList.get(server=server, port=port)
    return response.data



def addData(host, key, clock, value):
    return {"host": host, "key": key, "value": value, "clock": clock}


def startAgent():
    print("Start agent")
    keys = [item["key"] for item in getkey()]
    while True:
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
                elif key == "leftFromPaid":
                    request["data"].append(addData(hostname, key, clock, dev.devInfo[key] // 100))
                elif key == "sessionPaid":
                    request["data"].append(addData(hostname, key, clock, dev.devInfo[key] // 100))
                elif key == "totalPaid":
                    request["data"].append(addData(hostname, key, clock, dev.devInfo[key] // 100))
                else:
                    request["data"].append(addData(hostname, key, clock, dev.devInfo[key]))

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
        time.sleep(10)

if __name__ == "__main__":
    startAgent()