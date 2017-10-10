import zabbixactivechecks.zabbix_agent as zbx
from zabbixactivechecks import ItemList
from uartcontrol import dev
import json
import socket
import struct
import time


host = 'vodomat001'
server = "194.67.217.17"
port = 10051

def getkey():
    itemList = ItemList(host='vodomat001')
    response = itemList.get(server="194.67.217.17", port=10051)
    return response.data


def addData(host, key, value, clock):
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
                    request["data"].append(addData(host, key, clock, 1))
                else:
                    request["data"].append(addData(host, key, clock, dev.devInfo[key]))
            except:
                pass
        raw = zbx.get_data_to_send(json.dumps(request))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("194.67.217.17", 10051))
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