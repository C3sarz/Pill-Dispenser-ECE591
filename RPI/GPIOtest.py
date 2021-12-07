import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)

# Peripheral Pins
buzzer_pin = 13 # PWM Channel 1 Buzzer Pin
laser_pin = 25 # Pin to control the tripwire laser
chamber_led_pin = 9 # Pin to control the cylinder chamber LED
tripwire_input_pin  = 11 # Boolean input of the tripwire status
chamber_led_input_pin = 8 # Boolean input of the verification chamber status

GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(laser_pin, GPIO.OUT)
GPIO.setup(chamber_led_pin, GPIO.OUT)
GPIO.setup(tripwire_input_pin, GPIO.IN)
GPIO.setup(chamber_led_input_pin, GPIO.IN)


test = input("Mode: ")
while test != 'q':
	if test == 'b':
		GPIO.output(buzzer_pin, 1)
		time.sleep(2)
		GPIO.output(buzzer_pin, 0)
	elif test == 'l':
		GPIO.output(laser_pin, 1)
		time.sleep(2)
		GPIO.output(laser_pin, 0)
	elif test == 'c':
		GPIO.output(chamber_led_pin, 1)
		time.sleep(2)
		GPIO.output(chamber_led_pin, 0)
