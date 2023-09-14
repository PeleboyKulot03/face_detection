import calibration_test
import face_detection
import play_emotion as emotions
import hands_movements as hands
import cv2
import face_recognition_train
import face_recognition_test
import sys
from multiprocessing import Process, Queue

calibration_test.calibrate()

detection_queue = Queue()
emotion_queue = Queue()
# hands_queue = Queue()

process_display_emotion = Process(target=emotions.display_emotion, args=(emotion_queue,))
process_face_detection = Process(target=face_detection.start, args=(detection_queue,))
# process_hands = Process(target=hands.start, args=(hands_queue,))

process_display_emotion.start()
process_face_detection.start()
# process_hands.start()


def kill_process():
    emotion_queue.put("stop")
    detection_queue.put("stop")
        
    process_display_emotion.join()
    process_face_detection.join()
        
    
while True:
    command = input("type what emotion_queue next: ")
    
    if command == "what is my name":
        kill_process()
        queue = Queue()
        process_face_recognition = Process(target=face_recognition_test.start_recognizing, args=(queue,))
        
        process_face_recognition.start()
        process_face_recognition.join()
        print("hi " + queue.get())
        
        process_display_emotion = Process(target=emotions.display_emotion, args=(emotion_queue,))
        process_face_detection = Process(target=face_detection.start, args=(detection_queue,))

        process_display_emotion.start()
        process_face_detection.start()
        continue
    
    if command == "create new suki":
        kill_process()
        
        name = input("what is your name: ")
        
        process_face_recognition_train = Process(target=face_recognition_train.start, args=(name,))
        
        process_face_recognition_train.start()
        process_face_recognition_train.join()
        
        process_display_emotion = Process(target=emotions.display_emotion, args=(emotion_queue,))
        process_face_detection = Process(target=face_detection.start, args=(detection_queue,))

        process_display_emotion.start()
        process_face_detection.start()
        continue
    
    # to optimize
    # for now don't change the position of if block
    if command == "stop":
        kill_process()
        break
    
    emotion_queue.put(command)


sys.exit()