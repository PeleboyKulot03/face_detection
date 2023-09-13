import pigpio
import time

# Initialize pigpio
pi = pigpio.pi()

# Specify the GPIO pin connected to your servo
servo_pin = 18  # Change this to your GPIO pin
servo_pin1 = 17
servo_pin2 = 27
# Set the pulse width range for your servo
# Set the pulse width range for your servo
min_pulse_width = 1000  # Adjust this for your servo
max_pulse_width = 2000  # Adjust this for your servo
