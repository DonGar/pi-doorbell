#!/usr/bin/python

import time
import urllib

import RPi.GPIO as GPIO

BUTTON_URL = {
  7: 'http://www:8080/doorbell',
  11: 'http://www:8080/doorbell',
  13: 'http://www:8080/doorbell',
  15: 'http://www:8080/doorbell',
  8: 'http://www:8080/doorbell',
}


def button_pushed(pin):
  print 'Button down!: %d' % pin
  f = urllib.urlopen(BUTTON_URL[pin])
  f.read()
  f.close()

def main():
  button_pins = BUTTON_URL.keys()
  button_down = {}

  GPIO.setmode(GPIO.BOARD)
  GPIO.setwarnings(False)

  for pin in button_pins:
    GPIO.setup(pin, GPIO.IN)

  while True:
    # If the pin transitioned to low since we checked, it's been pushed.
    for pin in button_pins:

      read_down = GPIO.input(pin)

      if read_down != button_down.get(pin, False):
        button_down[pin] = read_down

        if read_down:
          button_pushed(pin)

    time.sleep(0.05)

if __name__ == "__main__":
    main()
