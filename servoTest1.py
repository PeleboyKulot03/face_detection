from gpiozero import AngularServo
from time import sleep

VELOCITY_TO_RIGHT = 236
VELOCITY_TO_LEFT = 253
ANGLE_TO_RIGHT = 0
ANGLE_TO_LEFT = 130

servo = AngularServo(18, min_angle=-90, max_angle=90, min_pulse_width=0.0008, max_pulse_width=0.0024)

def getTime(angle):
    return angle / VELOCITY_TO_RIGHT

def getTimeLeft(angle):
    return angle / VELOCITY_TO_LEFT


servo.angle = 90
sleep(1)
servo.angle = -90

# while True:
#     servo.angle = ANGLE_TO_RIGHT
#     sleep(getTime(180))
#     servo.angle = 70
#     sleep(1)
# 
#     servo.angle = ANGLE_TO_LEFT
#     sleep(getTimeLeft(180))
#     servo.angle = 68
#     sleep(1)
#     print("hi")