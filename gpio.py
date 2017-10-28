import os


def init():
    os.system("gpio mode 1 OUT")
    os.system("gpio write 1 1")


def reboot():
    os.system("gpio write 1 0;sleep 1s; gpio write 1 1;")
