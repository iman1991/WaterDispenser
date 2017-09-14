import json
import os
zabbix = {}
uart = {}

config_file = open("/opt/dl_config.json")

raw = config_file.read()

config_file.close()

config = json.loads(raw)

zabbix.update(config["zabbix"])

uart.update(config["uart"])

if __name__ == "__main__":
    os.system("cp dl_config.json /opt/dl_config.json")
