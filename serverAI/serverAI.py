import socket, threading, pickle, struct
from cv2 import VideoCapture
from flask import Flask, render_template, request,Response
import cv2,imutils,time
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import pyshine as ps
from imutils.video import VideoStream
import numpy as np
import argparse
import os
import urllib
import sys
from Adafruit_IO import MQTTClient


def detect_and_predict_mask(frame, faceNet, maskNet):
    # grab the dimensions of the frame and then construct a blob
    # from it
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
        (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the face detections
    faceNet.setInput(blob)
    detections = faceNet.forward()

    # initialize our list of faces, their corresponding locations,
    # and the list of predictions from our face mask network
    faces = []
    locs = []
    preds = []

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the detection
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the confidence is
        # greater than the minimum confidence
        if confidence > args["confidence"]:
            # compute the (x, y)-coordinates of the bounding box for
            # the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # ensure the bounding boxes fall within the dimensions of
            # the frame
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            # extract the face ROI, convert it from BGR to RGB channel
            # ordering, resize it to 224x224, and preprocess it
            face = frame[startY:endY, startX:endX]
            if face.any():
                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                face = cv2.resize(face, (224, 224))
                face = img_to_array(face)
                face = preprocess_input(face)

                # add the face and bounding boxes to their respective
                # lists
                faces.append(face)
                locs.append((startX, startY, endX, endY))

    # only make a predictions if at least one face was detected
    if len(faces) > 0:
        # for faster inference we'll make batch predictions on *all*
        # faces at the same time rather than one-by-one predictions
        # in the above `for` loop
        faces = np.array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=32)

    # return a 2-tuple of the face locations and their corresponding
    # locations
    return (locs, preds)

app = Flask(__name__)


# url="https://media.w3.org/2010/05/sintel/trailer_hd.mp4"
# url ="http://192.168.137.75/800x600.mjpeg"
url ="http://192.168.137.75/800x600.jpg"
# url="http://192.169.137.75:5000/video"


global frame
global prev_frame
frame=None
prev_frame=None
global fin
fin=0
is_mask=0
is_mask_prev=0
global args


def start_video_stream():
    global args
    global is_mask
    global is_mask_prev
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--face", type=str,
        default="face_detector",
        help="path to face detector model directory")
    ap.add_argument("-m", "--model", type=str,
        default="mask_detector.model",
        help="path to trained face mask detector model")
    ap.add_argument("-c", "--confidence", type=float, default=0.5,
        help="minimum probability to filter weak detections")
        
    args = vars(ap.parse_args())

    # load our serialized face detector model from disk
    print("[INFO] loading face detector model...")
    prototxtPath = os.path.sep.join([args["face"], "deploy.prototxt"])
    weightsPath = os.path.sep.join([args["face"],
        "res10_300x300_ssd_iter_140000.caffemodel"])
    faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

    # load the face mask detector model from disk
    print("[INFO] loading face mask detector model...")
    maskNet = load_model(args["model"])

    # initialize the video stream and allow the camera sensor to warm up
    print("[INFO] starting video stream...")
    # vs=cv2.VideoCapture(url)
    # Read until video is completed
    # fps=0
    # st=0
    # frames_to_count=20
    # cnt=0
    time_wait=0
    st=0
    print("Helllllllllll")
    global fin
    global frame
    global prev_frame
    while True:

        imgRes=urllib.request.urlopen(url)
        imgnp=np.array(bytearray(imgRes.read()),dtype=np.uint8)
        frame = cv2.imdecode(imgnp,-1)
        # ret, frame = vs.read()

    #     cv2.imshow("Test", frame)
    #     key = cv2.waitKey(1) & 0xFF

    # # if the `q` key was pressed, break from the loop
    #     if key == ord("q"):
    #         break
        # if ret==False:
        #     # print("Hell")
        #     #Reconnect to camserver after the amount of time
        #     if time_wait!=0:
        #         if (time.time()-st>5):
        #             time_wait=0
        #             try:
        #                 vs=cv2.VideoCapture(url)
        #                 time.sleep(5.0)
        #             except:
        #                 time_wait=1
        #     else:
        #         time_wait=1
        #         st=time.time()
        #         print("Wait")
        #     continue

        # print("Helooo")
        frame = imutils.resize(frame, width=400)



# detect faces in the frame and determine if they are wearing a
# face mask or not
        (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)
    # loop over the detected face locations and their corresponding
    # locations
        for (box, pred) in zip(locs, preds):
            # unpack the bounding box and predictions
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred

            # determine the class label and color we'll use to draw
            # the bounding box and text
            label = "Mask" if mask > withoutMask else "No Mask"
            # is_mask_prev=is_mask
            is_mask=1 if mask > withoutMask else 0

            color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
                
            # include the probability in the label
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

            # display the label and bounding box rectangle on the output
            # frame
            cv2.putText(frame, label, (startX, startY - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
        frame = imutils.resize(frame, width=1000)
        prev_frame=frame
        
        fin=1
        # time.sleep(0.01)
        cv2.imshow("Test", frame)
        key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break






def getimage():
    while True:
        global fin
        global prev_frame
        # print("Hellllllooooo")
        if fin==1:
            frame1 = cv2.imencode('.JPEG', prev_frame,[cv2.IMWRITE_JPEG_QUALITY,20])[1].tobytes()
            # print("Hii")
            time.sleep(0.016)
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n')




AIO_FEED_ID = ["btn-start", "swt-door"]
AIO_USERNAME = "GodOfThunderK19"
AIO_KEY = "aio_HEPK82iCycd8fBUTW5uO8Aoey2tz"

AIO_FEED_BUTTON_Start = "btn-start"
AIO_FEED_SWITCH_Door = "swt-door"

flag_start=0
time_start=0
count_mask=0
count_unmask=0
time_start=0
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
    global flag_start
    if payload == "START:ON":
        flag_start = 1
        print(flag_start)
        
def checkDoor():
    global flag_start
    global time_start
    global count_mask
    global count_unmask
    if(flag_start==1):
        if time_start==0:
            time_start=time.time()
        elif time.time()-time_start>9:
            return 0
        else:
            if(is_mask==1):
                count_mask+=1
            else:
                count_mask=0
            if(count_mask>200):
                return 1
    return -1



def mqttConnect():

    global flag_start
    global time_start
    global count_mask
    global count_unmask

    client = MQTTClient(AIO_USERNAME, AIO_KEY)
    client.on_connect = connected
    client.on_disconnect = disconnected
    client.on_subscribe = subscribe
    client.on_message = message
    client.connect()
    client.loop_background()
    flag_start = 0


    while True:
        # CheckDoor()
        re=checkDoor()
        if (re==0):
            time_start=0
            flag_start=0
            count_mask=0
            count_unmask=0
            client.publish(AIO_FEED_SWITCH_Door, "DOOR:CLOSE")
            client.publish(AIO_FEED_BUTTON_Start, "START:OFF")
        elif (re==1):
            time_start=0
            flag_start=0
            count_mask=0
            count_unmask=0
            client.publish(AIO_FEED_SWITCH_Door, "DOOR:OPEN")
            client.publish(AIO_FEED_BUTTON_Start, "START:OFF")

        time.sleep(0.01)

@app.route('/video')
def video_feed():
   	return Response(getimage(),mimetype='multipart/x-mixed-replace; boundary=frame')

def web():
    app.run(debug=True, host='localhost',port=9999,threaded=True, use_reloader=False)


if __name__ == "__main__":
	

    threading.Thread(target=start_video_stream, daemon=True).start()
    threading.Thread(target=mqttConnect, daemon=True).start()
    threading.Thread(target=web, daemon=True).start()
    while True:
        time.sleep(1)