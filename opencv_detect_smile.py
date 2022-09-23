#!/usr/bin/env python3

import cv2
import random
#import pygame
import os
import time
import opencv_state_machine

STATE_TIME_THRESHOLD = 4

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_smile.xml')

# prepare the sound interface and the sound objects
#pygame.mixer.init()
smile_file1 = "recordings/no_smile.wav"
smile_file2 = "recordings/queen.wav"
no_face_file1 = "recordings/come_here.wav"
no_face_file2 = "recordings/look_here.wav"
no_smile_file1 = "recordings/smile_already.wav"
no_smile_file2 = "recordings/smile_please.wav"
no_smile_file3 = "recordings/ugly.wav"

def handle_smile():
    if random.randrange(2) == 1:
      #pygame.mixer.music.load(smile_file1)
      os.system("aplay " + smile_file1)
    else:
      #pygame.mixer.music.load(smile_file2)
      os.system("aplay " + smile_file2)
    #pygame.mixer.music.play()
    #while pygame.mixer.get_busy():
    #    continue

def handle_no_face():
    if random.randrange(2) == 1:
      os.system("aplay " + no_face_file1)
    else:
      os.system("aplay " + no_face_file2)

def handle_no_smile():
    rnd = random.randrange(3)
    if rnd == 1:
      os.system("aplay " + no_smile_file1)
    elif rnd == 2:
      os.system("aplay " + no_smile_file2)
    else:
      os.system("aplay " + no_smile_file3)

last_sound_time = time.time()
last_state = opencv_state_machine.FaceStateMachine.STATE_NUM_STATES

def handle_state(state, last_state_time):
    global last_sound_time, last_state
    if (time.time() > last_sound_time + STATE_TIME_THRESHOLD) or last_state != state:
        last_state = state
        last_sound_time = time.time()

        if state == opencv_state_machine.FaceStateMachine.STATE_NO_FACE:
            handle_no_face()
        elif state == opencv_state_machine.FaceStateMachine.STATE_FACE_NO_SMILE:
            handle_no_smile()
        elif state == opencv_state_machine.FaceStateMachine.STATE_SMILE:
            handle_smile()

state_machine = opencv_state_machine.FaceStateMachine(handle_state)

video_capture = cv2.VideoCapture(0)
print(video_capture.get(cv2.CAP_PROP_FPS))
video_capture.set(cv2.CAP_PROP_FPS, 5.0)
print(video_capture.get(cv2.CAP_PROP_FPS))
while video_capture.isOpened():
    # Captures video_capture frame by frame
    _, frame = video_capture.read()
 
    # Capture image in monochrome
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
     
    # See if we detect any face
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        state_machine.process(opencv_state_machine.FaceStateMachine.STATE_NO_FACE)
        continue

    if len(faces) > 1:
        print("Faces detected")
        state_machine.process(opencv_state_machine.FaceStateMachine.STATE_MANY_FACES)
        continue

    print("Face detected")
    face = faces[0]
    (x,y,w,h) = face
    face_rect = gray[y:y+h, x:x+w]
    smiles = smile_cascade.detectMultiScale(face_rect, 1.8, 20)

    if len(smiles) > 0:
        print("Smile detected")
        state_machine.process(opencv_state_machine.FaceStateMachine.STATE_SMILE)
    else:
        print("No smile detected")
        state_machine.process(opencv_state_machine.FaceStateMachine.STATE_FACE_NO_SMILE)
 
# Release the capture once all the processing is done.
video_capture.release()
