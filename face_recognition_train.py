import cv2
import RPi.GPIO as GPIO
from time import sleep
import os
import numpy as np 
from PIL import Image
from gpiozero import AngularServo

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +
                                     "haarcascade_frontalface_default.xml")

recognizer = cv2.face.LBPHFaceRecognizer_create()
font = cv2.FONT_HERSHEY_SIMPLEX

def train_model():
    Face_ID = -1 
    pev_person_name = ""
    y_ID = []
    x_train = []
    face_images = os.path.join(os.getcwd(), "face_images")
    
    for root, dirs, files in os.walk(face_images): 
        for file in files:              
            path = os.path.join(root, file)
            person_name = os.path.basename(root)
            print(person_name)
                
            if pev_person_name != person_name:
                Face_ID = Face_ID+1 
                pev_person_name = person_name
            
            Gery_Image = Image.open(path).convert("L")
            Final_Image = np.array(Gery_Image, "uint8")
            
            faces = face_cascade.detectMultiScale(Final_Image)
            
            for (x,y,w,h) in faces:
                roi = Final_Image[y:y+h, x:x+w]
                x_train.append(roi)
                y_ID.append(Face_ID)


    recognizer.train(x_train, np.array(y_ID))
    recognizer.save("face_trainner.yml")


def start(name):
    path = os.path.join(os.getcwd(), "face_images/", name)
    
    # check whether directory already exists
    if not os.path.exists(path):
        os.mkdir(path)
        print("Folder %s created!" % path)
    else:
        print("Folder %s already exists" % path)

    stream = cv2.VideoCapture(0)
    cv2.namedWindow('face recognition', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('face recognition',cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    if not stream.isOpened():
        print("not streaming")
        exit()
        
    image_count = 0
    warm_up = is_first_batch = is_second_batch = is_third_batch = False
    counter = 3
    
    width  = stream.get(3)
    height = stream.get(4)
    
    print(width)
    print(height)
    while True:
        ret, frame = stream.read()
        if not warm_up:
            sleep(1)
            warm_up = True
            continue
        
        if not ret:
            print("no more stream")
            break
        
        if cv2.waitKey(1) == ord('q'):
            break

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(50, 50))

        if not image_count == 30:
            if not is_first_batch and image_count == 0:
                cv2.putText(frame, str(counter), (int((width // 2) - 30), int(height//2)), font, 5, (10,10,255), 5)
                cv2.imshow('face recognition', frame)
                
                counter -= 1
                sleep(1)
                if counter == 0:
                    is_first_batch = True
                    counter = 3
                continue
                
            if not is_second_batch and image_count == 9:
                cv2.putText(frame, str(counter), (int((width // 2) - 30), int(height//2)), font, 5, (10,10,255), 5)
                cv2.imshow('face recognition', frame)
                
                counter -= 1
                sleep(1)
                if counter == 0:
                    is_second_batch = True
                    counter = 3
                continue
            
            if not is_third_batch and image_count == 19:
                cv2.putText(frame, str(counter), (int(width // 2) - 30, int(height//2)), font, 5, (10,10,255), 5)
                cv2.imshow('face recognition', frame)
                
                counter -= 1
                sleep(1)
                if counter == 0:
                    is_third_batch = True
                    counter = 3
                continue
            
            if len(faces) == 1:
                for x,y,w,h in faces:
                    image_count += 1
                    roi_gray = gray[y:y+h, x:x+w]
                    cv2.imwrite(path + "/" + name + f"{image_count}" + ".jpg", roi_gray)
                    break
        else:
            print("Taking picture completed!")
            stream.release()
            cv2.destroyAllWindows()
            print("Remembering your face...")
            train_model()
            print("Remembering your face completed!")
            break
                
        
        cv2.imshow('face recognition', frame)
        if cv2.waitKey(1) == ord('q'):
            break
        

    stream.release()
    cv2.destroyAllWindows()
    