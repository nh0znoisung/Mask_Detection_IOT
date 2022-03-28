import sys
import random
import time
import serial.tools.list_ports
from Adafruit_IO import MQTTClient

AIO_FEED_ID = ["btn-start", "log-door", "sensor-light", "swt-light", "btn-authority"]
AIO_USERNAME = "GodOfThunderK19"
AIO_KEY = "aio_TYfj38SrTIvvdA8rLdxplyG2jFyQ"

AIO_FEED_BUTTON_Start = "btn-start"
AIO_FEED_SWITCH_Door = "swt-door"
AIO_FEED_SENSOR_Light = "sensor-light"
AIO_FEED_SWITCH_Light = "swt-light"
AIO_FEED_BUTTON_AuthorityDoor = "btn-authority"



def connected(client):
    for feed in AIO_FEED_ID:
        print("Connected successfully to " + feed)
        client.subscribe(feed)


def subscribe(client, userdata, mid, granted_qos):
    print("Subscribed successfully.")


def disconnected(client):
    print("Disconnecting.")
    sys.exit(1)


def message(client, feed_id, payload):
    print("Received data: " + payload)
    ser.write((str(payload) + "#").encode())

    # if is_microbit_connected:
        # ser.write(str(payload)+"#").encode()


client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_subscribe = subscribe
client.on_message = message
client.connect()
client.loop_background()
is_microbit_connected = False


def get_port():
    ports = serial.tools.list_ports.comports()
    n = len(ports)
    comm_port = "None"
    for i in range(n):
        port = ports[i]
        str_port = str(port)
        if "USB Serial Device" in str_port:
            split_port = str_port.split(" ")
            comm_port = split_port[0]
    return comm_port


if get_port() != "None":
    ser = serial.Serial(port= get_port(), baudrate=115200)
    is_microbit_connected = True


mess = ""


def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    sendData_Adafruit(splitData)
    
def sendData_Adafruit(splitedData):
    # if splitedData[0] == "btn-start":
    #     client.publish("btn-start",splitedData[1])
    try:
        if splitedData[0] == "btn-start":
            print("Gui thanh cong den " +AIO_FEED_BUTTON_Start)
            if  int(splitedData[1]) == 1:
                client.publish(AIO_FEED_BUTTON_Start,"START:ON")
            elif int(splitedData[1]) == 0:
                client.publish(AIO_FEED_BUTTON_Start,"START:OFF")
            # client.publish(AIO_FEED_BUTTON_Start,splitedData[1])
        elif splitedData[0] == "sensor-light":
            print("Gui thanh cong den " + AIO_FEED_SENSOR_Light)
            client.publish(AIO_FEED_SENSOR_Light, splitedData[1])
        elif splitedData[0] ==   "swt-light":
            print("Gui thanh cong den " + AIO_FEED_SWITCH_Light)
            if  int(splitedData[1]) == 1:
                client.publish(AIO_FEED_SWITCH_Light,"LIGHT:ON")
            elif int(splitedData[1]) == 0:
                client.publish(AIO_FEED_SWITCH_Light,"LIGHT:OFF")
            # print("Gui thanh cong den " + AIO_FEED_SWITCH_Light)
            # client.publish(AIO_FEED_SWITCH_Light,splitedData[1])
        elif splitedData[0] == "swt-door":
            print("Gui thanh cong den " + AIO_FEED_SWITCH_Door)
            if  int(splitedData[1]) == 1:
                client.publish(AIO_FEED_SWITCH_Door,"DOOR:OPEN")
            elif int(splitedData[1]) == 0:
                client.publish(AIO_FEED_SWITCH_Door,"DOOR:CLOSE")
            # client.publish(AIO_FEED_SWITCH_Door,splitedData[1])
    except:
        pass

def readSerial():
    global mess, ser
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

while True:
    if is_microbit_connected:
        readSerial()
    time.sleep(1)

