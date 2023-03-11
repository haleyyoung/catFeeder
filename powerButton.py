import RPi.GPIO as GPIO
import board
import time
from datetime import datetime
from utilities import Log
from catFeeder import CatFeeder

GPIO.setmode(GPIO.BCM)
powerButtonPin = 22
GPIO.setup(powerButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
onepawFeeder = CatFeeder()

def powerButtonPushed():
  isButtonPushed = GPIO.input(powerButtonPin)
  if isButtonPushed:
    time.sleep(0.25)
    if GPIO.input(powerButtonPin):
      onepawFeeder.toggleEnabled()
      Log.info("Power putton pushed, turning system {status}".format(status = onepawFeeder.isEnabled()))
      time.sleep(2)

try:
  while True:
    powerButtonPushed()
except KeyboardInterrupt:
  onepawFeeder.killAllMotors()
  Log.info("Power button dead")

