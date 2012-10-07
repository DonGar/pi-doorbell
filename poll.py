#!/usr/bin/python

import time
import urllib

import RPi.GPIO as GPIO

def button_pushed():
  print "Button down!"
  f = urllib.urlopen("http://www:8080/doorbell")
  f.readlines()
  f.close()

def main():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(0, GPIO.IN)

  button_down = False

  while True:
    # Gpio 0 is True for button up
    read_down = not GPIO.input(0)
  
    # If the button state changed
    if read_down != button_down:
      button_down = read_down
    
      # If the button when down, notify of a doorbell events
      if button_down:
        button_pushed()

    time.sleep(0.05)

# TODO: when the Raspbian kernel supports GPIO events correctly...

# GPIO.set_falling_event(0)
# while True:
#   time.sleep(1)
#   print GPIO.event_detected(0)

if __name__ == "__main__":
    main()
