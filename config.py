import json
import os

if __name__ == "__main__":
    os.system("cp dl_config.json /opt/dl_config.json")
else:
    zabbix = {}
    uart = {}
    mashine = {}
    server = {}

    config_file = open("/opt/dl_config.json")

    raw = config_file.read()

    config_file.close()

    config = json.loads(raw)

    zabbix.update(config["zabbix"])

    uart.update(config["uart"])

    mashine.update(config["mashine"])

    server.update(config["server"])
