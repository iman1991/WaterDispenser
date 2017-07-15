# import zabbixactivechecks.zabbix_agent as zbx
# from zabbixactivechecks import ItemList
import json
import time
import socket
import struct

DEFAULT_SOCKET_TIMEOUT = 5.0
ZABBIX_HEADER = b'ZBXD\1'

server = "194.67.217.17"
port = 10051


# itemList = ItemList(host='vodomat001')
# response = itemList.get(server="194.67.217.17", port=10051)
#
# keys = response.data

# time.sleep(30)

clock = int()

requst = {
    "request": "agent data",
    "data": [
        {
            "host": "vodomat001",
            "key": "agent.ping",
            "value": 1,
            "clock": clock,

        }
    ],
    "clock": clock,
}
raw = zbx.get_data_to_send(json.dumps(requst))
print(raw)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("194.67.217.17", 10051))
sock.send(raw)
data = sock.recv(5)
data = sock.recv(8)
l = struct.unpack("i", data[:4])[0]
print(sock.recv(l))
sock.close()
