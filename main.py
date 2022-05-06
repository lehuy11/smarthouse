import serial.tools.list_ports
import random
import time
import sys
from Adafruit_IO import MQTTClient

AIO_FEED_ID = ["do-an-led", "do-an-temperature", "do-an-humid", "do-an-pump", "do-an-gas", "do-an-fan"]
AIO_USERNAME = "huyle2905"
AIO_KEY = "aio_aQeB43P53iuHWKNh7glxH0K2WUWK"

def  connected(client):
    print("Ket noi thanh cong...")
    for feed in AIO_FEED_ID:
        client.subscribe(feed)

def  subscribe(client , userdata , mid , granted_qos):
    print("Subcribe thanh cong...")

def  disconnected(client):
    print("Ngat ket noi...")
    sys.exit (1)

def  message(client , feed_id , payload):
    print("Nhan du lieu: " + payload)
    if isMicrobitConnected:
        ser.write((str(payload) + "#").encode())

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort

isMicrobitConnected = False
if getPort() != "None":
    ser = serial.Serial( port=getPort(), baudrate=115200)
    isMicrobitConnected = True


def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    #print(splitData)
    try:
        if splitData[0] == "1":
            if splitData[1] == "TEMP":
                client.publish("do-an-temperature", splitData[2])
            elif splitData[1] == "HUMI":
               client.publish("do-an-humid", splitData[2])
            elif splitData[1] == "GAS":
                client.publish("do-an-gas", splitData[2])
            elif splitData[1] == "LIGHT":
                client.publish("do-an-led", splitData[2])
        print(splitData[1],":",splitData[2])
    except:
        pass

mess = ""
def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]
            


while True:


    #time.sleep(1)
    #pass
    
    #value = random.randint(0, 100)
    #print("Cap nhat:", value)
    #client.publish("test", value)
    #time.sleep(5)
    
    #readSerial()
    #time.sleep(1)
    
    if isMicrobitConnected:
        readSerial()
        
    time.sleep(1)