from multiprocessing import Process, Queue
import cv2
import numpy as np
import time
import hands_movements as hands
from multiprocessing import Process


# path to the video emotions
file_names = [
                "/home/tbm/eyes expressions/eyes_angry_low.mp4",
                "/home/tbm/eyes expressions/eyes_annoyed_low.mp4",
                "/home/tbm/eyes expressions/eyes_blinking_low.mp4",
                "/home/tbm/eyes expressions/eyes_happy_low.mp4",
                "/home/tbm/eyes expressions/eyes_idle_low.mp4",
                "/home/tbm/eyes expressions/eyes_love_low.mp4",
                "/home/tbm/eyes expressions/eyes_sad_low.mp4",
                "/home/tbm/eyes expressions/eyes_talking_low.mp4"
              ]


# function to give the new emotion
def change_emotion(emotion):
    ANGRY_EYES = cv2.VideoCapture(file_names[0])
    ANNOYED_EYES = cv2.VideoCapture(file_names[1])
    BLINKING_EYES = cv2.VideoCapture(file_names[2])
    HAPPY_EYES = cv2.VideoCapture(file_names[3])
    IDLE_EYES = cv2.VideoCapture(file_names[4])
    INLOVE_EYES = cv2.VideoCapture(file_names[5])
    SAD_EYES = cv2.VideoCapture(file_names[6])
    TALKING_EYES = cv2.VideoCapture(file_names[7])
    
    switch={
            "happy": HAPPY_EYES,
            "annoyed": ANNOYED_EYES,
            "angry": ANGRY_EYES,
            "blinking": BLINKING_EYES,
            "idle": IDLE_EYES,
            "inlove": INLOVE_EYES,
            "sad": SAD_EYES,
            "talking": TALKING_EYES
            }
        
    return switch.get(emotion, "Invalid input")
    

# function to display the emotion in the screen
def display_emotion(queue):
    emotion_change = False
    process_hands = Process(target=hands.start)
    cv2.namedWindow(' ', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(' ',cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    current_emotion = change_emotion("idle")
    
    while True:
        has_frame,frame = current_emotion.read()
        
        if not has_frame:
            if emotion_change:
                current_emotion.set(cv2.CAP_PROP_POS_FRAMES, 0)
                current_emotion = change_emotion('idle')
                emotion_change = False

            if not queue.empty():
                emotion = queue.get()
                if process_hands.is_alive():
                    process_hands.join()
                    
                if emotion == "stop":
                    break
                
                current_emotion.set(cv2.CAP_PROP_POS_FRAMES, 0)
                current_emotion = change_emotion(emotion)
                process_hands = Process(target=hands.start, args=(emotion,))
                process_hands.start()
                emotion_change = True
                
                
                
                continue
            
            current_emotion.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
                
        height, width, _ = frame.shape
        
        scale_percent = 80
        new_width = int(width * scale_percent / 100)
        new_height = int(height * scale_percent / 100)
        dim = (new_width - 90, new_height - 90)
        resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        
        frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        cv2.imshow(' ', frame)
        
        if cv2.waitKey(1) == ord('q'):
            break

    current_emotion.release()
    cv2.destroyAllWindows()
    

    
# start a new process
# def start_emotion_process():
#     queue = Queue()
#     process_display_emotion = Process(target=display_emotion, args=(queue,))
#     process_display_emotion.start() 
#     
#     return process_display_emotion, queue
    
