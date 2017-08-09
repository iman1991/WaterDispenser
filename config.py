import json
import sys
import os
zabbix = {}
uart = {}

def openCofigFile():
    config_file = open("/opt/dl_config.json")
    raw = config_file.read()
    config_file.close()
    return raw

try:
    text = openCofigFile()
except:
    os.system("cp dl_config.json /opt/dl_config.json")
    text = openCofigFile()

config = json.loads(text)
zabbix.update(config["zabbix"])
uart.update(config["uart"])

