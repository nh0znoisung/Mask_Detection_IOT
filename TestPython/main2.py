import sys
import random
import time

import Adafruit_IO
import serial.win32
from Adafruit_IO import MQTTClient
import serial.tools.list_ports

AIO_FEED_ID = ["btn-start", "log-door", "sensor-light", "swt-light", "btn-authority"]
AIO_USERNAME = "GodOfThunderK19"
AIO_KEY = "aio_pENq33jXeZyNS21M6b964HOvs9LB"

AIO_FEED_BUTTON_Start = "btn-start"
AIO_FEED_SWITCH_Door = "swt-door"
AIO_FEED_SENSOR_Light = "sensor-light"
AIO_FEED_SWITCH_Light = "swt-light"
AIO_FEED_BUTTON_AuthorityDoor = "btn-authority"


def connected(client):
    for feed in AIO_FEED_ID:
        print("Ket noi thanh cong den " + feed)
        client.subscribe(feed)
    # print("Ket noi thanh cong ...")
    # client.subscribe(AIO_FEED_ID)


def subscribe(client, userdata, mid, granted_qos):
    # print("Subscribe thanh cong ...")
    for feed in AIO_FEED_ID:
        print("Subscribe thanh cong den " + feed)


def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit(1)


def message(client, feed_id, payload):
    print("Nhan du lieu: " + payload)
    # if isMicrobitConnected:
    #     ser.write((str(payload) + "#").encode())  # đầy là lệnh ghi xuống microbit khi nhận dc dữ liệu



client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
# client.


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
if getPort() != "None":
    ser = serial.Serial(port=getPort(), baudrate=115200)
    isMicrobitConnected = True
# 2 hàm dưới dùng để đọc và xử lý serial data từ microbit
mess = ""
def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    sendData_Adafruit(splitData)

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
                mess = mess[end + 1:]


def sendData_Adafruit(splitedData):
    # if splitedData[0] == "btn-start":
    #     client.publish("btn-start",splitedData[1])
    try:
        match splitedData[0]:
            case "btn-start":
                print("Gui thanh cong den " +AIO_FEED_BUTTON_Start)
                client.publish(AIO_FEED_BUTTON_Start,splitedData[1])
            case "sensor-light":
                print("Gui thanh cong den " + AIO_FEED_SENSOR_Light)
                client.publish(AIO_FEED_SENSOR_Light, splitedData[1])
            case "swt-light":
                print("Gui thanh cong den " + AIO_FEED_SWITCH_Light)
                client.publish(AIO_FEED_SWITCH_Light,splitedData[1])
            case "swt-door":
                print("Gui thanh cong den " + AIO_FEED_SWITCH_Door)
                client.publish(AIO_FEED_SWITCH_Door,splitedData[1])
    except:
        pass
        # case "btn-authority":
        #     print("Gui thanh cong den " + AIO_FEED_BUTTON_AuthorityDoor)
        #     client.publish(AIO_FEED_BUTTON_AuthorityDoor,splitedData[1])



def writeData_Microbit():
    switchLight = client.receive(AIO_FEED_SWITCH_Light)
    openDoor = client.receive(AIO_FEED_BUTTON_AuthorityDoor)
    switchDoor = client.receive(AIO_FEED_SWITCH_Door)
    ser.write("swt-light:" + (str(switchLight) +"#").encode() )
    ser.write("open-door:" + (str(openDoor)+"#").encode())
    ser.write("swt-door:" + (str(switchDoor)+"#").encode())

count = 1000

while True:
    readSerial()

    if count == 0:
        count = 1000
        writeData_Microbit()
    else:
        --count

    # writeData_Microbit()

    time.sleep(1)
    #     value = random.randint(0, 100)
    #     print("Cap nhat:", value)
    #     client.publish("test-sensor", value)
    #
    #     time.sleep(1)
    # pass