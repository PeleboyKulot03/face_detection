import cv2
import numpy as np
import os 

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('face_trainner.yml')
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades +
                                     "haarcascade_frontalface_default.xml")

font = cv2.FONT_HERSHEY_SIMPLEX

names = []

def get_labels():
    labels = []
    pev_person_name = ""
    face_images = os.path.join(os.getcwd(), "face_images")
    
    for root, dirs, files in os.walk(face_images):
        for file in files:
            person_name = os.path.basename(root)
            labels.append(person_name)
            break    
        
    return labels


names = get_labels()

def start_recognizing(return_value):
    cam = cv2.VideoCapture(0)
    
    # Initialize and start realtime video capture
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height
    possible_name = {}
    name = 'unknown'
    number_of_try = 0
    
    while True:
        ret, img = cam.read()
        img = cv2.flip(img, 1)

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale( 
            gray,
            1.3,
            6,
            minSize=(60, 60)
           )

        for(x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

            # Check if confidence is less than 50
            # Note: confidence is in reverse (the less confidence, the more sure) 0 is the perfect match
            if confidence < 10:
                return_value.put(name)
                cam.release()
                cv2.destroyAllWindows()
                return
            
            if number_of_try >= 50:
                max_value = None
                for key in possible_name:
                    if max_value is None or max_value < possible_name[key]:
                        max_value = possible_name[key]
                        name = key
                
                cam.release()
                cv2.destroyAllWindows()
                return_value.put(name)
                return
            
            if (confidence < 50):
                id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
            
            possible_name.update({str(id):(possible_name.get(str(id)) + 1) if str(id) in possible_name.keys() else 1})
            
            number_of_try += 1
            cv2.putText(img, str(id), (x+5,y-5), font, 1, (0,255,0), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
        
#         cv2.imshow('camera',img) 

        if cv2.waitKey(1) == ord('q'):
            break

    return_value.put(name)
    cam.release()
    cv2.destroyAllWindows()


