import zabbixactivechecks.zabbix_agent as zbx
from zabbixactivechecks import ItemList
import json


itemList = ItemList(host='vodomat001')
response = itemList.get(server="194.67.217.17", port=10051)

# response.data[0].update({"valve": response.data[0]["key"]})
# response.data[1].update({"valve": 1})
val =  {
            "host":"<hostname>",
            "key":"agent.version",
            "value":"2.4.0",
            "clock":1400675595,
            "ns":76808644
        },



print(response.data)


# print(zbx.send(req, server="192.168.10.79", port=10051))