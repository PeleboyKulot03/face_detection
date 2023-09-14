import pigpio
from time import sleep

pi = pigpio.pi()

RIGHT_HAND = 27
LEFT_HAND = 17

min_pulse_width = 1000
max_pulse_width = 2000

GO_UP = min_pulse_width + 400
GO_DOWN = max_pulse_width - 400
STOP = (max_pulse_width + min_pulse_width) // 2
FULL_SWING = .8
PAUSE = 2


def hands_go_up():
    pi.set_servo_pulsewidth(RIGHT_HAND, GO_DOWN)
    pi.set_servo_pulsewidth(LEFT_HAND, GO_UP)

def hands_go_down():
    pi.set_servo_pulsewidth(RIGHT_HAND, GO_UP)
    pi.set_servo_pulsewidth(LEFT_HAND, GO_DOWN)

def stop():
    pi.set_servo_pulsewidth(RIGHT_HAND, STOP)
    pi.set_servo_pulsewidth(LEFT_HAND, STOP)

def say_hi():
    # hands go up
    hands_go_up()
    sleep(FULL_SWING)

    
    # do a half swing twice
    for i in range(1):
        # hands go down 
        hands_go_down()
        sleep(FULL_SWING / 2)
        
        # hands go up
        hands_go_up()
        sleep(FULL_SWING / 2)

    # hands go down
    hands_go_down()
    sleep(FULL_SWING)
    
    # stop the servo
    stop()
    
def sad_or_love_hands():
    # hands go up
    hands_go_up()
    sleep(FULL_SWING)
    
    # pause for 2 seconds
    stop()
    sleep(.5)
    
    # hands go down
    hands_go_down()
    sleep(FULL_SWING)
    
    stop()
    
def happy_or_angry_hands():
    # TO FIX HANDS AT THE MID WAVE
    pi.set_servo_pulsewidth(RIGHT_HAND, GO_DOWN)
    sleep(FULL_SWING)
 
    for i in range(1):
        pi.set_servo_pulsewidth(LEFT_HAND, GO_UP)
        pi.set_servo_pulsewidth(RIGHT_HAND, GO_UP)
        sleep(FULL_SWING)
        
        pi.set_servo_pulsewidth(LEFT_HAND, GO_DOWN)
        pi.set_servo_pulsewidth(RIGHT_HAND, GO_DOWN)
        sleep(FULL_SWING)
        
    pi.set_servo_pulsewidth(LEFT_HAND, STOP)
    pi.set_servo_pulsewidth(RIGHT_HAND, GO_UP)

    sleep(FULL_SWING)
    stop()

def annoyed_hands():
    # hands go up
    hands_go_up()
    sleep(FULL_SWING / 2)
    
    # pause for 2 seconds
    stop()
    sleep(.5)
    
    # hands go down
    hands_go_down()
    sleep(FULL_SWING / 2)
    
    stop()

def start(queue):    
    
    if queue == 'greet':
        say_hi()
        
    if queue == 'sad' or queue == 'inlove':
        sad_or_love_hands()
                
    if queue == 'happy' or queue == 'angry':
        happy_or_angry_hands()
                
    if queue == 'annoyed':
        annoyed_hands()
                
    if queue == 'stop':
        stop()
            