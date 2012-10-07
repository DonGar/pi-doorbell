#!/usr/bin/python

import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(0, GPIO.IN)

button_down = False

while True:
  # Gpio 0 is True for button up
  read_down = not GPIO.input(0)
  if read_down != button_down:
    button_down = read_down
    if button_down:
      print "Button down!"

  time.sleep(0.05)



# GPIO.set_falling_event(0)

# while True:
#   time.sleep(1)
#   print GPIO.event_detected(0)
