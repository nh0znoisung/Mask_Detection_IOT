import sys
import random
import time

import serial.win32
from Adafruit_IO import MQTTClient
import serial.tools.list_ports

AIO_FEED_ID = ["testing-1", "btn-start", "log-door", "sensor-light", "swt-light", "btn-authority"]
AIO_USERNAME = "GodOfThunderK19"
AIO_KEY = "aio_pENq33jXeZyNS21M6b964HOvs9LB"

AIO_FEED_BUTTON_Start = "btn-start"
AIO_FEED_LOG_Door = "log-door"
AIO_FEED_SENSOR_Light = "sensor-light"
AIO_FEED_SWITCH_Light = "swt-light"
AIO_FEED_BUTTON_Authority = "btn-authority"

def connected(client):
    for feed in AIO_FEED_ID:
        print("Ket noi thanh cong den " + feed)
        client.subscribe(feed)
    # print("Ket noi thanh cong ...")
    # client.subscribe(AIO_FEED_ID)

def subscribe(client, userdata, mid, granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit(1)

def message(client, feed_id, payload):
    print("Nhan du lieu: " + payload)
    if isMicrobitConnected:
        ser.write((str(payload) + "#").encode()) #đầy là lệnh ghi xuống microbit khi nhận dc dữ liệu

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()


# hàm này dùng để auto lấy port kết nối của Microbit
def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "com0com - serial port emulator" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort

isMicrobitConnected = False
if getPort()!= "None":
    ser = serial.Serial( port=getPort(), baudrate=115200)
    isMicrobitConnected = True
# 2 hàm dưới dùng để đọc và xử lý serial data từ microbit
mess = ""
def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if splitData[1] == "TEMP":
        client.publish("testing-1", splitData[2])

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

# def sendDataAdafruit():


while True:
    readSerial()
    time.sleep(1)
    #     value = random.randint(0, 100)
    #     print("Cap nhat:", value)
    #     client.publish("test-sensor", value)
    #
    #     time.sleep(1)
    # pass