#!/usr/bin/env python3

import cv2
import os
import time

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_smile.xml')

face_strikes = 0
null_strikes = 0
face_detected = False

smile_strikes = 0
nosmile_strikes = 0
smile_detected = False

video_capture = cv2.VideoCapture(0)
print(video_capture.get(cv2.CAP_PROP_FPS))
video_capture.set(cv2.CAP_PROP_FPS, 5.0)
print(video_capture.get(cv2.CAP_PROP_FPS))
while video_capture.isOpened():
    # Captures video_capture frame by frame
    _, frame = video_capture.read()
    _, frame = video_capture.read()
    _, frame = video_capture.read()

    # Capture image in monochrome
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
     
    # See if we detect any face
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4, minSize=(80,80))

    if len(faces) == 0:
        #print("No face detected")
        null_strikes += 1
        face_strikes = 0
        if null_strikes == 6:
            null_strikes = 0
            if face_detected:
                face_detected = False
                print("Face disappeared")
        continue

    #print("Faces detected")
    face_strikes += 1
    null_strikes = 0
    if face_strikes == 2:
        face_strikes = 0
        if not face_detected:
            face_detected = True
            print("Face appeared")

    if not face_detected:
        smile_strikes = 0
        nosmile_strikes = 0
        smile_detected = False
        continue

    print("number of detected faces:", len(faces))
    if len(faces) > 1:
        print(faces)
        cv2.imwrite("img.bmp", frame)
        continue
    face = faces[0]
    (x,y,w,h) = face
    face_rect = gray[y:y+h, x:x+w]
    smiles = smile_cascade.detectMultiScale(face_rect, scaleFactor=1.2, minNeighbors=9)

    if len(smiles) > 0:
        smile_strikes += 1
        nosmile_strikes = 0
        if smile_strikes == 4:
            smile_strikes = 0
            if not smile_detected:
                smile_detected = True
                print("Smile appeared")
    else:
        nosmile_strikes += 1
        smile_strikes = 0
        if nosmile_strikes == 2:
            nosmile_strikes = 0
            if smile_detected:
                smile_detected = False
                print("Smile disappeared")
 
# Release the capture once all the processing is done.
video_capture.release()
