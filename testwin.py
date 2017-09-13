import config
import uartcontrol

dev = uartcontrol.Vodomat("com4", 115200)

key  = input("test# ")
while key != "q":
    if key == "pay":
        m = input("money: ")
        m = int(m)*100
        print(dev.payment(m))
    elif key == "get":
        dev.readinfo()
        print(dev.devInfo)
    elif key == "put":
        print(dev.getPutting())
    key = input("test# ")
