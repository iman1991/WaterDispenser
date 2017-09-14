#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uartcontrol

dev = uartcontrol.Vodomat("com4", 9600)

key  = input("test# ")
while key != "q":
    if key == "pay":
        m = input("money: ")
        ff = int(m)*100
        print(dev.payment(ff))
    elif key == "get":
        dev.readinfo()
        print(dev.devInfo)
    elif key == "put":
        print(dev.getPutting())
    key = input("test# ")
