#!/usr/bin/env python3

import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_smile.xml')

video_capture = cv2.VideoCapture(0)
while video_capture.isOpened():
   # Captures video_capture frame by frame
    _, frame = video_capture.read()
 
    # Capture image in monochrome
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
     
    # See if we detect any face
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        print("Face detected")
        face = faces[0]
        (x,y,w,h) = face
        face_rect = gray[y:y+h, x:x+w]
        smiles = smile_cascade.detectMultiScale(face_rect, 1.8, 20)

        if len(smiles) > 0:
            print("Smile detected")
        else:
            print("No smile detected")
 
    # The control breaks once q key is pressed
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
 
# Release the capture once all the processing is done.
video_capture.release()
