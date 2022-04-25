import os
import cv2
import pickle
import numpy as np

def liveVideoTest():
    pick = open('Models/model.pkl', 'rb')
    model = pickle.load(pick)
    pick.close()

    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    font = cv2.FONT_HERSHEY_PLAIN

    cap=cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        for x, y, w, h in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 4)

            final_img = cv2.resize(roi_color, (48, 48))
            final_img = cv2.cvtColor(final_img, cv2.COLOR_BGR2GRAY)
            final_img = final_img.reshape(1, -1)
            emotion = model.predict(final_img)
            
            if emotion[0] == 0:
                status = "Angry"
                cv2.putText(frame, status, (x, y), font, 3, (0, 0, 255), 2, cv2.LINE_4)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255))
                directory = 'Songs/Angry Song/'

            if emotion[0] == 1:
                status = "Disgust"
                cv2.putText(frame, status, (x, y), font, 3, (0, 0, 255), 2, cv2.LINE_4)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255))
                directory = 'Songs/Disgust Song/'


            if emotion[0] == 2:
                status = "Surprise"
                cv2.putText(frame, status, (x, y), font, 3, (0, 0, 255), 2, cv2.LINE_4)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255))
                directory = 'Songs/Surprise Song/'

            if emotion[0] == 3:
                status = "Neutral"
                cv2.putText(frame, status, (x, y), font, 3, (0, 0, 255), 2, cv2.LINE_4)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255))
                directory = 'Songs/Neutral Song/'

            if emotion[0] == 4:
                status = "Fear"
                cv2.putText(frame, status, (x, y), font, 3, (0, 0, 255), 2, cv2.LINE_4)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255))
                directory = 'Songs/Fear Song/'

            if emotion[0] == 5:
                status = "Sad"
                cv2.putText(frame, status, (x, y), font, 3, (0, 0, 255), 2, cv2.LINE_4)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255))
                directory = 'Songs/Sad Song/'

            if emotion[0] == 6:
                status = "Happy"
                cv2.putText(frame, status, (x, y), font, 3, (0, 0, 255), 2, cv2.LINE_4)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255))
                directory = 'Songs/Happy Song/'

        resized_img = cv2.resize(frame, (800, 600))
        cv2.imshow('Face Emotion Recognition', resized_img)
        if cv2.waitKey(2) == 32:
            break

    cap.release()
    cv2.destroyAllWindows()
    
    return status, directory
    

# print(liveVideoTest())