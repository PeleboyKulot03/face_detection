import cv2
import pigpio
from time import sleep
import os
from multiprocessing import Process, Queue

# initialization
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
pi = pigpio.pi()

servo_pin = 18  # Change this to your GPIO pin
servo_pin1 = 17
servo_pin2 = 27

min_pulse_width = 1000
max_pulse_width = 2000
current_angle = 90
writer = ''

# defining constant values
GO_TO_LEFT = min_pulse_width + 400
GO_TO_RIGHT = max_pulse_width - 440
STOP = (max_pulse_width + min_pulse_width) // 2
MAX_RIGHT = 120
MAX_LEFT = 60

def track_face(point):
    global current_angle
    
    # person is in the left 
    if point >= 1 and point <= 2 and current_angle >= MAX_LEFT:
        # to left
        pi.set_servo_pulsewidth(servo_pin, GO_TO_LEFT)
        pi.set_servo_pulsewidth(servo_pin1, GO_T0_LEFT)
        pi.set_servo_pulsewidth(servo_pin2, GO_TO_LEFT)
        sleep(.07)
        current_angle -= .5
        
    # person is in the right
    if point >= 6 and point <= 10 and current_angle <= MAX_RIGHT:
        # to right
        pi.set_servo_pulsewidth(servo_pin, GO_TO_RIGHT)
        pi.set_servo_pulsewidth(servo_pin1, GO_TO_RIGHT)
        pi.set_servo_pulsewidth(servo_pin2, GO_TO_RIGHT)
        sleep(.05)
        current_angle += .5
    
    print(current_angle)
                
def detect_face(frame):
    global writer
    writer = open('last_known_angle.txt', 'w')
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 6, minSize=(70, 70))
    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        # get the current location of the face based on the bounding box
        cx = (x + x + w) // 2
        cy = (y + y + h) // 2
        point = int(cx) // 65
        
        print(point)
        # track the face and move the servo to re-allign the face in the middle
        track_face(point)
        
        # for the display only add bounding box to the dected face(s)
        frame = cv2.rectangle(frame, (x,y), (x+w, y+h), color=(0,255,0), thickness=5)
        break
    
    # stop the servo
    writer.write(str(current_angle))
    pi.set_servo_pulsewidth(servo_pin, STOP)
    pi.set_servo_pulsewidth(servo_pin1, STOP)
    pi.set_servo_pulsewidth(servo_pin2, STOP)
    
    sleep(.05)
    return frame    


def start(queue):
    counter = 0
    is_going_back = False
    stream = cv2.VideoCapture(0)
    if not stream.isOpened():
        pi.set_servo_pulsewidth(servo_pin, STOP)
        print("not streaming")
        exit()

    while True:
        ret, frame = stream.read()
        if not ret:
            print("no more stream")
            break
        if not queue.empty():
            if queue.get() == "stop":
                break
            
        frame = cv2.resize(frame, (640, 480))
        frame = cv2.flip(frame, 1)
        frame = detect_face(frame)
        cv2.imshow(' ', frame)        
        if cv2.waitKey(1) == ord('q'):
            break
    
    stream.release()
    cv2.destroyAllWindows()
    pi.set_servo_pulsewidth(servo_pin, STOP)
