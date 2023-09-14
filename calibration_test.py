import pigpio
from time import sleep

# Initialize pigpio
pi = pigpio.pi()

servo_pin = 18  # Change this to your GPIO pin

min_pulse_width = 1000
max_pulse_width = 2000

GO_TO_LEFT = min_pulse_width + 250
GO_TO_RIGHT = max_pulse_width - 100
STOP = (max_pulse_width + min_pulse_width) // 2

last_angle = open('last_known_angle.txt', 'r')
current_angle = float(last_angle.read())
last_angle.close()

# calibration
def calibrate():
    print("calibrating...")
    global current_angle
    while current_angle != 90:
        
#         adjust the servo to right
        if current_angle < 90:
            pi.set_servo_pulsewidth(servo_pin, GO_TO_RIGHT)
            sleep(.054)
            current_angle += .5
        
#         adjust the servo to left
        if current_angle > 90:
            pi.set_servo_pulsewidth(servo_pin, GO_TO_LEFT)
            sleep(.06)
            current_angle -= .5
        
        pi.set_servo_pulsewidth(servo_pin, STOP)
        sleep(.89)
    
    print("calibration done!")