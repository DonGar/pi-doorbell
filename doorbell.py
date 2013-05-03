#!/usr/bin/python

import time
import multiprocessing
import urllib

import RPi.GPIO as GPIO

# Which GPIO pins are used to detect a button press, or to ring the bell.
BUTTON = 7 # GPIO4
BELL = 11  # GPIO 17

# We only send an external notification if there wasn't a button press for
# at least this many seconds.
NOTIFY_DELAY = 30
NOTIFY_URL= 'http://www:8080/button?id=doorbell'

def notify():
  """Perform an external notify by opening a URL.

  This is a simple method to make it easier to call in a different process.
  This method could send email, or anything you find useful.
  """
  f = urllib.urlopen(NOTIFY_URL)
  f.read()
  f.close()


class Doorbell:
  """Handles doorbell rings by ringing the doorbell, sending notifications.
  """

  def __init__(self):
    self.down = False
    self.last_notify = 0
    self.process_pool = multiprocessing.Pool(6)

  def notify_handler(self):
    now = time.time()
    if now > self.last_notify + NOTIFY_DELAY:
      self.last_notify = now

      # We do the notification in a background process so it won't
      # affect our real-time GPIO polling.
      self.process_pool.apply_async(notify)

  def poll(self):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    GPIO.setup(BUTTON, GPIO.IN)
    GPIO.setup(BELL, GPIO.OUT)

    while True:
      # BUTTON reads low when pushed, high when up.
      read_down = not GPIO.input(BUTTON)

      if read_down != self.down:
        self.down = read_down
        print "Button is %s" % read_down

        # Activate the doorbell based on the button push.
        GPIO.output(BELL, self.down)

        # If the button was just pushed, try to trigger a notify.
        if self.down:
            self.notify_handler()

      # Sleep a little, saves a lot of power.
      time.sleep(0.05)

  def run(self):
    try:
      self.poll()
    finally:
      self.process_pool.close()
      self.process_pool.join()

if __name__ == "__main__":
    Doorbell().run()
